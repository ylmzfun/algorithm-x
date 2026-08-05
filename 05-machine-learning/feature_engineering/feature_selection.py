"""Feature Selection methods from scratch.

Includes:
- VarianceThreshold: remove low-variance features
- SelectKBest: select top k features by score (chi-squared, F-classif)
- RFE: Recursive Feature Elimination
"""

from __future__ import annotations

import numpy as np
from typing import Optional, Callable


class VarianceThreshold:
    """Feature selector that removes low-variance features.

    Parameters
    ----------
    threshold : float, default=0.0
        Features with variance below threshold are removed.

    Attributes
    ----------
    variances_ : np.ndarray of shape (n_features,)
        Variance of each feature.
    support_ : np.ndarray of shape (n_features,)
        Boolean mask of selected features.
    """

    def __init__(self, threshold: float = 0.0) -> None:
        self.threshold = threshold
        self.variances_: np.ndarray | None = None
        self.support_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: np.ndarray | None = None) -> VarianceThreshold:
        """Fit VarianceThreshold.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
        y : ignored

        Returns
        -------
        self
        """
        self.variances_ = np.var(X, axis=0)
        self.support_ = self.variances_ > self.threshold
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Reduce X to selected features.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        X_reduced : np.ndarray of shape (n_samples, n_selected)
        """
        return X[:, self.support_]

    def fit_transform(self, X: np.ndarray, y: np.ndarray | None = None) -> np.ndarray:
        """Fit and transform."""
        return self.fit(X).transform(X)


# ======================================================================
# Score functions
# ======================================================================


def _chi2_score(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Compute chi-squared statistic for each feature.

    Parameters
    ----------
    X : np.ndarray of shape (n_samples, n_features) — non-negative
    y : np.ndarray of shape (n_samples,) — class labels

    Returns
    -------
    scores : np.ndarray of shape (n_features,)
    """
    n_samples, n_features = X.shape
    classes = np.unique(y)
    scores = np.zeros(n_features)

    for f in range(n_features):
        col = X[:, f]
        # Observed counts per class
        observed = np.array([np.sum(col[y == c]) for c in classes])
        # Expected counts: (sum(col) / N) * N_c
        N = np.sum(col)
        if N == 0:
            scores[f] = 0
            continue
        expected = np.array([np.sum(y == c) / n_samples * N for c in classes])
        diff = observed - expected
        scores[f] = np.sum(diff ** 2 / (expected + 1e-10))
    return scores


