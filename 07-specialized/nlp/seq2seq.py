"""Sequence-to-Sequence model with attention from scratch using NumPy.

Implements:
- Encoder RNN that processes the input sequence
- Attention mechanism (additive / Bahdanau-style)
- Decoder RNN that generates output with attention over encoder states
- Training on copy/reverse tasks

Reference: Bahdanau et al., "Neural Machine Translation by Jointly
Learning to Align and Translate" (2015).
"""

from __future__ import annotations

import numpy as np
from typing import Optional


# ---------------------------------------------------------------------------
# Activation helpers
# ---------------------------------------------------------------------------

def _tanh(x: np.ndarray) -> np.ndarray:
    return np.tanh(x)


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -50, 50)))


def _softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    e = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return e / np.sum(e, axis=axis, keepdims=True)


# ---------------------------------------------------------------------------
# Encoder
# ---------------------------------------------------------------------------

class EncoderRNN:
    """Simple RNN encoder that reads an input sequence and returns hidden states.

    The encoder processes tokens one by one, maintaining a hidden state that
    summarizes the input seen so far. All hidden states are saved for the
    attention mechanism.

    Attributes:
        input_size: Dimension of input embeddings.
        hidden_size: Dimension of the hidden state.
        W_xh: Input-to-hidden weight matrix.
        W_hh: Hidden-to-hidden weight matrix.
        b_h: Hidden bias.
    """

    def __init__(self, input_size: int, hidden_size: int, seed: int = 42) -> None:
        """Initialize the encoder RNN.

        Args:
            input_size: Dimension of input token embeddings.
            hidden_size: Dimension of hidden state vectors.
            seed: Random seed.
        """
        rng = np.random.default_rng(seed)
        scale = np.sqrt(1.0 / hidden_size)
        self.hidden_size = hidden_size
        self.W_xh: np.ndarray = rng.uniform(-scale, scale, (hidden_size, input_size))
        self.W_hh: np.ndarray = rng.uniform(-scale, scale, (hidden_size, hidden_size))
        self.b_h: np.ndarray = np.zeros(hidden_size)

        # Cached for backprop
        self._cache: dict = {}

    def forward(self, inputs: np.ndarray) -> np.ndarray:
        """Forward pass over the full input sequence.

        Args:
            inputs: Input embeddings [seq_len, input_size].

        Returns:
            All hidden states [seq_len, hidden_size].
        """
        seq_len = inputs.shape[0]
        h = np.zeros(self.hidden_size)
        hidden_states = np.zeros((seq_len, self.hidden_size))
        self._cache["inputs"] = inputs
        self._cache["hiddens"] = np.zeros((seq_len, self.hidden_size))

        for t in range(seq_len):
            h = _tanh(self.W_xh @ inputs[t] + self.W_hh @ h + self.b_h)
            hidden_states[t] = h
            self._cache["hiddens"][t] = h

        return hidden_states


# ---------------------------------------------------------------------------
# Attention
# ---------------------------------------------------------------------------

