"""Mixed precision training explanation and FP16 simulation.

Simulates FP16 behavior (reduced mantissa) and implements loss scaling
to prevent underflow in FP16 training.
"""

import numpy as np
from typing import Optional


class FP16Simulator:
    """Simulate FP16 arithmetic by truncating mantissa.

    FP32 has 23 mantissa bits; FP16 has 10 mantissa bits.
    We simulate by rounding to fewer significant digits.
    """

    def __init__(self, mantissa_bits: int = 10):
        """Initialize FP16 simulator.

        Args:
            mantissa_bits: Number of mantissa bits to simulate (default 10 for FP16).
        """
        self.precision = 2 ** mantissa_bits  # ~1024 levels

    def to_fp16(self, x: np.ndarray) -> np.ndarray:
        """Simulate converting FP32 to FP16 (quantize).

        Args:
            x: FP32 array.

        Returns:
            Simulated FP16 array.
        """
        # Scale by max absolute value and quantize
        abs_max = np.max(np.abs(x))
        if abs_max < 1e-38:
            return x
        scaled = x / (abs_max + 1e-38)
        quantized = np.round(scaled * self.precision) / self.precision
        return quantized * abs_max

    def to_fp32(self, x: np.ndarray) -> np.ndarray:
        """FP32 is identity for our simulation.

        Args:
            x: Input array.

        Returns:
            Copy of the array (FP32).
        """
        return x.copy()

    def loss_scale_up(self, loss: float, scale: float) -> float:
        """Scale loss up to prevent underflow in FP16 gradients.

        Args:
            loss: Original loss value.
            scale: Loss scaling factor.

        Returns:
            Scaled loss.
        """
        return loss * scale

    def loss_scale_down(self, grads: dict[str, np.ndarray], scale: float) -> dict[str, np.ndarray]:
        """Scale gradients back down after FP16 backward pass.

        Args:
            grads: Scaled gradients.
            scale: Loss scaling factor.

        Returns:
            Unscaled gradients.
        """
        return {k: v / scale for k, v in grads.items()}

    def gradient_is_finite(self, grad: np.ndarray) -> bool:
        """Check if gradient contains NaN or Inf.

        Args:
            grad: Gradient array.

        Returns:
            True if gradient is valid (no NaN/Inf).
        """
        return bool(np.all(np.isfinite(grad)))

    def check_all_finite(self, grads: dict[str, np.ndarray]) -> bool:
        """Check if all gradients in a dict are finite.

        Args:
            grads: Gradient dict.

        Returns:
            True if all gradients are finite.
        """
        return all(self.gradient_is_finite(g) for g in grads.values())


