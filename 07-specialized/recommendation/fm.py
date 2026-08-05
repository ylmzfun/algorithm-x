"""Factorization Machines from scratch using NumPy.

Factorization Machines model pairwise feature interactions using
factorized parameters, enabling efficient learning from sparse data.

y(x) = w0 + Σ w_i·x_i + Σ_{i<j} <v_i, v_j>·x_i·x_j

The interaction term can be computed in O(k·n) time using:
    0.5 * Σ_f ( (Σ_i v_{i,f}·x_i)² - Σ_i v_{i,f}²·x_i² )

Reference: Rendle, "Factorization Machines" (2010).
"""

from __future__ import annotations

import numpy as np
from typing import Optional


class FactorizationMachine:
    """Factorization Machine model.

    Attributes:
        n_features: Number of input features.
        k: Latent factor dimension.
        w0: Global bias.
        w: Linear weights [n_features].
        V: Factorized interaction matrix [n_features, k].
    """

    def __init__(self, n_features: int, k: int = 8, seed: int = 42) -> None:
        """Initialize the factorization machine.

        Args:
            n_features: Number of features.
            k: Latent factor dimension.
            seed: Random seed.
        """
        rng = np.random.default_rng(seed)
        self.n_features = n_features
        self.k = k

        self.w0: float = 0.0
        self.w: np.ndarray = np.zeros(n_features)
        self.V: np.ndarray = rng.normal(0, 0.01, (n_features, k))

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Compute predictions for a batch of samples.

        Args:
            X: Feature matrix [N, n_features].

        Returns:
            Predictions [N].
        """
        # Linear part
        linear = self.w0 + X @ self.w  # [N]

        # Interaction part (O(k·n) computation)
        # Σ_f ( (Σ_i v_{i,f} x_i)² - Σ_i v_{i,f}² x_i² )
        xv = X @ self.V  # [N, k] — Σ_i v_{i,f}·x_i
        xv2 = (X ** 2) @ (self.V ** 2)  # [N, k] — Σ_i v_{i,f}²·x_i²
        interaction = 0.5 * np.sum(xv ** 2 - xv2, axis=1)  # [N]

        return linear + interaction

    def predict_single(self, x: np.ndarray) -> float:
        """Predict for a single sample.

        Args:
            x: Feature vector [n_features].

        Returns:
            Scalar prediction.
        """
        return float(self.predict(x.reshape(1, -1))[0])


def train_fm(
    model: FactorizationMachine,
    X: np.ndarray,
    y: np.ndarray,
    lr: float = 0.01,
    reg_w: float = 0.01,
    reg_v: float = 0.01,
    epochs: int = 100,
) -> list[float]:
    """Train a factorization machine using SGD.

    Args:
        model: The FactorizationMachine model.
        X: Training features [N, n_features].
        y: Target values [N].
        lr: Learning rate.
        reg_w: Regularization for linear weights.
        reg_v: Regularization for factorized interactions.
        epochs: Number of epochs.

    Returns:
        List of MSE values per epoch.
    """
    n = X.shape[0]
    losses: list[float] = []

    for epoch in range(epochs):
        total_loss = 0.0
        # Shuffle
        perm = np.random.permutation(n)
        X_shuf = X[perm]
        y_shuf = y[perm]

        for i in range(n):
            x = X_shuf[i]
            target = y_shuf[i]

            # Forward
            xv = x @ model.V  # [k]
            xv2 = (x ** 2) @ (model.V ** 2)  # [k]

            linear = model.w0 + np.dot(x, model.w)
            interaction = 0.5 * np.sum(xv ** 2 - xv2)
            pred = linear + interaction

            error = pred - target
            total_loss += error ** 2

            # Gradients
            # w0
            grad_w0 = error
            model.w0 -= lr * grad_w0

            # w
            grad_w = error * x + reg_w * model.w
            model.w -= lr * grad_w

            # V
            for f in range(model.k):
                # d/dv_{i,f} = error * (x_i * Σ_j v_{j,f}·x_j - v_{i,f}·x_i²)
                grad_v = error * (x * xv[f] - model.V[:, f] * x ** 2) \
                    + reg_v * model.V[:, f]
                model.V[:, f] -= lr * grad_v

        epoch_loss = total_loss / n
        losses.append(epoch_loss)

    return losses


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Testing fm.py — Factorization Machines")
    print("=" * 60)

    np.random.seed(42)

    # Create synthetic regression data with feature interactions
    n_samples = 200
    n_features = 10

    X = np.random.randn(n_samples, n_features)
    # True relationship: linear + interaction between features 0-1 and 2-3
    true_w0 = 2.0
    true_w = np.random.randn(n_features) * 0.5
    true_interaction = 3.0 * X[:, 0] * X[:, 1] - 2.0 * X[:, 2] * X[:, 3]

    y = true_w0 + X @ true_w + true_interaction + np.random.randn(n_samples) * 0.2

    # Split
    split = int(0.8 * n_samples)
    X_train, y_train = X[:split], y[:split]
    X_test, y_test = X[split:], y[split:]

    print(f"\nData: {n_samples} samples, {n_features} features")
    print(f"  Train: {len(X_train)}, Test: {len(X_test)}")

    all_pass = True

    # Train FM
    print("\n--- Factorization Machine ---")
    fm = FactorizationMachine(n_features=n_features, k=4, seed=42)
    fm_losses = train_fm(fm, X_train, y_train, lr=0.005,
                          reg_w=0.001, reg_v=0.001, epochs=50)

    print(f"  FM initial loss: {fm_losses[0]:.4f}")
    print(f"  FM final loss:   {fm_losses[-1]:.4f}")
    fm_improved = fm_losses[-1] < fm_losses[0]
    print(f"  FM loss decreased: {fm_improved}")
    all_pass = all_pass and fm_improved

    # Compare with simple linear regression
    # Linear: closed-form solution
    X_aug = np.column_stack([np.ones(len(X_train)), X_train])
    w_linear = np.linalg.lstsq(X_aug, y_train, rcond=None)[0]
    linear_pred_train = X_aug @ w_linear
    linear_pred_test = np.column_stack([np.ones(len(X_test)), X_test]) @ w_linear

    linear_mse_train = float(np.mean((y_train - linear_pred_train) ** 2))
    linear_mse_test = float(np.mean((y_test - linear_pred_test) ** 2))

    fm_pred_test = fm.predict(X_test)
    fm_mse_test = float(np.mean((y_test - fm_pred_test) ** 2))

    print(f"\n  Test MSE — Linear: {linear_mse_test:.4f}")
    print(f"  Test MSE — FM:     {fm_mse_test:.4f}")

    # FM should be better because data has interactions
    fm_better = fm_mse_test < linear_mse_test
    print(f"  FM beats Linear: {fm_better}")
    all_pass = all_pass and fm_better

    # Test single prediction
    p = fm.predict_single(X_test[0])
    print(f"\n  Single prediction: {p:.4f}")
    all_pass = all_pass and np.isfinite(p)

    print(f"\n{'PASS' if all_pass else 'FAIL'}: fm.py")
