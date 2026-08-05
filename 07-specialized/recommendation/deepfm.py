"""Simplified DeepFM from scratch using NumPy.

DeepFM combines:
- FM component: captures low-order (1st + 2nd order) feature interactions
- DNN component: captures high-order feature interactions
- Shared input embeddings between FM and DNN

Reference: Guo et al., "DeepFM: A Factorization-Machine based Neural
Network for CTR Prediction" (2017).
"""

from __future__ import annotations

import numpy as np
from typing import Optional


# ---------------------------------------------------------------------------
# FM Component
# ---------------------------------------------------------------------------

class FMComponent:
    """Factorization Machine component with shared embeddings.

    Computes:
        y_fm = w0 + Σ w_i·x_i + 0.5·Σ_f [ (Σ_i v_{i,f}·x_i)² - Σ_i v_{i,f}²·x_i² ]

    Attributes:
        n_features: Number of input features.
        k: Embedding dimension.
        w0: Global bias.
        w: Linear weights.
        V: Embedding matrix (shared with DNN).
    """

    def __init__(self, n_features: int, k: int = 8, seed: int = 42) -> None:
        """Initialize FM component.

        Args:
            n_features: Number of features.
            k: Embedding dimension.
            seed: Random seed.
        """
        rng = np.random.default_rng(seed)
        self.n_features = n_features
        self.k = k
        self.w0: float = 0.0
        self.w: np.ndarray = np.zeros(n_features)
        self.V: np.ndarray = rng.normal(0, 0.01, (n_features, k))

    def forward(self, X: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """FM forward pass.

        Args:
            X: Input features [N, n_features].

        Returns:
            Tuple of (fm_output [N], embeddings_out [N, n_features * k]).
        """
        # Linear part
        linear = self.w0 + X @ self.w  # [N]

        # Interaction part
        xv = X @ self.V  # [N, k]
        xv2 = (X ** 2) @ (self.V ** 2)
        interaction = 0.5 * np.sum(xv ** 2 - xv2, axis=1)  # [N]

        fm_out = linear + interaction

        # Prepare embedding output for DNN
        # For each feature, output its embedding scaled by x_i
        emb_out = (X[:, :, np.newaxis] * self.V[np.newaxis, :, :]).reshape(
            X.shape[0], -1
        )  # [N, n_features * k]

        return fm_out, emb_out


# ---------------------------------------------------------------------------
# DNN Component
# ---------------------------------------------------------------------------

class DNNComponent:
    """Deep Neural Network component for high-order interactions.

    Simple feed-forward network with ReLU activations.

    Attributes:
        layers: List of (W, b) tuples.
    """

    def __init__(
        self,
        input_dim: int,
        hidden_dims: tuple[int, ...] = (64, 32),
        seed: int = 42,
    ) -> None:
        """Initialize the DNN component.

        Args:
            input_dim: Input dimension (n_features * k).
            hidden_dims: Hidden layer sizes.
            seed: Random seed.
        """
        rng = np.random.default_rng(seed)
        dims = [input_dim] + list(hidden_dims) + [1]
        self.layers: list[tuple[np.ndarray, np.ndarray]] = []

        for i in range(len(dims) - 1):
            fan_in = dims[i]
            fan_out = dims[i + 1]
            scale = np.sqrt(2.0 / fan_in)
            W = rng.normal(0, scale, (fan_in, fan_out))
            b = np.zeros(fan_out)
            self.layers.append((W, b))

    def forward(self, X: np.ndarray) -> np.ndarray:
        """DNN forward pass.

        Args:
            X: Input [N, input_dim].

        Returns:
            Output [N, 1].
        """
        out = X
        for i, (W, b) in enumerate(self.layers):
            out = out @ W + b
            if i < len(self.layers) - 1:
                out = np.maximum(0, out)  # ReLU
        return out.squeeze(-1)  # [N]


# ---------------------------------------------------------------------------
# DeepFM
# ---------------------------------------------------------------------------

class DeepFM:
    """DeepFM: FM + DNN with shared embeddings.

    y_deepfm = sigmoid(y_fm + y_dnn)

    Attributes:
        fm: FM component (with shared embeddings).
        dnn: DNN component.
    """

    def __init__(
        self,
        n_features: int,
        k: int = 8,
        hidden_dims: tuple[int, ...] = (64, 32),
        seed: int = 42,
    ) -> None:
        """Initialize DeepFM.

        Args:
            n_features: Number of input features.
            k: Embedding dimension.
            hidden_dims: Hidden layer sizes for DNN.
            seed: Random seed.
        """
        self.fm = FMComponent(n_features, k, seed=seed)
        self.dnn = DNNComponent(
            input_dim=n_features * k,
            hidden_dims=hidden_dims,
            seed=seed + 100,
        )

    def forward(self, X: np.ndarray) -> np.ndarray:
        """Forward pass.

        Args:
            X: Input features [N, n_features].

        Returns:
            Predicted probabilities after sigmoid [N].
        """
        fm_out, emb_out = self.fm.forward(X)  # [N], [N, n_features*k]
        dnn_out = self.dnn.forward(emb_out)     # [N]
        logits = fm_out + dnn_out               # [N]
        return _sigmoid(logits)

    def predict(self, X: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        """Binary predictions.

        Args:
            X: Input features [N, n_features].
            threshold: Classification threshold.

        Returns:
            Binary predictions [N].
        """
        return (self.forward(X) >= threshold).astype(np.int64)

    def get_all_params(self) -> np.ndarray:
        """Get all trainable parameters as a flat array."""
        parts = [
            np.array([self.fm.w0]),
            self.fm.w.ravel(),
            self.fm.V.ravel(),
        ]
        for W, b in self.dnn.layers:
            parts.append(W.ravel())
            parts.append(b.ravel())
        return np.concatenate(parts)

    def set_all_params(self, flat: np.ndarray) -> None:
        """Set all trainable parameters from a flat array."""
        sizes = [1, self.fm.w.size, self.fm.V.size]
        for W, b in self.dnn.layers:
            sizes.append(W.size)
            sizes.append(b.size)
        offsets = np.cumsum([0] + sizes)

        self.fm.w0 = float(flat[offsets[0]])
        self.fm.w.ravel()[:] = flat[offsets[1]:offsets[2]]
        self.fm.V.ravel()[:] = flat[offsets[2]:offsets[3]]

        offset = offsets[3]
        for i, (W, b) in enumerate(self.dnn.layers):
            W.ravel()[:] = flat[offset:offset + W.size]
            offset += W.size
            b.ravel()[:] = flat[offset:offset + b.size]
            offset += b.size


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -50, 50)))


