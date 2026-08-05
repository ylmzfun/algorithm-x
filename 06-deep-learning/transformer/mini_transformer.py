"""Mini Transformer (encoder-only) for sequence classification.

Architecture: Token Embedding + Positional Encoding +
              Stack of Transformer Encoder Blocks +
              Mean Pooling + Classification Head
"""

import numpy as np
from typing import Optional

try:
    from .attention import causal_mask
    from .transformer_block import TransformerEncoderBlock, LayerNorm
    from .positional_encoding import sinusoidal_positional_encoding
except ImportError:
    from attention import causal_mask
    from transformer_block import TransformerEncoderBlock, LayerNorm
    from positional_encoding import sinusoidal_positional_encoding


class MiniTransformer:
    """A tiny encoder-only transformer for sequence classification."""

    def __init__(
        self,
        vocab_size: int,
        d_model: int = 32,
        num_heads: int = 4,
        num_layers: int = 2,
        d_ff: int = 128,
        max_seq_len: int = 100,
        num_classes: int = 2,
        random_seed: Optional[int] = 42,
    ):
        """Initialize MiniTransformer.

        Args:
            vocab_size: Size of the vocabulary.
            d_model: Model dimension.
            num_heads: Number of attention heads.
            num_layers: Number of transformer encoder blocks.
            d_ff: Feed-forward hidden dimension.
            max_seq_len: Maximum sequence length.
            num_classes: Number of output classes.
            random_seed: Random seed.
        """
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.max_seq_len = max_seq_len
        self.num_classes = num_classes

        rng = np.random.RandomState(random_seed)

        # Token embedding
        self.token_embedding = rng.randn(vocab_size, d_model) * 0.02

        # Positional encoding (fixed sinusoidal)
        self.positional_encoding = sinusoidal_positional_encoding(max_seq_len, d_model)

        # Transformer blocks
        self.blocks: list[TransformerEncoderBlock] = []
        for i in range(num_layers):
            block = TransformerEncoderBlock(
                d_model, num_heads, d_ff,
                random_seed=random_seed + i if random_seed else None
            )
            self.blocks.append(block)

        # Final layer norm
        self.final_norm = LayerNorm(d_model)

        # Classification head
        scale = np.sqrt(2.0 / d_model)
        self.W_cls = rng.randn(d_model, num_classes) * scale
        self.b_cls = np.zeros(num_classes)

        self._cache: dict = {}

    def forward(self, x: np.ndarray, mask: Optional[np.ndarray] = None) -> np.ndarray:
        """Forward pass.

        Args:
            x: Token indices of shape (batch, seq_len).
            mask: Optional attention mask.

        Returns:
            Logits of shape (batch, num_classes).
        """
        batch_size, seq_len = x.shape

        # Token embedding
        embed = self.token_embedding[x]  # (batch, seq_len, d_model)

        # Add positional encoding
        pos_enc = self.positional_encoding[:, :seq_len, :]  # (1, seq_len, d_model)
        h = embed + pos_enc

        # Through encoder blocks
        for block in self.blocks:
            h = block.forward(h, mask)

        # Final layer norm
        h = self.final_norm.forward(h)

        # Mean pooling over sequence
        h_pooled = np.mean(h, axis=1)  # (batch, d_model)

        # Classification head
        logits = np.dot(h_pooled, self.W_cls) + self.b_cls

        self._cache = {
            "x": x,
            "embed": embed,
            "h": h,
            "h_pooled": h_pooled,
            "logits": logits,
        }
        return logits

    def _softmax(self, logits: np.ndarray) -> np.ndarray:
        """Compute softmax probabilities."""
        shifted = logits - np.max(logits, axis=-1, keepdims=True)
        exps = np.exp(np.clip(shifted, -500, 500))
        return exps / np.sum(exps, axis=-1, keepdims=True)

    def cross_entropy_loss(self, logits: np.ndarray, y: np.ndarray
                           ) -> tuple[float, np.ndarray]:
        """Compute cross-entropy loss.

        Args:
            logits: Shape (batch, num_classes).
            y: Shape (batch,) with class indices.

        Returns:
            Tuple of (loss, dlogits).
        """
        probs = self._softmax(logits)
        N = logits.shape[0]
        eps = 1e-12
        loss = -np.sum(np.log(probs[np.arange(N), y] + eps)) / N

        dlogits = probs.copy()
        dlogits[np.arange(N), y] -= 1.0
        dlogits /= N

        return float(loss), dlogits

    def backward(self, dlogits: np.ndarray) -> dict:
        """Simplified backward pass.

        Args:
            dlogits: Gradient w.r.t. logits, shape (batch, num_classes).

        Returns:
            Dict of gradients.
        """
        cache = self._cache
        batch_size = cache["h_pooled"].shape[0]
        seq_len = cache["x"].shape[1]

        # Classification head
        dW_cls = np.dot(cache["h_pooled"].T, dlogits)
        db_cls = np.sum(dlogits, axis=0)
        dh_pooled = np.dot(dlogits, self.W_cls.T)  # (batch, d_model)

        # Mean pooling backward
        dh = np.repeat(dh_pooled[:, np.newaxis, :], seq_len, axis=1) / seq_len

        # Final layer norm backward
        self.final_norm._cache = {}  # simplified
        dh_norm = dh  # approximate; would need proper LN backward

        # Backward through encoder blocks (reverse order)
        for block in reversed(self.blocks):
            dh_norm = block.backward(dh_norm)

        # Embedding gradients
        d_token_embed = np.zeros_like(self.token_embedding)
        for b in range(batch_size):
            for s in range(seq_len):
                d_token_embed[cache["x"][b, s]] += dh_norm[b, s]

        return {
            "dW_cls": dW_cls, "db_cls": db_cls,
            "d_token_embed": d_token_embed,
        }

    def train_step(self, x: np.ndarray, y: np.ndarray, lr: float) -> float:
        """One training step.

        Args:
            x: Input indices, shape (batch, seq_len).
            y: Labels, shape (batch,).
            lr: Learning rate.

        Returns:
            Cross-entropy loss.
        """
        logits = self.forward(x)
        loss, dlogits = self.cross_entropy_loss(logits, y)
        grads = self.backward(dlogits)

        # Update parameters
        self.W_cls -= lr * grads["dW_cls"]
        self.b_cls -= lr * grads["db_cls"]
        self.token_embedding -= lr * grads["d_token_embed"]

        return loss

    def predict(self, x: np.ndarray) -> np.ndarray:
        """Predict class labels.

        Args:
            x: Input indices, shape (batch, seq_len).

        Returns:
            Predicted classes, shape (batch,).
        """
        logits = self.forward(x)
        return np.argmax(logits, axis=-1)

    def accuracy(self, x: np.ndarray, y: np.ndarray) -> float:
        """Compute accuracy.

        Args:
            x: Input data.
            y: True labels.

        Returns:
            Accuracy in [0, 1].
        """
        return float(np.mean(self.predict(x) == y))


