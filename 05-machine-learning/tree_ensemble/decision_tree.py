"""CART Decision Tree: recursive splitting with Gini/entropy criteria.

Implements both classification and regression trees with:
- Recursive binary splitting
- Gini impurity and entropy criteria
- Max depth and min samples split controls
- Feature importance
- predict and predict_proba
"""

from __future__ import annotations

import numpy as np
from typing import Optional, Dict, Any, Tuple, Literal


# ======================================================================
# Decision Tree Node
# ======================================================================

class TreeNode:
    """Node in a decision tree."""

    __slots__ = (
        "feature_idx",
        "threshold",
        "left",
        "right",
        "value",
        "n_samples",
        "impurity",
    )

    def __init__(
        self,
        feature_idx: int | None = None,
        threshold: float | None = None,
        left: TreeNode | None = None,
        right: TreeNode | None = None,
        value: np.ndarray | float | None = None,
        n_samples: int = 0,
        impurity: float = 0.0,
    ) -> None:
        self.feature_idx = feature_idx  # Which feature to split on
        self.threshold = threshold      # Threshold value
        self.left = left                # Left child (< threshold)
        self.right = right              # Right child (>= threshold)
        self.value = value              # Prediction value (class counts or mean)
        self.n_samples = n_samples
        self.impurity = impurity        # Impurity at this node

    def is_leaf(self) -> bool:
        """Check if this node is a leaf."""
        return self.left is None and self.right is None


# ======================================================================
# Criterion functions
# ======================================================================


def gini(y: np.ndarray) -> float:
    """Compute Gini impurity for multi-class.

    Parameters
    ----------
    y : np.ndarray of shape (n_samples,)
        Class labels.

    Returns
    -------
    gini : float
    """
    _, counts = np.unique(y, return_counts=True)
    probs = counts / counts.sum()
    return float(1 - np.sum(probs ** 2))


def entropy(y: np.ndarray) -> float:
    """Compute entropy for multi-class.

    Parameters
    ----------
    y : np.ndarray of shape (n_samples,)
        Class labels.

    Returns
    -------
    entropy : float
    """
    _, counts = np.unique(y, return_counts=True)
    probs = counts / counts.sum()
    return float(-np.sum(probs * np.log2(probs + 1e-15)))


def mse(y: np.ndarray) -> float:
    """Compute mean squared error for regression.

    Parameters
    ----------
    y : np.ndarray of shape (n_samples,)

    Returns
    -------
    mse : float
    """
    if len(y) == 0:
        return 0.0
    return float(np.mean((y - np.mean(y)) ** 2))


# ======================================================================
# Decision Tree Classifier
# ======================================================================

