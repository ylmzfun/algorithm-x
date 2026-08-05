"""MaxPool2d and AvgPool2d from scratch using NumPy.

Implements:
- MaxPool2d: max pooling with mask recording for backward pass
- AvgPool2d: average pooling with uniform gradient distribution in backward pass
"""

import numpy as np
from typing import Optional


class MaxPool2d:
    """2D max pooling layer.

    During forward pass, records which positions were the max (mask) for
    routing gradients in the backward pass.
    """

    def __init__(self, kernel_size: int, stride: Optional[int] = None):
        """Initialize MaxPool2d.

        Args:
            kernel_size: Size of the pooling window (square).
            stride: Stride of pooling. Defaults to kernel_size.
        """
        self.kernel_size = kernel_size
        self.stride = stride if stride is not None else kernel_size
        self._cache: dict = {}

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass: max pooling.

        Args:
            x: Input of shape (N, C, H, W).

        Returns:
            Output of shape (N, C, H_out, W_out).
        """
        N, C, H, W = x.shape
        kh, kw = self.kernel_size, self.kernel_size
        stride = self.stride

        out_h = (H - kh) // stride + 1
        out_w = (W - kw) // stride + 1

        out = np.zeros((N, C, out_h, out_w))
        mask = np.zeros_like(x)  # Records max positions

        for i in range(out_h):
            for j in range(out_w):
                h_start = i * stride
                h_end = h_start + kh
                w_start = j * stride
                w_end = w_start + kw

                region = x[:, :, h_start:h_end, w_start:w_end]          # (N, C, kh, kw)
                max_vals = np.max(region, axis=(2, 3), keepdims=True)   # (N, C, 1, 1)
                out[:, :, i, j] = max_vals.squeeze(2).squeeze(2)

                # Record mask: 1 at max position, 0 elsewhere
                is_max = (region == max_vals)
                mask[:, :, h_start:h_end, w_start:w_end] += is_max.astype(float)

        self._cache = {"mask": mask, "x_shape": x.shape}
        return out

    def backward(self, dout: np.ndarray) -> np.ndarray:
        """Backward pass: route gradient only through max positions.

        Args:
            dout: Upstream gradient of shape (N, C, H_out, W_out).

        Returns:
            Gradient w.r.t. input of shape (N, C, H, W).
        """
        mask = self._cache["mask"]
        N, C, H, W = self._cache["x_shape"]
        kh, kw = self.kernel_size, self.kernel_size
        stride = self.stride

        dx = np.zeros_like(mask)
        out_h, out_w = dout.shape[2], dout.shape[3]

        for i in range(out_h):
            for j in range(out_w):
                h_start = i * stride
                h_end = h_start + kh
                w_start = j * stride
                w_end = w_start + kw

                # Gradient flows only through max positions
                dx[:, :, h_start:h_end, w_start:w_end] += (
                    dout[:, :, i:i + 1, j:j + 1] *
                    mask[:, :, h_start:h_end, w_start:w_end]
                )

        return dx


class AvgPool2d:
    """2D average pooling layer.

    Output is the average of each pooling window.
    Gradient is evenly distributed back to all positions in the window.
    """

    def __init__(self, kernel_size: int, stride: Optional[int] = None):
        """Initialize AvgPool2d.

        Args:
            kernel_size: Size of the pooling window (square).
            stride: Stride of pooling. Defaults to kernel_size.
        """
        self.kernel_size = kernel_size
        self.stride = stride if stride is not None else kernel_size
        self._cache: dict = {}

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass: average pooling.

        Args:
            x: Input of shape (N, C, H, W).

        Returns:
            Output of shape (N, C, H_out, W_out).
        """
        N, C, H, W = x.shape
        kh, kw = self.kernel_size, self.kernel_size
        stride = self.stride

        out_h = (H - kh) // stride + 1
        out_w = (W - kw) // stride + 1

        out = np.zeros((N, C, out_h, out_w))
        area = kh * kw

        for i in range(out_h):
            for j in range(out_w):
                h_start = i * stride
                h_end = h_start + kh
                w_start = j * stride
                w_end = w_start + kw

                region = x[:, :, h_start:h_end, w_start:w_end]
                out[:, :, i, j] = np.mean(region, axis=(2, 3))

        self._cache = {"x_shape": x.shape, "area": area}
        return out

    def backward(self, dout: np.ndarray) -> np.ndarray:
        """Backward pass: evenly distribute gradient to all positions in window.

        Args:
            dout: Upstream gradient of shape (N, C, H_out, W_out).

        Returns:
            Gradient w.r.t. input of shape (N, C, H, W).
        """
        N, C, H, W = self._cache["x_shape"]
        kh, kw = self.kernel_size, self.kernel_size
        stride = self.stride
        area = self._cache["area"]

        dx = np.zeros((N, C, H, W))
        out_h, out_w = dout.shape[2], dout.shape[3]

        for i in range(out_h):
            for j in range(out_w):
                h_start = i * stride
                h_end = h_start + kh
                w_start = j * stride
                w_end = w_start + kw

                # Even distribution
                dx[:, :, h_start:h_end, w_start:w_end] += dout[:, :, i:i + 1, j:j + 1] / area

        return dx


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing Pooling layers...")

    np.random.seed(42)

    # Test 1: MaxPool2d output shape and values
    x = np.array([[[[1.0, 2.0, 3.0, 4.0],
                    [5.0, 6.0, 7.0, 8.0],
                    [9.0, 10.0, 11.0, 12.0],
                    [13.0, 14.0, 15.0, 16.0]]]])
    # x shape: (1, 1, 4, 4)

    mp = MaxPool2d(kernel_size=2, stride=2)
    out_mp = mp.forward(x)
    expected_mp = np.array([[[[6.0, 8.0], [14.0, 16.0]]]])
    assert out_mp.shape == (1, 1, 2, 2), f"Wrong MaxPool shape: {out_mp.shape}"
    assert np.allclose(out_mp, expected_mp), f"MaxPool values wrong: {out_mp}"
    print("  PASS: MaxPool2d output shape and values")

    # Test 2: AvgPool2d output
    ap = AvgPool2d(kernel_size=2, stride=2)
    out_ap = ap.forward(x)
    expected_ap = (1 + 2 + 5 + 6) / 4  # = 3.5 for first cell
    assert out_ap.shape == (1, 1, 2, 2)
    assert np.isclose(out_ap[0, 0, 0, 0], expected_ap), f"AvgPool values wrong: {out_ap[0,0,0,0]}"
    print("  PASS: AvgPool2d output shape and values")

    # Test 3: MaxPool backward
    dout = np.ones((1, 1, 2, 2))
    dx_mp = mp.backward(dout)
    # Only max positions should get gradient
    # Max positions were: (0,1,1), (0,1,3), (0,3,1), (0,3,3)
    # (batch, channel, row, col) with zero-indexing
    expected_mask = np.array([[[[0.0, 0.0, 0.0, 0.0],
                                [0.0, 1.0, 0.0, 1.0],
                                [0.0, 0.0, 0.0, 0.0],
                                [0.0, 1.0, 0.0, 1.0]]]])
    assert np.allclose(dx_mp, expected_mask), f"MaxPool backward wrong:\n{dx_mp}"
    assert np.sum(dx_mp) == np.sum(dout), f"Gradient sum not preserved: {np.sum(dx_mp)}"
    print("  PASS: MaxPool2d backward correct")

    # Test 4: AvgPool backward
    dx_ap = ap.backward(dout)
    assert np.sum(dx_ap) == np.sum(dout), f"AvgPool gradient sum not preserved: {np.sum(dx_ap)}"
    # Each value should be 1/4 = 0.25
    assert np.allclose(dx_ap, np.full((1, 1, 4, 4), 0.25)), f"AvgPool backward wrong"
    print("  PASS: AvgPool2d backward correct")

    # Test 5: Batched input
    x_batch = np.random.randn(4, 3, 8, 8)
    mp_batch = MaxPool2d(kernel_size=2, stride=2)
    out_batch = mp_batch.forward(x_batch)
    assert out_batch.shape == (4, 3, 4, 4), f"Batch MaxPool shape: {out_batch.shape}"
    dx_batch = mp_batch.backward(np.ones_like(out_batch))
    assert dx_batch.shape == x_batch.shape, f"Batch backward shape: {dx_batch.shape}"
    print(f"  PASS: Batched MaxPool: {out_batch.shape}")

    # Test 6: Gradient check for MaxPool
    x_grad = np.random.randn(1, 1, 4, 4)
    mp_grad = MaxPool2d(kernel_size=2, stride=2)
    out_grad = mp_grad.forward(x_grad)
    dout_grad = np.random.randn(*out_grad.shape)
    dx_grad = mp_grad.backward(dout_grad)

    eps = 1e-5
    num_dx = np.zeros_like(x_grad)
    for i in range(x_grad.size):
        idx = np.unravel_index(i, x_grad.shape)
        orig = x_grad[idx]
        x_grad[idx] = orig + eps
        yp = mp_grad.forward(x_grad)
        lp = np.sum(yp * dout_grad)
        x_grad[idx] = orig - eps
        ym = mp_grad.forward(x_grad)
        lm = np.sum(ym * dout_grad)
        x_grad[idx] = orig
        num_dx[idx] = (lp - lm) / (2 * eps)

    max_err = np.max(np.abs(dx_grad - num_dx)) / (np.max(np.abs(num_dx)) + 1e-10)
    assert max_err < 1e-6, f"MaxPool gradient check failed: {max_err:.2e}"
    print(f"  PASS: MaxPool gradient check, max rel error = {max_err:.2e}")

    # Test 7: Non-square kernel (kernel_size=3, stride=1)
    mp3 = MaxPool2d(kernel_size=3, stride=1)
    out3 = mp3.forward(x_batch)
    assert out3.shape == (4, 3, 6, 6), f"MaxPool3 shape: {out3.shape}"
    print(f"  PASS: kernel_size=3, stride=1 shape: {out3.shape}")

    print("\nAll Pooling tests passed!")
