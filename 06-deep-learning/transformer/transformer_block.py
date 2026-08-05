"""Transformer encoder block: LayerNorm + MultiHeadAttention + FeedForward.

Implements:
- LayerNorm from scratch
- FeedForward network (2-layer MLP with ReLU)
- TransformerEncoderBlock combining attention + FF with residual connections
"""

import numpy as np
from typing import Optional

try:
    from .attention import MultiHeadAttention
except ImportError:
    from attention import MultiHeadAttention


class LayerNorm:
    """Layer Normalization from scratch.

    Normalizes across the last dimension: y = gamma * (x - mean) / sqrt(var + eps) + beta.
    Unlike BatchNorm, computes mean/variance per sample (not per batch).
    """

    def __init__(self, d_model: int, eps: float = 1e-5):
        """Initialize LayerNorm.

        Args:
            d_model: Feature dimension to normalize over.
            eps: Small epsilon for numerical stability.
        """
        self.d_model = d_model
        self.eps = eps
        self.gamma = np.ones(d_model)
        self.beta = np.zeros(d_model)
        self._cache: dict = {}

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass: normalize across last dimension.

        Args:
            x: Input of shape (..., d_model).

        Returns:
            Normalized output of same shape.
        """
        mean = np.mean(x, axis=-1, keepdims=True)
        var = np.var(x, axis=-1, keepdims=True)
        std_inv = 1.0 / np.sqrt(var + self.eps)
        x_norm = (x - mean) * std_inv

        out = self.gamma * x_norm + self.beta

        self._cache = {
            "x": x, "mean": mean, "var": var,
            "std_inv": std_inv, "x_norm": x_norm,
        }
        return out

    def backward(self, dout: np.ndarray) -> np.ndarray:
        """Backward pass for LayerNorm.

        Args:
            dout: Upstream gradient of same shape as output.

        Returns:
            Gradient w.r.t. input, same shape.
        """
        cache = self._cache
        x_norm = cache["x_norm"]
        std_inv = cache["std_inv"]
        d = x_norm.shape[-1]

        # Gradient w.r.t. gamma and beta (accumulated, but not returned here)
        # dgamma = sum(dout * x_norm, axis=tuple for all but last)
        # dbeta = sum(dout, ...)
        # (We skip tracking these for simplicity in the block; they can be added)

        # Gradient w.r.t. x_norm
        dx_norm = dout * self.gamma

        # Gradient through normalization
        # dx = (1/d) * std_inv * (d * dx_norm - sum(dx_norm) - x_norm * sum(dx_norm * x_norm))
        sum_dx_norm = np.sum(dx_norm, axis=-1, keepdims=True)
        sum_xn_dxn = np.sum(x_norm * dx_norm, axis=-1, keepdims=True)

        dx = (1.0 / d) * std_inv * (
            d * dx_norm - sum_dx_norm - x_norm * sum_xn_dxn
        )
        return dx


class FeedForward:
    """Position-wise feed-forward network: Linear → ReLU → Linear."""

    def __init__(self, d_model: int, d_ff: int, random_seed: Optional[int] = 42):
        """Initialize FeedForward layer.

        Args:
            d_model: Input/output dimension.
            d_ff: Hidden dimension (typically 4 * d_model).
            random_seed: Random seed.
        """
        self.d_model = d_model
        self.d_ff = d_ff

        rng = np.random.RandomState(random_seed)
        scale = np.sqrt(2.0 / d_model)
        self.W1 = rng.randn(d_model, d_ff) * scale
        self.b1 = np.zeros(d_ff)
        self.W2 = rng.randn(d_ff, d_model) * scale
        self.b2 = np.zeros(d_model)
        self._cache: dict = {}

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass.

        Args:
            x: Input of shape (..., d_model).

        Returns:
            Output of same shape.
        """
        # First linear + ReLU
        z1 = np.dot(x, self.W1) + self.b1
        a1 = np.maximum(0, z1)

        # Second linear
        out = np.dot(a1, self.W2) + self.b2

        self._cache = {"x": x, "z1": z1, "a1": a1}
        return out

    def backward(self, dout: np.ndarray) -> tuple[np.ndarray, dict]:
        """Backward pass.

        Args:
            dout: Upstream gradient.

        Returns:
            Tuple of (dx, param_grads).
        """
        cache = self._cache

        # Flatten all leading dims for matmul
        orig_shape = dout.shape
        a1_flat = cache["a1"].reshape(-1, self.d_ff)
        dout_flat = dout.reshape(-1, self.d_model)
        x_flat = cache["x"].reshape(-1, self.d_model)
        z1_shape = cache["z1"].shape

        # Second linear
        dW2 = np.dot(a1_flat.T, dout_flat)
        db2 = np.sum(dout_flat, axis=0)
        da1_flat = np.dot(dout_flat, self.W2.T)

        # ReLU
        dz1_flat = da1_flat * (cache["z1"].reshape(-1, self.d_ff) > 0).astype(float)

        # First linear
        dW1 = np.dot(x_flat.T, dz1_flat)
        db1 = np.sum(dz1_flat, axis=0)
        dx_flat = np.dot(dz1_flat, self.W1.T)
        dx = dx_flat.reshape(orig_shape)

        grads = {"dW1": dW1, "db1": db1, "dW2": dW2, "db2": db2}
        return dx, grads