def mixed_precision_training_step(
    params: dict[str, np.ndarray],
    grads: dict[str, np.ndarray],
    loss_scale: float,
    optimizer: "Adam" = None,
    simulator: Optional[FP16Simulator] = None,
) -> tuple[dict[str, np.ndarray], float, bool]:
    """Simulate one step of mixed precision training with loss scaling.

    Args:
        params: Model parameters (FP32).
        grads: Gradients computed in FP16 (may overflow).
        loss_scale: Current loss scaling factor.
        optimizer: Optimizer to apply updates (default Adam if None).
        simulator: FP16 simulator instance.

    Returns:
        Tuple of (updated_params, new_loss_scale, step_successful).
    """
    if simulator is None:
        simulator = FP16Simulator()

    if optimizer is None:
        try:
            from .optimizers import Adam
        except ImportError:
            try:
                from training.optimizers import Adam
            except ImportError:
                from optimizers import Adam
        optimizer = Adam(lr=0.001)

    # Scale gradients down
    grads_unscaled = simulator.loss_scale_down(grads, loss_scale)

    # Simulate FP16 gradient computation
    grads_fp16 = {k: simulator.to_fp16(v) for k, v in grads_unscaled.items()}

    # Check for overflow
    if not simulator.check_all_finite(grads_fp16):
        # Overflow detected: skip update, reduce scale
        new_scale = loss_scale * 0.5
        return params, new_scale, False

    # Update parameters with FP32 precision
    params_fp32 = {k: simulator.to_fp32(v) for k, v in params.items()}
    optimizer.update(params_fp32, grads_fp16)

    # Increase scale (successful step, no overflow)
    new_scale = min(loss_scale * 2.0, 2.0 ** 16)  # cap at reasonable max

    return params_fp32, new_scale, True


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing Mixed Precision...")

    np.random.seed(42)

    sim = FP16Simulator(mantissa_bits=10)

    # Test 1: FP16 rounding reduces precision
    x = np.random.randn(100) * 0.001  # small values
    x_fp16 = sim.to_fp16(x)
    # FP16 and FP32 should differ (due to quantization)
    diff = np.max(np.abs(x - x_fp16))
    assert diff > 0, "FP16 should differ from FP32"
    print(f"  PASS: FP16 rounding changes values, max diff = {diff:.2e}")

    # Test 2: FP32 is identity
    x_fp32 = sim.to_fp32(x)
    assert np.allclose(x_fp32, x), "FP32 should be identity"
    print("  PASS: FP32 is identity")

    # Test 3: Loss scaling math
    loss = 1.5
    scale = 1024.0
    scaled_loss = sim.loss_scale_up(loss, scale)
    assert np.isclose(scaled_loss, 1536.0, atol=1e-6)
    print(f"  PASS: Loss scaling: {loss} × {scale} = {scaled_loss}")

    # Test 4: Loss unscaling
    grads = {"w": np.array([2.0, 4.0, 8.0])}
    unscaled = sim.loss_scale_down(grads, scale)
    assert np.allclose(unscaled["w"], [2.0/scale, 4.0/scale, 8.0/scale])
    print(f"  PASS: Loss unscaling correct")

    # Test 5: Gradient finiteness check
    assert sim.gradient_is_finite(np.array([1.0, 2.0, 3.0]))
    assert not sim.gradient_is_finite(np.array([1.0, np.nan, 3.0]))
    assert not sim.gradient_is_finite(np.array([1.0, np.inf, 3.0]))
    print("  PASS: Gradient finiteness detection correct")

    # Test 6: Mixed precision training step with overflow
    params = {"w": np.array([1.0, 2.0, 3.0])}
    # Gradients with overflow (inf)
    grads_overflow = {"w": np.array([0.1, np.inf, 0.3])}
    new_params, new_scale, success = mixed_precision_training_step(
        params, grads_overflow, loss_scale=1024.0, optimizer=None, simulator=sim
    )
    assert not success, "Should detect overflow"
    assert new_scale < 1024.0, f"Scale should decrease on overflow: {new_scale}"
    print(f"  PASS: Overflow detected, scale reduced: 1024.0 → {new_scale}")

    # Test 7: Mixed precision training step successful
    params2 = {"w": np.array([1.0, 2.0, 3.0])}
    grads_ok = {"w": np.array([1.0, 2.0, 3.0])}  # larger grads
    new_params2, new_scale2, success2 = mixed_precision_training_step(
        params2, grads_ok, loss_scale=1024.0, optimizer=None, simulator=sim
    )
    assert success2, "Should succeed with finite grads"
    assert new_scale2 > 1024.0, f"Scale should increase on success: {new_scale2}"
    assert not np.allclose(new_params2["w"], params2["w"]), "Params should be updated"
    print(f"  PASS: Successful step, scale increased: 1024.0 → {new_scale2}")

    # Test 8: Scale cap
    big_scale = 2.0 ** 15
    params3 = {"w": np.array([1.0])}
    grads_ok2 = {"w": np.array([0.1])}
    _, new_scale3, _ = mixed_precision_training_step(
        params3, grads_ok2, loss_scale=big_scale, optimizer=None, simulator=sim
    )
    assert new_scale3 <= 2.0 ** 16, f"Scale should be capped: {new_scale3}"
    print(f"  PASS: Loss scale capped at reasonable maximum: {new_scale3:.0f}")

    # Test 9: FP16 preserves rough magnitude
    x_large = np.array([1e5, -2e5, 3e5])
    x_fp16_large = sim.to_fp16(x_large)
    # Relative error should be reasonable
    rel_err = np.max(np.abs((x_large - x_fp16_large) / (np.abs(x_large) + 1e-38)))
    assert rel_err < 0.01, f"FP16 relative error too large: {rel_err:.4f}"
    print(f"  PASS: FP16 relative error: {rel_err:.4f}")

    print("\nAll Mixed Precision tests passed!")
