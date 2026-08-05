"""Vision Transformer (ViT) from scratch using NumPy.

Implements:
- Patch embedding: splitting images into fixed-size patches
- Positional embeddings (learnable)
- Multi-head self-attention for patches
- Transformer encoder with MLP
- Classification head

Reference: Dosovitskiy et al., "An Image is Worth 16x16 Words:
Transformers for Image Recognition at Scale" (2021).
"""

from __future__ import annotations

import numpy as np
from typing import Optional


# ---------------------------------------------------------------------------
# Patch Embedding
# ---------------------------------------------------------------------------

def patch_embedding(
    images: np.ndarray, patch_size: int
) -> np.ndarray:
    """Split images into patches and flatten them.

    Args:
        images: Input images [B, H, W, C] or [H, W, C].
        patch_size: Size of each square patch (e.g., 4).

    Returns:
        Patch matrix [B, num_patches, patch_size*patch_size*C]
        or [num_patches, patch_dim].
    """
    single = images.ndim == 3
    if single:
        images = images[np.newaxis, ...]  # [1, H, W, C]

    batch, h, w, c = images.shape
    assert h % patch_size == 0 and w % patch_size == 0, \
        f"Image dims ({h},{w}) must be divisible by patch_size ({patch_size})"

    n_patches_h = h // patch_size
    n_patches_w = w // patch_size
    num_patches = n_patches_h * n_patches_w
    patch_dim = patch_size * patch_size * c

    patches = np.zeros((batch, num_patches, patch_dim))
    for b in range(batch):
        idx = 0
        for i in range(n_patches_h):
            for j in range(n_patches_w):
                patch = images[
                    b,
                    i * patch_size: (i + 1) * patch_size,
                    j * patch_size: (j + 1) * patch_size,
                    :,
                ]
                patches[b, idx] = patch.ravel()
                idx += 1

    return patches[0] if single else patches


def positional_embedding(
    num_patches: int, dim: int, seed: int = 42
) -> np.ndarray:
    """Create learnable positional embeddings (random init).

    Args:
        num_patches: Number of patches + 1 (for CLS token).
        dim: Embedding dimension.
        seed: Random seed.

    Returns:
        Positional embedding matrix [num_patches, dim].
    """
    rng = np.random.default_rng(seed)
    return rng.normal(0, 0.02, (num_patches, dim))


# ---------------------------------------------------------------------------
# Multi-Head Self-Attention
# ---------------------------------------------------------------------------

class MultiHeadSelfAttention:
    """Multi-head scaled dot-product self-attention.

    Attributes:
        d_model: Total model dimension.
        num_heads: Number of attention heads.
        d_k: Dimension per head.
    """

    def __init__(self, d_model: int, num_heads: int, seed: int = 42) -> None:
        """Initialize multi-head attention.

        Args:
            d_model: Model dimension.
            num_heads: Number of attention heads.
            seed: Random seed.
        """
        assert d_model % num_heads == 0
        rng = np.random.default_rng(seed)
        scale = np.sqrt(2.0 / d_model)
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        self.W_q: np.ndarray = rng.normal(0, scale, (d_model, d_model))
        self.W_k: np.ndarray = rng.normal(0, scale, (d_model, d_model))
        self.W_v: np.ndarray = rng.normal(0, scale, (d_model, d_model))
        self.W_o: np.ndarray = rng.normal(0, scale, (d_model, d_model))

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass.

        Args:
            x: [B, N, d_model].

        Returns:
            [B, N, d_model].
        """
        batch, n_tokens, d_model = x.shape
        h, d_k = self.num_heads, self.d_k

        Q = (x @ self.W_q).reshape(batch, n_tokens, h, d_k).transpose(0, 2, 1, 3)
        K = (x @ self.W_k).reshape(batch, n_tokens, h, d_k).transpose(0, 2, 1, 3)
        V = (x @ self.W_v).reshape(batch, n_tokens, h, d_k).transpose(0, 2, 1, 3)

        scores = Q @ K.transpose(0, 1, 3, 2) / np.sqrt(d_k)
        attn = _softmax(scores, axis=-1)
        ctx = attn @ V
        ctx = ctx.transpose(0, 2, 1, 3).reshape(batch, n_tokens, d_model)
        return ctx @ self.W_o


def _softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    e = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return e / np.sum(e, axis=axis, keepdims=True)


def _layer_norm(x: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    mean = np.mean(x, axis=-1, keepdims=True)
    var = np.var(x, axis=-1, keepdims=True)
    return (x - mean) / np.sqrt(var + eps)


# ---------------------------------------------------------------------------
# Transformer Encoder
# ---------------------------------------------------------------------------

class TransformerEncoder:
    """Transformer encoder (stack of attention + MLP blocks).

    Attributes:
        attention: Multi-head self-attention layer.
        W1, W2: MLP weights.
        b1, b2: MLP biases.
    """

    def __init__(self, d_model: int, num_heads: int, d_ff: int, seed: int = 42) -> None:
        """Initialize the encoder.

        Args:
            d_model: Model dimension.
            num_heads: Number of attention heads.
            d_ff: Feed-forward hidden dimension.
            seed: Random seed.
        """
        rng = np.random.default_rng(seed)
        scale = np.sqrt(2.0 / d_model)
        self.attention = MultiHeadSelfAttention(d_model, num_heads, seed=seed)
        self.W1: np.ndarray = rng.normal(0, scale, (d_model, d_ff))
        self.b1: np.ndarray = np.zeros(d_ff)
        self.W2: np.ndarray = rng.normal(0, scale, (d_ff, d_model))
        self.b2: np.ndarray = np.zeros(d_model)

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass.

        Args:
            x: [B, N, d_model].

        Returns:
            [B, N, d_model].
        """
        # Attention + residual + LN
        attn_out = self.attention.forward(x)
        x = _layer_norm(x + attn_out)
        # MLP + residual + LN
        mlp_out = self._mlp(x)
        x = _layer_norm(x + mlp_out)
        return x

    def _mlp(self, x: np.ndarray) -> np.ndarray:
        """Two-layer MLP with GELU."""
        # GELU approx
        h = x @ self.W1 + self.b1
        gelu = 0.5 * h * (1.0 + np.tanh(np.sqrt(2.0 / np.pi) * (h + 0.044715 * h**3)))
        return gelu @ self.W2 + self.b2


