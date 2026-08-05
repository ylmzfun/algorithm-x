"""Positional encoding implementations.

Two variants:
1. Sinusoidal positional encoding (fixed, as in "Attention Is All You Need")
2. Learned positional encoding (trainable parameters)
"""

import numpy as np
from typing import Optional


def sinusoidal_positional_encoding(
    seq_len: int,
    d_model: int,
    base: float = 10000.0,
) -> np.ndarray:
    """Compute sinusoidal positional encoding.

    PE[pos, 2i]   = sin(pos / base^(2i/d_model))
    PE[pos, 2i+1] = cos(pos / base^(2i/d_model))

    Args:
        seq_len: Maximum sequence length.
        d_model: Model/embedding dimension.
        base: Base for the exponential (default 10000).

    Returns:
        Positional encoding of shape (1, seq_len, d_model).
    """
    position = np.arange(seq_len)[:, np.newaxis]  # (seq_len, 1)
    div_term = np.exp(
        np.arange(0, d_model, 2) * (-np.log(base) / d_model)
    )  # (d_model/2,)

    pe = np.zeros((seq_len, d_model))
    pe[:, 0::2] = np.sin(position * div_term)   # even indices
    pe[:, 1::2] = np.cos(position * div_term)   # odd indices

    return pe[np.newaxis, :, :]  # (1, seq_len, d_model)


class LearnedPositionalEncoding:
    """Learned positional encoding as a trainable parameter.

    Uses an embedding matrix of shape (max_seq_len, d_model).
    """

    def __init__(
        self,
        max_seq_len: int,
        d_model: int,
        random_seed: Optional[int] = 42,
    ):
        """Initialize learned positional encoding.

        Args:
            max_seq_len: Maximum sequence length.
            d_model: Embedding dimension.
            random_seed: Random seed.
        """
        self.max_seq_len = max_seq_len
        self.d_model = d_model

        rng = np.random.RandomState(random_seed)
        self.embedding = rng.randn(max_seq_len, d_model) * 0.02

    def forward(self, seq_len: int) -> np.ndarray:
        """Get positional encoding for a given sequence length.

        Args:
            seq_len: Current sequence length (must be <= max_seq_len).

        Returns:
            Positional encoding of shape (1, seq_len, d_model).
        """
        if seq_len > self.max_seq_len:
            raise ValueError(f"seq_len {seq_len} > max_seq_len {self.max_seq_len}")
        return self.embedding[:seq_len][np.newaxis, :, :]


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing Positional Encoding...")

    np.random.seed(42)

    # Test 1: Sinusoidal encoding dimensions
    pe = sinusoidal_positional_encoding(seq_len=50, d_model=64)
    assert pe.shape == (1, 50, 64), f"Wrong shape: {pe.shape}"
    print(f"  PASS: Sinusoidal PE shape: {pe.shape}")

    # Test 2: Sinusoidal encoding uses sin for even, cos for odd
    pe_2d = sinusoidal_positional_encoding(seq_len=100, d_model=8).squeeze(0)
    # Even columns (0, 2, 4, 6) should follow sin pattern
    # Odd columns (1, 3, 5, 7) should follow cos pattern
    even_col = pe_2d[:, 0]  # First even column
    odd_col = pe_2d[:, 1]   # First odd column
    # sin(0) = 0, cos(0) = 1
    assert np.isclose(even_col[0], 0.0, atol=1e-6), f"PE[0,0] should be 0, got {even_col[0]}"
    assert np.isclose(odd_col[0], 1.0, atol=1e-6), f"PE[0,1] should be 1, got {odd_col[0]}"
    print("  PASS: Sinusoidal PE uses correct sin/cos pattern")

    # Test 3: Different positions have different encodings
    pe_diff = sinusoidal_positional_encoding(seq_len=10, d_model=16).squeeze(0)
    # Check that PE for position 0 differs from position 1
    assert not np.allclose(pe_diff[0], pe_diff[1]), "Positions 0 and 1 have same encoding"
    print("  PASS: Different positions have different encodings")

    # Test 4: Encoding values are bounded
    assert np.max(np.abs(pe)) <= 1.0 + 1e-6, "PE values exceed [-1, 1]"
    print("  PASS: Sinusoidal PE values in [-1, 1]")

    # Test 5: Learned positional encoding
    lpe = LearnedPositionalEncoding(max_seq_len=100, d_model=32, random_seed=42)
    pe_learned = lpe.forward(seq_len=20)
    assert pe_learned.shape == (1, 20, 32), f"Wrong learned PE shape: {pe_learned.shape}"
    print(f"  PASS: Learned PE shape: {pe_learned.shape}")

    # Test 6: Learned encoding is different per position
    pe_l = pe_learned.squeeze(0)
    assert not np.allclose(pe_l[0], pe_l[5]), "Same learned encoding for different positions"
    print("  PASS: Learned encoding differs per position")

    # Test 7: Error on exceeding max_seq_len
    try:
        lpe.forward(seq_len=101)
        assert False, "Should have raised ValueError"
    except ValueError:
        print("  PASS: ValueError raised for seq_len > max_seq_len")

    # Test 8: Sinusoidal PE with different base values
    pe_small_base = sinusoidal_positional_encoding(seq_len=10, d_model=8, base=100.0)
    pe_large_base = sinusoidal_positional_encoding(seq_len=10, d_model=8, base=10000.0)
    # Different bases produce different encodings
    assert not np.allclose(pe_small_base, pe_large_base), "Different bases should differ"
    print("  PASS: Different base values produce different encodings")

    # Test 9: Visualization (optional)
    try:
        import matplotlib.pyplot as plt

        pe_vis = sinusoidal_positional_encoding(seq_len=50, d_model=32).squeeze(0)

        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        axes[0].imshow(pe_vis.T, aspect="auto", cmap="RdBu")
        axes[0].set_xlabel("Position")
        axes[0].set_ylabel("Dimension")
        axes[0].set_title("Sinusoidal Positional Encoding")

        # Plot selected dimensions
        for i in [0, 4, 8, 16, 24, 31]:
            axes[1].plot(pe_vis[:, i], label=f"dim {i}")
        axes[1].set_xlabel("Position")
        axes[1].set_ylabel("Encoding Value")
        axes[1].set_title("Encoding Values by Dimension")
        axes[1].legend(fontsize="small")

        plt.tight_layout()
        plt.savefig("/tmp/positional_encoding.png", dpi=100)
        plt.close()
        print("  PASS: Visualization saved to /tmp/positional_encoding.png")
    except ImportError:
        print("  SKIP: matplotlib not available")

    print("\nAll Positional Encoding tests passed!")
