"""Batch Normalization (BatchNorm1d) from scratch using NumPy.

Implements:
- Forward pass in training mode (using batch statistics, updating running mean/var)
- Forward pass in evaluation mode (using running statistics)
- Backward pass computing gradients w.r.t. input, gamma, and beta
"""

import numpy as np
from typing import Optional


class BatchNorm1d:
    """Batch Normalization for 1D inputs (fully-connected layers).

    During training: normalizes using batch mean/variance, updates running estimates.
    During evaluation: normalizes using running mean/variance.

    y = gamma * (x - mean) / sqrt(var + eps) + beta
    """

    def __init__(
        self,
        num_features: int,
        eps: float = 1e-5,
        momentum: float = 0.9,
        affine: bool = True,
    ):
        """Initialize BatchNorm1d.

        Args:
            num_features: Number of input features (C from (N, C)).
            eps: Small epsilon for numerical stability.
            momentum: Momentum for updating running mean/var.
            affine: If True, learn gamma and beta parameters.
        """
        self.num_features = num_features
        self.eps = eps
        self.momentum = momentum
        self.affine = affine

        # Learnable parameters
        self.gamma = np.ones((1, num_features)) if affine else None
        self.beta = np.zeros((1, num_features)) if affine else None

        # Running statistics (updated during training, used during eval)
        self.running_mean = np.zeros((1, num_features))
        self.running_var = np.ones((1, num_features))

        # Cache for backward pass
        self._cache: dict = {}

        # Training mode flag
        self.training: bool = True

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass for batch normalization.

        Args:
            x: Input of shape (N, C) where N is batch size, C is num_features.

        Returns:
            Normalized output of shape (N, C).
        """
        N = x.shape[0]

        if self.training:
            # Compute batch statistics
            batch_mean = np.mean(x, axis=0, keepdims=True)  # (1, C)
            batch_var = np.var(x, axis=0, keepdims=True)    # (1, C)

            # Update running statistics
            self.running_mean = (
                self.momentum * self.running_mean + (1 - self.momentum) * batch_mean
            )
            self.running_var = (
                self.momentum * self.running_var + (1 - self.momentum) * batch_var
            )

            # Normalize
            x_centered = x - batch_mean
            std_inv = 1.0 / np.sqrt(batch_var + self.eps)
            x_norm = x_centered * std_inv

            # Save for backward pass
            self._cache = {
                "x": x,
                "x_centered": x_centered,
                "x_norm": x_norm,
                "batch_mean": batch_mean,
                "batch_var": batch_var,
                "std_inv": std_inv,
                "N": N,
            }
        else:
            # Use running statistics
            x_centered = x - self.running_mean
            std_inv = 1.0 / np.sqrt(self.running_var + self.eps)
            x_norm = x_centered * std_inv

        # Scale and shift
        if self.affine:
            out = self.gamma * x_norm + self.beta
        else:
            out = x_norm
        return out

    def backward(self, dout: np.ndarray) -> tuple[np.ndarray, Optional[np.ndarray], Optional[np.ndarray]]:
        """Backward pass for batch normalization.

        Computes gradients w.r.t. input x, gamma, and beta.

        Args:
            dout: Upstream gradient of shape (N, C).

        Returns:
            Tuple of (dx, dgamma, dbeta).
            dgamma and dbeta are None if not affine.
        """
        if not self.training:
            raise RuntimeError("Backward pass only supported in training mode.")

        cache = self._cache
        x_norm = cache["x_norm"]
        std_inv = cache["std_inv"]
        N = cache["N"]

        # Gradient w.r.t. gamma and beta
        if self.affine:
            dgamma = np.sum(dout * x_norm, axis=0, keepdims=True)  # (1, C)
            dbeta = np.sum(dout, axis=0, keepdims=True)             # (1, C)

            # Gradient w.r.t. x_norm
            dx_norm = dout * self.gamma  # (N, C)
        else:
            dgamma = None
            dbeta = None
            dx_norm = dout

        # Gradient w.r.t. x through normalization
        # dx = (1/N) * std_inv * (N * dx_norm - sum(dx_norm) - x_norm * sum(dx_norm * x_norm))
        dx_norm_sum = np.sum(dx_norm, axis=0, keepdims=True)                       # (1, C)
        dx_norm_x_norm_sum = np.sum(dx_norm * x_norm, axis=0, keepdims=True)        # (1, C)

        dx = (1.0 / N) * std_inv * (
            N * dx_norm
            - dx_norm_sum
            - x_norm * dx_norm_x_norm_sum
        )

        return dx, dgamma, dbeta

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
    print("Testing BatchNorm1d...")

    np.random.seed(42)
    N, C = 100, 5
    x = np.random.randn(N, C) * 2.0 + 3.0  # mean≈3, std≈2

    # Test 1: Training mode forward reduces mean and unit-variances variance
    bn = BatchNorm1d(num_features=C, eps=1e-5, momentum=0.9)
    bn.train()
    out = bn.forward(x)
    out_mean = np.mean(out, axis=0)
    out_var = np.var(out, axis=0)
    assert np.allclose(out_mean, 0.0, atol=1e-6), f"Training output mean not zero: {out_mean}"
    assert np.allclose(out_var, 1.0, atol=1e-6), f"Training output var not one: {out_var}"
    print("  PASS: Training forward normalizes to mean≈0, var≈1")

    # Test 2: Running statistics updated
    assert not np.allclose(bn.running_mean, 0.0), "Running mean not updated"
    assert not np.allclose(bn.running_var, 1.0), "Running var not updated"
    print(f"  PASS: Running statistics updated (mean: {bn.running_mean[0, 0]:.4f})")

    # Test 3: Eval mode uses running statistics
    bn.eval()
    out_eval = bn.forward(x)
    out_eval_mean = np.mean(out_eval, axis=0)
    # In eval mode, output should be close to (x - running_mean)/sqrt(running_var)
    # since gamma=1, beta=0
    expected_eval = (x - bn.running_mean) / np.sqrt(bn.running_var + bn.eps)
    assert np.allclose(out_eval, expected_eval, atol=1e-6), "Eval mode output mismatch"
    print("  PASS: Eval mode matches manual computation")

    # Test 4: Affine parameters affect output
    bn2 = BatchNorm1d(num_features=C, eps=1e-5, affine=True)
    bn2.gamma = np.ones((1, C)) * 2.0
    bn2.beta = np.ones((1, C)) * 1.0
    bn2.train()
    out_aff = bn2.forward(x)
    # After scale+shift: mean≈beta=1, var≈gamma^2=4
    assert np.allclose(np.mean(out_aff, axis=0), 1.0, atol=1e-6), "Affine output mean wrong"
    assert np.allclose(np.var(out_aff, axis=0), 4.0, atol=1e-6), "Affine output var wrong"
    print("  PASS: Affine parameters (gamma=2, beta=1) applied correctly")

    # Test 5: Backward pass gradient check (numerical)
    # Use fresh BatchNorm per perturbation to avoid running-statistics drift
    x_small = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]], dtype=float)
    bn3 = BatchNorm1d(num_features=3, eps=1e-5, affine=True)
    bn3.train()
    out_small = bn3.forward(x_small)
    dout = np.ones_like(out_small)
    dx, dgamma, dbeta = bn3.backward(dout)

    num_dx = np.zeros_like(x_small)
    for i in range(x_small.shape[0]):
        for j in range(x_small.shape[1]):
            x_pert = x_small.copy()
            orig = x_pert[i, j]
            x_pert[i, j] = orig + 1e-5
            b1 = BatchNorm1d(num_features=3, eps=1e-5, affine=True)
            b1.train()
            lp = np.sum(b1.forward(x_pert))
            x_pert[i, j] = orig - 1e-5
            b2 = BatchNorm1d(num_features=3, eps=1e-5, affine=True)
            b2.train()
            lm = np.sum(b2.forward(x_pert))
            num_dx[i, j] = (lp - lm) / (2e-5)

    err = np.max(np.abs(dx - num_dx))
    assert err < 1e-4, f"Gradient check failed: max abs error = {err:.2e}"
    print(f"  PASS: Gradient check (dx), max abs error = {err:.2e}")

    # Test 6: Gamma and beta gradients
    bn3.train()
    _ = bn3.forward(x_small)
    dx2, dgamma2, dbeta2 = bn3.backward(dout)
    # dgamma = sum(dout * x_norm), dbeta = sum(dout)
    # With dout=1 everywhere: dgamma_i = sum_j x_norm[j,i], dbeta_i = N
    assert dbeta2.shape == (1, 3), f"Wrong dbeta shape: {dbeta2.shape}"
    assert dgamma2.shape == (1, 3), f"Wrong dgamma shape: {dgamma2.shape}"
    assert np.isclose(dbeta2[0, 0], 3.0, atol=1e-6), f"dbeta wrong value: {dbeta2}"
    print("  PASS: Gamma and beta gradient shapes and values correct")

    # Test 7: Output shape
    x_big = np.random.randn(50, 10)
    bn4 = BatchNorm1d(num_features=10)
    bn4.train()
    out_big = bn4.forward(x_big)
    assert out_big.shape == (50, 10), f"Wrong output shape: {out_big.shape}"
    print("  PASS: Output shape preserved")

    # Test 8: No-affine mode
    bn5 = BatchNorm1d(num_features=5, affine=False)
    bn5.train()
    out5 = bn5.forward(x)
    dx5, dg5, db5 = bn5.backward(np.ones_like(out5))
    assert dg5 is None and db5 is None, "No-affine should return None gradients"
    assert dx5.shape == x.shape
    print("  PASS: No-affine mode works")

    print("\nAll BatchNorm1d tests passed!")