def binary_cross_entropy(y_pred: np.ndarray, y_true: np.ndarray) -> float:
    """Binary cross-entropy loss.

    Args:
        y_pred: Predicted probabilities [N].
        y_true: True labels [N].

    Returns:
        Average BCE loss.
    """
    eps = 1e-12
    return float(-np.mean(
        y_true * np.log(y_pred + eps) + (1 - y_true) * np.log(1 - y_pred + eps)
    ))


def train_deepfm(
    model: DeepFM,
    X: np.ndarray,
    y: np.ndarray,
    epochs: int = 50,
    lr: float = 0.01,
) -> list[float]:
    """Train DeepFM model using SGD with finite-difference gradients.

    Args:
        model: DeepFM model.
        X: Training features [N, n_features].
        y: Labels [N].
        epochs: Number of epochs.
        lr: Learning rate.

    Returns:
        List of BCE losses per epoch.
    """
    n = X.shape[0]
    losses: list[float] = []

    for epoch in range(epochs):
        y_pred = model.forward(X)
        loss = binary_cross_entropy(y_pred, y)
        losses.append(loss)

        # SGD via finite differences on a subset of params
        eps_fd = 1e-4
        params = model.get_all_params()
        grad = np.zeros_like(params)
        subset = np.random.choice(len(params), min(30, len(params)), replace=False)

        for idx in subset:
            orig = params[idx]
            params[idx] = orig + eps_fd
            model.set_all_params(params)
            l_plus = binary_cross_entropy(model.forward(X), y)

            params[idx] = orig - eps_fd
            model.set_all_params(params)
            l_minus = binary_cross_entropy(model.forward(X), y)

            params[idx] = orig
            grad[idx] = (l_plus - l_minus) / (2 * eps_fd)

        params = params - lr * grad
        model.set_all_params(params)

    return losses


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Testing deepfm.py — DeepFM")
    print("=" * 60)

    np.random.seed(42)

    # Create synthetic binary classification data with feature interactions
    n_samples = 300
    n_features = 10

    X = np.random.randn(n_samples, n_features)
    # True relationship with interactions
    logit = (
        0.5 * X[:, 0]
        + 0.5 * X[:, 1]
        + 2.0 * X[:, 0] * X[:, 1]  # interaction
        - 1.5 * X[:, 2] * X[:, 3]  # interaction
        + 0.3 * X[:, 4]
    )
    prob = _sigmoid(logit)
    y = (np.random.random(n_samples) < prob).astype(np.float64)

    split = int(0.8 * n_samples)
    X_train, y_train = X[:split], y[:split]
    X_test, y_test = X[split:], y[split:]

    print(f"\nData: {n_samples} samples, {n_features} features")
    print(f"  Positive ratio: {np.mean(y):.2%}")

    all_pass = True

    # Train DeepFM
    print("\n--- DeepFM Training ---")
    model = DeepFM(n_features=n_features, k=4, hidden_dims=(32, 16), seed=42)
    losses = train_deepfm(model, X_train, y_train, epochs=30, lr=0.03)

    print(f"  Initial loss: {losses[0]:.4f}")
    print(f"  Final loss:   {losses[-1]:.4f}")
    loss_decreased = losses[-1] < losses[0]
    print(f"  Loss decreased: {loss_decreased}")
    all_pass = all_pass and loss_decreased

    # Evaluate on test set
    y_pred_prob = model.forward(X_test)
    y_pred = (y_pred_prob >= 0.5).astype(np.int64)
    accuracy = np.mean(y_pred == y_test)
    print(f"\n  Test Accuracy: {accuracy:.2%}")

    # Should beat random baseline
    baseline = max(np.mean(y_test), 1 - np.mean(y_test))
    print(f"  Baseline (most common): {baseline:.2%}")
    acc_ok = accuracy > baseline
    print(f"  Beats baseline: {acc_ok}")
    all_pass = all_pass and acc_ok

    # Test FM and DNN components separately
    fm_out, emb_out = model.fm.forward(X_test[:5])
    dnn_out = model.dnn.forward(emb_out)
    print(f"\n  FM output shape: {fm_out.shape} (expected (5,))")
    print(f"  DNN output shape: {dnn_out.shape} (expected (5,))")
    all_pass = all_pass and fm_out.shape == (5,)
    all_pass = all_pass and dnn_out.shape == (5,)

    print(f"\n{'PASS' if all_pass else 'FAIL'}: deepfm.py")
