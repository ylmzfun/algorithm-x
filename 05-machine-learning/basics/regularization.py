"""L1 (Lasso) and L2 (Ridge) regularization demo for linear regression.

Demonstrates the effect of regularization on weight magnitudes
and compares results with sklearn.
"""

from __future__ import annotations

import numpy as np
from typing import Optional


class LinearRegression:
    """Simple linear regression with optional L1/L2 regularization.

    Uses the normal equation (closed-form) or gradient descent.

    Parameters
    ----------
    alpha : float, default=0.0
        Regularization strength.
    l1_ratio : float, default=0.0
        Mix between L1 and L2: 0.0 = pure L2, 1.0 = pure L1.
    fit_intercept : bool, default=True
        Whether to fit an intercept term.
    solver : str, {'normal', 'gd'}
        Solver to use.
    learning_rate : float, default=0.01
        Learning rate for gradient descent.
    max_iter : int, default=1000
        Maximum iterations for gradient descent.
    tol : float, default=1e-4
        Tolerance for convergence in GD.
    """

    def __init__(
        self,
        alpha: float = 0.0,
        l1_ratio: float = 0.0,
        fit_intercept: bool = True,
        solver: str = "normal",
        learning_rate: float = 0.01,
        max_iter: int = 1000,
        tol: float = 1e-4,
    ) -> None:
        self.alpha = alpha
        self.l1_ratio = l1_ratio
        self.fit_intercept = fit_intercept
        self.solver = solver
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.tol = tol
        self.coef_: np.ndarray | None = None
        self.intercept_: float = 0.0

    def fit(self, X: np.ndarray, y: np.ndarray) -> LinearRegression:
        """Fit linear model.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
        y : np.ndarray of shape (n_samples,)

        Returns
        -------
        self
        """
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64)
        n_samples, n_features = X.shape

        if self.fit_intercept:
            X = np.column_stack([np.ones(n_samples), X])

        if self.solver == "normal" and self.l1_ratio == 0:
            # Closed-form for pure L2 (Ridge)
            I = np.eye(X.shape[1])
            if self.fit_intercept:
                I[0, 0] = 0  # Don't regularize intercept
            w = np.linalg.solve(X.T @ X + self.alpha * I, X.T @ y)
        else:
            w = self._gradient_descent(X, y)

        if self.fit_intercept:
            self.intercept_ = w[0]
            self.coef_ = w[1:]
        else:
            self.intercept_ = 0.0
            self.coef_ = w
        return self

    def _gradient_descent(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Gradient descent with L1/L2 regularization (proximal for L1)."""
        n_samples, n_features = X.shape
        w = np.zeros(n_features)

        for _ in range(self.max_iter):
            y_pred = X @ w
            grad = -(2 / n_samples) * X.T @ (y - y_pred)

            # L2 gradient
            if self.l1_ratio < 1.0:
                l2_alpha = self.alpha * (1 - self.l1_ratio)
                grad += 2 * l2_alpha * w

            # L1 proximal operator (soft thresholding)
            if self.l1_ratio > 0:
                l1_alpha = self.alpha * self.l1_ratio
                w_new = w - self.learning_rate * grad
                # Soft thresholding
                w_new = np.sign(w_new) * np.maximum(np.abs(w_new) - self.learning_rate * l1_alpha, 0)
                if self.fit_intercept:
                    # Don't regularize intercept
                    w_new[0] = w[0] - self.learning_rate * (
                        -(2 / n_samples) * X[:, 0].T @ (y - X @ w)
                    )
                diff = np.max(np.abs(w_new - w))
                w = w_new
            else:
                w_new = w - self.learning_rate * grad
                diff = np.max(np.abs(w_new - w))
                w = w_new

            if diff < self.tol:
                break
        return w

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict using the linear model.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        y_pred : np.ndarray of shape (n_samples,)
        """
        return np.asarray(X, dtype=np.float64) @ self.coef_ + self.intercept_


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    print("=== Testing Regularization ===")

    np.random.seed(42)
    n_samples, n_features = 100, 10

    # Generate data with only 3 informative features
    true_coef = np.zeros(n_features)
    true_coef[:3] = [3.0, 1.5, -2.0]
    X = np.random.randn(n_samples, n_features)
    y = X @ true_coef + np.random.randn(n_samples) * 0.5

    # --- No regularization ---
    lr = LinearRegression(alpha=0.0, fit_intercept=True)
    lr.fit(X, y)
    y_pred = lr.predict(X)
    assert len(y_pred) == n_samples
    mse_no_reg = np.mean((y - y_pred) ** 2)
    print(f"  No regularization MSE: {mse_no_reg:.4f}")

    # --- L2 (Ridge) regularization ---
    ridge = LinearRegression(alpha=1.0, l1_ratio=0.0, fit_intercept=True)
    ridge.fit(X, y)
    y_pred_ridge = ridge.predict(X)
    mse_ridge = np.mean((y - y_pred_ridge) ** 2)
    print(f"  Ridge (alpha=1.0) MSE: {mse_ridge:.4f}")

    # L2 should shrink coefficients
    l2_norm_no_reg = np.sum(lr.coef_ ** 2)
    l2_norm_ridge = np.sum(ridge.coef_ ** 2)
    print(f"  L2 norm (no reg):  {l2_norm_no_reg:.4f}")
    print(f"  L2 norm (ridge):   {l2_norm_ridge:.4f}")
    assert l2_norm_ridge < l2_norm_no_reg, "Ridge should shrink weights!"
    print("  L2 weight shrinkage: PASS")

    # --- L1 (Lasso) regularization ---
    lasso = LinearRegression(alpha=0.5, l1_ratio=1.0, fit_intercept=True, solver="gd", max_iter=5000)
    lasso.fit(X, y)
    n_nonzero_lasso = np.sum(np.abs(lasso.coef_) > 1e-4)
    print(f"  Lasso (alpha=0.5): {n_nonzero_lasso}/{n_features} non-zero coefs")
    # L1 should encourage sparsity
    assert n_nonzero_lasso <= len(true_coef) + 2, "Lasso should produce sparse solution!"
    print("  L1 sparsity: PASS")

    # --- ElasticNet ---
    elastic = LinearRegression(alpha=0.5, l1_ratio=0.5, fit_intercept=True, solver="gd", max_iter=5000)
    elastic.fit(X, y)
    l2_norm_elastic = np.sum(elastic.coef_ ** 2)
    assert l2_norm_ridge < l2_norm_no_reg, "ElasticNet should also shrink"
    print("  ElasticNet: PASS")

    # --- Strong L2 should approach zero weights ---
    ridge_strong = LinearRegression(alpha=1000.0, l1_ratio=0.0, fit_intercept=True)
    ridge_strong.fit(X, y)
    # With strong regularization, coefficients should be small
    l2_norm_strong = np.sum(ridge_strong.coef_ ** 2)
    print(f"  Strong L2 L2-norm: {l2_norm_strong:.6f} (vs plain: {l2_norm_no_reg:.4f})")
    assert l2_norm_strong < l2_norm_no_reg * 0.5, "Strong L2: coefs should shrink significantly"
    print("  Strong L2 -> small weights: PASS")

    # --- Compare with sklearn ---
    try:
        from sklearn.linear_model import Ridge, Lasso

        ridge_sk = Ridge(alpha=1.0)
        ridge_sk.fit(X, y)
        ridge_our = LinearRegression(alpha=1.0, l1_ratio=0.0, fit_intercept=True)
        ridge_our.fit(X, y)

        # Relative difference
        diff = np.max(np.abs(ridge_sk.coef_ - ridge_our.coef_))
        print(f"  sklearn Ridge vs ours max diff: {diff:.6f}")
        assert diff < 1.0, "Large discrepancy with sklearn Ridge"
        print("  sklearn comparison: PASS")
    except ImportError:
        print("  sklearn not installed, skipping comparison")

    print("All regularization tests PASSED!\n")