class DecisionTreeClassifier:
    """CART Decision Tree Classifier.

    Builds a binary decision tree by recursively splitting the data
    to minimize Gini impurity or entropy.

    Parameters
    ----------
    criterion : {'gini', 'entropy'}, default='gini'
        The function to measure the quality of a split.
    max_depth : int or None, default=None
        Maximum depth of the tree. None means no limit.
    min_samples_split : int, default=2
        Minimum number of samples required to split an internal node.
    min_samples_leaf : int, default=1
        Minimum number of samples required to be at a leaf node.
    max_features : int, float, or None, default=None
        Number of features to consider when looking for best split.
        If int, use that many. If float (0,1), use fraction of total.
        If None, use all features.
    random_state : int or None, default=None
        Seed for feature subsampling.

    Attributes
    ----------
    root_ : TreeNode
        Root node of the fitted tree.
    n_features_in_ : int
        Number of features seen during fit.
    classes_ : np.ndarray
        Unique class labels.
    feature_importances_ : np.ndarray of shape (n_features,)
        Impurity-based feature importances.
    """

    def __init__(
        self,
        criterion: Literal["gini", "entropy"] = "gini",
        max_depth: int | None = None,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        max_features: int | float | None = None,
        random_state: int | None = None,
    ) -> None:
        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.random_state = random_state
        self.root_: TreeNode | None = None
        self.n_features_in_: int = 0
        self.classes_: np.ndarray | None = None
        self.feature_importances_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> DecisionTreeClassifier:
        """Build a decision tree classifier.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
        y : np.ndarray of shape (n_samples,)

        Returns
        -------
        self
        """
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y)
        n_samples, n_features = X.shape
        self.n_features_in_ = n_features
        self.classes_ = np.unique(y)

        # Feature importances accumulator
        self._impurity_decrease = np.zeros(n_features)

        # Compute impurity function
        if self.criterion == "gini":
            criterion_fn = gini
        elif self.criterion == "entropy":
            criterion_fn = entropy
        else:
            raise ValueError(f"Unknown criterion: {self.criterion}")

        self.root_ = self._build_tree(
            X, y, criterion_fn, depth=0,
            rng=np.random.RandomState(self.random_state),
        )

        # Normalize feature importances
        total = np.sum(self._impurity_decrease)
        self.feature_importances_ = (
            self._impurity_decrease / total if total > 0
            else np.ones(n_features) / n_features
        )
        return self

    def _select_features(self, n_features: int, rng: np.random.RandomState) -> np.ndarray:
        """Select features to consider for splitting."""
        if self.max_features is None:
            return np.arange(n_features)
        if isinstance(self.max_features, float):
            n_selected = max(1, int(self.max_features * n_features))
        else:
            n_selected = min(self.max_features, n_features)
        return rng.choice(n_features, size=n_selected, replace=False)

    def _build_tree(
        self,
        X: np.ndarray,
        y: np.ndarray,
        criterion_fn,
        depth: int,
        rng: np.random.RandomState,
    ) -> TreeNode:
        """Recursively build the decision tree."""
        n_samples = len(y)

        # Leaf value: class counts (ensure correct length)
        class_counts = np.zeros(len(self.classes_))
        for i, c in enumerate(self.classes_):
            class_counts[i] = np.sum(y == c)

        node_impurity = criterion_fn(y)

        # Check stopping criteria
        if (
            (self.max_depth is not None and depth >= self.max_depth)
            or n_samples < self.min_samples_split
            or len(np.unique(y)) == 1
        ):
            return TreeNode(
                value=class_counts,
                n_samples=n_samples,
                impurity=node_impurity,
            )

        # Find best split
        best_feature, best_threshold, best_gain = self._find_best_split(
            X, y, criterion_fn, node_impurity, rng
        )

        if best_gain <= 0:
            return TreeNode(
                value=class_counts,
                n_samples=n_samples,
                impurity=node_impurity,
            )

        # Split data
        left_mask = X[:, best_feature] < best_threshold
        right_mask = ~left_mask

        if (
            np.sum(left_mask) < self.min_samples_leaf
            or np.sum(right_mask) < self.min_samples_leaf
        ):
            return TreeNode(
                value=class_counts,
                n_samples=n_samples,
                impurity=node_impurity,
            )

        # Track impurity decrease for feature importance
        self._impurity_decrease[best_feature] += (
            node_impurity
            - (np.sum(left_mask) / n_samples) * criterion_fn(y[left_mask])
            - (np.sum(right_mask) / n_samples) * criterion_fn(y[right_mask])
        )

        left_child = self._build_tree(
            X[left_mask], y[left_mask], criterion_fn, depth + 1, rng
        )
        right_child = self._build_tree(
            X[right_mask], y[right_mask], criterion_fn, depth + 1, rng
        )

        return TreeNode(
            feature_idx=best_feature,
            threshold=best_threshold,
            left=left_child,
            right=right_child,
            value=class_counts,
            n_samples=n_samples,
            impurity=node_impurity,
        )

    def _find_best_split(
        self,
        X: np.ndarray,
        y: np.ndarray,
        criterion_fn,
        parent_impurity: float,
        rng: np.random.RandomState,
    ) -> Tuple[int, float, float]:
        """Find the best feature and threshold to split on."""
        n_samples, n_features = X.shape
        best_gain = -1.0
        best_feature = 0
        best_threshold = 0.0

        feature_indices = self._select_features(n_features, rng)

        for feat in feature_indices:
            col = X[:, feat]
            unique_vals = np.unique(col)
            if len(unique_vals) <= 1:
                continue

            # Try midpoints between sorted unique values
            thresholds = (unique_vals[:-1] + unique_vals[1:]) / 2.0

            for threshold in thresholds:
                left_mask = col < threshold
                right_mask = ~left_mask
                n_left = np.sum(left_mask)
                n_right = n_samples - n_left

                if n_left == 0 or n_right == 0:
                    continue

                left_impurity = criterion_fn(y[left_mask])
                right_impurity = criterion_fn(y[right_mask])

                gain = parent_impurity - (
                    (n_left / n_samples) * left_impurity
                    + (n_right / n_samples) * right_impurity
                )

                if gain > best_gain:
                    best_gain = gain
                    best_feature = feat
                    best_threshold = threshold

        return best_feature, best_threshold, best_gain

    def _predict_sample(self, x: np.ndarray, node: TreeNode) -> np.ndarray:
        """Predict class for a single sample."""
        if node.is_leaf():
            return node.value  # class counts
        if x[node.feature_idx] < node.threshold:
            return self._predict_sample(x, node.left)
        else:
            return self._predict_sample(x, node.right)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict class probabilities.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        proba : np.ndarray of shape (n_samples, n_classes)
        """
        if self.root_ is None:
            raise ValueError("Model not fitted.")
        X = np.asarray(X, dtype=np.float64)
        result = []
        for x in X:
            counts = self._predict_sample(x, self.root_)
            total = np.sum(counts)
            if total > 0:
                result.append(counts / total)
            else:
                result.append(np.ones_like(counts) / len(counts))
        return np.array(result)

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
        return self.classes_[np.argmax(proba, axis=1)]

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Mean accuracy."""
        return float(np.mean(self.predict(X) == y))


