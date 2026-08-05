"""Graph Convolutional Network (GCN) from scratch using NumPy.

Implements:
- Adjacency matrix normalization with self-loops
- GCN layer: X' = A_norm @ X @ W
- Multi-layer GCN for node classification
"""

import numpy as np
from typing import Optional


def normalize_adjacency(A: np.ndarray) -> np.ndarray:
    """Normalize adjacency matrix with self-loops: D^(-1/2) * (A + I) * D^(-1/2).

    Args:
        A: Adjacency matrix of shape (N, N), values 0 or 1.

    Returns:
        Normalized adjacency matrix of shape (N, N).
    """
    A_hat = A + np.eye(A.shape[0])  # Add self-loops
    D_hat = np.sum(A_hat, axis=1)    # Degree of A_hat
    D_hat_inv_sqrt = np.diag(1.0 / np.sqrt(D_hat + 1e-8))
    A_norm = D_hat_inv_sqrt @ A_hat @ D_hat_inv_sqrt
    return A_norm


class GCNLayer:
    """Single GCN layer: X' = A_norm @ X @ W + b."""

    def __init__(
        self,
        input_dim: int,
        output_dim: int,
        use_bias: bool = True,
        random_seed: Optional[int] = 42,
    ):
        """Initialize GCN layer.

        Args:
            input_dim: Input feature dimension.
            output_dim: Output feature dimension.
            use_bias: Whether to include bias term.
            random_seed: Random seed.
        """
        rng = np.random.RandomState(random_seed)
        scale = np.sqrt(2.0 / input_dim)
        self.W = rng.randn(input_dim, output_dim) * scale
        self.b = np.zeros((1, output_dim)) if use_bias else None
        self._cache: dict = {}

    def forward(self, X: np.ndarray, A_norm: np.ndarray) -> np.ndarray:
        """Forward pass.

        Args:
            X: Node features of shape (N, input_dim).
            A_norm: Normalized adjacency of shape (N, N).

        Returns:
            Output features of shape (N, output_dim).
        """
        # Message passing: aggregate neighbor features
        support = np.dot(X, self.W)  # (N, output_dim)
        out = np.dot(A_norm, support)  # (N, output_dim)

        if self.b is not None:
            out += self.b

        self._cache = {"X": X, "A_norm": A_norm, "support": support}
        return out

    def backward(self, dout: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Backward pass.

        Args:
            dout: Upstream gradient of shape (N, output_dim).

        Returns:
            Tuple of (dX, dW, db).
        """
        cache = self._cache

        # Gradient through A_norm
        d_support = np.dot(cache["A_norm"].T, dout)  # (N, output_dim)

        # Gradient w.r.t. weights
        dW = np.dot(cache["X"].T, d_support)
        db = np.sum(dout, axis=0, keepdims=True) if self.b is not None else None

        # Gradient w.r.t. input
        dX = np.dot(d_support, self.W.T)

        return dX, dW, db


class GCN:
    """Multi-layer Graph Convolutional Network.

    Architecture: GCNLayer → ReLU → GCNLayer → ReLU → GCNLayer → Softmax
    """

    def __init__(
        self,
        input_dim: int,
        hidden_dims: list[int],
        output_dim: int,
        random_seed: Optional[int] = 42,
    ):
        """Initialize GCN.

        Args:
            input_dim: Input feature dimension.
            hidden_dims: List of hidden layer dimensions.
            output_dim: Number of output classes.
            random_seed: Random seed.
        """
        dims = [input_dim] + hidden_dims + [output_dim]
        self.layers: list[GCNLayer] = []
        for i in range(len(dims) - 1):
            use_bias = True
            seed = random_seed + i if random_seed else None
            self.layers.append(GCNLayer(dims[i], dims[i + 1], use_bias=use_bias, random_seed=seed))

        self._cache: dict = {}

    def forward(self, X: np.ndarray, A: np.ndarray) -> np.ndarray:
        """Forward pass.

        Args:
            X: Node features of shape (N, input_dim).
            A: Raw adjacency matrix of shape (N, N).

        Returns:
            Class logits of shape (N, output_dim).
        """
        A_norm = normalize_adjacency(A)
        h = X
        h_list = [h]

        for i, layer in enumerate(self.layers):
            h = layer.forward(h, A_norm)
            if i < len(self.layers) - 1:
                h = np.maximum(0, h)  # ReLU
            h_list.append(h.copy())

        self._cache = {"h_list": h_list, "A_norm": A_norm}
        return h

    def _softmax(self, x: np.ndarray) -> np.ndarray:
        """Softmax over last dimension."""
        shifted = x - np.max(x, axis=-1, keepdims=True)
        exps = np.exp(np.clip(shifted, -500, 500))
        return exps / np.sum(exps, axis=-1, keepdims=True)

    def cross_entropy_loss(self, logits: np.ndarray, y: np.ndarray,
                           mask: Optional[np.ndarray] = None) -> tuple[float, np.ndarray]:
        """Cross-entropy loss for node classification.

        Args:
            logits: Shape (N, num_classes).
            y: Shape (N,) with class indices.
            mask: Optional boolean mask of shape (N,) for labeled nodes.

        Returns:
            Tuple of (loss, dlogits).
        """
        if mask is None:
            mask = np.ones(len(y), dtype=bool)
        mask = mask.astype(bool)

        probs = self._softmax(logits)
        N = mask.sum()
        eps = 1e-12
        loss = -np.sum(np.log(probs[mask, y[mask]] + eps)) / max(N, 1)

        dlogits = probs.copy()
        dlogits[mask, y[mask]] -= 1.0
        dlogits /= max(N, 1)
        dlogits[~mask] = 0.0  # Zero gradients for unlabeled nodes

        return float(loss), dlogits

    def backward(self, dlogits: np.ndarray) -> dict:
        """Backward pass.

        Args:
            dlogits: Gradient w.r.t. logits, shape (N, num_classes).

        Returns:
            Dict of gradients per layer.
        """
        cache = self._cache
        grads = {}
        dh = dlogits

        for i in reversed(range(len(self.layers))):
            if i < len(self.layers) - 1:
                # ReLU backward
                dh = dh * (cache["h_list"][i + 1] > 0).astype(float)

            dX, dW, db = self.layers[i].backward(dh)
            grads[f"dW_{i}"] = dW
            grads[f"db_{i}"] = db
            dh = dX

        return grads

    def train_step(self, X: np.ndarray, A: np.ndarray, y: np.ndarray,
                   lr: float, mask: Optional[np.ndarray] = None) -> float:
        """One training step.

        Args:
            X: Node features.
            A: Adjacency matrix.
            y: Node labels.
            lr: Learning rate.
            mask: Train node mask.

        Returns:
            Cross-entropy loss.
        """
        logits = self.forward(X, A)
        loss, dlogits = self.cross_entropy_loss(logits, y, mask)
        grads = self.backward(dlogits)

        for i in range(len(self.layers)):
            self.layers[i].W -= lr * grads[f"dW_{i}"]
            if self.layers[i].b is not None:
                self.layers[i].b -= lr * grads[f"db_{i}"]

        return loss

    def predict(self, X: np.ndarray, A: np.ndarray) -> np.ndarray:
        """Predict node classes.

        Args:
            X: Node features.
            A: Adjacency matrix.

        Returns:
            Class predictions of shape (N,).
        """
        logits = self.forward(X, A)
        return np.argmax(logits, axis=-1)


def generate_cora_like_data(
    n_nodes: int = 100,
    n_features: int = 20,
    n_classes: int = 3,
    random_seed: int = 42,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Generate synthetic citation-network-like graph data.

    Args:
        n_nodes: Number of nodes.
        n_features: Number of features per node.
        n_classes: Number of classes.
        random_seed: Random seed.

    Returns:
        Tuple of (X, A, y, train_mask, val_mask).
    """
    rng = np.random.RandomState(random_seed)

    # Node features: clusters by class
    X = np.zeros((n_nodes, n_features))
    y = rng.randint(0, n_classes, n_nodes)
    for c in range(n_classes):
        idx = y == c
        n_c = idx.sum()
        X[idx] = rng.randn(n_c, n_features) + c * 3.0

    # Adjacency: nodes are more likely to connect to same-class nodes
    A = np.zeros((n_nodes, n_nodes))
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            if y[i] == y[j]:
                prob = 0.05
            else:
                prob = 0.01
            if rng.rand() < prob:
                A[i, j] = 1.0
                A[j, i] = 1.0

    # Train/val split (semi-supervised)
    n_train = n_nodes // 5
    indices = rng.permutation(n_nodes)
    train_mask = np.zeros(n_nodes, dtype=bool)
    train_mask[indices[:n_train]] = True
    val_mask = np.ones(n_nodes, dtype=bool)

    return X, A, y, train_mask, val_mask


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing GCN...")

    np.random.seed(42)

    # Generate data
    X, A, y, train_mask, val_mask = generate_cora_like_data(
        n_nodes=100, n_features=10, n_classes=3, random_seed=42
    )
    print(f"  Data: {X.shape[0]} nodes, {X.shape[1]} features, {y.max()+1} classes")
    print(f"  Train nodes: {train_mask.sum()}")

    # Test 1: Adjacency normalization
    A_norm = normalize_adjacency(A)
    assert A_norm.shape == (100, 100)
    # Row sums of A_norm should not be 1 (since it's D^(-1/2) A_hat D^(-1/2))
    assert np.all(np.isfinite(A_norm)), "A_norm contains NaN/Inf"
    print("  PASS: Adjacency normalization produced finite values")

    # Test 2: GCNLayer forward
    layer = GCNLayer(input_dim=10, output_dim=8, random_seed=42)
    out = layer.forward(X, A_norm)
    assert out.shape == (100, 8), f"Wrong output shape: {out.shape}"
    print(f"  PASS: GCNLayer output shape: {out.shape}")

    # Test 3: GCN forward
    gcn = GCN(input_dim=10, hidden_dims=[16], output_dim=3, random_seed=42)
    logits = gcn.forward(X, A)
    assert logits.shape == (100, 3), f"Wrong logits shape: {logits.shape}"
    print(f"  PASS: GCN logits shape: {logits.shape}")

    # Test 4: Loss computation
    loss, dlogits = gcn.cross_entropy_loss(logits, y, train_mask)
    assert loss > 0 and np.isfinite(loss), f"Invalid loss: {loss}"
    print(f"  PASS: Cross-entropy loss: {loss:.4f}")

    # Test 5: Training reduces loss
    gcn2 = GCN(input_dim=10, hidden_dims=[16], output_dim=3, random_seed=123)
    initial_loss = gcn2.train_step(X, A, y, lr=0.01, mask=train_mask)

    losses = []
    for _ in range(500):
        loss_val = gcn2.train_step(X, A, y, lr=0.1, mask=train_mask)
        losses.append(loss_val)

    assert losses[-1] < initial_loss, f"Loss did not decrease: {initial_loss:.4f} → {losses[-1]:.4f}"
    print(f"  PASS: Training reduced loss: {initial_loss:.4f} → {losses[-1]:.4f}")

    # Test 6: Predictions
    preds = gcn2.predict(X, A)
    assert preds.shape == (100,)
    train_acc = np.mean(preds[train_mask] == y[train_mask])
    print(f"  PASS: Train accuracy: {train_acc:.3f}")

    # Test 7: Gradient check for GCNLayer
    layer_grad = GCNLayer(input_dim=4, output_dim=2, random_seed=99)
    X_small = np.random.randn(5, 4)
    A_small = np.array([
        [1, 1, 0, 0, 0],
        [1, 1, 1, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 1, 1],
        [0, 0, 0, 1, 1],
    ], dtype=float)
    A_small_norm = normalize_adjacency(A_small)

    out_small = layer_grad.forward(X_small, A_small_norm)
    dout = np.random.randn(*out_small.shape)
    _, dW, _ = layer_grad.backward(dout)

    eps = 1e-5
    num_dW = np.zeros_like(layer_grad.W)
    for i in range(layer_grad.W.size):
        idx = np.unravel_index(i, layer_grad.W.shape)
        orig = layer_grad.W[idx]
        layer_grad.W[idx] = orig + eps
        yp = layer_grad.forward(X_small, A_small_norm)
        lp = np.sum(yp * dout)
        layer_grad.W[idx] = orig - eps
        ym = layer_grad.forward(X_small, A_small_norm)
        lm = np.sum(ym * dout)
        layer_grad.W[idx] = orig
        num_dW[idx] = (lp - lm) / (2 * eps)

    max_err = np.max(np.abs(dW - num_dW)) / (np.max(np.abs(num_dW)) + 1e-10)
    assert max_err < 1e-4, f"GCN gradient check failed: {max_err:.2e}"
    print(f"  PASS: GCN gradient check, max rel error = {max_err:.2e}")

    print("\nAll GCN tests passed!")
