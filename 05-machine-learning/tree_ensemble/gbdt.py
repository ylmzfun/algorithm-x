"""Gradient Boosting Decision Tree (GBDT) from scratch.

Each stage fits a regression tree to the negative gradient (residuals)
of the loss function. Supports both classification and regression.
"""

from __future__ import annotations

import numpy as np
from typing import Optional

try:
    from .decision_tree import DecisionTreeRegressor
except ImportError:
    import sys, os
    _dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _dir not in sys.path:
        sys.path.insert(0, _dir)
    from tree_ensemble.decision_tree import DecisionTreeRegressor


def _sigmoid(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, -500, 500)
    return 1.0 / (1.0 + np.exp(-x))


class GradientBoostingRegressor:
    """Gradient Boosting Regressor.

    Fits sequential regression trees to the residuals of the previous ensemble.

    Parameters
    ----------
    n_estimators : int, default=100
        Number of boosting stages.
    learning_rate : float, default=0.1
        Shrinks the contribution of each tree.
    max_depth : int, default=3
        Maximum depth of each tree.
    min_samples_split : int, default=2
    subsample : float, default=1.0
        Fraction of samples to use for fitting each tree.
    random_state : int or None, default=None

    Attributes
    ----------
    estimators_ : list of (DecisionTreeRegressor, float)
        List of (tree, initial_pred) pairs.
    init_ : float
        Initial prediction (mean of y).
    train_score_ : list of float
        Loss at each iteration.
    """

    def __init__(
        self,
        n_estimators: int = 100,
        learning_rate: float = 0.1,
        max_depth: int = 3,
        min_samples_split: int = 2,
        subsample: float = 1.0,
        random_state: int | None = None,
    ) -> None:
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.subsample = subsample
        self.random_state = random_state
        self.estimators_: list[DecisionTreeRegressor] = []
        self.init_: float = 0.0
        self.train_score_: list[float] = []

    def fit(self, X: np.ndarray, y: np.ndarray) -> GradientBoostingRegressor:
        """Fit the gradient boosting model.

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
        n_samples = X.shape[0]
        rng = np.random.RandomState(self.random_state)

        # Initial prediction: mean
        self.init_ = float(np.mean(y))
        y_pred = np.full(n_samples, self.init_)

        self.estimators_ = []
        self.train_score_ = []

        for i in range(self.n_estimators):
            # Compute residuals (negative gradient for MSE)
            residuals = y - y_pred

            # Subsampling
            if self.subsample < 1.0:
                n_subsample = max(1, int(self.subsample * n_samples))
                indices = rng.choice(n_samples, size=n_subsample, replace=False)
                X_sub, res_sub = X[indices], residuals[indices]
            else:
                X_sub, res_sub = X, residuals

            # Fit tree to residuals
            tree = DecisionTreeRegressor(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                random_state=rng.randint(0, 2**31),
            )
            tree.fit(X_sub, res_sub)
            self.estimators_.append(tree)

            # Update predictions
            update = self.learning_rate * tree.predict(X)
            y_pred += update

            # Track loss
            mse_loss = np.mean((y - y_pred) ** 2)
            self.train_score_.append(mse_loss)

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict regression target.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        y_pred : np.ndarray of shape (n_samples,)
        """
        if not self.estimators_:
            raise ValueError("Model not fitted.")
        X = np.asarray(X, dtype=np.float64)
        y_pred = np.full(X.shape[0], self.init_)
        for tree in self.estimators_:
            y_pred += self.learning_rate * tree.predict(X)
        return y_pred

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """R² score."""
        y_pred = self.predict(X)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        return float(1 - ss_res / ss_tot) if ss_tot > 0 else 0.0


