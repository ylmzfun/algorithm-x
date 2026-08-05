"""Dropout regularization from scratch using NumPy.

Implements inverted dropout:
- Training: randomly zero out neurons, scale survivors by 1/(1-p)
- Evaluation: identity (no dropout)
"""

import numpy as np
from typing import Optional


class Dropout:
    """Dropout regularization layer.

    During training, each element is independently set to zero with probability p,
    and survivors are scaled by 1/(1-p) (inverted dropout). During evaluation,
    the layer is an identity function.

    This ensures the expected value of the output is the same during training
    and evaluation without needing to rescale at test time.
    """

    def __init__(self, p: float = 0.5, random_seed: Optional = None):
        """Initialize Dropout layer.

        Args:
            p: Probability of dropping a neuron (0 < p < 1).
            random_seed: Optional seed for reproducibility.
        """
        if not (0 < p < 1):
            raise ValueError(f"Dropout probability p must be in (0, 1), got {p}")
        self.p = p
        self.scale = 1.0 / (1.0 - p)
        self.training: bool = True
        self._rng = np.random.RandomState(random_seed)

        # Cache mask for backward pass
        self._mask: Optional[np.ndarray] = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass with inverted dropout.

        Args:
            x: Input array of any shape.

        Returns:
            Output: x in eval mode; x * mask * scale in training mode.
        """
        if self.training:
            # Generate dropout mask: keep with prob (1-p)
            self._mask = (self._rng.rand(*x.shape) > self.p).astype(float)
            return x * self._mask * self.scale
        else:
            self._mask = None
            return x

    def backward(self, dout: np.ndarray) -> np.ndarray:
        """Backward pass: gradient flows only through active neurons.

        Args:
            dout: Upstream gradient of same shape as forward output.

        Returns:
            Gradient w.r.t. input.
        """
        if self.training:
            return dout * self._mask * self.scale
        else:
            return dout

    def __call__(self, x: np.ndarray) -> np.ndarray:
        """Convenience call for forward pass."""
        return self.forward(x)

    def train(self):
        """Set module to training mode."""
        self.training = True

    def eval(self):
        """Set module to evaluation mode."""
        self.training = False


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing Dropout...")

    np.random.seed(42)

    # Test 1: Training mode drops approximately p fraction of neurons
    dropout = Dropout(p=0.5, random_seed=42)
    dropout.train()
    x = np.random.randn(10000, 20)
    out = dropout.forward(x)
    frac_zero = np.mean(out == 0)
    expected = dropout.p
    assert abs(frac_zero - expected) < 0.02, (
        f"Expected ~{expected:.1%} zeros, got {frac_zero:.1%}"
    )
    print(f"  PASS: Dropout rate ≈ {frac_zero:.3f} (expected {expected:.3f})")

    # Test 2: Inverted dropout preserves expected value
    x_small = np.ones((50000, 1))
    dropout2 = Dropout(p=0.3, random_seed=123)
    dropout2.train()
    out_small = dropout2.forward(x_small)
    # Expected value of each element = 1.0 (since inverted dropout scales survivors)
    mean_val = np.mean(out_small)
    assert abs(mean_val - 1.0) < 0.02, f"Expected mean ≈ 1.0, got {mean_val:.4f}"
    print(f"  PASS: Inverted dropout preserves mean: {mean_val:.4f} ≈ 1.0")

    # Test 3: Eval mode is identity
    dropout.eval()
    x_test = np.random.randn(100, 10)
    out_eval = dropout.forward(x_test)
    assert np.allclose(out_eval, x_test), "Eval mode must be identity"
    print("  PASS: Eval mode is identity")

    # Test 4: Backward pass in training mode
    dropout3 = Dropout(p=0.4, random_seed=99)
    dropout3.train()
    x_bw = np.random.randn(50, 8)
    out_bw = dropout3.forward(x_bw)
    mask = dropout3._mask
    dout = np.ones_like(out_bw)
    dx = dropout3.backward(dout)
    # dx should be zero where mask is zero, and scaled where mask is 1
    scale = dropout3.scale
    expected_dx = dout * mask * scale
    assert np.allclose(dx, expected_dx), "Backward gradient mismatch"
    # Non-zero entries should equal scale
    nonzero_dx = dx[mask == 1]
    assert np.allclose(nonzero_dx, scale), f"Non-zero dx entries should be {scale}"
    print(f"  PASS: Backward gradient correct (scale={scale:.3f})")

    # Test 5: Backward pass in eval mode
    dropout3.eval()
    out_eval2 = dropout3.forward(x_bw)
    dx_eval = dropout3.backward(dout)
    assert np.allclose(dx_eval, dout), "Eval backward must be identity"
    print("  PASS: Eval backward is identity")

    # Test 6: Different dropout probabilities
    for p in [0.1, 0.3, 0.5, 0.7, 0.9]:
        dp = Dropout(p=p, random_seed=42)
        dp.train()
        x_p = np.ones((20000, 1))
        out_p = dp.forward(x_p)
        frac = np.mean(out_p == 0)
        # Allow slightly wider tolerance for extreme p values
        assert abs(frac - p) < 0.03, f"p={p}: expected {p:.1%} zeros, got {frac:.1%}"
    print("  PASS: Various dropout probabilities verified")

    # Test 7: Reproducibility with seed
    dp_a = Dropout(p=0.5, random_seed=42)
    dp_b = Dropout(p=0.5, random_seed=42)
    x_r = np.random.randn(20, 5)
    out_a = dp_a.forward(x_r)
    out_b = dp_b.forward(x_r)
    assert np.allclose(out_a, out_b), "Same seed should produce same mask"
    print("  PASS: Reproducibility with fixed seed")

    # Test 8: Error on invalid p
    try:
        Dropout(p=1.5)
        assert False, "Should have raised ValueError"
    except ValueError:
        print("  PASS: ValueError raised for invalid p")

    print("\nAll Dropout tests passed!")
