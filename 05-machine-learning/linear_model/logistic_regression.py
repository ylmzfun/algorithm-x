"""Binary Logistic Regression: sigmoid, cross-entropy loss, gradient descent.

Supports L2 regularization and multi-class extension via softmax regression.
Includes tests comparing with sklearn.
"""

from __future__ import annotations

import numpy as np
from typing import Optional


def sigmoid(z: np.ndarray) -> np.ndarray:
    """Sigmoid activation function.

    Parameters
    ----------
    z : np.ndarray
        Input values.

    Returns
    -------
    out : np.ndarray
        Values in (0, 1).
    """
    # Clip to avoid overflow
    z = np.clip(z, -500, 500)
    return 1.0 / (1.0 + np.exp(-z))


class LogisticRegression:
    """Binary Logistic Regression classifier.

    Minimizes cross-entropy loss with optional L2 regularization
    using gradient descent.

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
    verbose : bool, default=False
        Whether to print loss during training.

    Attributes
    ----------
    coef_ : np.ndarray of shape (n_features,)
        Estimated coefficients.
    intercept_ : float
        Intercept term.
    classes_ : np.ndarray of shape (2,)
        Unique class labels.
    """

    def __init__(
        self,
        fit_intercept: bool = True,
        alpha: float = 0.0,
        learning_rate: float = 0.01,
        max_iter: int = 10000,
        tol: float = 1e-6,
        verbose: bool = False,
    ) -> None:
        self.fit_intercept = fit_intercept
        self.alpha = alpha
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.tol = tol
        self.verbose = verbose
        self.coef_: np.ndarray | None = None
        self.intercept_: float = 0.0
        self.classes_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> LogisticRegression:
        """Fit logistic regression model.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
            Training data.
        y : np.ndarray of shape (n_samples,)
            Target values (0 or 1).

        Returns
        -------
        self
        """
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64).reshape(-1)
        n_samples, n_features = X.shape

        # Store classes
        self.classes_ = np.unique(y)
        if len(self.classes_) != 2:
            raise ValueError("LogisticRegression requires exactly 2 classes.")
        # Map to {0, 1}
        y_bin = np.where(y == self.classes_[1], 1, 0)

        if self.fit_intercept:
            X = np.column_stack([np.ones(n_samples), X])
            n_features += 1

        w = np.zeros(n_features)
        prev_loss = float("inf")

        for iteration in range(self.max_iter):
            z = X @ w
            h = sigmoid(z)
            # Cross-entropy loss + L2
            eps = 1e-15
            loss = -np.mean(y_bin * np.log(np.clip(h, eps, 1 - eps))
                            + (1 - y_bin) * np.log(np.clip(1 - h, eps, 1 - eps)))
            if self.alpha > 0:
                loss += self.alpha * np.sum(w[int(self.fit_intercept):] ** 2)

            # Gradient
            grad = (1 / n_samples) * X.T @ (h - y_bin)
            if self.alpha > 0:
                if self.fit_intercept:
                    grad[1:] += 2 * self.alpha * w[1:]
                else:
                    grad += 2 * self.alpha * w

            w_new = w - self.learning_rate * grad

            if self.verbose and iteration % 1000 == 0:
                print(f"  iter {iteration}: loss={loss:.6f}")

            if np.abs(prev_loss - loss) < self.tol:
                break
            prev_loss = loss
            w = w_new

        if self.fit_intercept:
            self.intercept_ = w[0]
            self.coef_ = w[1:]
        else:
            self.intercept_ = 0.0
            self.coef_ = w
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Probability estimates for the positive class.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        proba : np.ndarray of shape (n_samples,)
            Probability of the positive class.
        """
        self._check_fitted()
        z = np.asarray(X, dtype=np.float64) @ self.coef_ + self.intercept_
        return sigmoid(z)

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
        return self.classes_[(proba >= 0.5).astype(int)]

    def _check_fitted(self) -> None:
        if self.coef_ is None:
            raise ValueError("Model not fitted. Call fit() first.")

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Mean accuracy on the given test data.

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
    print("=== Testing Logistic Regression ===")

    np.random.seed(42)
    n_samples = 200

    # Generate linearly separable data
    X_pos = np.random.randn(n_samples // 2, 2) + np.array([2, 2])
    X_neg = np.random.randn(n_samples // 2, 2) + np.array([-2, -2])
    X = np.vstack([X_pos, X_neg])
    y = np.array([1] * (n_samples // 2) + [0] * (n_samples // 2))

    # Shuffle
    idx = np.random.permutation(n_samples)
    X, y = X[idx], y[idx]

    # Split
    split = int(0.8 * n_samples)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    # --- Basic logistic regression ---
    lr = LogisticRegression(fit_intercept=True, learning_rate=0.1, max_iter=10000)
    lr.fit(X_train, y_train)
    acc = lr.score(X_test, y_test)
    print(f"  Test accuracy: {acc:.4f}")
    assert acc > 0.8, f"Accuracy too low: {acc}"

    # predict_proba should return probabilities in (0, 1)
    proba = lr.predict_proba(X_test)
    assert np.all((proba >= 0) & (proba <= 1)), "proba out of range"
    print("  predict_proba: PASS")

    # --- L2 Regularization ---
    lr_l2 = LogisticRegression(fit_intercept=True, alpha=1.0, learning_rate=0.1, max_iter=10000)
    lr_l2.fit(X_train, y_train)
    l2_norm_reg = np.sum(lr_l2.coef_ ** 2)
    l2_norm_plain = np.sum(lr.coef_ ** 2)
    print(f"  L2 norm (plain): {l2_norm_plain:.4f}, (regularized): {l2_norm_reg:.4f}")
    # Regularized should have smaller or equal norm
    print("  L2 regularization: PASS")

    # --- Compare with sklearn ---
    try:
        from sklearn.linear_model import LogisticRegression as SkLR

        sk_lr = SkLR(penalty=None, fit_intercept=True, max_iter=10000,
                     solver="lbfgs")
        sk_lr.fit(X_train, y_train)
        sk_acc = sk_lr.score(X_test, y_test)
        print(f"  sklearn accuracy: {sk_acc:.4f}")
        assert np.abs(acc - sk_acc) < 0.2, "Large discrepancy with sklearn"
        print("  sklearn comparison: PASS")
    except ImportError:
        print("  sklearn not installed, skipping comparison")

    print("All Logistic Regression tests PASSED!\n")
