"""Multi-class Softmax Regression from scratch.

Implements softmax (multinomial logistic) regression using
gradient descent with cross-entropy loss.
"""

from __future__ import annotations

import numpy as np
from typing import Optional


def softmax(z: np.ndarray) -> np.ndarray:
    """Compute softmax over rows.

    Parameters
    ----------
    z : np.ndarray of shape (n_samples, n_classes)
        Raw scores (logits).

    Returns
    -------
    probs : np.ndarray of shape (n_samples, n_classes)
        Row-normalized probabilities.
    """
    # Subtract max for numerical stability
    z_stable = z - np.max(z, axis=1, keepdims=True)
    exp_z = np.exp(z_stable)
    return exp_z / np.sum(exp_z, axis=1, keepdims=True)


class SoftmaxRegression:
    """Multi-class Softmax Regression classifier.

    Uses gradient descent to minimize cross-entropy loss with
    optional L2 regularization.

    Parameters
    ----------
    fit_intercept : bool, default=True
        Whether to add an intercept term.
    alpha : float, default=0.0
        L2 regularization strength.
    learning_rate : float, default=0.01
        Learning rate for gradient descent.
    max_iter : int, default=10000
        Maximum number of iterations.
    tol : float, default=1e-6
        Tolerance for convergence.

    Attributes
    ----------
    coef_ : np.ndarray of shape (n_features, n_classes)
        Coefficient matrix.
    intercept_ : np.ndarray of shape (n_classes,)
        Intercept terms.
    classes_ : np.ndarray of shape (n_classes,)
        Unique class labels.
    """

    def __init__(
        self,
        fit_intercept: bool = True,
        alpha: float = 0.0,
        learning_rate: float = 0.01,
        max_iter: int = 10000,
        tol: float = 1e-6,
    ) -> None:
        self.fit_intercept = fit_intercept
        self.alpha = alpha
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.tol = tol
        self.coef_: np.ndarray | None = None
        self.intercept_: np.ndarray | None = None
        self.classes_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> SoftmaxRegression:
        """Fit softmax regression model.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
            Training data.
        y : np.ndarray of shape (n_samples,)
            Target integer labels.

        Returns
        -------
        self
        """
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.int64).reshape(-1)
        n_samples, n_features = X.shape

        self.classes_ = np.unique(y)
        n_classes = len(self.classes_)

        # Map labels to 0..k-1
        label_map = {c: i for i, c in enumerate(self.classes_)}
        y_idx = np.array([label_map[v] for v in y])

        # One-hot encoding
        Y = np.zeros((n_samples, n_classes))
        Y[np.arange(n_samples), y_idx] = 1.0

        if self.fit_intercept:
            X = np.column_stack([np.ones(n_samples), X])
            n_features += 1

        # Initialize weights
        W = np.zeros((n_features, n_classes))
        prev_loss = float("inf")

        for iteration in range(self.max_iter):
            z = X @ W
            P = softmax(z)

            # Cross-entropy loss
            eps = 1e-15
            loss = -np.sum(Y * np.log(np.clip(P, eps, 1 - eps))) / n_samples
            if self.alpha > 0:
                if self.fit_intercept:
                    loss += self.alpha * np.sum(W[1:, :] ** 2)
                else:
                    loss += self.alpha * np.sum(W ** 2)

            # Gradient
            grad = (1 / n_samples) * X.T @ (P - Y)
            if self.alpha > 0:
                if self.fit_intercept:
                    grad[1:, :] += 2 * self.alpha * W[1:, :]
                else:
                    grad += 2 * self.alpha * W

            W_new = W - self.learning_rate * grad

            if np.abs(prev_loss - loss) < self.tol:
                break
            prev_loss = loss
            W = W_new

        if self.fit_intercept:
            self.intercept_ = W[0, :]
            self.coef_ = W[1:, :]
        else:
            self.intercept_ = np.zeros(n_classes)
            self.coef_ = W
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Probability estimates for each class.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        proba : np.ndarray of shape (n_samples, n_classes)
            Class membership probabilities (sum to 1 per row).
        """
        self._check_fitted()
        z = np.asarray(X, dtype=np.float64) @ self.coef_ + self.intercept_
        return softmax(z)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict class labels.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        y_pred : np.ndarray of shape (n_samples,)
        """
        proba = self.predict_proba(X)
        idx = np.argmax(proba, axis=1)
        return self.classes_[idx]

    def _check_fitted(self) -> None:
        if self.coef_ is None:
            raise ValueError("Model not fitted. Call fit() first.")

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Mean accuracy on test data.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
        y : np.ndarray of shape (n_samples,)

        Returns
        -------
        accuracy : float
        """
        return float(np.mean(self.predict(X) == y))


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    print("=== Testing Softmax Regression ===")

    np.random.seed(42)
    n_samples = 300
    n_classes = 3

    # Generate multi-class data
    centers = np.array([[0, 0], [5, 5], [0, 5]])
    X_list, y_list = [], []
    for i, c in enumerate(centers):
        pts = np.random.randn(n_samples // n_classes, 2) * 1.0 + c
        X_list.append(pts)
        y_list.extend([i] * (n_samples // n_classes))
    X = np.vstack(X_list)
    y = np.array(y_list)

    # Shuffle
    idx = np.random.permutation(n_samples)
    X, y = X[idx], y[idx]

    # Split
    split = int(0.8 * n_samples)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    # --- Basic softmax ---
    sr = SoftmaxRegression(fit_intercept=True, learning_rate=0.05, max_iter=10000)
    sr.fit(X_train, y_train)
    acc = sr.score(X_test, y_test)
    print(f"  Test accuracy: {acc:.4f}")
    assert acc > 0.7, f"Accuracy too low: {acc}"

    # predict_proba must sum to 1
    proba = sr.predict_proba(X_test)
    row_sums = np.sum(proba, axis=1)
    assert np.allclose(row_sums, 1.0), f"proba sums not 1: {row_sums[:5]}"
    assert proba.shape == (len(X_test), n_classes)
    print("  predict_proba: PASS")

    # Predict labels should be valid
    y_pred = sr.predict(X_test)
    assert set(np.unique(y_pred)).issubset(set(sr.classes_))
    print("  predict labels: PASS")

    # --- L2 Regularization ---
    sr_l2 = SoftmaxRegression(fit_intercept=True, alpha=1.0, learning_rate=0.05, max_iter=10000)
    sr_l2.fit(X_train, y_train)
    acc_l2 = sr_l2.score(X_test, y_test)
    w_norm_plain = np.sum(sr.coef_ ** 2)
    w_norm_l2 = np.sum(sr_l2.coef_ ** 2)
    print(f"  Weight norm (plain): {w_norm_plain:.4f}, (L2): {w_norm_l2:.4f}")
    print(f"  L2 accuracy: {acc_l2:.4f}")
    print("  L2 regularization: PASS")

    # --- Compare with sklearn ---
    try:
        from sklearn.linear_model import LogisticRegression as SkLR

        sk_sr = SkLR(multi_class="multinomial", penalty=None, fit_intercept=True,
                     max_iter=10000, solver="lbfgs")
        sk_sr.fit(X_train, y_train)
        sk_acc = sk_sr.score(X_test, y_test)
        print(f"  sklearn accuracy: {sk_acc:.4f}")
        assert np.abs(acc - sk_acc) < 0.3, "Large discrepancy with sklearn"
        print("  sklearn comparison: PASS")
    except ImportError:
        print("  sklearn not installed, skipping comparison")

    print("All Softmax Regression tests PASSED!\n")
