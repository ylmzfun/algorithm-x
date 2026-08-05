"""Simplified U-Net architecture and segmentation metrics from scratch.

Implements:
- Dice loss and IoU/Jaccard metric
- Simplified conv block (numpy-simulated)
- U-Net architecture explanation with encoder-decoder skip connections

Reference: Ronneberger et al., "U-Net: Convolutional Networks for
Biomedical Image Segmentation" (2015).
"""

from __future__ import annotations

import numpy as np
from typing import Optional


# ---------------------------------------------------------------------------
# Loss and Metric Functions
# ---------------------------------------------------------------------------

def dice_loss(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    smooth: float = 1.0,
) -> float:
    """Compute Dice loss for segmentation.

    Dice = 2 * |A ∩ B| / (|A| + |B|)
    Dice Loss = 1 - Dice

    Args:
        y_true: Ground truth binary mask [H, W] or [B, H, W].
        y_pred: Predicted probabilities [H, W] or [B, H, W] in [0, 1].
        smooth: Smoothing constant to avoid division by zero.

    Returns:
        Dice loss value.
    """
    y_true_f = y_true.ravel()
    y_pred_f = y_pred.ravel()
    intersection = np.sum(y_true_f * y_pred_f)
    dice = (2.0 * intersection + smooth) / (
        np.sum(y_true_f) + np.sum(y_pred_f) + smooth
    )
    return float(1.0 - dice)


def iou_metric(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    smooth: float = 1.0,
) -> float:
    """Compute IoU / Jaccard metric for segmentation.

    IoU = |A ∩ B| / |A ∪ B|

    Args:
        y_true: Ground truth binary mask [H, W] or [B, H, W].
        y_pred: Predicted probabilities [H, W] or [B, H, W] in [0, 1].
        smooth: Smoothing constant.

    Returns:
        IoU value in [0, 1].
    """
    y_true_f = y_true.ravel()
    y_pred_f = y_pred.ravel()
    intersection = np.sum(y_true_f * y_pred_f)
    union = np.sum(y_true_f) + np.sum(y_pred_f) - intersection
    return float((intersection + smooth) / (union + smooth))


def dice_coefficient(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    smooth: float = 1.0,
) -> float:
    """Compute Dice coefficient (F1 score for segmentation).

    Args:
        y_true: Ground truth binary mask.
        y_pred: Predicted binary mask or probabilities.
        smooth: Smoothing constant.

    Returns:
        Dice coefficient in [0, 1].
    """
    return 1.0 - dice_loss(y_true, y_pred, smooth)


# ---------------------------------------------------------------------------
# Conv Block (Simulated)
# ---------------------------------------------------------------------------

