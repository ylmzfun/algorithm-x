"""Skip-gram Word2Vec implementation from scratch using NumPy.

Implements:
- Vocabulary building from corpus
- Skip-gram model with negative sampling
- Training loop with SGD
- Word similarity computation

Reference: Mikolov et al., "Efficient Estimation of Word Representations
in Vector Space" (2013) and "Distributed Representations of Words and
Phrases and their Compositionality" (2013).
"""

from __future__ import annotations

import numpy as np
from collections import Counter
from typing import Optional


class Vocabulary:
    """Build and manage a word vocabulary from a text corpus.

    Attributes:
        word2idx: Mapping from word string to integer index.
        idx2word: Mapping from integer index to word string.
        word_freq: Raw frequency count of each word.
        vocab_size: Number of unique words in the vocabulary.
    """

    def __init__(self, min_count: int = 1) -> None:
        """Initialize an empty vocabulary.

        Args:
            min_count: Minimum frequency for a word to be included.
        """
        self.min_count = min_count
        self.word2idx: dict[str, int] = {}
        self.idx2word: dict[int, str] = {}
        self.word_freq: Counter[str] = Counter()
        self.vocab_size: int = 0

    def build(self, sentences: list[list[str]]) -> None:
        """Build vocabulary from a list of tokenized sentences.

        Args:
            sentences: List of sentences, where each sentence is a list of tokens.
        """
        self.word_freq = Counter()
        for sentence in sentences:
            self.word_freq.update(sentence)

        # Filter by min_count
        filtered = {w: c for w, c in self.word_freq.items() if c >= self.min_count}
        sorted_words = sorted(filtered.keys())

        self.word2idx = {w: i for i, w in enumerate(sorted_words)}
        self.idx2word = {i: w for i, w in enumerate(sorted_words)}
        self.vocab_size = len(self.word2idx)

    def encode(self, tokens: list[str]) -> list[int]:
        """Convert a list of tokens to their integer indices.

        Args:
            tokens: List of word strings.

        Returns:
            List of integer indices (unknown words are skipped).
        """
        return [self.word2idx[t] for t in tokens if t in self.word2idx]


class SkipGramModel:
    """Skip-gram Word2Vec model with negative sampling.

    The skip-gram model predicts context words given a centre word.
    Negative sampling is used to approximate the full softmax efficiently.

    Attributes:
        vocab_size: Number of words in the vocabulary.
        embed_dim: Dimension of word embeddings.
        W_in: Input (centre-word) embedding matrix [vocab_size, embed_dim].
        W_out: Output (context-word) embedding matrix [vocab_size, embed_dim].
    """

    def __init__(self, vocab_size: int, embed_dim: int = 100, seed: int = 42) -> None:
        """Initialize the skip-gram model.

        Args:
            vocab_size: Number of unique words.
            embed_dim: Dimension of the embedding vectors.
            seed: Random seed for reproducibility.
        """
        rng = np.random.default_rng(seed)
        scale = 0.5 / embed_dim
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        self.W_in: np.ndarray = rng.uniform(-scale, scale, (vocab_size, embed_dim))
        self.W_out: np.ndarray = rng.uniform(-scale, scale, (vocab_size, embed_dim))

    def forward(self, centre_idx: int) -> tuple[np.ndarray, np.ndarray]:
        """Forward pass: get centre word embedding and output logits.

        Args:
            centre_idx: Index of the centre word.

        Returns:
            Tuple of (hidden vector [embed_dim], output scores [vocab_size]).
        """
        h = self.W_in[centre_idx]  # [embed_dim]
        scores = self.W_out @ h     # [vocab_size]
        return h, scores

    def negative_sampling_loss(
        self,
        centre_idx: int,
        pos_context_idx: int,
        neg_indices: np.ndarray,
    ) -> tuple[float, np.ndarray, np.ndarray]:
        """Compute loss and gradients for one centre–context pair with negative samples.

        Args:
            centre_idx: Index of the centre word.
            pos_context_idx: Index of the positive context word.
            neg_indices: Array of negative sample indices [K].

        Returns:
            Tuple of (loss, grad_W_in, grad_W_out).
                grad_W_in: [vocab_size, embed_dim] — only row centre_idx is non-zero.
                grad_W_out: [vocab_size, embed_dim] — rows for pos + neg samples updated.
        """
        h = self.W_in[centre_idx]  # [embed_dim]

        # Positive sample
        pos_score = self.W_out[pos_context_idx] @ h
        pos_sigmoid = 1.0 / (1.0 + np.exp(-pos_score))
        loss = -np.log(pos_sigmoid + 1e-12)

        # Negative samples
        neg_scores = self.W_out[neg_indices] @ h  # [K]
        neg_sigmoid = 1.0 / (1.0 + np.exp(neg_scores))  # sigmoid(-score)
        loss += -np.sum(np.log(neg_sigmoid + 1e-12))

        # Gradients
        grad_W_out = np.zeros_like(self.W_out)
        grad_W_out[pos_context_idx] = (pos_sigmoid - 1.0) * h
        for i, ni in enumerate(neg_indices):
            grad_W_out[ni] += (1.0 - neg_sigmoid[i]) * h  # sigmoid(score) * h

        grad_h = (pos_sigmoid - 1.0) * self.W_out[pos_context_idx]
        for i, ni in enumerate(neg_indices):
            grad_h += (1.0 - neg_sigmoid[i]) * self.W_out[ni]

        grad_W_in = np.zeros_like(self.W_in)
        grad_W_in[centre_idx] = grad_h

        return loss, grad_W_in, grad_W_out


