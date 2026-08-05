"""Classic CNN architectures implemented with PyTorch.

Includes: LeNet-5, simplified VGG, ResNet block, and simplified ResNet-18.
"""

import numpy as np
from typing import Optional

_HAS_TORCH = False
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    _HAS_TORCH = True
except ImportError:
    pass


# ============================================================================
# LeNet-5
# ============================================================================
class LeNet5(nn.Module if _HAS_TORCH else object):
    """LeNet-5 architecture for 32×32 grayscale input.

    Original LeNet-5 used 32×32 input. Architecture:
    Conv(1→6, 5×5) → AvgPool(2×2) → Conv(6→16, 5×5) → AvgPool(2×2) →
    Flatten → FC(120) → FC(84) → FC(10)
    """

    def __init__(self, num_classes: int = 10):
        """Initialize LeNet-5.

        Args:
            num_classes: Number of output classes.
        """
        if not _HAS_TORCH:
            raise ImportError("PyTorch is required for LeNet5. Install with: pip install torch")
        super().__init__()
        self.conv1 = nn.Conv2d(1, 6, kernel_size=5, stride=1, padding=2)
        self.pool1 = nn.AvgPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(6, 16, kernel_size=5, stride=1)
        self.pool2 = nn.AvgPool2d(kernel_size=2, stride=2)
        # After two 2×2 pools on 32×32 → 6×6 feature maps
        self.fc1 = nn.Linear(16 * 6 * 6, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, num_classes)

    def forward(self, x: "torch.Tensor") -> "torch.Tensor":
        """Forward pass.

        Args:
            x: Input of shape (N, 1, 32, 32).

        Returns:
            Logits of shape (N, num_classes).
        """
        x = self.pool1(F.relu(self.conv1(x)))    # (N, 6, 16, 16)
        x = self.pool2(F.relu(self.conv2(x)))    # (N, 16, 6, 6)
        x = x.view(x.size(0), -1)                # (N, 16*6*6)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


# ============================================================================
# Simplified VGG
# ============================================================================
class SimpleVGG(nn.Module if _HAS_TORCH else object):
    """Simplified VGG-style network with configurable architecture.

    Uses blocks of Conv → Conv → MaxPool with batch normalization.
    """

    def __init__(
        self,
        conv_config: list[tuple[int, int]] = None,
        num_classes: int = 10,
        input_channels: int = 3,
    ):
        """Initialize SimpleVGG.

        Args:
            conv_config: List of (out_channels, num_convs) per block.
                         Default: [(64, 2), (128, 2), (256, 3)].
            num_classes: Number of output classes.
            input_channels: Number of input channels (3 for RGB).
        """
        if not _HAS_TORCH:
            raise ImportError("PyTorch is required for SimpleVGG.")
        super().__init__()

        if conv_config is None:
            conv_config = [(64, 2), (128, 2), (256, 3)]

        layers = []
        in_ch = input_channels
        for out_ch, n_convs in conv_config:
            for _ in range(n_convs):
                layers.append(nn.Conv2d(in_ch, out_ch, kernel_size=3, padding=1))
                layers.append(nn.BatchNorm2d(out_ch))
                layers.append(nn.ReLU(inplace=True))
                in_ch = out_ch
            layers.append(nn.MaxPool2d(2))

        self.features = nn.Sequential(*layers)

        # Compute FC input size (assuming 32×32 input)
        with torch.no_grad():
            dummy = torch.zeros(1, input_channels, 32, 32)
            dummy_out = self.features(dummy)
            fc_in = dummy_out.view(1, -1).size(1)

        self.classifier = nn.Sequential(
            nn.Linear(fc_in, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes),
        )

    def forward(self, x: "torch.Tensor") -> "torch.Tensor":
        """Forward pass.

        Args:
            x: Input of shape (N, C, 32, 32).

        Returns:
            Logits of shape (N, num_classes).
        """
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x


# ============================================================================
# ResNet Block
# ============================================================================
class ResNetBlock(nn.Module if _HAS_TORCH else object):
    """Basic ResNet block with skip connection.

    Architecture: Conv → BN → ReLU → Conv → BN → (+skip) → ReLU
    If stride != 1 or in_channels != out_channels, uses 1×1 conv in skip.
    """

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        stride: int = 1,
        downsample: bool = False,
    ):
        """Initialize ResNet block.

        Args:
            in_channels: Number of input channels.
            out_channels: Number of output channels.
            stride: Stride for the first conv layer.
            downsample: Whether to use 1×1 conv in skip connection.
        """
        if not _HAS_TORCH:
            raise ImportError("PyTorch is required for ResNetBlock.")
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3,
                               stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3,
                               stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)

        # Skip connection
        if stride != 1 or in_channels != out_channels or downsample:
            self.skip = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1,
                         stride=stride, bias=False),
                nn.BatchNorm2d(out_channels),
            )
        else:
            self.skip = nn.Identity()

    def forward(self, x: "torch.Tensor") -> "torch.Tensor":
        """Forward pass with skip connection.

        Args:
            x: Input of shape (N, in_channels, H, W).

        Returns:
            Output of shape (N, out_channels, H', W').
        """
        identity = self.skip(x)
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += identity
        out = F.relu(out)
        return out