class ConvBlock:
    """Simplified convolutional block simulated with NumPy operations.

    In real U-Net this would be: Conv2D -> BatchNorm -> ReLU.
    Here we simulate with matrix operations for educational purposes.

    Attributes:
        in_channels: Number of input channels.
        out_channels: Number of output channels.
        kernel: Simulated convolution kernel.
    """

    def __init__(self, in_channels: int, out_channels: int, seed: int = 42) -> None:
        """Initialize a simulated conv block.

        Args:
            in_channels: Number of input channels.
            out_channels: Number of output channels.
            seed: Random seed.
        """
        rng = np.random.default_rng(seed)
        self.in_channels = in_channels
        self.out_channels = out_channels
        # Simulated kernel weights (3x3 conv simulated as dense projection)
        scale = np.sqrt(2.0 / (in_channels * 9))
        self.weight: np.ndarray = rng.normal(0, scale, (out_channels, in_channels, 9))
        self.bias: np.ndarray = np.zeros(out_channels)

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Simulated forward pass with edge-aware local averaging.

        Applies a learned linear combination of 3x3 patch values,
        followed by ReLU.

        Args:
            x: Input [H, W, C] or [B, H, W, C].

        Returns:
            Output with out_channels channels, same spatial dims.
        """
        if x.ndim == 3:
            return self._forward_2d(x)
        elif x.ndim == 4:
            outputs = [self._forward_2d(x[b]) for b in range(x.shape[0])]
            return np.stack(outputs, axis=0)
        raise ValueError(f"Expected 3D or 4D input, got shape {x.shape}")

    def _forward_2d(self, x: np.ndarray) -> np.ndarray:
        """2D forward with simulated 3x3 convolution."""
        h, w, c_in = x.shape
        c_out = self.out_channels
        # Pad input
        padded = np.pad(x, ((1, 1), (1, 1), (0, 0)), mode="reflect")
        out = np.zeros((h, w, c_out))
        for i in range(h):
            for j in range(w):
                patch = padded[i:i+3, j:j+3, :].reshape(-1)  # [c_in * 9]
                for co in range(c_out):
                    w_flat = self.weight[co].reshape(-1)
                    out[i, j, co] = np.dot(w_flat, patch) + self.bias[co]
        # ReLU
        return np.maximum(0, out)


# ---------------------------------------------------------------------------
# Simple U-Net
# ---------------------------------------------------------------------------

class SimpleUNet:
    """Simplified U-Net architecture for educational purposes.

    Architecture:
    - Encoder (contracting path): repeated ConvBlock + downsampling
    - Bottleneck: ConvBlock at the lowest resolution
    - Decoder (expanding path): upsampling + ConvBlock with skip connections

    Skip connections concatenate encoder features at the same resolution
    with the upsampled decoder features, preserving fine-grained spatial
    information.

    Attributes:
        enc1, enc2: Encoder ConvBlocks.
        bottleneck: Bottleneck ConvBlock.
        dec2, dec1: Decoder ConvBlocks.
        final: Final 1x1 conv to produce single-channel output.
    """

    def __init__(self, in_channels: int = 1, seed: int = 42) -> None:
        """Initialize a simplified U-Net.

        Args:
            in_channels: Number of input channels (1 for grayscale, 3 for RGB).
            seed: Random seed.
        """
        self.in_channels = in_channels

        # Encoder (downward path)
        self.enc1 = ConvBlock(in_channels, 16, seed=seed)
        self.enc2 = ConvBlock(16, 32, seed=seed + 1)

        # Bottleneck
        self.bottleneck = ConvBlock(32, 64, seed=seed + 2)

        # Decoder (upward path with skip connections)
        self.dec2 = ConvBlock(64 + 32, 32, seed=seed + 3)  # +32 from skip enc2
        self.dec1 = ConvBlock(32 + 16, 16, seed=seed + 4)  # +16 from skip enc1

        # Final 1x1 convolution
        rng = np.random.default_rng(seed + 5)
        self.final_weight: np.ndarray = rng.normal(0, 0.1, (16, 1))
        self.final_bias: np.ndarray = np.zeros(1)

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass through the U-Net.

        Args:
            x: Input image [H, W, C] or [B, H, W, C].

        Returns:
            Segmentation logits/probabilities [H, W, 1] or [B, H, W, 1].
        """
        if x.ndim == 3:
            return self._forward_2d(x)
        elif x.ndim == 4:
            outputs = [self._forward_2d(x[b]) for b in range(x.shape[0])]
            return np.stack(outputs, axis=0)
        raise ValueError(f"Expected 3D or 4D input, got shape {x.shape}")

    def _forward_2d(self, x: np.ndarray) -> np.ndarray:
        """2D forward pass with encoder-decoder and skip connections."""
        h, w, _ = x.shape

        # Encoder
        e1 = self.enc1.forward(x)                         # [H, W, 16]

        # Downsample (simple 2x2 average pooling)
        e1_ds = _avg_pool2d(e1, 2)                         # [H/2, W/2, 16]
        e2 = self.enc2.forward(e1_ds)                       # [H/2, W/2, 32]

        # Downsample
        e2_ds = _avg_pool2d(e2, 2)                          # [H/4, W/4, 32]

        # Bottleneck
        b = self.bottleneck.forward(e2_ds)                  # [H/4, W/4, 64]

        # Decoder — upsample + concat skip + conv
        # Upsample bottleneck to match e2 spatial dims
        b_up = _upsample_nearest(b, e2.shape[0])            # [H/2, W/2, 64]
        d2_in = np.concatenate([b_up, e2], axis=-1)         # [H/2, W/2, 96]
        d2 = self.dec2.forward(d2_in)                        # [H/2, W/2, 32]

        # Upsample to match e1 spatial dims
        d2_up = _upsample_nearest(d2, e1.shape[0])           # [H, W, 32]
        d1_in = np.concatenate([d2_up, e1], axis=-1)         # [H, W, 48]
        d1 = self.dec1.forward(d1_in)                        # [H, W, 16]

        # Final 1x1 conv
        out = np.zeros((h, w, 1))
        for i in range(h):
            for j in range(w):
                out[i, j, 0] = np.dot(d1[i, j], self.final_weight[:, 0]) + self.final_bias[0]

        # Sigmoid for binary segmentation
        out = 1.0 / (1.0 + np.exp(-np.clip(out, -50, 50)))
        return out