def _build_sampling_table(word_freq: Counter[str], word2idx: dict[str, int],
                          power: float = 0.75) -> np.ndarray:
    """Build a unigram table for negative sampling with exponentiated frequencies.

    Args:
        word_freq: Word frequency counter.
        word2idx: Word-to-index mapping.
        power: Exponent applied to frequencies (default 0.75 as in the paper).

    Returns:
        Sampling table as an array of word indices proportional to freq^power.
    """
    freqs = np.array([word_freq[word] ** power for word in word2idx], dtype=np.float64)
    probs = freqs / freqs.sum()
    table_size = 10_000_000
    table = np.random.choice(len(word2idx), size=table_size, p=probs)
    return table


def train_word2vec(
    model: SkipGramModel,
    corpus: list[list[str]],
    vocab: Vocabulary,
    window_size: int = 2,
    neg_samples: int = 5,
    lr: float = 0.05,
    epochs: int = 5,
) -> list[float]:
    """Train a skip-gram Word2Vec model on a corpus.

    Args:
        model: The SkipGramModel to train.
        corpus: List of tokenized sentences.
        vocab: Vocabulary built from the corpus.
        window_size: Context window radius.
        neg_samples: Number of negative samples per positive pair.
        lr: Learning rate.
        epochs: Number of training epochs.

    Returns:
        List of average losses per epoch.
    """
    sampling_table = _build_sampling_table(vocab.word_freq, vocab.word2idx)
    epoch_losses: list[float] = []

    for epoch in range(epochs):
        total_loss = 0.0
        pair_count = 0

        for sentence in corpus:
            indices = vocab.encode(sentence)
            sent_len = len(indices)
            for i, centre_idx in enumerate(indices):
                # Context window
                start = max(0, i - window_size)
                end = min(sent_len, i + window_size + 1)
                for j in range(start, end):
                    if j == i:
                        continue
                    pos_idx = indices[j]
                    # Sample negatives (ensure they don't include positive)
                    neg_idx_set = {pos_idx, centre_idx}
                    neg_arr = []
                    attempts = 0
                    while len(neg_arr) < neg_samples and attempts < neg_samples * 20:
                        ns = sampling_table[np.random.randint(0, len(sampling_table))]
                        if ns not in neg_idx_set:
                            neg_arr.append(ns)
                            neg_idx_set.add(ns)
                        attempts += 1
                    if len(neg_arr) < neg_samples:
                        continue
                    neg_indices = np.array(neg_arr, dtype=np.int64)

                    loss, grad_W_in, grad_W_out = model.negative_sampling_loss(
                        centre_idx, pos_idx, neg_indices
                    )
                    model.W_in -= lr * grad_W_in
                    model.W_out -= lr * grad_W_out
                    total_loss += loss
                    pair_count += 1

        avg_loss = total_loss / max(pair_count, 1)
        epoch_losses.append(avg_loss)

    return epoch_losses


