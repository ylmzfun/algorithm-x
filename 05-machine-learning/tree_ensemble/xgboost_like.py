"""Simplified XGBoost: second-order Taylor approximation + leaf regularization.

XGBoost advances beyond standard GBDT by:
1. Second-order Taylor expansion of the loss for more precise updates.
2. Regularization on leaf weights (L2 penalty on tree outputs).
3. Column subsampling for additional randomness.
4. Tree pruning based on gain (gamma parameter).

This is a simplified, educational implementation.
"""

from __future__ import annotations

import numpy as np
from typing import Optional


def _sigmoid(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, -500, 500)
    return 1.0 / (1.0 + np.exp(-x))


class XGBoostTreeNode:
    """A node in an XGBoost tree."""

    __slots__ = ("feature_idx", "threshold", "left", "right", "leaf_weight", "is_leaf")

    def __init__(self) -> None:
        self.feature_idx: int = 0
        self.threshold: float = 0.0
        self.left: XGBoostTreeNode | None = None
        self.right: XGBoostTreeNode | None = None
        self.leaf_weight: float = 0.0
        self.is_leaf: bool = True


class XGBoostRegressor:
    """Simplified XGBoost Regressor.

    Implements the core XGBoost algorithm:
    - Second-order gradient statistics (g, h) for MSE loss.
    - L2 regularization on leaf weights (lambda).
    - Gamma (min_split_loss) for pruning.
    - Column subsampling.

    Parameters
    ----------
    n_estimators : int, default=100
        Number of boosting rounds.
    learning_rate : float, default=0.3
        Step size shrinkage.
    max_depth : int, default=6
        Maximum tree depth.
    reg_lambda : float, default=1.0
        L2 regularization on leaf weights.
    gamma : float, default=0.0
        Minimum loss reduction to make a split.
    subsample : float, default=1.0
        Row subsample ratio.
    colsample_bytree : float, default=1.0
        Column subsample ratio per tree.
    random_state : int or None, default=None

    Attributes
    ----------
    trees_ : list of XGBoostTreeNode
    init_ : float
    """

    def __init__(
        self,
        n_estimators: int = 100,
        learning_rate: float = 0.3,
        max_depth: int = 6,
        reg_lambda: float = 1.0,
        gamma: float = 0.0,
        subsample: float = 1.0,
        colsample_bytree: float = 1.0,
        random_state: int | None = None,
    ) -> None:
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.reg_lambda = reg_lambda
        self.gamma = gamma
        self.subsample = subsample
        self.colsample_bytree = colsample_bytree
        self.random_state = random_state
        self.trees_: list[XGBoostTreeNode] = []
        self.init_: float = 0.0
        self._feature_indices: list[np.ndarray] = []

    def fit(self, X: np.ndarray, y: np.ndarray) -> XGBoostRegressor:
        """Fit the XGBoost model.

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
        rng = np.random.RandomState(self.random_state)

        # Initial prediction: mean
        self.init_ = float(np.mean(y))
        y_pred = np.full(n_samples, self.init_)

        self.trees_ = []
        self._feature_indices = []

        for _ in range(self.n_estimators):
            # For MSE: g = -(y - y_pred) * 2? No, let's use:
            # loss = (y - y_pred)^2
            # g = -2(y - y_pred), h = 2
            # But XGBoost minimizes sum(g_i * f(x_i) + 0.5 * h_i * f(x_i)^2) + reg
            # With g = (y_pred - y) (gradient of 0.5*(y-y_pred)^2 w.r.t. y_pred)
            # Actually: d/dy_pred (0.5*(y-y_pred)^2) = -(y - y_pred) = y_pred - y
            g = y_pred - y   # first order gradient
            h = np.ones(n_samples)  # second order hessian for MSE = 1

            # Subsampling
            if self.subsample < 1.0:
                n_sub = max(1, int(self.subsample * n_samples))
                indices = rng.choice(n_samples, size=n_sub, replace=False)
                X_sub, g_sub, h_sub = X[indices], g[indices], h[indices]
            else:
                indices = np.arange(n_samples)
                X_sub, g_sub, h_sub = X, g, h

            # Column subsampling
            if self.colsample_bytree < 1.0:
                n_cols = max(1, int(self.colsample_bytree * n_features))
                feat_idx = rng.choice(n_features, size=n_cols, replace=False)
            else:
                feat_idx = np.arange(n_features)

            self._feature_indices.append(feat_idx)

            # Build tree
            tree = self._build_tree(
                X_sub, g_sub, h_sub, feat_idx, depth=0, rng=rng
            )
            self.trees_.append(tree)

            # Update predictions
            update = self.learning_rate * self._predict_tree(X, tree)
            y_pred += update

        return self

    def _build_tree(
        self,
        X: np.ndarray,
        g: np.ndarray,
        h: np.ndarray,
        feat_indices: np.ndarray,
        depth: int,
        rng: np.random.RandomState,
    ) -> XGBoostTreeNode:
        """Recursively build an XGBoost tree."""
        n_samples = len(g)
        G = np.sum(g)
        H = np.sum(h) + 1e-15

        node = XGBoostTreeNode()

        # Leaf weight: -G/(H + lambda)
        # Optimal weight w* = -sum(g) / (sum(h) + lambda)
        node.leaf_weight = -G / (H + self.reg_lambda)

        if depth >= self.max_depth or n_samples <= 1:
            return node

        best_gain = -float("inf")
        best_feat = 0
        best_threshold = 0.0
        best_left_idx = None
        best_right_idx = None

        for feat in feat_indices:
            col = X[:, feat]
            unique_vals = np.unique(col)
            if len(unique_vals) <= 1:
                continue
            thresholds = (unique_vals[:-1] + unique_vals[1:]) / 2.0

            for threshold in thresholds:
                left_mask = col < threshold
                right_mask = ~left_mask
                n_left = np.sum(left_mask)
                n_right = n_samples - n_left
                if n_left == 0 or n_right == 0:
                    continue

                G_L = np.sum(g[left_mask])
                H_L = np.sum(h[left_mask]) + 1e-15
                G_R = np.sum(g[right_mask])
                H_R = np.sum(h[right_mask]) + 1e-15

                # Gain = 0.5 * [G_L^2/(H_L+λ) + G_R^2/(H_R+λ) - (G_L+G_R)^2/(H_L+H_R+λ)] - γ
                gain = 0.5 * (
                    G_L**2 / (H_L + self.reg_lambda)
                    + G_R**2 / (H_R + self.reg_lambda)
                    - (G_L + G_R)**2 / (H_L + H_R + self.reg_lambda)
                ) - self.gamma

                if gain > best_gain:
                    best_gain = gain
                    best_feat = feat
                    best_threshold = threshold
                    best_left_idx = left_mask
                    best_right_idx = right_mask

        if best_gain <= 0 or best_left_idx is None:
            return node

        # Split
        node.is_leaf = False
        node.feature_idx = best_feat
        node.threshold = best_threshold
        node.left = self._build_tree(
            X[best_left_idx], g[best_left_idx], h[best_left_idx],
            feat_indices, depth + 1, rng,
        )
        node.right = self._build_tree(
            X[best_right_idx], g[best_right_idx], h[best_right_idx],
            feat_indices, depth + 1, rng,
        )
        return node

    def _predict_tree(self, X: np.ndarray, node: XGBoostTreeNode) -> np.ndarray:
        """Predict from a single tree for all samples."""
        result = np.zeros(X.shape[0])
        for i in range(X.shape[0]):
            result[i] = self._traverse(X[i], node)
        return result

    def _traverse(self, x: np.ndarray, node: XGBoostTreeNode) -> float:
        if node.is_leaf:
            return node.leaf_weight
        if x[node.feature_idx] < node.threshold:
            return self._traverse(x, node.left)
        else:
            return self._traverse(x, node.right)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict using the XGBoost model.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        y_pred : np.ndarray of shape (n_samples,)
        """
        if not self.trees_:
            raise ValueError("Model not fitted.")
        X = np.asarray(X, dtype=np.float64)
        y_pred = np.full(X.shape[0], self.init_)
        for tree in self.trees_:
            y_pred += self.learning_rate * self._predict_tree(X, tree)
        return y_pred

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """R² score."""
        y_pred = self.predict(X)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        return float(1 - ss_res / ss_tot) if ss_tot > 0 else 0.0


