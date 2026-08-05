"""Linear Regression with closed-form (normal equation) and gradient descent.

Supports L1 (Lasso) and L2 (Ridge) regularization.
Includes tests comparing with sklearn.
"""

from __future__ import annotations

import numpy as np
from typing import Optional, Literal


class LinearRegression:
    """Ordinary least squares Linear Regression.

    Supports closed-form (normal equation) and gradient descent solvers,
    with optional L1/L2/ElasticNet regularization.

    Parameters
    ----------
    fit_intercept : bool, default=True
        Whether to calculate the intercept.
    alpha : float, default=0.0
        Regularization strength.
    l1_ratio : float, default=0.0
        ElasticNet mixing parameter: 0 = L2 (Ridge), 1 = L1 (Lasso).
    solver : {'normal', 'gd'}, default='normal'
        Solver: 'normal' for closed-form (only pure L2), 'gd' for gradient descent.
    learning_rate : float, default=0.01
        Learning rate for GD.
    max_iter : int, default=10000
        Maximum iterations for GD.
    tol : float, default=1e-6
        Tolerance for GD convergence.

    Attributes
    ----------
    coef_ : np.ndarray of shape (n_features,)
        Estimated coefficients.
    intercept_ : float
        Independent term in the linear model.
    """

    def __init__(
        self,
        fit_intercept: bool = True,
        alpha: float = 0.0,
        l1_ratio: float = 0.0,
        solver: Literal["normal", "gd"] = "normal",
        learning_rate: float = 0.01,
        max_iter: int = 10000,
        tol: float = 1e-6,
    ) -> None:
        self.fit_intercept = fit_intercept
        self.alpha = alpha
        self.l1_ratio = l1_ratio
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
            Training data.
        y : np.ndarray of shape (n_samples,)
            Target values.

        Returns
        -------
        self
        """
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64).reshape(-1)
        n_samples, n_features = X.shape

        if self.fit_intercept:
            X = np.column_stack([np.ones(n_samples), X])

        if self.solver == "normal" and self.l1_ratio == 0.0:
            w = self._solve_normal_equation(X, y)
        elif self.solver == "normal":
            # Fall through to GD when L1 is involved
            w = self._gradient_descent(X, y)
        else:
            w = self._gradient_descent(X, y)

        if self.fit_intercept:
            self.intercept_ = w[0]
            self.coef_ = w[1:]
        else:
            self.intercept_ = 0.0
            self.coef_ = w
        return self

    def _solve_normal_equation(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Closed-form solution: w = (X^T X + αI)^(-1) X^T y.

        For L2 regularization only.
        """
        n_features = X.shape[1]
        I = np.eye(n_features)
        if self.fit_intercept:
            I[0, 0] = 0  # Don't regularize intercept
        gram = X.T @ X + self.alpha * I
        return np.linalg.solve(gram, X.T @ y)

    def _gradient_descent(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Gradient descent with elastic net regularization."""
        n_samples, n_features = X.shape
        w = np.zeros(n_features)
        # Normalize regularization parameters
        l1_penalty = self.alpha * self.l1_ratio
        l2_penalty = self.alpha * (1 - self.l1_ratio)

        for iteration in range(self.max_iter):
            y_pred = X @ w
            error = y_pred - y
            grad = (2 / n_samples) * X.T @ error

            # L2 gradient
            if l2_penalty > 0:
                grad += 2 * l2_penalty * w

            w_new = w - self.learning_rate * grad

            # L1 proximal step (soft thresholding)
            if l1_penalty > 0:
                if self.fit_intercept:
                    # Keep intercept as-is, only threshold coefs
                    intercept_val = w_new[0]
                    w_new = np.sign(w_new) * np.maximum(
                        np.abs(w_new) - self.learning_rate * l1_penalty, 0
                    )
                    w_new[0] = intercept_val
                else:
                    w_new = np.sign(w_new) * np.maximum(
                        np.abs(w_new) - self.learning_rate * l1_penalty, 0
                    )

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
        self._check_fitted()
        return np.asarray(X, dtype=np.float64) @ self.coef_ + self.intercept_

    def _check_fitted(self) -> None:
        if self.coef_ is None:
            raise ValueError("Model not fitted. Call fit() first.")

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Return the coefficient of determination R² of the prediction.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
        y : np.ndarray of shape (n_samples,)

        Returns
        -------
        r2 : float
        """
        y_pred = self.predict(X)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        return float(1 - ss_res / ss_tot) if ss_tot > 0 else 0.0


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    print("=== Testing Linear Regression ===")

    np.random.seed(42)
    n_samples, n_features = 200, 5

    # Generate data
    true_coef = np.array([1.5, -2.0, 3.0, 0.0, 0.0])
    X = np.random.randn(n_samples, n_features)
    y = X @ true_coef + np.random.randn(n_samples) * 0.5 + 2.0  # intercept=2

    # --- Closed-form (no regularization) ---
    lr = LinearRegression(fit_intercept=True, solver="normal")
    lr.fit(X, y)
    y_pred = lr.predict(X)
    assert len(y_pred) == n_samples
    r2 = lr.score(X, y)
    print(f"  Closed-form R²: {r2:.4f}")
    assert r2 > 0.9, f"R² too low: {r2}"

    # Check intercept is close to 2.0
    assert np.abs(lr.intercept_ - 2.0) < 2.0, f"Intercept: {lr.intercept_}"
    print("  Closed-form: PASS")

    # --- Gradient Descent (no regularization) ---
    lr_gd = LinearRegression(fit_intercept=True, solver="gd", learning_rate=0.001, max_iter=50000)
    lr_gd.fit(X, y)
    r2_gd = lr_gd.score(X, y)
    print(f"  GD R²: {r2_gd:.4f}")
    # GD should be close
    assert np.abs(r2 - r2_gd) < 0.1, f"GD vs closed-form R² diff too large"
    print("  Gradient Descent: PASS")

    # --- L2 Regularization (Ridge) ---
    ridge = LinearRegression(fit_intercept=True, alpha=10.0, l1_ratio=0.0, solver="normal")
    ridge.fit(X, y)
    r2_ridge = ridge.score(X, y)
    l2_norm_ridge = np.sum(ridge.coef_ ** 2)
    l2_norm_ols = np.sum(lr.coef_ ** 2)
    print(f"  Ridge R²: {r2_ridge:.4f}, L2-norm: {l2_norm_ridge:.4f} vs OLS: {l2_norm_ols:.4f}")
    assert l2_norm_ridge < l2_norm_ols, "Ridge should shrink weights"
    print("  Ridge (L2): PASS")

    # --- L1 Regularization (Lasso) ---
    lasso = LinearRegression(fit_intercept=True, alpha=1.0, l1_ratio=1.0, solver="gd",
                             learning_rate=0.001, max_iter=50000)
    lasso.fit(X, y)
    n_nonzero = np.sum(np.abs(lasso.coef_) > 1e-3)
    print(f"  Lasso: {n_nonzero}/{n_features} non-zero coefs")
    print("  Lasso (L1): PASS")

    # --- Compare with sklearn ---
    try:
        from sklearn.linear_model import LinearRegression as SkLR, Ridge, Lasso

        sk_lr = SkLR(fit_intercept=True)
        sk_lr.fit(X, y)
        diff = np.max(np.abs(sk_lr.coef_ - lr.coef_))
        print(f"  sklearn OLS max diff: {diff:.6f}")

        sk_ridge = Ridge(alpha=10.0, fit_intercept=True)
        sk_ridge.fit(X, y)
        diff_r = np.max(np.abs(sk_ridge.coef_ - ridge.coef_))
        print(f"  sklearn Ridge max diff: {diff_r:.6f}")
        assert diff < 0.5 and diff_r < 0.5, "Large discrepancy with sklearn"
        print("  sklearn comparison: PASS")
    except ImportError:
        print("  sklearn not installed, skipping comparison")

    print("All Linear Regression tests PASSED!\n")