def word_similarity(
    model: SkipGramModel,
    word: str,
    vocab: Vocabulary,
    top_k: int = 5,
) -> list[tuple[str, float]]:
    """Find the top-k most similar words using cosine similarity.

    Args:
        model: Trained SkipGramModel.
        word: Query word.
        vocab: Vocabulary.
        top_k: Number of similar words to return.

    Returns:
        List of (word, similarity score) tuples sorted by similarity descending.
    """
    if word not in vocab.word2idx:
        return []
    idx = vocab.word2idx[word]
    vec = model.W_in[idx]
    # Normalize all vectors
    norms = np.linalg.norm(model.W_in, axis=1, keepdims=True) + 1e-12
    normalized = model.W_in / norms
    query_norm = vec / (np.linalg.norm(vec) + 1e-12)
    sims = normalized @ query_norm  # [vocab_size]

    # Get top-k (excluding the query word itself)
    sims[idx] = -1.0
    top_indices = np.argsort(sims)[::-1][:top_k]
    return [(vocab.idx2word[i], float(sims[i])) for i in top_indices]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Testing word_vectors.py — Skip-gram Word2Vec")
    print("=" * 60)

    # Toy corpus of related words
    corpus = [
        ["king", "queen", "man", "woman", "royal", "crown"],
        ["king", "rules", "the", "kingdom", "with", "queen"],
        ["man", "works", "in", "the", "office", "every", "day"],
        ["woman", "is", "a", "doctor", "at", "the", "hospital"],
        ["queen", "and", "king", "live", "in", "the", "castle"],
        ["man", "and", "woman", "walk", "in", "the", "park"],
        ["the", "king", "wears", "a", "crown", "of", "gold"],
        ["the", "queen", "has", "royal", "jewels"],
        ["the", "doctor", "helps", "the", "woman"],
        ["the", "man", "is", "a", "teacher"],
        ["king", "queen", "royal", "castle", "kingdom"],
        ["man", "woman", "doctor", "teacher", "office"],
        ["the", "dog", "and", "cat", "are", "pets"],
        ["dog", "cat", "bird", "fish", "animals"],
        ["the", "dog", "barks", "at", "the", "cat"],
        ["i", "like", "to", "eat", "pizza", "and", "pasta"],
        ["pizza", "pasta", "bread", "food", "delicious"],
        ["dog", "food", "is", "in", "the", "bowl"],
        ["cat", "eats", "fish", "every", "day"],
        ["king", "and", "queen", "are", "royal", "rulers"],
    ]

    print(f"\nCorpus: {len(corpus)} sentences")

    # Build vocabulary
    vocab = Vocabulary(min_count=1)
    vocab.build(corpus)
    print(f"Vocabulary size: {vocab.vocab_size}")

    # Train model
    model = SkipGramModel(vocab.vocab_size, embed_dim=50, seed=42)
    losses = train_word2vec(model, corpus, vocab, window_size=2,
                            neg_samples=3, lr=0.05, epochs=15)
    print(f"Final loss: {losses[-1]:.4f}")
    print(f"Loss decreased: {losses[-1] < losses[0]:.4f}")

    # Test similarity: related pairs should appear in each other's top-k
    related_pairs = [
        ("king", "queen"),
        ("man", "woman"),
        ("dog", "cat"),
        ("pizza", "pasta"),
    ]

    all_pass = True
    for w1, w2 in related_pairs:
        sim = word_similarity(model, w1, vocab, top_k=10)
        sim_words = [s[0] for s in sim]
        is_related = w2 in sim_words
        print(f"  Similar words for '{w1}': {sim_words[:5]} ... "
              f"(contains '{w2}'? {is_related})")
        if not is_related:
            all_pass = False

    # Unrelated pair should NOT be in top-k
    sim_king = word_similarity(model, "king", vocab, top_k=10)
    sim_king_words = [s[0] for s in sim_king]
    unrelated_ok = "dog" not in sim_king_words
    print(f"  'dog' NOT in top-10 for 'king': {unrelated_ok}")
    all_pass = all_pass and unrelated_ok

    # Verify that related word pairs have higher cosine similarity than unrelated
    king_queen_sim = float(
        np.dot(
            model.W_in[vocab.word2idx["king"]]
            / (np.linalg.norm(model.W_in[vocab.word2idx["king"]]) + 1e-12),
            model.W_in[vocab.word2idx["queen"]]
            / (np.linalg.norm(model.W_in[vocab.word2idx["queen"]]) + 1e-12),
        )
    )
    king_dog_sim = float(
        np.dot(
            model.W_in[vocab.word2idx["king"]]
            / (np.linalg.norm(model.W_in[vocab.word2idx["king"]]) + 1e-12),
            model.W_in[vocab.word2idx["dog"]]
            / (np.linalg.norm(model.W_in[vocab.word2idx["dog"]]) + 1e-12),
        )
    )
    print(f"  Cosine(king, queen) = {king_queen_sim:.3f}")
    print(f"  Cosine(king, dog)   = {king_dog_sim:.3f}")
    if king_queen_sim <= king_dog_sim:
        print("  FAIL: related words should have higher similarity")
        all_pass = False

    print(f"\n{'PASS' if all_pass else 'FAIL'}: word_vectors.py")