def _f_classif_score(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Compute ANOVA F-value for each feature.

    Parameters
    ----------
    X : np.ndarray of shape (n_samples, n_features)
    y : np.ndarray of shape (n_samples,)

    Returns
    -------
    scores : np.ndarray of shape (n_features,)
    """
    n_samples, n_features = X.shape
    classes = np.unique(y)
    n_classes = len(classes)

    scores = np.zeros(n_features)
    for f in range(n_features):
        col = X[:, f]
        overall_mean = np.mean(col)

        ss_between = 0.0
        ss_within = 0.0
        for c in classes:
            col_c = col[y == c]
            n_c = len(col_c)
            if n_c == 0:
                continue
            mean_c = np.mean(col_c)
            ss_between += n_c * (mean_c - overall_mean) ** 2
            ss_within += np.sum((col_c - mean_c) ** 2)

        if n_classes > 1:
            ms_between = ss_between / (n_classes - 1)
        else:
            ms_between = 0
        ms_within = ss_within / max(n_samples - n_classes, 1)
        scores[f] = ms_between / max(ms_within, 1e-10)

    return scores


def _mutual_info_score(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Compute mutual information between each feature and target.

    Parameters
    ----------
    X : np.ndarray of shape (n_samples, n_features)
    y : np.ndarray of shape (n_samples,)

    Returns
    -------
    scores : np.ndarray of shape (n_features,)
    """
    n_samples, n_features = X.shape
    classes = np.unique(y)
    n_classes = len(classes)

    # Entropy of target
    p_y = np.array([np.mean(y == c) for c in classes])
    H_y = -np.sum(p_y * np.log(p_y + 1e-15))

    scores = np.zeros(n_features)
    for f in range(n_features):
        col = X[:, f]
        # Discretize into bins for MI estimation
        n_bins = min(10, n_samples // 10)
        if n_bins < 2:
            continue
        bins = np.percentile(col, np.linspace(0, 100, n_bins + 1))
        bin_indices = np.digitize(col, bins[:-1]) - 1
        bin_indices = np.clip(bin_indices, 0, n_bins - 1)

        # Conditional entropy H(y|X_f)
        H_cond = 0.0
        for b in range(n_bins):
            mask = bin_indices == b
            n_b = np.sum(mask)
            if n_b == 0:
                continue
            for c in classes:
                p_joint = np.sum((mask) & (y == c)) / n_samples
                if p_joint > 0:
                    p_cond = p_joint / (n_b / n_samples)
                    H_cond -= p_joint * np.log(p_cond + 1e-15)

        scores[f] = H_y - H_cond

    return scores


# ======================================================================
# SelectKBest
# ======================================================================


class SelectKBest:
    """Select features according to the k highest scores.

    Parameters
    ----------
    score_func : callable, default=_f_classif_score
        Function taking (X, y) and returning array of scores.
    k : int, default=10
        Number of top features to select.

    Attributes
    ----------
    scores_ : np.ndarray of shape (n_features,)
        Scores for each feature.
    support_ : np.ndarray of shape (n_features,)
        Boolean mask of selected features.
    """

    def __init__(self, score_func: Callable = _f_classif_score, k: int = 10) -> None:
        self.score_func = score_func
        self.k = k
        self.scores_: np.ndarray | None = None
        self.support_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> SelectKBest:
        """Run score function and select top k features.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
        y : np.ndarray of shape (n_samples,)

        Returns
        -------
        self
        """
        self.scores_ = self.score_func(X, y)
        n_features = X.shape[1]
        k = min(self.k, n_features)
        top_indices = np.argsort(self.scores_)[::-1][:k]
        self.support_ = np.zeros(n_features, dtype=bool)
        self.support_[top_indices] = True
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Reduce X to selected features.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        X_reduced : np.ndarray of shape (n_samples, k)
        """
        return X[:, self.support_]

    def fit_transform(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Fit and transform."""
        return self.fit(X, y).transform(X)


# ======================================================================
# Recursive Feature Elimination (RFE)
# ======================================================================


class RFE:
    """Recursive Feature Elimination.

    Selects features by recursively considering smaller sets.
    At each step, the least important feature is removed.

    Parameters
    ----------
    estimator : object
        A fitted estimator with `coef_` or `feature_importances_` attribute.
    n_features_to_select : int or None, default=None
        Number of features to select. If None, select half.

    Attributes
    ----------
    support_ : np.ndarray of shape (n_features,)
        Boolean mask of selected features.
    ranking_ : np.ndarray of shape (n_features,)
        Feature ranking (1 = best).
    """

    def __init__(self, estimator, n_features_to_select: int | None = None) -> None:
        self.estimator = estimator
        self.n_features_to_select = n_features_to_select
        self.support_: np.ndarray | None = None
        self.ranking_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> RFE:
        """Fit RFE.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
        y : np.ndarray of shape (n_samples,)

        Returns
        -------
        self
        """
        X = np.asarray(X, dtype=np.float64)
        n_features = X.shape[1]

        if self.n_features_to_select is None:
            n_to_select = n_features // 2
        else:
            n_to_select = min(self.n_features_to_select, n_features)

        # Initialize: all features active
        support = np.ones(n_features, dtype=bool)
        ranking = np.ones(n_features, dtype=int)

        while np.sum(support) > n_to_select:
            # Fit estimator on current features
            active_indices = np.where(support)[0]
            self.estimator.fit(X[:, active_indices], y)

            # Get feature importances
            if hasattr(self.estimator, "coef_"):
                importances = np.abs(self.estimator.coef_)
            elif hasattr(self.estimator, "feature_importances_"):
                importances = self.estimator.feature_importances_
            else:
                raise ValueError("Estimator must have coef_ or feature_importances_")

            if importances.ndim > 1:
                importances = np.mean(np.abs(importances), axis=0)

            # Find least important feature
            least_important = active_indices[np.argmin(importances)]
            support[least_important] = False
            ranking[least_important] = np.sum(support) + 1

        # Set ranking for selected features
        ranking[support] = 1

        self.support_ = support
        self.ranking_ = ranking
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Reduce X to selected features."""
        return X[:, self.support_]

    def fit_transform(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Fit and transform."""
        return self.fit(X, y).transform(X)


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    print("=== Testing Feature Selection ===")

    np.random.seed(42)
    n_samples, n_features = 200, 10

    # Generate data where only first 3 features are informative
    X = np.random.randn(n_samples, n_features)
    y = (X[:, 0] + X[:, 1] - X[:, 2] > 0).astype(int)

    # Add constant feature for variance threshold test
    X[:, 9] = 1.0

    # --- VarianceThreshold ---
    vt = VarianceThreshold(threshold=0.01)
    X_vt = vt.fit_transform(X)
    assert X_vt.shape[1] < n_features, "Should remove constant feature"
    assert vt.variances_[9] < 0.01, "Constant feature should have low variance"
    print(f"  VarianceThreshold: removed {n_features - X_vt.shape[1]} features")

    # --- SelectKBest (F-classif) ---
    skb = SelectKBest(score_func=_f_classif_score, k=3)
    X_skb = skb.fit_transform(X, y)
    assert X_skb.shape[1] == 3
    # Top features should include the informative ones
    top_features = np.argsort(skb.scores_)[::-1][:3]
    print(f"  SelectKBest top features: {top_features}")
    assert 0 in top_features or 1 in top_features or 2 in top_features, \
        "Should select informative features"
    print("  SelectKBest (F-classif): PASS")

    # --- SelectKBest (chi-squared) ---
    # Shift X to be non-negative
    X_nonneg = X - X.min(axis=0)
    skb_chi = SelectKBest(score_func=_chi2_score, k=3)
    X_chi = skb_chi.fit_transform(X_nonneg, y)
    assert X_chi.shape[1] == 3
    print("  SelectKBest (chi-squared): PASS")

    # --- Mutual Information ---
    mi_scores = _mutual_info_score(X, y)
    print(f"  Mutual information scores: {mi_scores[:5]}...")
    assert np.any(mi_scores > 0), "Should have positive MI for some features"
    print("  Mutual information: PASS")

    # --- RFE ---
    try:
        from ..linear_model.logistic_regression import LogisticRegression
    except ImportError:
        # Fallback when run as script directly
        import sys
        sys.path.insert(0, '/Users/ylmzfun/Public/item/mine/algorithm-x/algorithm-python/05-machine-learning')
        from linear_model.logistic_regression import LogisticRegression
    lr = LogisticRegression(fit_intercept=True, max_iter=5000)
    rfe = RFE(estimator=lr, n_features_to_select=3)
    X_rfe = rfe.fit_transform(X, y)
    assert X_rfe.shape[1] == 3
    print(f"  RFE ranking: {rfe.ranking_}")
    # Best features should have rank 1
    assert np.sum(rfe.ranking_ == 1) == 3
    print("  RFE: PASS")

    print("All Feature Selection tests PASSED!\n")
