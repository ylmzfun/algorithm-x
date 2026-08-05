"""Conv2d from scratch using the im2col approach.

Implements:
- im2col: transform image patches into matrix columns for efficient convolution
- col2im: inverse transform (for backward pass)
- Conv2d: 2D convolution with stride and padding support, forward + backward passes
"""

import numpy as np
from typing import Optional


def im2col(
    x: np.ndarray,
    kernel_h: int,
    kernel_w: int,
    stride: int,
    padding: int,
) -> np.ndarray:
    """Transform image regions into columns for efficient convolution.

    Rearranges a 4D input (N, C, H, W) into a 2D matrix (C*kh*kw, N*oh*ow)
    where each column corresponds to one convolution window.

    Args:
        x: Input of shape (N, C, H, W).
        kernel_h: Kernel height.
        kernel_w: Kernel width.
        stride: Convolution stride.
        padding: Zero-padding size.

    Returns:
        2D matrix of shape (C*kh*kw, N*oh*ow).
    """
    N, C, H, W = x.shape
    out_h = (H + 2 * padding - kernel_h) // stride + 1
    out_w = (W + 2 * padding - kernel_w) // stride + 1

    # Pad input
    if padding > 0:
        x_padded = np.pad(x, ((0, 0), (0, 0), (padding, padding), (padding, padding)), mode="constant")
    else:
        x_padded = x

    cols = np.zeros((N, C, kernel_h, kernel_w, out_h, out_w))
    for y in range(kernel_h):
        y_max = y + stride * out_h
        for xc in range(kernel_w):
            x_max = xc + stride * out_w
            cols[:, :, y, xc, :, :] = x_padded[:, :, y:y_max:stride, xc:x_max:stride]

    cols = cols.transpose(1, 2, 3, 0, 4, 5).reshape(C * kernel_h * kernel_w, N * out_h * out_w)
    return cols


def col2im(
    cols: np.ndarray,
    x_shape: tuple,
    kernel_h: int,
    kernel_w: int,
    stride: int,
    padding: int,
) -> np.ndarray:
    """Transform columns back to image shape (used in backward pass).

    Args:
        cols: Matrix of shape (C*kh*kw, N*oh*ow).
        x_shape: Original input shape (N, C, H, W).
        kernel_h: Kernel height.
        kernel_w: Kernel width.
        stride: Convolution stride.
        padding: Zero-padding size.

    Returns:
        Reconstructed array of shape x_shape.
    """
    N, C, H, W = x_shape
    out_h = (H + 2 * padding - kernel_h) // stride + 1
    out_w = (W + 2 * padding - kernel_w) // stride + 1

    cols_reshaped = cols.reshape(C, kernel_h, kernel_w, N, out_h, out_w).transpose(3, 0, 1, 2, 4, 5)
    img = np.zeros((N, C, H + 2 * padding + stride - 1, W + 2 * padding + stride - 1))

    for y in range(kernel_h):
        y_max = y + stride * out_h
        for xc in range(kernel_w):
            x_max = xc + stride * out_w
            img[:, :, y:y_max:stride, xc:x_max:stride] += cols_reshaped[:, :, y, xc, :, :]

    if padding > 0:
        return img[:, :, padding : padding + H, padding : padding + W]
    return img[:, :, :H, :W]


