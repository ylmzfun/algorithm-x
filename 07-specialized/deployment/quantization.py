"""Post-training quantization concepts from scratch.

Implements:
- Symmetric quantization
- Asymmetric quantization with zero point
- Dequantization
- Quantized linear layer (simulated 8-bit inference)
- Quantization error measurement

Reference: Jacob et al., "Quantization and Training of Neural Networks
for Efficient Integer-Arithmetic-Only Inference" (2018).
"""

from __future__ import annotations

import numpy as np
from typing import Optional


# ---------------------------------------------------------------------------
# Quantization Functions
# ---------------------------------------------------------------------------

def symmetric_quantize(
    weights: np.ndarray, num_bits: int = 8
) -> tuple[np.ndarray, float]:
    """Symmetric quantization: scales weights to [-2^(n-1), 2^(n-1)-1].

    scale = max(|w|) / (2^(n-1) - 1)
    q = round(w / scale), clamped to range.

    Args:
        weights: Floating-point weight matrix.
        num_bits: Bit-width for quantization.

    Returns:
        Tuple of (quantized_weights as integers, scale).
    """
    qmax = 2 ** (num_bits - 1) - 1
    scale = np.max(np.abs(weights)) / qmax
    if scale == 0:
        scale = 1e-12
    q_weights = np.clip(np.round(weights / scale), -qmax, qmax).astype(np.int32)
    return q_weights, float(scale)


def asymmetric_quantize(
    weights: np.ndarray, num_bits: int = 8
) -> tuple[np.ndarray, float, int]:
    """Asymmetric quantization with zero point.

    Maps [w_min, w_max] → [0, 2^n - 1].
    scale = (w_max - w_min) / (2^n - 1)
    zero_point = round(-w_min / scale)

    Args:
        weights: Floating-point weight matrix.
        num_bits: Bit-width.

    Returns:
        Tuple of (quantized_weights, scale, zero_point).
    """
    qmin = 0
    qmax = 2**num_bits - 1
    w_min = np.min(weights)
    w_max = np.max(weights)

    scale = (w_max - w_min) / (qmax - qmin)
    if scale == 0:
        scale = 1e-12
    zero_point = int(np.round(qmin - w_min / scale))
    zero_point = max(qmin, min(qmax, zero_point))

    q_weights = np.clip(
        np.round(weights / scale) + zero_point, qmin, qmax
    ).astype(np.int32)
    return q_weights, float(scale), zero_point


def dequantize(
    q_weights: np.ndarray,
    scale: float,
    zero_point: int = 0,
) -> np.ndarray:
    """Dequantize weights back to floating point.

    For symmetric:  w ≈ q * scale
    For asymmetric: w ≈ (q - zero_point) * scale

    Args:
        q_weights: Quantized integer weights.
        scale: Quantization scale.
        zero_point: Quantization zero point (0 for symmetric).

    Returns:
        Dequantized floating-point weights.
    """
    return (q_weights.astype(np.float64) - zero_point) * scale


def quantization_error(
    original: np.ndarray, dequantized: np.ndarray
) -> float:
    """Compute MSE between original and dequantized weights.

    Args:
        original: Original floating-point matrix.
        dequantized: Reconstructed matrix after quantization/dequantization.

    Returns:
        Mean squared error.
    """
    return float(np.mean((original - dequantized) ** 2))


# ---------------------------------------------------------------------------
# Quantized Linear Layer
# ---------------------------------------------------------------------------

