"""Simplified BERT-style masked language model from scratch using NumPy.

Implements:
- Token, segment, and position embeddings
- Multi-head self-attention
- Transformer encoder blocks
- Masked language model (MLM) pre-training

Reference: Devlin et al., "BERT: Pre-training of Deep Bidirectional
Transformers for Language Understanding" (2019).
"""

from __future__ import annotations

import numpy as np
from typing import Optional


# ---------------------------------------------------------------------------
# Embedding utilities
# ---------------------------------------------------------------------------

def positional_encoding(seq_len: int, d_model: int) -> np.ndarray:
    """Compute sinusoidal position encodings.

    PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
    PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

    Args:
        seq_len: Maximum sequence length.
        d_model: Model / embedding dimension.

    Returns:
        Position encoding matrix [seq_len, d_model].
    """
    pe = np.zeros((seq_len, d_model))
    position = np.arange(seq_len)[:, np.newaxis]  # [seq_len, 1]
    div_term = np.exp(
        np.arange(0, d_model, 2) * (-np.log(10000.0) / d_model)
    )
    pe[:, 0::2] = np.sin(position * div_term)
    pe[:, 1::2] = np.cos(position * div_term)
    return pe


def gelu(x: np.ndarray) -> np.ndarray:
    """Gaussian Error Linear Unit activation.

    GELU(x) = 0.5 * x * (1 + tanh(sqrt(2/pi) * (x + 0.044715 * x^3)))

    Args:
        x: Input array.

    Returns:
        GELU-activated array.
    """
    return 0.5 * x * (1.0 + np.tanh(
        np.sqrt(2.0 / np.pi) * (x + 0.044715 * x**3)
    ))