# ============================================================================
# Simplified ResNet-18
# ============================================================================
class ResNet18(nn.Module if _HAS_TORCH else object):
    """Simplified ResNet-18 architecture.

    Architecture: Conv7×7 → MaxPool → [2×ResBlock, 2×ResBlock, 2×ResBlock, 2×ResBlock] → AvgPool → FC
    """

    def __init__(self, num_classes: int = 10, input_channels: int = 3):
        """Initialize ResNet-18.

        Args:
            num_classes: Number of output classes.
            input_channels: Number of input channels.
        """
        if not _HAS_TORCH:
            raise ImportError("PyTorch is required for ResNet18.")
        super().__init__()

        self.conv1 = nn.Conv2d(input_channels, 64, kernel_size=7, stride=2,
                               padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        # Layer blocks
        self.layer1 = self._make_layer(64, 64, 2, stride=1)
        self.layer2 = self._make_layer(64, 128, 2, stride=2)
        self.layer3 = self._make_layer(128, 256, 2, stride=2)
        self.layer4 = self._make_layer(256, 512, 2, stride=2)

        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512, num_classes)

    def _make_layer(
        self,
        in_channels: int,
        out_channels: int,
        num_blocks: int,
        stride: int,
    ) -> "nn.Sequential":
        """Create a layer of ResNet blocks.

        Args:
            in_channels: Input channels.
            out_channels: Output channels.
            num_blocks: Number of ResNet blocks.
            stride: Stride for the first block.

        Returns:
            Sequential container of ResNet blocks.
        """
        layers = []
        layers.append(ResNetBlock(in_channels, out_channels, stride=stride,
                                   downsample=(in_channels != out_channels)))
        for _ in range(1, num_blocks):
            layers.append(ResNetBlock(out_channels, out_channels, stride=1))
        return nn.Sequential(*layers)

    def forward(self, x: "torch.Tensor") -> "torch.Tensor":
        """Forward pass.

        Args:
            x: Input of shape (N, C, H, W).

        Returns:
            Logits of shape (N, num_classes).
        """
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.maxpool(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    if not _HAS_TORCH:
        print("SKIP: PyTorch not installed. Install with: pip install torch")
        exit(0)

    print("Testing classic networks (PyTorch)...")

    device = torch.device("cpu")
    batch_size = 4

    # Test 1: LeNet-5 forward shape
    lenet = LeNet5(num_classes=10)
    x = torch.randn(batch_size, 1, 32, 32)
    out = lenet(x)
    assert out.shape == (batch_size, 10), f"LeNet-5 output shape wrong: {out.shape}"
    n_params = sum(p.numel() for p in lenet.parameters())
    print(f"  PASS: LeNet-5 output shape: {out.shape}, params: {n_params:,}")

    # Test 2: LeNet-5 training step
    optimizer = torch.optim.SGD(lenet.parameters(), lr=0.01)
    y = torch.randint(0, 10, (batch_size,))
    loss = F.cross_entropy(out, y)
    loss.backward()
    optimizer.step()
    assert loss.item() > 0, "Loss should be positive"
    print(f"  PASS: LeNet-5 training step, loss: {loss.item():.4f}")

    # Test 3: SimpleVGG forward
    vgg = SimpleVGG(conv_config=[(32, 2), (64, 2)], num_classes=10, input_channels=3)
    x_vgg = torch.randn(batch_size, 3, 32, 32)
    out_vgg = vgg(x_vgg)
    assert out_vgg.shape == (batch_size, 10), f"VGG output shape wrong: {out_vgg.shape}"
    n_params_vgg = sum(p.numel() for p in vgg.parameters())
    print(f"  PASS: SimpleVGG output shape: {out_vgg.shape}, params: {n_params_vgg:,}")

    # Test 4: ResNetBlock forward
    block = ResNetBlock(64, 128, stride=2, downsample=True)
    x_block = torch.randn(batch_size, 64, 32, 32)
    out_block = block(x_block)
    assert out_block.shape == (batch_size, 128, 16, 16), f"ResBlock shape wrong: {out_block.shape}"
    print(f"  PASS: ResNetBlock output shape: {out_block.shape}")

    # Test 5: ResNetBlock identity (same channels)
    block_id = ResNetBlock(64, 64, stride=1)
    x_id = torch.randn(batch_size, 64, 32, 32)
    out_id = block_id(x_id)
    assert out_id.shape == x_id.shape, f"Identity block should preserve shape: {out_id.shape}"
    assert out_id.shape == (batch_size, 64, 32, 32)
    print("  PASS: ResNetBlock identity preserves shape")

    # Test 6: ResNet-18 forward (small input)
    resnet = ResNet18(num_classes=10, input_channels=3)
    x_rn = torch.randn(batch_size, 3, 64, 64)
    out_rn = resnet(x_rn)
    assert out_rn.shape == (batch_size, 10), f"ResNet-18 output shape wrong: {out_rn.shape}"
    n_params_rn = sum(p.numel() for p in resnet.parameters())
    print(f"  PASS: ResNet-18 output shape: {out_rn.shape}, params: {n_params_rn:,}")

    # Test 7: All models produce valid logits
    for name, model in [("LeNet5", lenet), ("SimpleVGG", vgg), ("ResNet18", resnet)]:
        model.eval()
        with torch.no_grad():
            for param in model.parameters():
                assert not torch.isnan(param).any(), f"{name} has NaN parameters"
        assert not torch.isnan(out).any(), f"{name} outputs NaN"
    print("  PASS: All models produce valid (non-NaN) outputs")

    print("\nAll classic network tests passed!")