def _avg_pool2d(x: np.ndarray, kernel_size: int = 2) -> np.ndarray:
    """Simple 2D average pooling with stride = kernel_size.

    Args:
        x: Input [H, W, C].
        kernel_size: Pooling kernel size.

    Returns:
        Downsampled output.
    """
    h, w, c = x.shape
    new_h, new_w = h // kernel_size, w // kernel_size
    out = np.zeros((new_h, new_w, c))
    for i in range(new_h):
        for j in range(new_w):
            i_start = i * kernel_size
            j_start = j * kernel_size
            patch = x[i_start:i_start+kernel_size, j_start:j_start+kernel_size, :]
            out[i, j] = np.mean(patch, axis=(0, 1))
    return out


def _upsample_nearest(x: np.ndarray, target_h: int) -> np.ndarray:
    """Simple nearest-neighbour upsampling to reach target height.

    Args:
        x: Input [H_in, W_in, C].
        target_h: Target height (width will scale proportionally).

    Returns:
        Upsampled output [target_h, target_w, C].
    """
    h_in, w_in, c = x.shape
    target_w = int(w_in * target_h / h_in)
    out = np.zeros((target_h, target_w, c))
    for i in range(target_h):
        for j in range(target_w):
            si = int(i * h_in / target_h)
            sj = int(j * w_in / target_w)
            si = min(si, h_in - 1)
            sj = min(sj, w_in - 1)
            out[i, j] = x[si, sj]
    return out


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Testing image_segmentation.py — U-Net & Segmentation")
    print("=" * 60)

    all_pass = True

    # Test 1: Dice loss and IoU
    print("\n--- Dice Loss & IoU ---")
    # Create toy ground truth (rectangle)
    gt = np.zeros((32, 32))
    gt[8:24, 8:24] = 1.0

    # Perfect prediction
    dice_perfect = dice_coefficient(gt, gt)
    iou_perfect = iou_metric(gt, gt)
    print(f"  Perfect prediction: Dice={dice_perfect:.3f}, IoU={iou_perfect:.3f}")
    all_pass = all_pass and abs(dice_perfect - 1.0) < 0.01
    all_pass = all_pass and abs(iou_perfect - 1.0) < 0.01

    # Inverted prediction
    dice_inv = dice_coefficient(gt, 1.0 - gt)
    print(f"  Inverted prediction: Dice={dice_inv:.3f}")
    all_pass = all_pass and dice_inv < 0.5

    # Partial overlap
    pred_partial = np.zeros((32, 32))
    pred_partial[12:28, 12:28] = 1.0
    dice_partial = dice_coefficient(gt, pred_partial)
    print(f"  Partial overlap: Dice={dice_partial:.3f}")
    all_pass = all_pass and 0.3 < dice_partial < 0.9

    # Test 2: ConvBlock
    print("\n--- ConvBlock ---")
    conv = ConvBlock(1, 8, seed=42)
    dummy = np.random.randn(32, 32, 1)
    out = conv.forward(dummy)
    print(f"  Input shape:  {dummy.shape}")
    print(f"  Output shape: {out.shape}")
    shape_pass = out.shape == (32, 32, 8)
    all_pass = all_pass and shape_pass

    # Test 3: U-Net forward
    print("\n--- Simple U-Net ---")
    unet = SimpleUNet(in_channels=1, seed=42)
    test_img = np.random.randn(32, 32, 1)
    pred = unet.forward(test_img)
    print(f"  Input shape:  {test_img.shape}")
    print(f"  Output shape: {pred.shape}")
    unet_shape_pass = pred.shape == (32, 32, 1)
    all_pass = all_pass and unet_shape_pass

    # Test 4: Toy segmentation with shapes
    print("\n--- Toy Segmentation ---")
    # Ground truth: simple circle and rectangle
    gt_img = np.zeros((32, 32))
    # Draw circle in top-left
    for i in range(16):
        for j in range(16):
            if (i - 8)**2 + (j - 8)**2 <= 36:
                gt_img[i, j] = 1.0
    # Draw rectangle in bottom-right
    gt_img[18:28, 18:28] = 1.0

    # Simple threshold-based prediction (simulates model output near GT)
    pred_img = np.random.random((32, 32)) * 0.3 + gt_img * 0.7
    pred_img = np.clip(pred_img, 0, 1)

    dice = dice_coefficient(gt_img, pred_img)
    iou_val = iou_metric(gt_img, gt_img, smooth=0.5)
    dice_pred = dice_coefficient(gt_img, pred_img > 0.5)
    print(f"  Ground truth vs binarized pred: Dice={dice_pred:.3f}, "
          f"Soft Dice={dice:.3f}")
    all_pass = all_pass and dice_pred > 0.5

    print(f"\n{'PASS' if all_pass else 'FAIL'}: image_segmentation.py")