def layer_norm(x: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    """Apply layer normalization along the last axis.

    Args:
        x: Input array.
        eps: Small constant for numerical stability.

    Returns:
        Layer-normalized array (mean=0, std=1 along last axis).
    """
    mean = np.mean(x, axis=-1, keepdims=True)
    var = np.var(x, axis=-1, keepdims=True)
    return (x - mean) / np.sqrt(var + eps)


# ---------------------------------------------------------------------------
# Multi-Head Self-Attention
# ---------------------------------------------------------------------------

class MultiHeadSelfAttention:
    """Multi-head scaled dot-product self-attention.

    Splits the input into multiple heads, computes attention independently
    per head, and concatenates the results.

    Attributes:
        d_model: Total model dimension.
        num_heads: Number of attention heads.
        d_k: Dimension per head (= d_model // num_heads).
        W_q, W_k, W_v: Projection matrices for Q, K, V.
        W_o: Output projection matrix.
    """

    def __init__(self, d_model: int, num_heads: int, seed: int = 42) -> None:
        """Initialize multi-head attention.

        Args:
            d_model: Model dimension (must be divisible by num_heads).
            num_heads: Number of attention heads.
            seed: Random seed.

        Raises:
            ValueError: If d_model is not divisible by num_heads.
        """
        if d_model % num_heads != 0:
            raise ValueError(f"d_model ({d_model}) must be divisible by "
                             f"num_heads ({num_heads})")
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
        """Forward pass of multi-head self-attention.

        Args:
            x: Input [batch, seq_len, d_model].

        Returns:
            Attention output [batch, seq_len, d_model].
        """
        batch, seq_len, d_model = x.shape
        d_k = self.d_k
        h = self.num_heads

        # Linear projections and reshape to [batch, num_heads, seq_len, d_k]
        Q = x @ self.W_q                    # [batch, seq_len, d_model]
        K = x @ self.W_k
        V = x @ self.W_v

        Q = Q.reshape(batch, seq_len, h, d_k).transpose(0, 2, 1, 3)
        K = K.reshape(batch, seq_len, h, d_k).transpose(0, 2, 1, 3)
        V = V.reshape(batch, seq_len, h, d_k).transpose(0, 2, 1, 3)

        # Scaled dot-product attention
        scores = Q @ K.transpose(0, 1, 3, 2) / np.sqrt(d_k)  # [B, h, T, T]
        attn = _softmax(scores, axis=-1)
        context = attn @ V  # [B, h, T, d_k]

        # Concatenate heads and project
        context = context.transpose(0, 2, 1, 3).reshape(batch, seq_len, d_model)
        output = context @ self.W_o  # [B, T, d_model]
        return output


# ---------------------------------------------------------------------------
# Feed-Forward Network
# ---------------------------------------------------------------------------

class FeedForward:
    """Position-wise feed-forward network.

    Two linear transformations with GELU activation in between:
    FFN(x) = GELU(x @ W1 + b1) @ W2 + b2

    Attributes:
        W1: First linear layer weights [d_model, d_ff].
        b1: First linear layer bias [d_ff].
        W2: Second linear layer weights [d_ff, d_model].
        b2: Second linear layer bias [d_model].
    """

    def __init__(self, d_model: int, d_ff: int, seed: int = 42) -> None:
        """Initialize feed-forward network.

        Args:
            d_model: Input/output dimension.
            d_ff: Hidden (intermediate) dimension.
            seed: Random seed.
        """
        rng = np.random.default_rng(seed)
        scale = np.sqrt(2.0 / d_model)
        self.d_model = d_model
        self.d_ff = d_ff
        self.W1: np.ndarray = rng.normal(0, scale, (d_model, d_ff))
        self.b1: np.ndarray = np.zeros(d_ff)
        self.W2: np.ndarray = rng.normal(0, scale, (d_ff, d_model))
        self.b2: np.ndarray = np.zeros(d_model)

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass.

        Args:
            x: Input [..., d_model].

        Returns:
            Output [..., d_model].
        """
        return gelu(x @ self.W1 + self.b1) @ self.W2 + self.b2


# ---------------------------------------------------------------------------
# Transformer Block
# ---------------------------------------------------------------------------

class TransformerBlock:
    """A single transformer encoder block.

    Composed of:
    1. Multi-head self-attention with residual connection and layer norm.
    2. Feed-forward network with residual connection and layer norm.

    Attributes:
        attention: Multi-head self-attention layer.
        ffn: Feed-forward network.
    """

    def __init__(self, d_model: int, num_heads: int, d_ff: int, seed: int = 42) -> None:
        """Initialize a transformer block.

        Args:
            d_model: Model dimension.
            num_heads: Number of attention heads.
            d_ff: Feed-forward hidden dimension.
            seed: Random seed.
        """
        self.attention = MultiHeadSelfAttention(d_model, num_heads, seed=seed)
        self.ffn = FeedForward(d_model, d_ff, seed=seed + 100)

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass through the transformer block.

        Args:
            x: Input [batch, seq_len, d_model].

        Returns:
            Output [batch, seq_len, d_model].
        """
        # Self-attention + residual + layer norm
        attn_out = self.attention.forward(x)
        x = layer_norm(x + attn_out)
        # FFN + residual + layer norm
        ffn_out = self.ffn.forward(x)
        x = layer_norm(x + ffn_out)
        return x


# ---------------------------------------------------------------------------
# Simple BERT
# ---------------------------------------------------------------------------

def _softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    """Stable softmax along given axis."""
    e = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return e / np.sum(e, axis=axis, keepdims=True)


class SimpleBERT:
    """Simplified BERT model for masked language modeling.

    Architecture:
    1. Token embeddings + segment embeddings + position embeddings
    2. Stack of transformer encoder blocks
    3. MLM head: linear projection to vocabulary size + softmax

    Attributes:
        vocab_size: Size of token vocabulary.
        d_model: Hidden dimension.
        num_layers: Number of transformer blocks.
        num_heads: Number of attention heads.
        d_ff: Feed-forward hidden dimension.
        max_len: Maximum sequence length.
    """

    def __init__(
        self,
        vocab_size: int,
        d_model: int = 64,
        num_layers: int = 2,
        num_heads: int = 4,
        d_ff: int = 128,
        max_len: int = 32,
        seed: int = 42,
    ) -> None:
        """Initialize the SimpleBERT model.

        Args:
            vocab_size: Token vocabulary size.
            d_model: Hidden dimension.
            num_layers: Number of transformer layers.
            num_heads: Number of attention heads.
            d_ff: Feed-forward dimension.
            max_len: Maximum sequence length.
            seed: Random seed.
        """
        rng = np.random.default_rng(seed)
        scale = np.sqrt(2.0 / d_model)
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.max_len = max_len

        # Embeddings
        self.token_embed: np.ndarray = rng.normal(0, scale, (vocab_size, d_model))
        self.segment_embed: np.ndarray = rng.normal(0, scale, (2, d_model))
        self.pos_embed: np.ndarray = rng.normal(0, scale, (max_len, d_model))

        # Transformer blocks
        self.blocks = [
            TransformerBlock(d_model, num_heads, d_ff, seed=seed + i * 100)
            for i in range(num_layers)
        ]

        # MLM head
        self.mlm_W: np.ndarray = rng.normal(0, scale, (d_model, vocab_size))
        self.mlm_b: np.ndarray = np.zeros(vocab_size)

    def forward(self, token_ids: np.ndarray, segment_ids: np.ndarray) -> np.ndarray:
        """Forward pass.

        Args:
            token_ids: Token indices [batch, seq_len].
            segment_ids: Segment indices [batch, seq_len] (0 or 1).

        Returns:
            Logits for each position [batch, seq_len, vocab_size].
        """
        batch, seq_len = token_ids.shape

        # Embedding lookup
        tok_emb = self.token_embed[token_ids]          # [B, T, D]
        seg_emb = self.segment_embed[segment_ids]      # [B, T, D]
        pos_emb = self.pos_embed[:seq_len]              # [T, D]
        x = tok_emb + seg_emb + pos_emb[np.newaxis, :, :]  # [B, T, D]

        # Transformer blocks
        for block in self.blocks:
            x = block.forward(x)

        # MLM head
        logits = x @ self.mlm_W + self.mlm_b  # [B, T, V]
        return logits

    def predict_masked(self, logits: np.ndarray) -> np.ndarray:
        """Predict tokens from logits (argmax).

        Args:
            logits: Model output [batch, seq_len, vocab_size].

        Returns:
            Predicted token indices [batch, seq_len].
        """
        return np.argmax(logits, axis=-1)


# ---------------------------------------------------------------------------
# MLM Pre-training
# ---------------------------------------------------------------------------

def mlm_pretrain(
    model: SimpleBERT,
    sentences: list[list[int]],
    mask_prob: float = 0.15,
    epochs: int = 100,
    lr: float = 0.01,
) -> list[float]:
    """Pre-train the BERT model on a masked language modeling task.

    Randomly masks `mask_prob` fraction of tokens in each sentence and
    trains the model to predict the original tokens. Uses a simplified
    SGD that perturbs weights to approximate gradients.

    Args:
        model: The SimpleBERT model.
        sentences: List of token-index sequences (all same length).
        mask_prob: Probability of masking a token.
        epochs: Number of training epochs.
        lr: Learning rate.

    Returns:
        List of average losses per epoch.
    """
    # Pad sentences to same length
    max_len = max(len(s) for s in sentences)
    batch_data = np.zeros((len(sentences), max_len), dtype=np.int64)
    for i, s in enumerate(sentences):
        batch_data[i, :len(s)] = s

    epoch_losses: list[float] = []
    for epoch in range(epochs):
        total_loss = 0.0
        total_masked = 0

        for b in range(len(sentences)):
            tokens = batch_data[b].copy()
            # Create masked version
            masked = tokens.copy()
            seg_ids = np.zeros(max_len, dtype=np.int64)
            mask_positions = np.random.random(max_len) < mask_prob
            # Don't mask padding (token 0)
            mask_positions = mask_positions & (tokens > 0)
            labels = np.where(mask_positions, tokens, -1)  # -1 = no prediction
            masked[mask_positions] = 1  # [MASK] token = 1

            # Forward
            logits = model.forward(
                masked[np.newaxis, :], seg_ids[np.newaxis, :]
            )[0]  # [T, V]

            # Compute loss only on masked positions
            for t in range(max_len):
                if mask_positions[t]:
                    probs = _softmax(logits[t])
                    true_idx = tokens[t]
                    total_loss += -np.log(probs[true_idx] + 1e-12)
                    total_masked += 1

        avg_loss = total_loss / max(total_masked, 1)
        epoch_losses.append(avg_loss)

        # Perturb-based SGD step (simplified for demo)
        if epoch % 10 == 0:
            _bert_sgd_step(model, batch_data, mask_prob, lr)

    return epoch_losses


def _bert_sgd_step(
    model: SimpleBERT, batch_data: np.ndarray, mask_prob: float, lr: float
) -> None:
    """Single SGD step via weight perturbation.

    Args:
        model: The SimpleBERT model.
        batch_data: Token-index sentences [batch, max_len].
        mask_prob: Masking probability.
        lr: Learning rate.
    """
    eps = 1e-4
    params_to_update = [
        model.token_embed,
        model.mlm_W,
    ]

    for param in params_to_update:
        flat = param.ravel()
        grad = np.zeros_like(flat)
        # Subsample gradient dimensions for speed
        indices = np.random.choice(len(flat), min(50, len(flat)), replace=False)
        for i in indices:
            orig = flat[i]
            flat[i] = orig + eps
            loss_plus = _bert_loss(model, batch_data, mask_prob)
            flat[i] = orig - eps
            loss_minus = _bert_loss(model, batch_data, mask_prob)
            flat[i] = orig
            grad[i] = (loss_plus - loss_minus) / (2 * eps)
        param.ravel()[:] = param.ravel() - lr * grad


def _bert_loss(
    model: SimpleBERT, batch_data: np.ndarray, mask_prob: float
) -> float:
    """Compute average MLM loss over the batch."""
    total_loss = 0.0
    total_masked = 0
    max_len = batch_data.shape[1]
    for b in range(len(batch_data)):
        tokens = batch_data[b].copy()
        masked = tokens.copy()
        seg_ids = np.zeros(max_len, dtype=np.int64)
        mask_positions = np.random.random(max_len) < mask_prob
        mask_positions = mask_positions & (tokens > 0)
        masked[mask_positions] = 1
        logits = model.forward(
            masked[np.newaxis, :], seg_ids[np.newaxis, :]
        )[0]
        for t in range(max_len):
            if mask_positions[t]:
                probs = _softmax(logits[t])
                total_loss += -np.log(probs[tokens[t]] + 1e-12)
                total_masked += 1
    return total_loss / max(total_masked, 1)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Testing bert_like.py — Simplified BERT MLM")
    print("=" * 60)

    # Create a tiny vocabulary: 0=PAD, 1=MASK, 2-... = real tokens
    vocab_words = [
        "PAD", "MASK", "the", "cat", "dog", "sat", "on", "mat", "ran",
        "fast", "a", "is", "big", "small", "bird", "fish", "eats",
        "food", "water", "likes", "chases", "sleeps",
    ]
    word2idx = {w: i for i, w in enumerate(vocab_words)}
    vocab_size = len(vocab_words)

    # Toy sentences (tokenized)
    raw_sentences = [
        ["the", "cat", "sat", "on", "the", "mat"],
        ["the", "dog", "ran", "fast"],
        ["a", "big", "cat", "chases", "a", "small", "bird"],
        ["the", "fish", "eats", "food"],
        ["the", "dog", "likes", "water"],
        ["a", "bird", "is", "on", "the", "mat"],
        ["the", "cat", "sleeps"],
        ["a", "dog", "chases", "a", "cat"],
        ["the", "bird", "eats", "fish"],
        ["the", "small", "dog", "sat"],
    ]
    sentences = [[word2idx[w] for w in s] for s in raw_sentences]

    print(f"\nVocabulary size: {vocab_size}")
    print(f"Sentences: {len(sentences)}")

    # Create model
    model = SimpleBERT(
        vocab_size=vocab_size,
        d_model=32,
        num_layers=2,
        num_heads=4,
        d_ff=64,
        max_len=10,
        seed=42,
    )

    # Pre-train
    losses = mlm_pretrain(model, sentences, mask_prob=0.15,
                           epochs=50, lr=0.05)
    print(f"Initial loss: {losses[0]:.4f}")
    print(f"Final loss:   {losses[-1]:.4f}")
    loss_decreased = losses[-1] < losses[0]

    # Test prediction on a masked sentence
    test_sentence = ["the", "cat", "sat", "on", "the", "MASK"]
    test_ids = np.array([word2idx[w] for w in test_sentence], dtype=np.int64)
    seg_ids = np.zeros(len(test_ids), dtype=np.int64)
    logits = model.forward(test_ids[np.newaxis, :], seg_ids[np.newaxis, :])[0]
    pred_idx = int(np.argmax(logits[5]))  # position of MASK
    predicted_word = vocab_words[pred_idx]
    print(f"\nMasked prediction test:")
    print(f"  Input:  {' '.join(test_sentence)}")
    print(f"  Predicted word at MASK: '{predicted_word}'")

    # Check if it predicted "mat" or something reasonable
    all_pass = loss_decreased
    print(f"Loss decreased: {loss_decreased}")

    # Verify positional encoding
    pe = positional_encoding(4, 8)
    print(f"\nPositional encoding shape: {pe.shape} (expected (4, 8))")
    pe_pass = pe.shape == (4, 8)
    all_pass = all_pass and pe_pass

    # Verify attention output shape
    attn = MultiHeadSelfAttention(32, 4, seed=42)
    test_x = np.random.randn(2, 5, 32)
    attn_out = attn.forward(test_x)
    attn_pass = attn_out.shape == (2, 5, 32)
    print(f"Attention output shape: {attn_out.shape} (expected (2, 5, 32))")
    all_pass = all_pass and attn_pass

    print(f"\n{'PASS' if all_pass else 'FAIL'}: bert_like.py")