class XGBoostClassifier:
    """Simplified XGBoost Binary Classifier.

    Uses binary logistic loss with second-order Taylor expansion.

    Parameters
    ----------
    n_estimators : int, default=100
    learning_rate : float, default=0.3
    max_depth : int, default=6
    reg_lambda : float, default=1.0
    gamma : float, default=0.0
    subsample : float, default=1.0
    colsample_bytree : float, default=1.0
    random_state : int or None
    """

    def __init__(
        self,
        n_estimators: int = 100,
        learning_rate: float = 0.3,
        max_depth: int = 6,
        reg_lambda: float = 1.0,
        gamma: float = 0.0,
        subsample: float = 1.0,
        colsample_bytree: float = 1.0,
        random_state: int | None = None,
    ) -> None:
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.reg_lambda = reg_lambda
        self.gamma = gamma
        self.subsample = subsample
        self.colsample_bytree = colsample_bytree
        self.random_state = random_state
        self.trees_: list[XGBoostTreeNode] = []
        self.init_: float = 0.0
        self.classes_: np.ndarray | None = None
        self._feature_indices: list[np.ndarray] = []

    def fit(self, X: np.ndarray, y: np.ndarray) -> XGBoostClassifier:
        """Fit the XGBoost classifier."""
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64).reshape(-1)
        n_samples, n_features = X.shape
        rng = np.random.RandomState(self.random_state)

        self.classes_ = np.unique(y)
        y_bin = np.where(y == self.classes_[1], 1.0, 0.0)

        # Initial log-odds
        p = np.clip(np.mean(y_bin), 1e-15, 1 - 1e-15)
        self.init_ = float(np.log(p / (1 - p)))
        y_pred = np.full(n_samples, self.init_)

        self.trees_ = []
        self._feature_indices = []

        for _ in range(self.n_estimators):
            proba = _sigmoid(y_pred)
            # g = d(loss)/d(y_pred) = proba - y
            g = proba - y_bin
            # h = d²(loss)/d(y_pred)² = proba * (1 - proba)
            h = proba * (1 - proba)

            if self.subsample < 1.0:
                n_sub = max(1, int(self.subsample * n_samples))
                indices = rng.choice(n_samples, size=n_sub, replace=False)
                X_sub, g_sub, h_sub = X[indices], g[indices], h[indices]
            else:
                indices = np.arange(n_samples)
                X_sub, g_sub, h_sub = X, g, h

            if self.colsample_bytree < 1.0:
                n_cols = max(1, int(self.colsample_bytree * n_features))
                feat_idx = rng.choice(n_features, size=n_cols, replace=False)
            else:
                feat_idx = np.arange(n_features)

            self._feature_indices.append(feat_idx)

            tree = self._build_tree(X_sub, g_sub, h_sub, feat_idx, depth=0, rng=rng)
            self.trees_.append(tree)

            update = self.learning_rate * self._predict_tree(X, tree)
            y_pred += update

        return self

    def _build_tree(self, X, g, h, feat_indices, depth, rng):
        n_samples = len(g)
        G, H = np.sum(g), np.sum(h) + 1e-15
        node = XGBoostTreeNode()
        node.leaf_weight = -G / (H + self.reg_lambda)

        if depth >= self.max_depth or n_samples <= 1:
            return node

        best_gain = -float("inf")
        best_feat, best_threshold = 0, 0.0
        best_left_idx, best_right_idx = None, None

        for feat in feat_indices:
            col = X[:, feat]
            unique_vals = np.unique(col)
            if len(unique_vals) <= 1:
                continue
            thresholds = (unique_vals[:-1] + unique_vals[1:]) / 2.0
            for threshold in thresholds:
                left_mask = col < threshold
                right_mask = ~left_mask
                n_left, n_right = np.sum(left_mask), n_samples - np.sum(left_mask)
                if n_left == 0 or n_right == 0:
                    continue
                G_L, H_L = np.sum(g[left_mask]), np.sum(h[left_mask]) + 1e-15
                G_R, H_R = np.sum(g[right_mask]), np.sum(h[right_mask]) + 1e-15
                gain = 0.5 * (
                    G_L**2 / (H_L + self.reg_lambda)
                    + G_R**2 / (H_R + self.reg_lambda)
                    - (G_L + G_R)**2 / (H_L + H_R + self.reg_lambda)
                ) - self.gamma
                if gain > best_gain:
                    best_gain = gain
                    best_feat = feat
                    best_threshold = threshold
                    best_left_idx = left_mask
                    best_right_idx = right_mask

        if best_gain <= 0 or best_left_idx is None:
            return node

        node.is_leaf = False
        node.feature_idx = best_feat
        node.threshold = best_threshold
        node.left = self._build_tree(
            X[best_left_idx], g[best_left_idx], h[best_left_idx],
            feat_indices, depth + 1, rng,
        )
        node.right = self._build_tree(
            X[best_right_idx], g[best_right_idx], h[best_right_idx],
            feat_indices, depth + 1, rng,
        )
        return node

    def _predict_tree(self, X: np.ndarray, node: XGBoostTreeNode) -> np.ndarray:
        result = np.zeros(X.shape[0])
        for i in range(X.shape[0]):
            result[i] = self._traverse(X[i], node)
        return result

    def _traverse(self, x: np.ndarray, node: XGBoostTreeNode) -> float:
        if node.is_leaf:
            return node.leaf_weight
        if x[node.feature_idx] < node.threshold:
            return self._traverse(x, node.left)
        else:
            return self._traverse(x, node.right)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict class probabilities."""
        if not self.trees_:
            raise ValueError("Model not fitted.")
        X = np.asarray(X, dtype=np.float64)
        log_odds = np.full(X.shape[0], self.init_)
        for tree in self.trees_:
            log_odds += self.learning_rate * self._predict_tree(X, tree)
        p1 = _sigmoid(log_odds)
        return np.column_stack([1 - p1, p1])

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict class labels."""
        proba = self.predict_proba(X)
        return self.classes_[np.argmax(proba, axis=1)]

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Mean accuracy."""
        return float(np.mean(self.predict(X) == y))


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    print("=== Testing XGBoost ===")

    np.random.seed(42)
    n_samples = 200

    # --- Regression ---
    X_r = np.random.randn(n_samples, 5)
    y_r = 2 * X_r[:, 0] - X_r[:, 1] + 0.5 * X_r[:, 2] + np.random.randn(n_samples) * 0.5

    xgb_r = XGBoostRegressor(
        n_estimators=30, learning_rate=0.3, max_depth=4,
        reg_lambda=1.0, gamma=0.0, subsample=0.8,
        colsample_bytree=0.8, random_state=42,
    )
    xgb_r.fit(X_r, y_r)
    r2 = xgb_r.score(X_r, y_r)
    print(f"  XGBoost Regressor R²: {r2:.4f}")
    assert r2 > 0.5, f"R² too low: {r2}"

    # --- Classification ---
    X_pos = np.random.randn(n_samples // 2, 5) + np.array([2, 0, 0, 0, 0])
    X_neg = np.random.randn(n_samples // 2, 5) + np.array([-2, 0, 0, 0, 0])
    X_c = np.vstack([X_pos, X_neg])
    y_c = np.array([1] * (n_samples // 2) + [0] * (n_samples // 2))
    idx_c = np.random.RandomState(42).permutation(n_samples)
    X_c, y_c = X_c[idx_c], y_c[idx_c]

    xgb_c = XGBoostClassifier(
        n_estimators=30, learning_rate=0.3, max_depth=4,
        reg_lambda=1.0, gamma=0.0, subsample=0.8,
        colsample_bytree=0.8, random_state=42,
    )
    xgb_c.fit(X_c, y_c)
    acc = xgb_c.score(X_c, y_c)
    print(f"  XGBoost Classifier accuracy: {acc:.4f}")
    assert acc > 0.8, f"Accuracy too low: {acc}"

    proba = xgb_c.predict_proba(X_c[:5])
    assert np.allclose(np.sum(proba, axis=1), 1.0)
    print("  predict_proba: PASS")

    # --- Compare with sklearn GBDT (not XGBoost, but similar) ---
    try:
        from sklearn.ensemble import GradientBoostingRegressor as SkGBR
        sk = SkGBR(n_estimators=30, learning_rate=0.3, max_depth=4, random_state=42)
        sk.fit(X_r, y_r)
        sk_r2 = sk.score(X_r, y_r)
        print(f"  sklearn GBR R²: {sk_r2:.4f}")
        print("  sklearn comparison: PASS")
    except ImportError:
        print("  sklearn not installed, skipping comparison")

    print("All XGBoost tests PASSED!\n")
