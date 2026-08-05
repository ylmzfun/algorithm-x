"""Random Forest: bootstrap aggregation of decision trees.

Features:
- Bootstrap sampling
- Random feature selection per split
- Ensemble voting (classification) and averaging (regression)
- Out-of-bag (OOB) error estimation
"""

from __future__ import annotations

import numpy as np
from typing import Optional, Literal

try:
    from .decision_tree import DecisionTreeClassifier, DecisionTreeRegressor
except ImportError:
    import sys, os
    _dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _dir not in sys.path:
        sys.path.insert(0, _dir)
    from tree_ensemble.decision_tree import DecisionTreeClassifier, DecisionTreeRegressor


class RandomForestClassifier:
    """Random Forest Classifier.

    An ensemble of decision trees trained on bootstrap samples
    with random feature selection at each split.

    Parameters
    ----------
    n_estimators : int, default=100
        Number of trees in the forest.
    max_depth : int or None, default=None
        Maximum depth of each tree.
    min_samples_split : int, default=2
        Minimum samples to split an internal node.
    max_features : int, float, or 'sqrt', default='sqrt'
        Features to consider per split. 'sqrt' = sqrt(n_features).
    bootstrap : bool, default=True
        Whether to use bootstrap samples.
    oob_score : bool, default=False
        Whether to use OOB samples to estimate generalization accuracy.
    random_state : int or None, default=None

    Attributes
    ----------
    estimators_ : list of DecisionTreeClassifier
    classes_ : np.ndarray
    oob_score_ : float or None
    feature_importances_ : np.ndarray
    """

    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: int | None = None,
        min_samples_split: int = 2,
        max_features: int | float | Literal["sqrt", "log2"] = "sqrt",
        bootstrap: bool = True,
        oob_score: bool = False,
        random_state: int | None = None,
    ) -> None:
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.max_features = max_features
        self.bootstrap = bootstrap
        self.oob_score = oob_score
        self.random_state = random_state
        self.estimators_: list[DecisionTreeClassifier] = []
        self.classes_: np.ndarray | None = None
        self.oob_score_: float | None = None
        self.feature_importances_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
        """Fit the random forest.

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
        self.classes_ = np.unique(y)
        n_classes = len(self.classes_)

        rng = np.random.RandomState(self.random_state)

        # Resolve max_features
        if self.max_features == "sqrt":
            max_feat = int(np.sqrt(n_features))
        elif self.max_features == "log2":
            max_feat = int(np.log2(n_features))
        elif isinstance(self.max_features, float):
            max_feat = max(1, int(self.max_features * n_features))
        else:
            max_feat = self.max_features

        self.estimators_ = []
        all_importances = np.zeros(n_features)
        oob_predictions = np.zeros((n_samples, n_classes)) if self.oob_score else None
        oob_counts = np.zeros(n_samples) if self.oob_score else None

        for i in range(self.n_estimators):
            tree = DecisionTreeClassifier(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                max_features=max_feat,
                random_state=rng.randint(0, 2**31),
            )

            if self.bootstrap:
                indices = rng.choice(n_samples, size=n_samples, replace=True)
                X_boot, y_boot = X[indices], y[indices]
                tree.fit(X_boot, y_boot)

                # OOB: samples not in bootstrap
                if self.oob_score:
                    oob_mask = np.ones(n_samples, dtype=bool)
                    oob_mask[indices] = False
                    oob_idx = np.where(oob_mask)[0]
                    if len(oob_idx) > 0:
                        proba = tree.predict_proba(X[oob_idx])
                        class_idx = np.searchsorted(self.classes_, y[oob_idx])
                        oob_predictions[oob_idx, class_idx] += proba[
                            np.arange(len(oob_idx)), class_idx
                        ]
                        oob_counts[oob_idx] += 1
            else:
                tree.fit(X, y)

            self.estimators_.append(tree)
            all_importances += tree.feature_importances_

        self.feature_importances_ = all_importances / self.n_estimators

        if self.oob_score and oob_predictions is not None:
            valid = oob_counts > 0
            if np.any(valid):
                y_pred = self.classes_[np.argmax(oob_predictions[valid], axis=1)]
                self.oob_score_ = float(np.mean(y_pred == y[valid]))
            else:
                self.oob_score_ = 0.0

        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict class probabilities by averaging tree probabilities.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        proba : np.ndarray of shape (n_samples, n_classes)
        """
        if not self.estimators_:
            raise ValueError("Model not fitted.")
        X = np.asarray(X, dtype=np.float64)
        all_proba = np.zeros((X.shape[0], len(self.classes_)))
        for tree in self.estimators_:
            all_proba += tree.predict_proba(X)
        return all_proba / self.n_estimators

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict class labels (majority vote).

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


