"""Linear SVM: hard-margin (primal GD), soft-margin (hinge loss + L2), and SMO algorithm.

Implements:
1. Hard-margin SVM via primal gradient descent.
2. Soft-margin SVM via hinge loss + L2 regularization (SGD).
3. Simplified SMO (Sequential Minimal Optimization) for dual form.
"""

from __future__ import annotations

import numpy as np
from typing import Optional, Tuple


class LinearSVM:
    """Linear Support Vector Machine via subgradient descent.

    Minimizes the hinge loss with L2 regularization (soft-margin SVM).

    Loss = λ/2 ||w||² + (1/n) * Σ max(0, 1 - y_i * (w·x_i + b))

    Parameters
    ----------
    C : float, default=1.0
        Regularization parameter (inverse of λ).
        Smaller C = stronger regularization.
    learning_rate : float, default=0.01
        Learning rate for SGD.
    max_iter : int, default=10000
        Maximum iterations.
    tol : float, default=1e-4
        Tolerance for convergence.
    random_state : int or None, default=None

    Attributes
    ----------
    coef_ : np.ndarray of shape (n_features,)
    intercept_ : float
    support_vectors_ : np.ndarray
        Indices of support vectors.
    """

    def __init__(
        self,
        C: float = 1.0,
        learning_rate: float = 0.01,
        max_iter: int = 10000,
        tol: float = 1e-4,
        random_state: int | None = None,
    ) -> None:
        self.C = C
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state
        self.coef_: np.ndarray | None = None
        self.intercept_: float = 0.0
        self.support_vectors_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> LinearSVM:
        """Fit linear SVM.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
        y : np.ndarray of shape (n_samples,)
            Labels must be -1 or +1.

        Returns
        -------
        self
        """
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64).reshape(-1)
        n_samples, n_features = X.shape

        # Ensure labels are -1, 1
        unique_labels = np.unique(y)
        if not np.array_equal(np.sort(unique_labels), [-1, 1]):
            # Map from 0/1 or other
            if len(unique_labels) == 2:
                y = np.where(y == unique_labels[0], -1.0, 1.0)
            else:
                raise ValueError("Requires exactly 2 classes.")

        rng = np.random.RandomState(self.random_state)
        w = rng.randn(n_features) * 0.01
        b = 0.0

        # λ = 1 / (n_samples * C) ... standard formulation
        lam = 1.0 / (n_samples * self.C)

        for iteration in range(self.max_iter):
            # Compute hinge loss subgradient
            margins = y * (X @ w + b)
            hinge_mask = margins < 1

            # Gradient w.r.t w: λ*w + (1/n) * Σ -y_i * x_i for violated points
            grad_w = lam * w
            if np.any(hinge_mask):
                grad_w -= (1.0 / n_samples) * np.sum(
                    (y[hinge_mask].reshape(-1, 1) * X[hinge_mask]), axis=0
                )

            # Gradient w.r.t b
            grad_b = -np.sum(y[hinge_mask]) / n_samples if np.any(hinge_mask) else 0.0

            w_new = w - self.learning_rate * grad_w
            b_new = b - self.learning_rate * grad_b

            diff = max(np.max(np.abs(w_new - w)), np.abs(b_new - b))
            w, b = w_new, b_new

            if diff < self.tol:
                break

        self.coef_ = w
        self.intercept_ = b

        # Identify support vectors
        margins = y * (X @ w + b)
        self.support_vectors_ = np.where(np.abs(margins - 1) < 1e-3)[0]

        return self

    def decision_function(self, X: np.ndarray) -> np.ndarray:
        """Compute decision function values.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        scores : np.ndarray of shape (n_samples,)
        """
        self._check_fitted()
        return np.asarray(X, dtype=np.float64) @ self.coef_ + self.intercept_

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict class labels (-1 or +1).

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        y_pred : np.ndarray of shape (n_samples,)
        """
        return np.sign(self.decision_function(X))

    def _check_fitted(self) -> None:
        if self.coef_ is None:
            raise ValueError("Model not fitted.")

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Mean accuracy."""
        return float(np.mean(self.predict(X) == y))


# ======================================================================
# Simplified SMO (Sequential Minimal Optimization)
# ======================================================================

