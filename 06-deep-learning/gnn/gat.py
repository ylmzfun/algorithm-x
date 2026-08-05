"""Graph Attention Network (GAT) from scratch using NumPy.

Implements multi-head self-attention over graph neighbors.
For each node, attention coefficients are computed per neighbor and normalized.
"""

import numpy as np
from typing import Optional


class GATLayer:
    """Graph Attention Network layer with multi-head attention.

    For each head:
        e_ij = LeakyReLU(a^T @ [W @ h_i || W @ h_j])
        α_ij = softmax_j(e_ij) over neighbors
        h_i' = σ(sum_j α_ij * W @ h_j)

    Multi-head: concatenate or average outputs from different heads.
    """

    def __init__(
        self,
        input_dim: int,
        output_dim: int,
        num_heads: int = 4,
        concat: bool = True,
        alpha: float = 0.2,
        random_seed: Optional[int] = 42,
    ):
        """Initialize GAT layer.

        Args:
            input_dim: Input feature dimension.
            output_dim: Output dimension per head.
            num_heads: Number of attention heads.
            concat: If True, concatenate head outputs. If False, average them.
            alpha: Negative slope for LeakyReLU in attention.
            random_seed: Random seed.
        """
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.num_heads = num_heads
        self.concat = concat
        self.alpha = alpha

        rng = np.random.RandomState(random_seed)
        scale = np.sqrt(2.0 / input_dim)

        # Weight matrices per head: (head, input_dim, output_dim)
        self.W = np.array([
            rng.randn(input_dim, output_dim) * scale
            for _ in range(num_heads)
        ])

        # Attention vectors per head: (head, 2*output_dim)
        self.a = np.array([
            rng.randn(2 * output_dim) * scale
            for _ in range(num_heads)
        ])

        self._cache: dict = {}

    def _leaky_relu(self, x: np.ndarray) -> np.ndarray:
        """LeakyReLU activation."""
        return np.where(x > 0, x, self.alpha * x)

    def forward(self, X: np.ndarray, A: np.ndarray) -> np.ndarray:
        """Forward pass for all nodes.

        Args:
            X: Node features of shape (N, input_dim).
            A: Adjacency matrix of shape (N, N) with 0/1 values.

        Returns:
            Output features:
            - If concat: shape (N, num_heads * output_dim)
            - If average: shape (N, output_dim)
        """
        N = X.shape[0]
        heads_out = []

        all_attn_weights = []

        for h in range(self.num_heads):
            # Linear transformation: (N, output_dim)
            X_trans = np.dot(X, self.W[h])  # (N, out_dim)

            # Compute attention scores: e_ij = LeakyReLU(a^T @ [Wh_i || Wh_j])
            # For all pairs (i, j) with A[i,j] = 1
            e = np.zeros((N, N))
            for i in range(N):
                Wh_i = X_trans[i]  # (out_dim,)
                for j in range(N):
                    if A[i, j] > 0 or i == j:
                        Wh_j = X_trans[j]
                        concat_ij = np.concatenate([Wh_i, Wh_j])  # (2*out_dim,)
                        e[i, j] = np.dot(self.a[h], concat_ij)

            e = self._leaky_relu(e)

            # Mask non-neighbors with -inf
            mask = (A + np.eye(N)) > 0
            e_masked = np.where(mask, e, -1e9)

            # Softmax over neighbors
            e_max = np.max(e_masked, axis=1, keepdims=True)
            e_exp = np.exp(np.clip(e_masked - e_max, -500, 500))
            attn = e_exp / (np.sum(e_exp * mask, axis=1, keepdims=True) + 1e-10)
            attn = attn * mask

            all_attn_weights.append(attn)

            # Aggregate: h_i' = ReLU(sum_j α_ij * W @ h_j)
            h_out = np.dot(attn, X_trans)  # (N, out_dim)
            h_out = np.maximum(0, h_out)   # ReLU

            heads_out.append(h_out)

        self._cache = {
            "X": X, "A": A,
            "heads_out": heads_out,
            "attn_weights": all_attn_weights,
        }

        if self.concat:
            return np.concatenate(heads_out, axis=1)  # (N, num_heads * out_dim)
        else:
            return np.mean(np.stack(heads_out), axis=0)  # (N, out_dim)


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing GAT...")

    np.random.seed(42)

    # Create a small graph
    A = np.array([
        [0, 1, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [0, 0, 1, 0],
    ], dtype=float)
    X = np.random.randn(4, 6)

    # Test 1: GATLayer forward (concat heads)
    gat = GATLayer(input_dim=6, output_dim=4, num_heads=3, concat=True, random_seed=42)
    out = gat.forward(X, A)
    expected_dim = 3 * 4  # num_heads * output_dim
    assert out.shape == (4, expected_dim), f"Wrong output shape: {out.shape}"
    print(f"  PASS: GAT (concat) output shape: {out.shape}")

    # Test 2: GATLayer forward (average heads)
    gat_avg = GATLayer(input_dim=6, output_dim=8, num_heads=4, concat=False, random_seed=42)
    out_avg = gat_avg.forward(X, A)
    assert out_avg.shape == (4, 8), f"Wrong avg output shape: {out_avg.shape}"
    print(f"  PASS: GAT (average) output shape: {out_avg.shape}")

    # Test 3: Attention weights sum to 1 for each node (softmax property)
    attn_weights = gat._cache["attn_weights"][0]  # First head
    for i in range(4):
        attn_sum = np.sum(attn_weights[i])
        assert np.isclose(attn_sum, 1.0, atol=1e-6), \
               f"Attention weights don't sum to 1 for node {i}: sum={attn_sum:.4f}"
    print("  PASS: Attention weights sum to 1 for each node's neighbors")

    # Test 4: Attention respects adjacency (no edges = 0 attention)
    for i in range(4):
        for j in range(4):
            if A[i, j] == 0 and i != j:
                assert attn_weights[i, j] < 1e-6, f"Attention to non-neighbor: {attn_weights[i,j]}"
    print("  PASS: Attention respects adjacency (non-neighbors get 0 weight)")

    # Test 5: Multiple heads produce different attention
    attns = gat._cache["attn_weights"]
    assert not np.allclose(attns[0], attns[1]), "Different heads should differ"
    print("  PASS: Different heads produce different attention patterns")

    # Test 6: Single head
    gat_single = GATLayer(input_dim=6, output_dim=4, num_heads=1, concat=True, random_seed=42)
    out_single = gat_single.forward(X, A)
    assert out_single.shape == (4, 4)
    print(f"  PASS: Single-head GAT output: {out_single.shape}")

    # Test 7: No edges (only self-loops should remain)
    A_empty = np.zeros((4, 4))
    out_empty = gat.forward(X, A_empty)
    assert out_empty.shape == (4, expected_dim), "Should work with empty graph (self-loops)"
    print("  PASS: GAT with no edges (self-loops only)")

    # Test 8: LeakyReLU gradient behavior
    x_test = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
    lr_out = gat._leaky_relu(x_test)
    expected = np.array([-0.4, -0.2, 0.0, 1.0, 2.0])
    assert np.allclose(lr_out, expected, atol=1e-6), f"LeakyReLU wrong: {lr_out}"
    print("  PASS: LeakyReLU correct")

    print("\nAll GAT tests passed!")
