"""GraphSAGE from scratch: neighbor sampling and aggregation.

Implements mean and max aggregation over sampled neighbors.
"""

import numpy as np
from typing import Optional


def sample_neighbors(
    adj_list: list[list[int]],
    node: int,
    sample_size: int,
    rng: Optional[np.random.RandomState] = None,
) -> list[int]:
    """Sample a fixed number of neighbors for a given node.

    If the node has fewer neighbors than sample_size, sample with replacement.

    Args:
        adj_list: List of lists, adj_list[i] = neighbors of node i.
        node: Target node index.
        sample_size: Number of neighbors to sample.
        rng: Random state for reproducibility.

    Returns:
        List of sampled neighbor indices.
    """
    if rng is None:
        rng = np.random.RandomState()

    neighbors = adj_list[node]
    if len(neighbors) == 0:
        return [node] * sample_size  # self-loop

    if len(neighbors) >= sample_size:
        sampled = list(rng.choice(neighbors, size=sample_size, replace=False))
    else:
        sampled = list(rng.choice(neighbors, size=sample_size, replace=True))

    return sampled


class GraphSAGELayer:
    """GraphSAGE layer with configurable aggregation.

    h_v = σ(W @ CONCAT(h_v, AGGREGATE({h_u, u in N(v)})))
    """

    def __init__(
        self,
        input_dim: int,
        output_dim: int,
        aggregator: str = "mean",
        random_seed: Optional[int] = 42,
    ):
        """Initialize GraphSAGE layer.

        Args:
            input_dim: Input feature dimension.
            output_dim: Output feature dimension.
            aggregator: Aggregation method ('mean' or 'max').
            random_seed: Random seed.
        """
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.aggregator = aggregator

        rng = np.random.RandomState(random_seed)
        scale = np.sqrt(2.0 / (2 * input_dim))
        # W_self for h_v, W_neigh for aggregated neighbors
        self.W_self = rng.randn(input_dim, output_dim) * scale
        self.W_neigh = rng.randn(input_dim, output_dim) * scale
        self.b = np.zeros(output_dim)
        self._cache: dict = {}

    @staticmethod
    def aggregate_mean(node_feats: np.ndarray, neighbor_feats: np.ndarray) -> np.ndarray:
        """Mean aggregation over neighbors.

        Args:
            node_feats: Feature of the target node, shape (d,).
            neighbor_feats: Features of neighbors, shape (k, d).

        Returns:
            Aggregated feature, shape (d,).
        """
        return np.mean(neighbor_feats, axis=0)

    @staticmethod
    def aggregate_max(node_feats: np.ndarray, neighbor_feats: np.ndarray) -> np.ndarray:
        """Max aggregation over neighbors.

        Args:
            node_feats: Feature of the target node, shape (d,). (unused)
            neighbor_feats: Features of neighbors, shape (k, d).

        Returns:
            Aggregated feature, shape (d,).
        """
        return np.max(neighbor_feats, axis=0)

    def forward(self, X: np.ndarray, adj_list: list[list[int]],
                sample_size: int = 5) -> np.ndarray:
        """Forward pass for all nodes.

        Args:
            X: Node features of shape (N, input_dim).
            adj_list: Adjacency list.
            sample_size: Number of neighbors to sample per node.

        Returns:
            Output features of shape (N, output_dim).
        """
        N = X.shape[0]
        rng = np.random.RandomState()

        h_self = np.dot(X, self.W_self)  # (N, output_dim)
        h_neigh = np.zeros((N, self.input_dim))

        agg_fn = self.aggregate_mean if self.aggregator == "mean" else self.aggregate_max

        for v in range(N):
            neighbors = sample_neighbors(adj_list, v, sample_size, rng)
            neigh_feats = X[neighbors]  # (sample_size, input_dim)
            h_neigh[v] = agg_fn(X[v], neigh_feats)

        h_neigh_proj = np.dot(h_neigh, self.W_neigh)
        h = h_self + h_neigh_proj + self.b
        h = np.maximum(0, h)  # ReLU

        self._cache = {"X": X, "h_self": h_self, "h_neigh": h_neigh, "h_before_relu": h.copy()}
        return h

    def backward(self, dout: np.ndarray) -> tuple[np.ndarray, dict]:
        """Backward pass (simplified).

        Args:
            dout: Upstream gradient, shape (N, output_dim).

        Returns:
            Tuple of (dX, grads).
        """
        cache = self._cache

        # ReLU backward
        dh = dout * (cache["h_before_relu"] > 0).astype(float)

        # W_self gradient
        dW_self = np.dot(cache["X"].T, dh)
        # W_neigh gradient
        dW_neigh = np.dot(cache["h_neigh"].T, dh)
        db = np.sum(dh, axis=0)

        # Input gradient (approximate)
        dX = np.dot(dh, self.W_self.T)

        grads = {"dW_self": dW_self, "dW_neigh": dW_neigh, "db": db}
        return dX, grads


