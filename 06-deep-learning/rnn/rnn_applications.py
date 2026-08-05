"""Character-level language model using RNN/LSTM, implemented from scratch with NumPy.

Trains on a tiny built-in text corpus and generates text character by character.
"""

import numpy as np
from typing import Optional


class CharRNN:
    """Character-level RNN language model.

    Architecture: Embedding → RNNCell → Output projection → Softmax
    Trained with cross-entropy loss over the vocabulary.
    """

    def __init__(
        self,
        vocab_size: int,
        embedding_dim: int = 16,
        hidden_size: int = 64,
        seq_length: int = 25,
        random_seed: Optional[int] = 42,
    ):
        """Initialize character-level RNN.

        Args:
            vocab_size: Number of unique characters.
            embedding_dim: Dimension of character embeddings.
            hidden_size: Hidden state dimension.
            seq_length: Training sequence length.
            random_seed: Random seed.
        """
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.hidden_size = hidden_size
        self.seq_length = seq_length

        rng = np.random.RandomState(random_seed)

        # Embedding layer
        self.W_embed = rng.randn(vocab_size, embedding_dim) * 0.01

        # RNN cell (using tanh RNN)
        scale = np.sqrt(1.0 / hidden_size)
        self.W_xh = rng.randn(embedding_dim, hidden_size) * scale
        self.W_hh = rng.randn(hidden_size, hidden_size) * scale
        self.b_h = np.zeros((1, hidden_size))

        # Output projection
        self.W_out = rng.randn(hidden_size, vocab_size) * scale
        self.b_out = np.zeros((1, vocab_size))

        self._cache: dict = {}

    def forward(self, x_seq: np.ndarray, h0: Optional[np.ndarray] = None
                ) -> np.ndarray:
        """Forward pass through the sequence.

        Args:
            x_seq: Input character indices of shape (seq_len, batch_size).
            h0: Initial hidden state of shape (batch_size, hidden_size).

        Returns:
            Logits of shape (seq_len, batch_size, vocab_size).
        """
        seq_len, batch_size = x_seq.shape

        if h0 is None:
            h = np.zeros((batch_size, self.hidden_size))
        else:
            h = h0

        logits = np.zeros((seq_len, batch_size, self.vocab_size))
        h_states = [h.copy()]

        for t in range(seq_len):
            # Embedding lookup
            indices = x_seq[t]  # (batch_size,)
            embed = self.W_embed[indices]  # (batch_size, embedding_dim)

            # RNN step
            z = np.dot(embed, self.W_xh) + np.dot(h, self.W_hh) + self.b_h
            h = np.tanh(z)
            h_states.append(h.copy())

            # Output projection
            logits[t] = np.dot(h, self.W_out) + self.b_out

        self._cache = {
            "x_seq": x_seq,
            "h_states": h_states,
            "logits": logits,
        }
        return logits

    def _softmax(self, logits: np.ndarray) -> np.ndarray:
        """Compute softmax over vocabulary dimension.

        Args:
            logits: Shape (..., vocab_size).

        Returns:
            Probabilities of same shape.
        """
        shifted = logits - np.max(logits, axis=-1, keepdims=True)
        exps = np.exp(np.clip(shifted, -500, 500))
        return exps / np.sum(exps, axis=-1, keepdims=True)

    def cross_entropy_loss(self, logits: np.ndarray, targets: np.ndarray) -> tuple[float, np.ndarray]:
        """Compute cross-entropy loss and gradient w.r.t. logits.

        Args:
            logits: Shape (seq_len * batch_size, vocab_size).
            targets: Shape (seq_len * batch_size,) with class indices.

        Returns:
            Tuple of (loss, dlogits).
        """
        probs = self._softmax(logits)
        N = logits.shape[0]
        eps = 1e-12
        loss = -np.sum(np.log(probs[np.arange(N), targets] + eps)) / N

        dlogits = probs.copy()
        dlogits[np.arange(N), targets] -= 1.0
        dlogits /= N

        return float(loss), dlogits

    def backward(self, dlogits_seq: np.ndarray) -> dict:
        """Backward pass through the sequence.

        Args:
            dlogits_seq: Gradient w.r.t. logits, shape (seq_len, batch_size, vocab_size).

        Returns:
            Dict of parameter gradients.
        """
        cache = self._cache
        x_seq = cache["x_seq"]
        h_states = cache["h_states"]
        seq_len, batch_size = x_seq.shape

        # Initialize gradient accumulators
        dW_embed = np.zeros_like(self.W_embed)
        dW_xh = np.zeros_like(self.W_xh)
        dW_hh = np.zeros_like(self.W_hh)
        db_h = np.zeros_like(self.b_h)
        dW_out = np.zeros_like(self.W_out)
        db_out = np.zeros_like(self.b_out)

        dh_next = np.zeros((batch_size, self.hidden_size))

        for t in reversed(range(seq_len)):
            h = h_states[t + 1]     # current hidden state
            h_prev = h_states[t]    # previous hidden state

            # Gradient from output layer
            dout_t = dlogits_seq[t]  # (batch, vocab)
            dW_out += np.dot(h.T, dout_t)
            db_out += np.sum(dout_t, axis=0, keepdims=True)
            dh = np.dot(dout_t, self.W_out.T) + dh_next

            # Gradient through tanh
            dz = dh * (1 - h ** 2)

            # Embedding gradient
            indices = x_seq[t]
            embed = self.W_embed[indices]
            dx_embed = np.dot(dz, self.W_xh.T)  # (batch, embedding_dim)
            for b in range(batch_size):
                dW_embed[indices[b]] += dx_embed[b]

            dW_xh += np.dot(embed.T, dz)
            dW_hh += np.dot(h_prev.T, dz)
            db_h += np.sum(dz, axis=0, keepdims=True)
            dh_next = np.dot(dz, self.W_hh.T)

        return {
            "dW_embed": dW_embed,
            "dW_xh": dW_xh, "dW_hh": dW_hh, "db_h": db_h,
            "dW_out": dW_out, "db_out": db_out,
        }

    def train_step(self, x_seq: np.ndarray, y_seq: np.ndarray, lr: float) -> float:
        """One training step.

        Args:
            x_seq: Input indices of shape (seq_len, batch_size).
            y_seq: Target indices of shape (seq_len, batch_size).
            lr: Learning rate.

        Returns:
            Cross-entropy loss.
        """
        logits = self.forward(x_seq)
        seq_len, batch_size, vocab_size = logits.shape

        # Flatten for loss computation
        logits_flat = logits.reshape(-1, vocab_size)
        targets_flat = y_seq.reshape(-1)

        loss, dlogits_flat = self.cross_entropy_loss(logits_flat, targets_flat)
        dlogits_seq = dlogits_flat.reshape(seq_len, batch_size, vocab_size)

        grads = self.backward(dlogits_seq)

        # Update parameters
        self.W_embed -= lr * grads["dW_embed"]
        self.W_xh -= lr * grads["dW_xh"]
        self.W_hh -= lr * grads["dW_hh"]
        self.b_h -= lr * grads["db_h"]
        self.W_out -= lr * grads["dW_out"]
        self.b_out -= lr * grads["db_out"]

        return loss

    def sample(self, seed_char: str, length: int, temperature: float = 1.0,
               char_to_idx: Optional[dict] = None,
               idx_to_char: Optional[dict] = None) -> str:
        """Generate text from the model.

        Args:
            seed_char: Starting character.
            length: Number of characters to generate.
            temperature: Sampling temperature (higher = more random).
            char_to_idx: Character to index mapping.
            idx_to_char: Index to character mapping.

        Returns:
            Generated string.
        """
        if char_to_idx is None or idx_to_char is None:
            raise ValueError("char_to_idx and idx_to_char must be provided")

        result = [seed_char]
        h = np.zeros((1, self.hidden_size))
        idx = char_to_idx.get(seed_char, 0)

        for _ in range(length):
            embed = self.W_embed[idx].reshape(1, -1)
            z = np.dot(embed, self.W_xh) + np.dot(h, self.W_hh) + self.b_h
            h = np.tanh(z)
            logits = np.dot(h, self.W_out) + self.b_out

            # Apply temperature
            logits = logits / max(temperature, 1e-8)

            # Sample from softmax distribution
            probs = self._softmax(logits).flatten()
            idx = np.random.choice(self.vocab_size, p=probs)
            result.append(idx_to_char.get(idx, "?"))

        return "".join(result)