class TransformerEncoderBlock:
    """Transformer encoder block: MHA + Add&Norm + FF + Add&Norm."""

    def __init__(
        self,
        d_model: int,
        num_heads: int,
        d_ff: int,
        random_seed: Optional[int] = 42,
    ):
        """Initialize encoder block.

        Args:
            d_model: Model dimension.
            num_heads: Number of attention heads.
            d_ff: Feed-forward hidden dimension.
            random_seed: Random seed.
        """
        self.attention = MultiHeadAttention(d_model, num_heads, random_seed=random_seed)
        self.norm1 = LayerNorm(d_model)
        self.ff = FeedForward(d_model, d_ff, random_seed=random_seed + 100 if random_seed else None)
        self.norm2 = LayerNorm(d_model)
        self._cache: dict = {}

    def forward(self, x: np.ndarray, mask: Optional[np.ndarray] = None) -> np.ndarray:
        """Forward pass.

        Args:
            x: Input of shape (batch, seq_len, d_model).
            mask: Optional attention mask.

        Returns:
            Output of same shape.
        """
        # Self-attention + residual + norm
        attn_out = self.attention.forward(x, x, x, mask)
        x = self.norm1.forward(x + attn_out)

        # Cache for backward
        attn_cache = self.attention._cache.copy()
        norm1_cache = self.norm1._cache.copy()
        x_before_ff = x.copy()

        # Feed-forward + residual + norm
        ff_out = self.ff.forward(x)
        x = self.norm2.forward(x + ff_out)

        ff_cache = self.ff._cache.copy()
        norm2_cache = self.norm2._cache.copy()

        self._cache = {
            "attn_cache": attn_cache,
            "norm1_cache": norm1_cache,
            "x_before_ff": x_before_ff,
            "ff_cache": ff_cache,
            "norm2_cache": norm2_cache,
            "x_after_attn": x_before_ff,
        }
        return x

    def backward(self, dout: np.ndarray) -> np.ndarray:
        """Backward pass.

        Args:
            dout: Upstream gradient.

        Returns:
            Gradient w.r.t. input.
        """
        cache = self._cache

        # Restore norm2 cache
        self.norm2._cache = cache["norm2_cache"]
        d_res2 = self.norm2.backward(dout)

        # Restore FF cache
        self.ff._cache = cache["ff_cache"]
        d_ff_in, _ = self.ff.backward(d_res2)

        # Residual: x_before_ff + ff(x_before_ff)
        dx_norm1 = d_res2 + d_ff_in

        # Restore norm1 cache
        self.norm1._cache = cache["norm1_cache"]
        d_res1 = self.norm1.backward(dx_norm1)

        # Restore attention cache
        self.attention._cache = cache["attn_cache"]
        dQ, _, _, _ = self.attention.backward(d_res1)

        # Residual: original x + attn(x)
        dx = d_res1 + dQ

        return dx


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing Transformer Block...")

    np.random.seed(42)

    # Test 1: LayerNorm forward/backward
    ln = LayerNorm(d_model=4)
    x = np.random.randn(3, 6, 4)  # batch=3, seq=6, d=4
    out = ln.forward(x)
    # Mean should be ~0, std ~1 per sample
    out_mean = np.mean(out, axis=-1)
    out_var = np.var(out, axis=-1)
    assert np.allclose(out_mean, 0, atol=1e-4), f"LayerNorm mean not zero: {out_mean[0,0]}"
    assert np.allclose(out_var, 1, atol=1e-4), f"LayerNorm var not one: {out_var[0,0]}"
    print("  PASS: LayerNorm normalizes to mean≈0, var≈1")

    dx_ln = ln.backward(np.ones_like(out))
    assert dx_ln.shape == x.shape
    print(f"  PASS: LayerNorm backward shape: {dx_ln.shape}")

    # Test 2: FeedForward shape
    ff = FeedForward(d_model=8, d_ff=32, random_seed=42)
    x_ff = np.random.randn(4, 10, 8)
    out_ff = ff.forward(x_ff)
    assert out_ff.shape == (4, 10, 8), f"FF output shape wrong: {out_ff.shape}"
    dx_ff, grads_ff = ff.backward(np.ones_like(out_ff))
    assert dx_ff.shape == x_ff.shape
    assert grads_ff["dW1"].shape == (8, 32)
    print("  PASS: FeedForward shapes correct")

    # Test 3: TransformerEncoderBlock forward
    block = TransformerEncoderBlock(d_model=16, num_heads=4, d_ff=64, random_seed=42)
    x_block = np.random.randn(2, 5, 16)
    out_block = block.forward(x_block)
    assert out_block.shape == (2, 5, 16), f"Encoder block output shape: {out_block.shape}"
    print(f"  PASS: Encoder block output shape: {out_block.shape}")

    # Test 4: Encoder block with causal mask
    try:
        from .attention import causal_mask
    except ImportError:
        from attention import causal_mask
    mask = causal_mask(5)
    out_masked = block.forward(x_block, mask=mask)
    assert out_masked.shape == (2, 5, 16)
    print("  PASS: Encoder block with mask preserves shape")

    # Test 5: Encoder block backward
    dx_block = block.backward(np.ones_like(out_block))
    assert dx_block.shape == (2, 5, 16), f"Block backward shape: {dx_block.shape}"
    assert np.all(np.isfinite(dx_block)), "Block backward produced NaN/Inf"
    print("  PASS: Encoder block backward produces finite gradients")

    # Test 6: Gradient check for LayerNorm
    ln2 = LayerNorm(d_model=4)
    x_small = np.array([[1.0, 2.0, 3.0, 4.0], [5.0, 6.0, 7.0, 8.0]], dtype=float)
    out_small = ln2.forward(x_small)
    dx_small = ln2.backward(np.ones_like(out_small))

    eps = 1e-6
    num_dx = np.zeros_like(x_small)
    for i in range(x_small.size):
        idx = np.unravel_index(i, x_small.shape)
        orig = x_small[idx]
        x_small[idx] = orig + eps
        yp = ln2.forward(x_small)
        lp = np.sum(yp)
        x_small[idx] = orig - eps
        ym = ln2.forward(x_small)
        lm = np.sum(ym)
        x_small[idx] = orig
        num_dx[idx] = (lp - lm) / (2 * eps)

    max_err = np.max(np.abs(dx_small - num_dx))
    assert max_err < 1e-6, f"LayerNorm gradient check failed: max abs error = {max_err:.2e}"
    print(f"  PASS: LayerNorm gradient check, max abs error = {max_err:.2e}")

    print("\nAll Transformer Block tests passed!")