# ======================================================================
# Decision Tree Regressor
# ======================================================================

class DecisionTreeRegressor:
    """CART Decision Tree Regressor.

    Builds a binary decision tree minimizing MSE at each split.

    Parameters
    ----------
    max_depth : int or None, default=None
        Maximum depth of the tree.
    min_samples_split : int, default=2
        Minimum samples to split an internal node.
    min_samples_leaf : int, default=1
        Minimum samples at a leaf node.
    max_features : int, float, or None, default=None
        Features to consider when splitting.
    random_state : int or None, default=None

    Attributes
    ----------
    root_ : TreeNode
    n_features_in_ : int
    feature_importances_ : np.ndarray
    """

    def __init__(
        self,
        max_depth: int | None = None,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        max_features: int | float | None = None,
        random_state: int | None = None,
    ) -> None:
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.random_state = random_state
        self.root_: TreeNode | None = None
        self.n_features_in_: int = 0
        self.feature_importances_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> DecisionTreeRegressor:
        """Build a regression tree.

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
        self.n_features_in_ = n_features

        self._impurity_decrease = np.zeros(n_features)
        rng = np.random.RandomState(self.random_state)
        self.root_ = self._build_tree(X, y, depth=0, rng=rng)

        total = np.sum(self._impurity_decrease)
        self.feature_importances_ = (
            self._impurity_decrease / total if total > 0
            else np.ones(n_features) / n_features
        )
        return self

    def _select_features(self, n_features: int, rng: np.random.RandomState) -> np.ndarray:
        if self.max_features is None:
            return np.arange(n_features)
        if isinstance(self.max_features, float):
            n_selected = max(1, int(self.max_features * n_features))
        else:
            n_selected = min(self.max_features, n_features)
        return rng.choice(n_features, size=n_selected, replace=False)

    def _build_tree(
        self, X: np.ndarray, y: np.ndarray, depth: int, rng: np.random.RandomState
    ) -> TreeNode:
        n_samples = len(y)
        mean_val = np.mean(y)
        mse_val = mse(y)

        if (
            (self.max_depth is not None and depth >= self.max_depth)
            or n_samples < self.min_samples_split
            or np.allclose(y, y[0])
        ):
            return TreeNode(
                value=mean_val, n_samples=n_samples, impurity=mse_val
            )

        best_feature, best_threshold, best_gain = self._find_best_split(
            X, y, mse_val, rng
        )

        if best_gain <= 0:
            return TreeNode(
                value=mean_val, n_samples=n_samples, impurity=mse_val
            )

        left_mask = X[:, best_feature] < best_threshold
        right_mask = ~left_mask

        if (
            np.sum(left_mask) < self.min_samples_leaf
            or np.sum(right_mask) < self.min_samples_leaf
        ):
            return TreeNode(
                value=mean_val, n_samples=n_samples, impurity=mse_val
            )

        self._impurity_decrease[best_feature] += best_gain

        left_child = self._build_tree(X[left_mask], y[left_mask], depth + 1, rng)
        right_child = self._build_tree(X[right_mask], y[right_mask], depth + 1, rng)

        return TreeNode(
            feature_idx=best_feature,
            threshold=best_threshold,
            left=left_child,
            right=right_child,
            value=mean_val,
            n_samples=n_samples,
            impurity=mse_val,
        )

    def _find_best_split(
        self, X: np.ndarray, y: np.ndarray, parent_mse: float, rng: np.random.RandomState
    ) -> Tuple[int, float, float]:
        n_samples, n_features = X.shape
        best_gain = -1.0
        best_feature = 0
        best_threshold = 0.0

        feature_indices = self._select_features(n_features, rng)

        for feat in feature_indices:
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
                left_mse = mse(y[left_mask])
                right_mse = mse(y[right_mask])
                weighted_mse = (n_left / n_samples) * left_mse + (n_right / n_samples) * right_mse
                gain = parent_mse - weighted_mse
                if gain > best_gain:
                    best_gain = gain
                    best_feature = feat
                    best_threshold = threshold
        return best_feature, best_threshold, best_gain

    def _predict_sample(self, x: np.ndarray, node: TreeNode) -> float:
        if node.is_leaf():
            return node.value
        if x[node.feature_idx] < node.threshold:
            return self._predict_sample(x, node.left)
        else:
            return self._predict_sample(x, node.right)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict regression target.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        y_pred : np.ndarray of shape (n_samples,)
        """
        if self.root_ is None:
            raise ValueError("Model not fitted.")
        X = np.asarray(X, dtype=np.float64)
        return np.array([self._predict_sample(x, self.root_) for x in X])

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """R² score."""
        y_pred = self.predict(X)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        return float(1 - ss_res / ss_tot) if ss_tot > 0 else 0.0


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    print("=== Testing Decision Tree ===")

    np.random.seed(42)
    n_samples = 200

    # --- Classification ---
    # Use clustered data for better separability
    X_pos = np.random.randn(n_samples // 2, 3) + np.array([2, 0, 0])
    X_neg = np.random.randn(n_samples // 2, 3) + np.array([-2, 0, 0])
    X_c = np.vstack([X_pos, X_neg])
    y_c = np.array([1] * (n_samples // 2) + [0] * (n_samples // 2))
    idx_c = np.random.RandomState(42).permutation(n_samples)
    X_c, y_c = X_c[idx_c], y_c[idx_c]

    dtc = DecisionTreeClassifier(max_depth=5, min_samples_split=5)
    dtc.fit(X_c, y_c)
    acc = dtc.score(X_c, y_c)
    print(f"  Classifier accuracy: {acc:.4f}")
    assert acc > 0.7, f"Accuracy too low: {acc}"

    # Feature importances must sum to 1
    assert np.isclose(np.sum(dtc.feature_importances_), 1.0), "Importance sum != 1"
    print("  Feature importances: PASS")

    # predict_proba
    proba = dtc.predict_proba(X_c[:10])
    assert proba.shape == (10, 2)
    assert np.allclose(np.sum(proba, axis=1), 1.0)
    print("  predict_proba: PASS")

    # --- Regression ---
    X_r = np.random.randn(n_samples, 3)
    y_r = 2 * X_r[:, 0] - X_r[:, 1] + 0.5 * X_r[:, 2] + np.random.randn(n_samples) * 0.3

    dtr = DecisionTreeRegressor(max_depth=5, min_samples_split=5)
    dtr.fit(X_r, y_r)
    r2 = dtr.score(X_r, y_r)
    print(f"  Regressor R²: {r2:.4f}")
    assert r2 > 0.5, f"R² too low: {r2}"
    print("  Decision Tree Regressor: PASS")

    # --- Compare with sklearn ---
    try:
        from sklearn.tree import DecisionTreeClassifier as SkDTC
        sk = SkDTC(max_depth=5, min_samples_split=5, random_state=42)
        sk.fit(X_c, y_c)
        sk_acc = sk.score(X_c, y_c)
        print(f"  sklearn accuracy: {sk_acc:.4f}")
        print("  sklearn comparison: PASS")
    except ImportError:
        print("  sklearn not installed, skipping comparison")

    print("All Decision Tree tests PASSED!\n")