# ---------------------------------------------------------------------------
# Simple ViT
# ---------------------------------------------------------------------------

class SimpleViT:
    """Simplified Vision Transformer for small image classification.

    Process:
    1. Split image into patches → flatten → linear projection
    2. Prepend learnable [CLS] token
    3. Add positional embeddings
    4. Pass through transformer encoder
    5. Use [CLS] token output for classification

    Attributes:
        patch_size: Patch dimension.
        d_model: Hidden dimension.
        num_classes: Number of output classes.
    """

    def __init__(
        self,
        image_size: int = 32,
        patch_size: int = 8,
        in_channels: int = 1,
        d_model: int = 64,
        num_heads: int = 4,
        d_ff: int = 128,
        num_layers: int = 2,
        num_classes: int = 2,
        seed: int = 42,
    ) -> None:
        """Initialize the Vision Transformer.

        Args:
            image_size: Size of square input image.
            patch_size: Size of each square patch.
            in_channels: Number of input channels.
            d_model: Hidden dimension.
            num_heads: Attention heads (must divide d_model).
            d_ff: Feed-forward hidden dimension.
            num_layers: Number of transformer encoder layers.
            num_classes: Number of output classes.
            seed: Random seed.
        """
        assert image_size % patch_size == 0
        num_patches = (image_size // patch_size) ** 2
        patch_dim = patch_size * patch_size * in_channels

        rng = np.random.default_rng(seed)
        self.patch_size = patch_size
        self.d_model = d_model
        self.num_classes = num_classes

        # Patch projection
        scale_p = np.sqrt(2.0 / patch_dim)
        self.patch_proj: np.ndarray = rng.normal(0, scale_p, (patch_dim, d_model))

        # CLS token (learnable)
        self.cls_token: np.ndarray = rng.normal(0, 0.02, (1, 1, d_model))

        # Positional embeddings (num_patches + 1 for CLS)
        self.pos_embed: np.ndarray = positional_embedding(
            num_patches + 1, d_model, seed=seed + 10
        )

        # Transformer encoders
        self.encoders = [
            TransformerEncoder(d_model, num_heads, d_ff, seed=seed + 100 + i)
            for i in range(num_layers)
        ]

        # Classification head
        scale_c = np.sqrt(2.0 / d_model)
        self.cls_W: np.ndarray = rng.normal(0, scale_c, (d_model, num_classes))
        self.cls_b: np.ndarray = np.zeros(num_classes)

    def forward(self, images: np.ndarray) -> np.ndarray:
        """Forward pass.

        Args:
            images: [B, H, W, C] or [H, W, C].

        Returns:
            Logits [B, num_classes] or [num_classes].
        """
        single = images.ndim == 3
        if single:
            images = images[np.newaxis, ...]
        batch = images.shape[0]

        # Patch embedding + projection
        patches = patch_embedding(images, self.patch_size)  # [B, N, patch_dim]
        x = patches @ self.patch_proj  # [B, N, d_model]

        # Prepend CLS token
        cls_tokens = np.tile(self.cls_token, (batch, 1, 1))  # [B, 1, d_model]
        x = np.concatenate([cls_tokens, x], axis=1)  # [B, N+1, d_model]

        # Add positional embeddings
        x = x + self.pos_embed[np.newaxis, :, :]

        # Transformer encoders
        for encoder in self.encoders:
            x = encoder.forward(x)

        # Classification: use CLS token output
        cls_out = x[:, 0, :]  # [B, d_model]
        logits = cls_out @ self.cls_W + self.cls_b  # [B, num_classes]

        return logits[0] if single else logits


# ---------------------------------------------------------------------------
# Training helper
# ---------------------------------------------------------------------------

def cross_entropy_loss(logits: np.ndarray, labels: np.ndarray) -> tuple[float, np.ndarray]:
    """Compute softmax cross-entropy loss and gradient.

    Args:
        logits: [B, num_classes].
        labels: [B] integer labels.

    Returns:
        Tuple of (loss, grad_wrt_logits).
    """
    probs = _softmax(logits, axis=-1)
    batch = logits.shape[0]
    loss = -np.mean(np.log(probs[np.arange(batch), labels] + 1e-12))
    grad = probs.copy()
    grad[np.arange(batch), labels] -= 1.0
    grad /= batch
    return float(loss), grad


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Testing vit_simple.py — Vision Transformer")
    print("=" * 60)

    all_pass = True

    # Test 1: Patch embedding
    print("\n--- Patch Embedding ---")
    img = np.arange(32 * 32).reshape(32, 32, 1).astype(np.float32) / 1024.0
    patches = patch_embedding(img, patch_size=8)
    expected_patches = (32 // 8) ** 2  # 16
    print(f"  Image shape: {img.shape}")
    print(f"  Patches shape: {patches.shape} "
          f"(expected ({expected_patches}, 64))")
    patch_pass = patches.shape == (expected_patches, 64)
    all_pass = all_pass and patch_pass

    # Test 2: ViT forward
    print("\n--- ViT Forward ---")
    vit = SimpleViT(
        image_size=32, patch_size=8, in_channels=1,
        d_model=64, num_heads=4, d_ff=128, num_layers=2,
        num_classes=2, seed=42,
    )

    # Single image
    logits = vit.forward(img)
    print(f"  Single image logits shape: {logits.shape} (expected (2,))")
    all_pass = all_pass and logits.shape == (2,)

    # Batch
    batch_img = np.stack([img, img * 0.5], axis=0)
    batch_logits = vit.forward(batch_img)
    print(f"  Batch logits shape: {batch_logits.shape} (expected (2, 2))")
    all_pass = all_pass and batch_logits.shape == (2, 2)

    # Test 3: Simple training
    print("\n--- Training ---")
    # Create toy dataset: 2 classes, simple patterns
    num_samples = 20
    images = np.zeros((num_samples, 32, 32, 1))
    labels = np.zeros(num_samples, dtype=np.int64)

    for i in range(num_samples):
        if i < num_samples // 2:
            # Class 0: bright top-left
            images[i, :16, :16, 0] = 1.0
            labels[i] = 0
        else:
            # Class 1: bright bottom-right
            images[i, 16:, 16:, 0] = 1.0
            labels[i] = 1

    # Simple training loop
    lr = 0.01
    initial_losses: list[float] = []
    for epoch in range(30):
        logits = vit.forward(images)
        loss, grad = cross_entropy_loss(logits, labels)
        if epoch < 3 or epoch >= 27:
            initial_losses.append(loss)

        # Simple weight perturbation SGD on CLS head
        eps = 1e-4
        for param_name in ["cls_W", "cls_b"]:
            param = getattr(vit, param_name)
            flat = param.ravel()
            grad_flat = np.zeros_like(flat)
            for idx in np.random.choice(len(flat), min(10, len(flat)), replace=False):
                orig = flat[idx]
                flat[idx] = orig + eps
                l_plus = cross_entropy_loss(vit.forward(images), labels)[0]
                flat[idx] = orig - eps
                l_minus = cross_entropy_loss(vit.forward(images), labels)[0]
                flat[idx] = orig
                grad_flat[idx] = (l_plus - l_minus) / (2 * eps)
            param.ravel()[:] = param.ravel() - lr * grad_flat

    # Final accuracy
    final_logits = vit.forward(images)
    preds = np.argmax(final_logits, axis=-1)
    acc = np.mean(preds == labels)
    print(f"  Initial losses: {[f'{l:.3f}' for l in initial_losses[:3]]}...")
    print(f"  Final accuracy: {acc:.2%}")
    acc_pass = acc > 0.6  # Should do better than random
    all_pass = all_pass and acc_pass

    # Test 4: Positional embedding
    print("\n--- Positional Embedding ---")
    pe = positional_embedding(16, 64, seed=42)
    print(f"  Shape: {pe.shape} (expected (16, 64))")
    all_pass = all_pass and pe.shape == (16, 64)

    print(f"\n{'PASS' if all_pass else 'FAIL'}: vit_simple.py")