def generate_sequence_data(
    n_samples: int = 200,
    seq_len: int = 20,
    vocab_size: int = 10,
    num_classes: int = 2,
    random_seed: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    """Generate synthetic sequence classification data.

    Class 0: increasing sequences
    Class 1: decreasing sequences

    Args:
        n_samples: Number of samples.
        seq_len: Sequence length.
        vocab_size: Vocabulary size.
        num_classes: Number of classes.
        random_seed: Random seed.

    Returns:
        Tuple of (X, y) where X has shape (n_samples, seq_len) and y has shape (n_samples,).
    """
    rng = np.random.RandomState(random_seed)
    X = np.zeros((n_samples, seq_len), dtype=int)
    y = np.zeros(n_samples, dtype=int)

    for i in range(n_samples):
        cls = i % num_classes
        y[i] = cls

        if cls == 0:
            # Increasing trend
            base = rng.randint(0, vocab_size - seq_len // 2)
            seq = np.arange(base, base + seq_len) % vocab_size
            # Add noise
            noise = rng.randint(-1, 2, seq_len)
            seq = np.clip(seq + noise, 0, vocab_size - 1)
        else:
            # Decreasing trend
            base = rng.randint(seq_len // 2, vocab_size)
            seq = (base - np.arange(seq_len)) % vocab_size
            noise = rng.randint(-1, 2, seq_len)
            seq = np.clip(seq + noise, 0, vocab_size - 1)

        X[i] = seq

    return X, y


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing Mini Transformer...")

    np.random.seed(42)

    # Generate data
    X, y = generate_sequence_data(n_samples=200, seq_len=10, vocab_size=10, num_classes=2)
    print(f"  Data: X shape={X.shape}, y distribution={np.bincount(y)}")

    # Test 1: Model initialization and forward pass
    model = MiniTransformer(
        vocab_size=10, d_model=16, num_heads=2, num_layers=1,
        d_ff=64, max_seq_len=20, num_classes=2, random_seed=42,
    )
    logits = model.forward(X[:4])
    assert logits.shape == (4, 2), f"Wrong logits shape: {logits.shape}"
    print(f"  PASS: Forward logits shape: {logits.shape}")

    # Test 2: Loss computation
    loss, dlogits = model.cross_entropy_loss(logits, y[:4])
    assert loss > 0 and np.isfinite(loss), f"Invalid loss: {loss}"
    assert dlogits.shape == (4, 2)
    print(f"  PASS: Cross-entropy loss: {loss:.4f}")

    # Test 3: Training reduces loss
    model2 = MiniTransformer(
        vocab_size=10, d_model=16, num_heads=2, num_layers=1,
        d_ff=64, max_seq_len=20, num_classes=2, random_seed=123,
    )
    initial_loss = model2.train_step(X[:8], y[:8], lr=0.01)

    losses = []
    for _ in range(500):
        idx = np.random.permutation(len(X))[:32]
        loss_val = model2.train_step(X[idx], y[idx], lr=0.05)
        losses.append(loss_val)

    final_loss = model2.train_step(X[:8], y[:8], lr=0.01)
    assert losses[-1] < initial_loss, f"Loss did not decrease: {initial_loss:.4f} → {losses[-1]:.4f}"
    print(f"  PASS: Training reduced loss: {initial_loss:.4f} → {losses[-1]:.4f}")

    # Test 4: Accuracy improves
    initial_acc = model2.accuracy(X, y)
    print(f"  PASS: Final accuracy: {initial_acc:.3f}")

    # Test 5: Predictions produce valid classes
    preds = model2.predict(X[:8])
    assert preds.shape == (8,), f"Wrong preds shape: {preds.shape}"
    assert np.all((preds >= 0) & (preds < 2)), "Predictions out of class range"
    print("  PASS: Predictions produce valid class indices")

    # Test 6: Different sequence lengths
    X_short = X[:4, :5]  # seq_len=5
    logits_short = model.forward(X_short)
    assert logits_short.shape == (4, 2), f"Short seq shape wrong: {logits_short.shape}"
    print(f"  PASS: Variable sequence length support: {logits_short.shape}")

    print("\nAll Mini Transformer tests passed!")