class QuantizedLinear:
    """Simulated 8-bit quantized linear layer.

    In a real deployment, the weights are stored as INT8 and the
    matrix multiply uses integer arithmetic with re-scaling.
    Here we simulate the process by storing quantized weights,
    dequantizing on-the-fly, and computing in float.

    Attributes:
        in_features: Input dimension.
        out_features: Output dimension.
        q_weight: Quantized weight matrix [out_features, in_features].
        scale: Quantization scale.
        zero_point: Zero point for asymmetric quantization.
        bias: Optional bias term.
    """

    def __init__(
        self,
        in_features: int,
        out_features: int,
        num_bits: int = 8,
        symmetric: bool = True,
        bias: bool = True,
        seed: int = 42,
    ) -> None:
        """Initialize a quantized linear layer.

        Args:
            in_features: Input dimension.
            out_features: Output dimension.
            num_bits: Bit-width for weight quantization.
            symmetric: Use symmetric quantization if True.
            bias: Include a bias term.
            seed: Random seed.
        """
        rng = np.random.default_rng(seed)
        self.in_features = in_features
        self.out_features = out_features
        self.num_bits = num_bits
        self.symmetric = symmetric

        # Create original weights and quantize
        scale_w = np.sqrt(2.0 / in_features)
        weight = rng.normal(0, scale_w, (out_features, in_features))

        if symmetric:
            self.q_weight, self.scale = symmetric_quantize(weight, num_bits)
            self.zero_point = 0
        else:
            self.q_weight, self.scale, self.zero_point = asymmetric_quantize(
                weight, num_bits
            )

        self.bias = rng.normal(0, 0.1, out_features) if bias else np.zeros(out_features)

        # Store original for comparison
        self._original_weight = weight

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass using quantized weights (simulated).

        Dequantizes weights, then performs float matmul + bias.
        In real INT8 inference, the matmul would be done in integer
        arithmetic with accumulation in INT32.

        Args:
            x: Input [N, in_features].

        Returns:
            Output [N, out_features].
        """
        w = dequantize(self.q_weight, self.scale, self.zero_point)
        return x @ w.T + self.bias

    def weight_error(self) -> float:
        """Compute quantization error for the weights.

        Returns:
            MSE between original and quantized-dequantized weights.
        """
        w_deq = dequantize(self.q_weight, self.scale, self.zero_point)
        return quantization_error(self._original_weight, w_deq)

    def compression_ratio(self) -> float:
        """Estimate compression ratio vs FP32.

        Returns:
            Compression ratio (original/compressed).
        """
        fp32_bits = 32
        return fp32_bits / self.num_bits


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Testing quantization.py — Post-Training Quantization")
    print("=" * 60)

    all_pass = True

    # Test 1: Symmetric quantization of random weights
    print("\n--- Symmetric Quantization ---")
    np.random.seed(42)
    weights = np.random.randn(100, 50)

    for bits in [8, 4]:
        q_w, scale = symmetric_quantize(weights, num_bits=bits)
        w_deq = dequantize(q_w, scale)
        error = quantization_error(weights, w_deq)

        print(f"  {bits}-bit symmetric: MSE = {error:.6f}, "
              f"scale = {scale:.4f}")
        all_pass = all_pass and error < 1.0  # Should be reasonable

        # Verify quantized values are in range
        qmax = 2 ** (bits - 1) - 1
        in_range = np.all(np.abs(q_w) <= qmax)
        print(f"    Values in range [-{qmax}, {qmax}]: {in_range}")
        all_pass = all_pass and in_range

    # Verify 8-bit has lower error than 4-bit
    q8, s8 = symmetric_quantize(weights, 8)
    q4, s4 = symmetric_quantize(weights, 4)
    err8 = quantization_error(weights, dequantize(q8, s8))
    err4 = quantization_error(weights, dequantize(q4, s4))
    print(f"\n  8-bit error: {err8:.6f}")
    print(f"  4-bit error: {err4:.6f}")
    print(f"  8-bit < 4-bit: {err8 < err4}")
    all_pass = all_pass and err8 < err4

    # Test 2: Asymmetric quantization
    print("\n--- Asymmetric Quantization ---")
    # Data with positive bias
    pos_weights = np.random.randn(100, 50) * 2 + 5  # mean ~5
    q_w_a, scale_a, zp = asymmetric_quantize(pos_weights, num_bits=8)
    w_deq_a = dequantize(q_w_a, scale_a, zp)
    error_a = quantization_error(pos_weights, w_deq_a)

    print(f"  8-bit asymmetric: MSE = {error_a:.6f}, "
          f"scale = {scale_a:.4f}, zp = {zp}")
    all_pass = all_pass and error_a < 1.0

    # Compare symmetric vs asymmetric on biased data
    q_w_s, scale_s = symmetric_quantize(pos_weights, num_bits=8)
    error_s = quantization_error(pos_weights, dequantize(q_w_s, scale_s))
    print(f"  8-bit symmetric (biased data): MSE = {error_s:.6f}")
    asym_better = error_a < error_s
    print(f"  Asymmetric better on biased data: {asym_better}")
    all_pass = all_pass and asym_better

    # Test 3: QuantizedLinear layer
    print("\n--- Quantized Linear Layer ---")
    qlinear = QuantizedLinear(
        in_features=10, out_features=5, num_bits=8,
        symmetric=True, seed=42,
    )
    x = np.random.randn(3, 10)
    out = qlinear.forward(x)
    w_err = qlinear.weight_error()
    comp_ratio = qlinear.compression_ratio()

    print(f"  Output shape: {out.shape} (expected (3, 5))")
    print(f"  Weight quantization error: {w_err:.6f}")
    print(f"  Compression ratio vs FP32: {comp_ratio:.1f}x")
    all_pass = all_pass and out.shape == (3, 5)
    all_pass = all_pass and w_err < 0.1
    all_pass = all_pass and comp_ratio > 1.0

    # Test 4: Edge cases
    print("\n--- Edge Cases ---")
    # Constant weights
    const_w = np.ones((10, 5)) * 3.0
    q_c, s_c = symmetric_quantize(const_w, num_bits=8)
    w_c_deq = dequantize(q_c, s_c)
    err_c = quantization_error(const_w, w_c_deq)
    print(f"  Constant weights error: {err_c:.10f} (should be ~0)")
    all_pass = all_pass and err_c < 0.01

    # Zero weights
    zero_w = np.zeros((10, 5))
    q_z, s_z = symmetric_quantize(zero_w, num_bits=8)
    w_z_deq = dequantize(q_z, s_z)
    err_z = quantization_error(zero_w, w_z_deq)
    print(f"  Zero weights error: {err_z:.10f} (should be 0)")
    all_pass = all_pass and err_z < 0.001

    print(f"\n{'PASS' if all_pass else 'FAIL'}: quantization.py")