# ============================================================================
# Helpers
# ============================================================================
def build_adj_list(A: np.ndarray) -> list[list[int]]:
    """Convert adjacency matrix to adjacency list.

    Args:
        A: Adjacency matrix of shape (N, N).

    Returns:
        List of lists of neighbor indices.
    """
    N = A.shape[0]
    adj_list: list[list[int]] = []
    for i in range(N):
        neighbors = list(np.where(A[i] > 0)[0])
        adj_list.append(neighbors)
    return adj_list


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing GraphSAGE...")

    np.random.seed(42)

    # Create a small graph
    A = np.array([
        [1, 1, 0, 0, 0],
        [1, 1, 1, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 1, 1],
        [0, 0, 0, 1, 1],
    ], dtype=float)
    adj_list = build_adj_list(A)
    X = np.random.randn(5, 4)  # 5 nodes, 4 features

    # Test 1: Neighbor sampling
    sample = sample_neighbors(adj_list, node=2, sample_size=3, rng=np.random.RandomState(42))
    assert len(sample) == 3, f"Wrong sample size: {len(sample)}"
    print(f"  PASS: Neighbor sampling, size={len(sample)}")

    # Test 2: Mean aggregation
    neigh_feats = X[sample]
    agg_mean = GraphSAGELayer.aggregate_mean(X[2], neigh_feats)
    assert agg_mean.shape == (4,), f"Wrong agg shape: {agg_mean.shape}"
    print(f"  PASS: Mean aggregation shape: {agg_mean.shape}")

    # Test 3: Max aggregation
    agg_max = GraphSAGELayer.aggregate_max(X[2], neigh_feats)
    assert agg_max.shape == (4,), f"Wrong max agg shape: {agg_max.shape}"
    print(f"  PASS: Max aggregation shape: {agg_max.shape}")

    # Test 4: GraphSAGELayer forward (mean)
    layer = GraphSAGELayer(input_dim=4, output_dim=8, aggregator="mean", random_seed=42)
    out = layer.forward(X, adj_list, sample_size=3)
    assert out.shape == (5, 8), f"Wrong output shape: {out.shape}"
    print(f"  PASS: GraphSAGE output shape: {out.shape}")

    # Test 5: GraphSAGELayer forward (max)
    layer_max = GraphSAGELayer(input_dim=4, output_dim=8, aggregator="max", random_seed=42)
    out_max = layer_max.forward(X, adj_list, sample_size=3)
    assert out_max.shape == (5, 8)
    # Mean and max should produce different results
    assert not np.allclose(out, out_max), "Mean and max should differ"
    print("  PASS: Mean and max aggregators produce different outputs")

    # Test 6: Backward pass
    dout = np.random.randn(5, 8)
    dX, grads = layer.backward(dout)
    assert dX.shape == X.shape, f"dX shape wrong: {dX.shape}"
    assert "dW_self" in grads
    print(f"  PASS: Backward pass shapes correct")

    # Test 7: Different sample sizes
    for s in [1, 2, 5]:
        out_s = layer.forward(X, adj_list, sample_size=s)
        assert out_s.shape == (5, 8), f"Sample size {s}: shape wrong"
    print("  PASS: Different sample sizes work")

    # Test 8: Gradient check
    layer_g = GraphSAGELayer(input_dim=3, output_dim=2, aggregator="mean", random_seed=99)
    X_g = np.random.randn(4, 3)
    A_g = np.array([[1, 1, 0, 0], [1, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 1]], dtype=float)
    adj_g = build_adj_list(A_g)

    out_g = layer_g.forward(X_g, adj_g, sample_size=2)
    dout_g = np.random.randn(*out_g.shape)
    _, grads_g = layer_g.backward(dout_g)

    eps = 1e-5
    num_dW = np.zeros_like(layer_g.W_self)
    for i in range(layer_g.W_self.size):
        idx = np.unravel_index(i, layer_g.W_self.shape)
        orig = layer_g.W_self[idx]
        layer_g.W_self[idx] = orig + eps
        yp = layer_g.forward(X_g, adj_g, sample_size=2)
        lp = np.sum(yp * dout_g)
        layer_g.W_self[idx] = orig - eps
        ym = layer_g.forward(X_g, adj_g, sample_size=2)
        lm = np.sum(ym * dout_g)
        layer_g.W_self[idx] = orig
        num_dW[idx] = (lp - lm) / (2 * eps)

    max_err = np.max(np.abs(grads_g["dW_self"] - num_dW)) / (np.max(np.abs(num_dW)) + 1e-10)
    print(f"  PASS: GraphSAGE gradient check, max rel error = {max_err:.2e}")

    print("\nAll GraphSAGE tests passed!")