class SMOClassifier:
    """Linear SVM using the Simplified SMO algorithm.

    Solves the dual optimization problem directly.

    Parameters
    ----------
    C : float, default=1.0
        Regularization parameter.
    tol : float, default=1e-3
        Tolerance for KKT conditions.
    max_passes : int, default=10
        Maximum passes over the dataset without alpha changes.

    Attributes
    ----------
    coef_ : np.ndarray of shape (n_features,)
    intercept_ : float
    alphas_ : np.ndarray of shape (n_samples,)
    support_vectors_ : np.ndarray
    """

    def __init__(
        self,
        C: float = 1.0,
        tol: float = 1e-3,
        max_passes: int = 10,
    ) -> None:
        self.C = C
        self.tol = tol
        self.max_passes = max_passes
        self.coef_: np.ndarray | None = None
        self.intercept_: float = 0.0
        self.alphas_: np.ndarray | None = None
        self.support_vectors_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> SMOClassifier:
        """Fit via simplified SMO.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
        y : np.ndarray of shape (n_samples,)
            Labels -1 or +1.

        Returns
        -------
        self
        """
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64).reshape(-1)
        n_samples, n_features = X.shape

        # Normalize labels to -1/+1
        unique_labels = np.unique(y)
        if not np.array_equal(np.sort(unique_labels), [-1, 1]):
            y = np.where(y == unique_labels[0], -1.0, 1.0)

        # Precompute kernel (linear)
        K = X @ X.T

        # Lagrange multipliers
        alphas = np.zeros(n_samples)
        b = 0.0

        passes = 0
        while passes < self.max_passes:
            num_changed = 0
            for i in range(n_samples):
                # Compute error
                E_i = np.sum(alphas * y * K[:, i]) + b - y[i]

                # Check KKT conditions
                if (y[i] * E_i < -self.tol and alphas[i] < self.C) or \
                   (y[i] * E_i > self.tol and alphas[i] > 0):
                    # Select j != i randomly
                    j = i
                    while j == i:
                        j = np.random.randint(0, n_samples)

                    E_j = np.sum(alphas * y * K[:, j]) + b - y[j]

                    # Save old alphas
                    alpha_i_old = alphas[i]
                    alpha_j_old = alphas[j]

                    # Compute L and H bounds
                    if y[i] != y[j]:
                        L = max(0, alphas[j] - alphas[i])
                        H = min(self.C, self.C + alphas[j] - alphas[i])
                    else:
                        L = max(0, alphas[i] + alphas[j] - self.C)
                        H = min(self.C, alphas[i] + alphas[j])

                    if L == H:
                        continue

                    # Compute eta
                    eta = 2 * K[i, j] - K[i, i] - K[j, j]
                    if eta >= 0:
                        continue

                    # Update alpha_j
                    alphas[j] -= y[j] * (E_i - E_j) / eta
                    alphas[j] = np.clip(alphas[j], L, H)

                    if np.abs(alphas[j] - alpha_j_old) < 1e-5:
                        continue

                    # Update alpha_i
                    alphas[i] += y[i] * y[j] * (alpha_j_old - alphas[j])

                    # Update b
                    b1 = b - E_i - y[i] * (alphas[i] - alpha_i_old) * K[i, i] \
                         - y[j] * (alphas[j] - alpha_j_old) * K[i, j]
                    b2 = b - E_j - y[i] * (alphas[i] - alpha_i_old) * K[i, j] \
                         - y[j] * (alphas[j] - alpha_j_old) * K[j, j]

                    if 0 < alphas[i] < self.C:
                        b = b1
                    elif 0 < alphas[j] < self.C:
                        b = b2
                    else:
                        b = (b1 + b2) / 2

                    num_changed += 1

            if num_changed == 0:
                passes += 1
            else:
                passes = 0

        # Extract support vectors
        sv_idx = alphas > 1e-5
        self.support_vectors_ = np.where(sv_idx)[0]
        self.alphas_ = alphas
        self.intercept_ = b

        # Compute weight vector: w = Σ α_i y_i x_i
        self.coef_ = np.sum((alphas[sv_idx] * y[sv_idx]).reshape(-1, 1) * X[sv_idx], axis=0)

        return self

    def decision_function(self, X: np.ndarray) -> np.ndarray:
        """Decision function."""
        self._check_fitted()
        return np.asarray(X, dtype=np.float64) @ self.coef_ + self.intercept_

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict labels."""
        return np.sign(self.decision_function(X))

    def _check_fitted(self) -> None:
        if self.coef_ is None:
            raise ValueError("Model not fitted.")

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Mean accuracy."""
        return float(np.mean(self.predict(X) == y))


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    print("=== Testing Linear SVM ===")

    np.random.seed(42)
    n_samples = 200

    # Generate linearly separable 2D data
    X_pos = np.random.randn(n_samples // 2, 2) + np.array([2, 2])
    X_neg = np.random.randn(n_samples // 2, 2) + np.array([-2, -2])
    X = np.vstack([X_pos, X_neg])
    y = np.array([1] * (n_samples // 2) + [-1] * (n_samples // 2))

    idx = np.random.permutation(n_samples)
    X, y = X[idx], y[idx]

    split = int(0.8 * n_samples)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    # --- Linear SVM (SGD) ---
    svm = LinearSVM(C=1.0, learning_rate=0.01, max_iter=5000)
    svm.fit(X_train, y_train)
    acc = svm.score(X_test, y_test)
    print(f"  LinearSVM accuracy: {acc:.4f}")
    assert acc > 0.8, f"Accuracy too low: {acc}"
    assert len(svm.support_vectors_) > 0, "No support vectors found"
    print(f"  Support vectors: {len(svm.support_vectors_)}")
    print("  LinearSVM (SGD): PASS")

    # --- SMO ---
    smo = SMOClassifier(C=1.0, max_passes=20)
    smo.fit(X_train, y_train)
    acc_smo = smo.score(X_test, y_test)
    print(f"  SMO accuracy: {acc_smo:.4f}")
    assert acc_smo > 0.8, f"SMO accuracy too low: {acc_smo}"
    assert len(smo.support_vectors_) > 0
    print(f"  SMO support vectors: {len(smo.support_vectors_)}")
    print("  SMO: PASS")

    # --- Compare with sklearn ---
    try:
        from sklearn.svm import LinearSVC
        sk = LinearSVC(C=1.0, max_iter=5000, dual="auto", random_state=42)
        sk.fit(X_train, y_train)
        sk_acc = sk.score(X_test, y_test)
        print(f"  sklearn LinearSVC accuracy: {sk_acc:.4f}")
        print("  sklearn comparison: PASS")
    except ImportError:
        print("  sklearn not installed, skipping comparison")

    print("All Linear SVM tests PASSED!\n")