class Attention:
    """Additive (Bahdanau-style) attention mechanism.

    Computes attention scores between the decoder's current hidden state
    and all encoder hidden states, producing a context vector.

    Attributes:
        hidden_size: Dimension of encoder/decoder hidden states.
        W_a: Weight for decoder state in attention score.
        U_a: Weight for encoder states in attention score.
        v_a: Weight vector for computing scalar score.
    """

    def __init__(self, hidden_size: int, seed: int = 42) -> None:
        """Initialize the attention mechanism.

        Args:
            hidden_size: Hidden state dimension (same for encoder and decoder).
            seed: Random seed.
        """
        rng = np.random.default_rng(seed)
        scale = np.sqrt(1.0 / hidden_size)
        self.hidden_size = hidden_size
        self.W_a: np.ndarray = rng.uniform(-scale, scale, (hidden_size, hidden_size))
        self.U_a: np.ndarray = rng.uniform(-scale, scale, (hidden_size, hidden_size))
        self.v_a: np.ndarray = rng.uniform(-scale, scale, hidden_size)

    def forward(
        self, decoder_hidden: np.ndarray, encoder_states: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        """Compute attention weights and context vector.

        score(s, h_i) = v_a^T * tanh(W_a * s + U_a * h_i)

        Args:
            decoder_hidden: Current decoder hidden state [hidden_size].
            encoder_states: All encoder hidden states [seq_len, hidden_size].

        Returns:
            Tuple of (context_vector [hidden_size], attention_weights [seq_len]).
        """
        # decoder_hidden: [H], encoder_states: [T, H]
        w_s = self.W_a @ decoder_hidden          # [H]
        u_h = encoder_states @ self.U_a.T         # [T, H]
        scores = (w_s + u_h) @ self.v_a           # [T] — broadcast: w_s added to each row
        attn_weights = _softmax(scores)
        context = attn_weights @ encoder_states   # [H]
        return context, attn_weights


# ---------------------------------------------------------------------------
# Decoder
# ---------------------------------------------------------------------------

class DecoderRNN:
    """RNN decoder with attention.

    At each step, the decoder computes an attention context from the encoder
    states, then produces the next hidden state and output token probabilities.

    Attributes:
        output_size: Size of output vocabulary.
        embed_size: Size of input embeddings.
        hidden_size: Hidden state dimension.
        W_emb: Embedding lookup matrix.
        W_h: Hidden state update weights.
        b_h: Hidden bias.
        W_out: Output projection weights.
        b_out: Output bias.
    """

    def __init__(
        self, output_size: int, embed_size: int, hidden_size: int, seed: int = 42
    ) -> None:
        """Initialize the decoder RNN.

        Args:
            output_size: Output vocabulary size.
            embed_size: Embedding dimension for input tokens.
            hidden_size: Hidden state dimension.
            seed: Random seed.
        """
        rng = np.random.default_rng(seed)
        scale = np.sqrt(1.0 / hidden_size)
        self.output_size = output_size
        self.embed_size = embed_size
        self.hidden_size = hidden_size

        self.W_emb: np.ndarray = rng.uniform(-scale, scale, (output_size, embed_size))
        self.W_h: np.ndarray = rng.uniform(
            -scale, scale, (hidden_size, embed_size + hidden_size)
        )
        self.b_h: np.ndarray = np.zeros(hidden_size)
        self.W_out: np.ndarray = rng.uniform(-scale, scale, (output_size, hidden_size))
        self.b_out: np.ndarray = np.zeros(output_size)

    def step(
        self,
        prev_token: int,
        prev_hidden: np.ndarray,
        context: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Single decoder step.

        Args:
            prev_token: Index of the previously generated token.
            prev_hidden: Previous hidden state [hidden_size].
            context: Attention context vector [hidden_size].

        Returns:
            Tuple of (next_hidden [hidden_size], logits [output_size],
                      probs [output_size]).
        """
        embed = self.W_emb[prev_token]              # [embed_size]
        combined = np.concatenate([embed, context])  # [embed_size + hidden_size]
        h = _tanh(self.W_h @ combined + self.b_h)    # [hidden_size]
        logits = self.W_out @ h + self.b_out          # [output_size]
        probs = _softmax(logits)
        return h, logits, probs


# ---------------------------------------------------------------------------
# Seq2Seq
# ---------------------------------------------------------------------------

class Seq2Seq:
    """Complete sequence-to-sequence model with attention.

    Combines an encoder, attention mechanism, and decoder.

    Attributes:
        encoder: The EncoderRNN.
        attention: The Attention mechanism.
        decoder: The DecoderRNN.
    """

    def __init__(
        self,
        input_vocab_size: int,
        output_vocab_size: int,
        embed_size: int,
        hidden_size: int,
        seed: int = 42,
    ) -> None:
        """Initialize the Seq2Seq model.

        Args:
            input_vocab_size: Size of the input vocabulary.
            output_vocab_size: Size of the output vocabulary.
            embed_size: Token embedding dimension.
            hidden_size: Hidden state dimension.
            seed: Random seed.
        """
        self.input_vocab_size = input_vocab_size
        self.output_vocab_size = output_vocab_size
        self.hidden_size = hidden_size

        # Input embedding matrix (one-hot input)
        rng = np.random.default_rng(seed)
        scale = np.sqrt(1.0 / embed_size)
        self.W_embed_in: np.ndarray = rng.uniform(
            -scale, scale, (embed_size, input_vocab_size)
        )

        self.encoder = EncoderRNN(embed_size, hidden_size, seed=seed + 1)
        self.attention = Attention(hidden_size, seed=seed + 2)
        self.decoder = DecoderRNN(output_vocab_size, embed_size, hidden_size,
                                  seed=seed + 3)

    def forward(
        self, input_seq: np.ndarray, target_seq: np.ndarray
    ) -> tuple[np.ndarray, float]:
        """Forward pass with teacher forcing.

        Args:
            input_seq: Input token indices [input_len].
            target_seq: Target token indices [output_len].

        Returns:
            Tuple of (all_output_probs [output_len, output_vocab_size], loss).
        """
        # Encode input
        input_emb = self.W_embed_in[:, input_seq].T   # [input_len, embed_size]
        enc_states = self.encoder.forward(input_emb)    # [input_len, hidden_size]

        # Decode with teacher forcing
        out_len = len(target_seq)
        h = enc_states[-1].copy()  # initial decoder hidden = last encoder state
        all_probs = np.zeros((out_len, self.output_vocab_size))
        loss = 0.0

        # SOS token = 0 (first token of target)
        prev_token = target_seq[0]
        for t in range(1, out_len):
            context, _ = self.attention.forward(h, enc_states)
            h, logits, probs = self.decoder.step(prev_token, h, context)
            all_probs[t] = probs
            loss += -np.log(probs[target_seq[t]] + 1e-12)
            prev_token = target_seq[t]  # teacher forcing

        return all_probs, loss

    def greedy_decode(
        self, input_seq: np.ndarray, max_len: int, sos_token: int
    ) -> list[int]:
        """Generate output sequence greedily.

        Args:
            input_seq: Input token indices [input_len].
            max_len: Maximum output length.
            sos_token: Start-of-sequence token index.

        Returns:
            Generated token indices (including SOS).
        """
        input_emb = self.W_embed_in[:, input_seq].T
        enc_states = self.encoder.forward(input_emb)
        h = enc_states[-1].copy()

        output = [sos_token]
        prev_token = sos_token
        for _ in range(max_len - 1):
            context, _ = self.attention.forward(h, enc_states)
            h, _, probs = self.decoder.step(prev_token, h, context)
            next_token = int(np.argmax(probs))
            output.append(next_token)
            prev_token = next_token
        return output


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------

def train_seq2seq(
    model: Seq2Seq,
    pairs: list[tuple[list[int], list[int]]],
    epochs: int = 100,
    lr: float = 0.01,
) -> list[float]:
    """Train the Seq2Seq model with SGD on a set of input-output pairs.

    Args:
        model: The Seq2Seq model.
        pairs: List of (input_seq, target_seq) token-index pairs.
        epochs: Number of training epochs.
        lr: Learning rate.

    Returns:
        List of losses per epoch.
    """
    epoch_losses: list[float] = []
    for epoch in range(epochs):
        total_loss = 0.0
        for inp, tgt in pairs:
            inp_arr = np.array(inp, dtype=np.int64)
            tgt_arr = np.array(tgt, dtype=np.int64)
            _, loss = model.forward(inp_arr, tgt_arr)
            total_loss += loss

            # Manual SGD — update all parameters
            # For simplicity, we perturb weights and check if loss decreases
            # (This is a simplified training procedure; in practice, full
            #  BPTT would be used. Here we use a finite-difference approach.)

        avg_loss = total_loss / len(pairs)
        epoch_losses.append(avg_loss)

        # Perturb-based SGD (simplified for educational demo)
        if epoch % 20 == 0:
            _sgd_step(model, pairs, lr)

    return epoch_losses


def _sgd_step(model: Seq2Seq, pairs: list[tuple[list[int], list[int]]],
              lr: float) -> None:
    """One SGD step using finite-difference gradient approximation.

    This is a simplified training approach for demonstration purposes.
    In real implementations, full backpropagation through time (BPTT)
    would be used.

    Args:
        model: The Seq2Seq model.
        pairs: Training pairs.
        lr: Learning rate.
    """
    eps = 1e-6
    params = [
        (model.encoder, "W_xh"),
        (model.encoder, "W_hh"),
        (model.decoder, "W_h"),
        (model.decoder, "W_out"),
    ]

    for obj, attr in params:
        w = getattr(obj, attr)
        grad = np.zeros_like(w)
        flat = w.ravel()
        for i in range(min(len(flat), 50)):  # subsample for speed
            old_val = flat[i]
            flat[i] = old_val + eps
            setattr(obj, attr, w.reshape(getattr(obj, attr).shape))
            loss_plus = _compute_total_loss(model, pairs)
            flat[i] = old_val - eps
            setattr(obj, attr, w.reshape(getattr(obj, attr).shape))
            loss_minus = _compute_total_loss(model, pairs)
            flat[i] = old_val
            grad_flat = grad.ravel()
            grad_flat[i] = (loss_plus - loss_minus) / (2 * eps)
            grad = grad_flat.reshape(grad.shape)
        setattr(obj, attr, w - lr * grad)


def _compute_total_loss(
    model: Seq2Seq, pairs: list[tuple[list[int], list[int]]]
) -> float:
    total = 0.0
    for inp, tgt in pairs:
        _, loss = model.forward(np.array(inp), np.array(tgt))
        total += loss
    return total


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Testing seq2seq.py — Seq2Seq with Attention")
    print("=" * 60)

    # Simple reverse task
    # Vocabulary: SOS=0, digits 1-9
    vocab = {"<SOS>": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5,
             "6": 6, "7": 7, "8": 8, "9": 9}
    inv_vocab = {v: k for k, v in vocab.items()}
    vocab_size = len(vocab)

    # Generate training pairs: input = [1,3,5] -> target = [SOS, 5,3,1]
    pairs: list[tuple[list[int], list[int]]] = []
    for seq_len in [2, 3, 4]:
        for _ in range(20):
            seq = list(np.random.randint(1, 10, size=seq_len))
            tgt = [0] + seq[::-1]  # reverse with SOS
            pairs.append((seq, tgt))

    print(f"\nTraining pairs: {len(pairs)}")

    # Create model
    model = Seq2Seq(
        input_vocab_size=vocab_size,
        output_vocab_size=vocab_size,
        embed_size=16,
        hidden_size=16,
        seed=42,
    )

    # Train
    losses = train_seq2seq(model, pairs, epochs=100, lr=0.05)
    print(f"Initial loss: {losses[0]:.2f}, Final loss: {losses[-1]:.2f}")

    # Test on a few examples
    test_pairs = [
        ([1, 2, 3], [0, 3, 2, 1]),
        ([5, 9], [0, 9, 5]),
        ([7, 8, 9, 6], [0, 6, 9, 8, 7]),
    ]

    all_pass = True
    for inp, expected in test_pairs:
        result = model.greedy_decode(np.array(inp), max_len=len(expected), sos_token=0)
        pred_str = [inv_vocab[r] for r in result]
        exp_str = [inv_vocab[e] for e in expected]
        exact_match = result == expected
        print(f"  Input: {inp} -> Pred: {pred_str}, Expected: {exp_str} "
              f"({'OK' if exact_match else 'FAIL'})")
        if not exact_match:
            all_pass = False

    # Verify loss decreased
    loss_decreased = losses[-1] < losses[0]
    print(f"Loss decreased: {loss_decreased}")

    final_pass = all_pass and loss_decreased
    print(f"\n{'PASS' if final_pass else 'FAIL'}: seq2seq.py")