# ============================================================================
# Helpers
# ============================================================================
def build_vocab(text: str) -> tuple[dict, dict, int]:
    """Build character-level vocabulary.

    Args:
        text: Input text corpus.

    Returns:
        Tuple of (char_to_idx, idx_to_char, vocab_size).
    """
    chars = sorted(set(text))
    char_to_idx = {ch: i for i, ch in enumerate(chars)}
    idx_to_char = {i: ch for ch, i in char_to_idx.items()}
    return char_to_idx, idx_to_char, len(chars)


def text_to_sequences(text: str, char_to_idx: dict, seq_length: int
                      ) -> tuple[np.ndarray, np.ndarray]:
    """Convert text to input/target sequences for training.

    Args:
        text: Input text.
        char_to_idx: Character to index mapping.
        seq_length: Sequence length.

    Returns:
        Tuple of (x, y), each of shape (num_sequences, seq_length).
    """
    data = np.array([char_to_idx[ch] for ch in text])
    num_seqs = (len(data) - 1) // seq_length
    data = data[:num_seqs * seq_length + 1]

    x = data[:-1].reshape(num_seqs, seq_length).T  # (seq_len, batch)
    y = data[1:].reshape(num_seqs, seq_length).T
    return x, y


# Tiny Shakespeare-like corpus
TINY_CORPUS = (
    "to be or not to be that is the question "
    "whether tis nobler in the mind to suffer "
    "the slings and arrows of outrageous fortune "
    "or to take arms against a sea of troubles "
    "and by opposing end them to die to sleep "
    "no more and by a sleep to say we end "
    "the heartache and the thousand natural shocks "
    "that flesh is heir to tis a consummation "
    "devoutly to be wished to die to sleep "
    "to sleep perchance to dream ay there the rub "
    "for in that sleep of death what dreams may come "
    "when we have shuffled off this mortal coil "
    "must give us pause there the respect "
    "that makes calamity of so long life "
)


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing CharRNN...")

    np.random.seed(42)

    # Build vocabulary
    text = TINY_CORPUS
    char_to_idx, idx_to_char, vocab_size = build_vocab(text)
    print(f"  Vocab size: {vocab_size}")

    # Test 1: Forward pass shapes
    model = CharRNN(vocab_size=vocab_size, embedding_dim=8, hidden_size=32,
                    seq_length=10, random_seed=42)

    x_data, y_data = text_to_sequences(text, char_to_idx, seq_length=10)
    logits = model.forward(x_data[:2, :2])  # seq_len=2, batch=2
    assert logits.shape == (2, 2, vocab_size), f"Wrong logits shape: {logits.shape}"
    print(f"  PASS: Forward shape: {logits.shape}")

    # Test 2: Loss computation
    loss, dlogits = model.cross_entropy_loss(
        logits.reshape(-1, vocab_size),
        y_data[:2, :2].reshape(-1)
    )
    assert loss > 0 and np.isfinite(loss), f"Invalid loss: {loss}"
    print(f"  PASS: Loss: {loss:.4f}")

    # Test 3: Backward pass
    dlogits_seq = dlogits.reshape(2, 2, vocab_size)
    grads = model.backward(dlogits_seq)
    assert "dW_embed" in grads, "Missing dW_embed"
    assert grads["dW_xh"].shape == (8, 32), f"dW_xh shape: {grads['dW_xh'].shape}"
    print("  PASS: Backward pass produced all gradients")

    # Test 4: Training reduces loss
    model2 = CharRNN(vocab_size=vocab_size, embedding_dim=8, hidden_size=32,
                     seq_length=10, random_seed=123)
    x_train, y_train = text_to_sequences(text, char_to_idx, seq_length=10)

    initial_loss = model2.train_step(x_train[:, :1], y_train[:, :1], lr=0.01)
    losses = []
    for _ in range(1000):
        loss = model2.train_step(x_train[:, :1], y_train[:, :1], lr=0.1)
        losses.append(loss)

    assert losses[-1] < initial_loss, f"Loss did not decrease: {initial_loss:.4f} → {losses[-1]:.4f}"
    print(f"  PASS: Training reduced loss: {initial_loss:.4f} → {losses[-1]:.4f}")

    # Test 5: Text generation
    generated = model2.sample("t", length=50, temperature=0.8,
                              char_to_idx=char_to_idx, idx_to_char=idx_to_char)
    assert len(generated) == 51, f"Wrong generated length: {len(generated)}"
    assert generated[0] == "t", f"Wrong seed char: {generated[0]}"
    print(f"  PASS: Generated text: '{generated[:30]}...'")

    # Test 6: Temperature scaling
    gen_hot = model2.sample("a", length=20, temperature=5.0,
                            char_to_idx=char_to_idx, idx_to_char=idx_to_char)
    gen_cold = model2.sample("a", length=20, temperature=0.1,
                             char_to_idx=char_to_idx, idx_to_char=idx_to_char)
    print(f"  PASS: Hot temp sample: '{gen_hot}'")
    print(f"  PASS: Cold temp sample: '{gen_cold}'")

    print("\nAll CharRNN tests passed!")