class Conv2d:
    """2D convolutional layer with im2col-based implementation.

    Supports stride, padding, and computes gradients for input, weights, and bias.
    """

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        kernel_size: int,
        stride: int = 1,
        padding: int = 0,
        random_seed: Optional[int] = 42,
    ):
        """Initialize Conv2d layer.

        Args:
            in_channels: Number of input channels.
            out_channels: Number of output channels (filters).
            kernel_size: Size of the square convolutional kernel.
            stride: Stride of convolution.
            padding: Zero-padding added to both sides of input.
            random_seed: Seed for weight initialization.
        """
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding

        rng = np.random.RandomState(random_seed)
        scale = np.sqrt(2.0 / (in_channels * kernel_size * kernel_size))
        # Weights: (out_channels, in_channels, kh, kw)
        self.W = rng.randn(out_channels, in_channels, kernel_size, kernel_size) * scale
        self.b = np.zeros((out_channels,))

        # Cache for backward pass
        self._cache: dict = {}

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass for Conv2d.

        Args:
            x: Input of shape (N, in_channels, H, W).

        Returns:
            Output of shape (N, out_channels, H_out, W_out).
        """
        N, C, H, W = x.shape
        out_h = (H + 2 * self.padding - self.kernel_size) // self.stride + 1
        out_w = (W + 2 * self.padding - self.kernel_size) // self.stride + 1

        # im2col
        cols = im2col(x, self.kernel_size, self.kernel_size, self.stride, self.padding)
        # cols: (C*kh*kw, N*oh*ow)

        # Reshape weights to (out_channels, C*kh*kw)
        W_col = self.W.reshape(self.out_channels, -1)

        # Convolution: (out_channels, C*kh*kw) @ (C*kh*kw, N*oh*ow) = (out_channels, N*oh*ow)
        out = np.dot(W_col, cols) + self.b.reshape(-1, 1)
        out = out.reshape(self.out_channels, N, out_h, out_w).transpose(1, 0, 2, 3)

        # Cache for backward
        self._cache = {"cols": cols, "x_shape": x.shape, "W_col": W_col}

        return out

    def backward(self, dout: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Backward pass for Conv2d.

        Args:
            dout: Upstream gradient of shape (N, out_channels, H_out, W_out).

        Returns:
            Tuple of (dx, dW, db): gradients w.r.t. input, weights, and bias.
        """
        cols = self._cache["cols"]
        x_shape = self._cache["x_shape"]
        N = x_shape[0]

        # dout shape: (N, out_channels, oh, ow)
        # Reshape to (out_channels, N*oh*ow)
        dout_flat = dout.transpose(1, 0, 2, 3).reshape(self.out_channels, -1)

        # Gradient w.r.t. weights: dW = dout_flat @ cols.T
        dW = np.dot(dout_flat, cols.T).reshape(self.out_channels, self.in_channels,
                                                self.kernel_size, self.kernel_size)

        # Gradient w.r.t. bias: db = sum over spatial and batch dims
        db = np.sum(dout, axis=(0, 2, 3))

        # Gradient w.r.t. input: dx = W_col.T @ dout_flat, then col2im
        W_col = self._cache["W_col"]
        dcols = np.dot(W_col.T, dout_flat)  # (C*kh*kw, N*oh*ow)
        dx = col2im(dcols, x_shape, self.kernel_size, self.kernel_size,
                    self.stride, self.padding)

        return dx, dW, db

    def __call__(self, x: np.ndarray) -> np.ndarray:
        """Convenience call for forward pass."""
        return self.forward(x)


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing Conv2d (im2col approach)...")

    np.random.seed(42)

    # Test 1: im2col and col2im round-trip
    x = np.arange(1 * 3 * 4 * 4).reshape(1, 3, 4, 4).astype(float)
    cols = im2col(x, kernel_h=3, kernel_w=3, stride=1, padding=0)
    x_recon = col2im(cols, x.shape, kernel_h=3, kernel_w=3, stride=1, padding=0)
    # col2im fills overlapping regions additively; the reconstruction won't be exact
    # but the shape should match
    assert x_recon.shape == x.shape, f"col2im shape mismatch: {x_recon.shape}"
    print("  PASS: im2col/col2im shapes correct")

    # Test 2: Forward pass output shape
    conv = Conv2d(in_channels=3, out_channels=8, kernel_size=3, stride=1, padding=1)
    x2 = np.random.randn(2, 3, 32, 32)
    out = conv.forward(x2)
    expected_h = (32 + 2 * 1 - 3) // 1 + 1
    assert expected_h == 32, f"Unexpected output height: {expected_h}"
    assert out.shape == (2, 8, 32, 32), f"Wrong output shape: {out.shape}"
    print(f"  PASS: Forward output shape: {out.shape}")

    # Test 3: Forward with stride
    conv_s2 = Conv2d(in_channels=3, out_channels=4, kernel_size=3, stride=2, padding=1)
    out_s2 = conv_s2.forward(x2)
    expected_h2 = (32 + 2 * 1 - 3) // 2 + 1
    assert out_s2.shape == (2, 4, expected_h2, expected_h2), f"Wrong stride output: {out_s2.shape}"
    print(f"  PASS: Stride=2 output shape: {out_s2.shape}")

    # Test 4: Forward with padding=0
    conv_p0 = Conv2d(in_channels=3, out_channels=4, kernel_size=3, stride=1, padding=0)
    out_p0 = conv_p0.forward(x2)
    expected_h0 = 32 - 3 + 1
    assert out_p0.shape == (2, 4, expected_h0, expected_h0), f"Wrong no-padding output: {out_p0.shape}"
    print(f"  PASS: Padding=0 output shape: {out_p0.shape}")

    # Test 5: Backward pass shapes
    dout = np.random.randn(*out.shape)
    dx, dW, db = conv.backward(dout)
    assert dx.shape == x2.shape, f"dx shape mismatch: {dx.shape}"
    assert dW.shape == conv.W.shape, f"dW shape mismatch: {dW.shape}"
    assert db.shape == (8,), f"db shape mismatch: {db.shape}"
    print("  PASS: Backward pass gradient shapes correct")

    # Test 6: Gradient check (numerical)
    conv_check = Conv2d(in_channels=2, out_channels=1, kernel_size=2, stride=1, padding=0, random_seed=123)
    x_check = np.random.randn(1, 2, 3, 3)
    dout_check = np.random.randn(1, 1, 2, 2)

    out_check = conv_check.forward(x_check)
    dx_check, dW_check, db_check = conv_check.backward(dout_check)

    # Numerical gradient for input
    eps = 1e-5
    num_dx = np.zeros_like(x_check)
    for i in range(x_check.size):
        idx = np.unravel_index(i, x_check.shape)
        orig = x_check[idx]
        x_check[idx] = orig + eps
        y_plus = conv_check.forward(x_check)
        lp = np.sum(y_plus * dout_check)
        x_check[idx] = orig - eps
        y_minus = conv_check.forward(x_check)
        lm = np.sum(y_minus * dout_check)
        x_check[idx] = orig
        num_dx[idx] = (lp - lm) / (2 * eps)

    max_err = np.max(np.abs(dx_check - num_dx)) / (np.max(np.abs(num_dx)) + 1e-10)
    assert max_err < 1e-4, f"Gradient check failed: max rel error = {max_err:.2e}"
    print(f"  PASS: Gradient check (dx), max rel error = {max_err:.2e}")

    # Test 7: Different kernel sizes
    for ks in [1, 3, 5]:
        c = Conv2d(in_channels=3, out_channels=2, kernel_size=ks, stride=1, padding=ks // 2)
        out_ks = c.forward(x2)
        assert out_ks.shape[2] == x2.shape[2], f"kernel_size={ks}: height changed"
        assert out_ks.shape[3] == x2.shape[3], f"kernel_size={ks}: width changed"
    print("  PASS: Various kernel sizes with same-spacing padding preserve dimensions")

    print("\nAll Conv2d tests passed!")