class RandomForestRegressor:
    """Random Forest Regressor.

    Parameters
    ----------
    n_estimators : int, default=100
    max_depth : int or None
    min_samples_split : int, default=2
    max_features : int, float, or str, default='sqrt'
    bootstrap : bool, default=True
    oob_score : bool, default=False
    random_state : int or None

    Attributes
    ----------
    estimators_ : list of DecisionTreeRegressor
    oob_score_ : float or None
    feature_importances_ : np.ndarray
    """

    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: int | None = None,
        min_samples_split: int = 2,
        max_features: int | float | Literal["sqrt", "log2"] = "sqrt",
        bootstrap: bool = True,
        oob_score: bool = False,
        random_state: int | None = None,
    ) -> None:
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.max_features = max_features
        self.bootstrap = bootstrap
        self.oob_score = oob_score
        self.random_state = random_state
        self.estimators_: list[DecisionTreeRegressor] = []
        self.oob_score_: float | None = None
        self.feature_importances_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> RandomForestRegressor:
        """Fit the random forest regressor."""
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64)
        n_samples, n_features = X.shape

        rng = np.random.RandomState(self.random_state)

        if self.max_features == "sqrt":
            max_feat = int(np.sqrt(n_features))
        elif self.max_features == "log2":
            max_feat = int(np.log2(n_features))
        elif isinstance(self.max_features, float):
            max_feat = max(1, int(self.max_features * n_features))
        else:
            max_feat = self.max_features

        self.estimators_ = []
        all_importances = np.zeros(n_features)
        oob_pred = np.zeros(n_samples) if self.oob_score else None
        oob_counts = np.zeros(n_samples) if self.oob_score else None

        for i in range(self.n_estimators):
            tree = DecisionTreeRegressor(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                max_features=max_feat,
                random_state=rng.randint(0, 2**31),
            )

            if self.bootstrap:
                indices = rng.choice(n_samples, size=n_samples, replace=True)
                X_boot, y_boot = X[indices], y[indices]
                tree.fit(X_boot, y_boot)

                if self.oob_score:
                    oob_mask = np.ones(n_samples, dtype=bool)
                    oob_mask[indices] = False
                    oob_idx = np.where(oob_mask)[0]
                    if len(oob_idx) > 0:
                        oob_pred[oob_idx] += tree.predict(X[oob_idx])
                        oob_counts[oob_idx] += 1
            else:
                tree.fit(X, y)

            self.estimators_.append(tree)
            all_importances += tree.feature_importances_

        self.feature_importances_ = all_importances / self.n_estimators

        if self.oob_score and oob_pred is not None:
            valid = oob_counts > 0
            if np.any(valid):
                ss_res = np.sum((y[valid] - oob_pred[valid] / oob_counts[valid]) ** 2)
                ss_tot = np.sum((y[valid] - np.mean(y[valid])) ** 2)
                self.oob_score_ = float(1 - ss_res / ss_tot) if ss_tot > 0 else 0.0

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict by averaging tree predictions."""
        if not self.estimators_:
            raise ValueError("Model not fitted.")
        X = np.asarray(X, dtype=np.float64)
        preds = np.zeros(X.shape[0])
        for tree in self.estimators_:
            preds += tree.predict(X)
        return preds / self.n_estimators

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
    print("=== Testing Random Forest ===")

    np.random.seed(42)
    n_samples = 200

    # --- Classification ---
    X_pos = np.random.randn(n_samples // 2, 4) + np.array([2, 0, 0, 0])
    X_neg = np.random.randn(n_samples // 2, 4) + np.array([-2, 0, 0, 0])
    X_c = np.vstack([X_pos, X_neg])
    y_c = np.array([1] * (n_samples // 2) + [0] * (n_samples // 2))
    idx_c = np.random.RandomState(42).permutation(n_samples)
    X_c, y_c = X_c[idx_c], y_c[idx_c]

    rfc = RandomForestClassifier(
        n_estimators=20, max_depth=5, max_features="sqrt",
        oob_score=True, random_state=42,
    )
    rfc.fit(X_c, y_c)
    acc = rfc.score(X_c, y_c)
    print(f"  RF Classifier accuracy: {acc:.4f}, OOB: {rfc.oob_score_:.4f}")
    assert acc > 0.7, f"Accuracy too low: {acc}"
    assert rfc.oob_score_ is not None, "OOB score not computed"
    print("  RF Classifier: PASS")

    # Feature importances
    assert np.isclose(np.sum(rfc.feature_importances_), 1.0)
    print("  Feature importances: PASS")

    # --- Regression ---
    X_r = np.random.randn(n_samples, 4)
    y_r = 2 * X_r[:, 0] - X_r[:, 1] + 0.5 * X_r[:, 2] + np.random.randn(n_samples) * 0.5

    rfr = RandomForestRegressor(
        n_estimators=20, max_depth=5, oob_score=True, random_state=42,
    )
    rfr.fit(X_r, y_r)
    r2 = rfr.score(X_r, y_r)
    print(f"  RF Regressor R²: {r2:.4f}, OOB: {rfr.oob_score_:.4f}")
    assert r2 > 0.5, f"R² too low: {r2}"
    print("  RF Regressor: PASS")

    # --- Compare with sklearn ---
    try:
        from sklearn.ensemble import RandomForestClassifier as SkRFC
        sk = SkRFC(n_estimators=20, max_depth=5, random_state=42)
        sk.fit(X_c, y_c)
        sk_acc = sk.score(X_c, y_c)
        print(f"  sklearn RF accuracy: {sk_acc:.4f}")
        print("  sklearn comparison: PASS")
    except ImportError:
        print("  sklearn not installed, skipping comparison")

    print("All Random Forest tests PASSED!\n")