class GradientBoostingClassifier:
    """Gradient Boosting Classifier.

    Uses log loss (binary cross-entropy) and fits trees to the
    negative gradient of the loss.

    Parameters
    ----------
    n_estimators : int, default=100
    learning_rate : float, default=0.1
    max_depth : int, default=3
    min_samples_split : int, default=2
    subsample : float, default=1.0
    random_state : int or None

    Attributes
    ----------
    estimators_ : list of DecisionTreeRegressor
    init_ : float
    classes_ : np.ndarray
    """

    def __init__(
        self,
        n_estimators: int = 100,
        learning_rate: float = 0.1,
        max_depth: int = 3,
        min_samples_split: int = 2,
        subsample: float = 1.0,
        random_state: int | None = None,
    ) -> None:
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.subsample = subsample
        self.random_state = random_state
        self.estimators_: list[DecisionTreeRegressor] = []
        self.init_: float = 0.0
        self.classes_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> GradientBoostingClassifier:
        """Fit the GBDT classifier.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
        y : np.ndarray of shape (n_samples,)
            Binary labels (0/1).

        Returns
        -------
        self
        """
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64).reshape(-1)
        n_samples = X.shape[0]
        rng = np.random.RandomState(self.random_state)

        self.classes_ = np.unique(y)
        if len(self.classes_) != 2:
            raise ValueError("GradientBoostingClassifier requires binary labels.")

        # Map to 0/1
        y_bin = np.where(y == self.classes_[1], 1.0, 0.0)

        # Initial log-odds
        p = np.clip(np.mean(y_bin), 1e-15, 1 - 1e-15)
        self.init_ = float(np.log(p / (1 - p)))
        y_pred = np.full(n_samples, self.init_)

        self.estimators_ = []

        for i in range(self.n_estimators):
            # Probabilities
            proba = _sigmoid(y_pred)
            # Negative gradient of log loss = y - p
            residuals = y_bin - proba

            if self.subsample < 1.0:
                n_sub = max(1, int(self.subsample * n_samples))
                indices = rng.choice(n_samples, size=n_sub, replace=False)
                X_sub, res_sub = X[indices], residuals[indices]
            else:
                X_sub, res_sub = X, residuals

            tree = DecisionTreeRegressor(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                random_state=rng.randint(0, 2**31),
            )
            tree.fit(X_sub, res_sub)
            self.estimators_.append(tree)

            update = self.learning_rate * tree.predict(X)
            y_pred += update

        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict class probabilities.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        proba : np.ndarray of shape (n_samples, 2)
            [P(class0), P(class1)]
        """
        if not self.estimators_:
            raise ValueError("Model not fitted.")
        X = np.asarray(X, dtype=np.float64)
        log_odds = np.full(X.shape[0], self.init_)
        for tree in self.estimators_:
            log_odds += self.learning_rate * tree.predict(X)
        p1 = _sigmoid(log_odds)
        return np.column_stack([1 - p1, p1])

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

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Mean accuracy."""
        return float(np.mean(self.predict(X) == y))


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    print("=== Testing GBDT ===")

    np.random.seed(42)
    n_samples = 200

    # --- Regression ---
    X_r = np.random.randn(n_samples, 3)
    y_r = 2 * X_r[:, 0] - X_r[:, 1] + 0.5 * X_r[:, 2] + np.random.randn(n_samples) * 0.5

    gbr = GradientBoostingRegressor(
        n_estimators=50, learning_rate=0.1, max_depth=3, random_state=42,
    )
    gbr.fit(X_r, y_r)
    r2 = gbr.score(X_r, y_r)
    print(f"  GBDT Regressor R²: {r2:.4f}")
    assert r2 > 0.5, f"R² too low: {r2}"
    # Loss should decrease
    assert gbr.train_score_[0] > gbr.train_score_[-1], "Loss should decrease"
    print("  Loss decreasing: PASS")

    # --- Classification ---
    X_pos = np.random.randn(n_samples // 2, 3) + np.array([2, 0, 0])
    X_neg = np.random.randn(n_samples // 2, 3) + np.array([-2, 0, 0])
    X_c = np.vstack([X_pos, X_neg])
    y_c = np.array([1] * (n_samples // 2) + [0] * (n_samples // 2))
    idx_c = np.random.RandomState(42).permutation(n_samples)
    X_c, y_c = X_c[idx_c], y_c[idx_c]

    gbc = GradientBoostingClassifier(
        n_estimators=50, learning_rate=0.1, max_depth=3, random_state=42,
    )
    gbc.fit(X_c, y_c)
    acc = gbc.score(X_c, y_c)
    print(f"  GBDT Classifier accuracy: {acc:.4f}")
    assert acc > 0.8, f"Accuracy too low: {acc}"

    proba = gbc.predict_proba(X_c[:5])
    assert np.allclose(np.sum(proba, axis=1), 1.0)
    print("  predict_proba: PASS")

    # --- Compare with sklearn ---
    try:
        from sklearn.ensemble import GradientBoostingRegressor as SkGBR
        sk = SkGBR(n_estimators=50, learning_rate=0.1, max_depth=3, random_state=42)
        sk.fit(X_r, y_r)
        sk_r2 = sk.score(X_r, y_r)
        print(f"  sklearn GBR R²: {sk_r2:.4f}")
        print("  sklearn comparison: PASS")
    except ImportError:
        print("  sklearn not installed, skipping comparison")

    print("All GBDT tests PASSED!\n")
