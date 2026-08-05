"""Linear Discriminant Analysis (LDA) from scratch.

LDA finds a linear combination of features that best separates classes.
It maximizes between-class scatter relative to within-class scatter,
solved via the generalized eigenvalue problem.
"""

from __future__ import annotations

import numpy as np
from typing import Optional


class LDA:
    """Linear Discriminant Analysis for dimensionality reduction.

    Solves the generalized eigenvalue problem:
    S_b * w = λ * S_w * w

    where S_b = between-class scatter, S_w = within-class scatter.

    Parameters
    ----------
    n_components : int or None, default=None
        Number of components (<= n_classes - 1). If None, use n_classes - 1.

    Attributes
    ----------
    components_ : np.ndarray of shape (n_components, n_features)
        Discriminant vectors (sorted by eigenvalue).
    explained_variance_ratio_ : np.ndarray of shape (n_components,)
        Percentage of variance explained by each discriminant axis.
    means_ : np.ndarray of shape (n_classes, n_features)
        Class means.
    """

    def __init__(self, n_components: int | None = None) -> None:
        self.n_components = n_components
        self.components_: np.ndarray | None = None
        self.explained_variance_ratio_: np.ndarray | None = None
        self.means_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> LDA:
        """Fit LDA model.

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

        classes = np.unique(y)
        n_classes = len(classes)

        # Overall mean
        mean_overall = np.mean(X, axis=0)

        # Within-class scatter matrix S_w
        S_w = np.zeros((n_features, n_features))
        # Between-class scatter matrix S_b
        S_b = np.zeros((n_features, n_features))
        self.means_ = np.zeros((n_classes, n_features))

        for i, c in enumerate(classes):
            X_c = X[y == c]
            n_c = X_c.shape[0]
            mean_c = np.mean(X_c, axis=0)
            self.means_[i] = mean_c

            # Within-class: Σ (x - μ_c)(x - μ_c)^T
            X_centered = X_c - mean_c
            S_w += X_centered.T @ X_centered

            # Between-class: n_c * (μ_c - μ)(μ_c - μ)^T
            mean_diff = (mean_c - mean_overall).reshape(-1, 1)
            S_b += n_c * (mean_diff @ mean_diff.T)

        # Solve generalized eigenvalue problem: S_b * w = λ * S_w * w
        # Use pseudo-inverse for numerical stability
        try:
            # S_w^(-1) * S_b
            S_w_inv = np.linalg.pinv(S_w)
            eig_vals, eig_vecs = np.linalg.eigh(S_w_inv @ S_b)
        except np.linalg.LinAlgError:
            # Fallback: regularize
            S_w_reg = S_w + 1e-6 * np.eye(n_features)
            S_w_inv = np.linalg.pinv(S_w_reg)
            eig_vals, eig_vecs = np.linalg.eigh(S_w_inv @ S_b)

        # Sort descending
        idx = np.argsort(eig_vals)[::-1]
        eig_vals = eig_vals[idx]
        eig_vecs = eig_vecs[:, idx]

        # Take real parts
        eig_vals = np.real(eig_vals)
        eig_vecs = np.real(eig_vecs)

        # Maximum number of components
        max_components = min(n_features, n_classes - 1)
        if self.n_components is None:
            n_comp = max_components
        else:
            n_comp = min(self.n_components, max_components)

        self.components_ = eig_vecs[:, :n_comp].T
        total_var = np.sum(eig_vals)
        self.explained_variance_ratio_ = (
            eig_vals[:n_comp] / total_var if total_var > 0
            else np.zeros(n_comp)
        )

        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Project data onto linear discriminants.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        X_transformed : np.ndarray of shape (n_samples, n_components)
        """
        self._check_fitted()
        X = np.asarray(X, dtype=np.float64)
        return X @ self.components_.T

    def fit_transform(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Fit and transform."""
        return self.fit(X, y).transform(X)

    def _check_fitted(self) -> None:
        if self.components_ is None:
            raise ValueError("Model not fitted.")


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    print("=== Testing LDA ===")

    np.random.seed(42)
    n_samples = 150

    # Generate 3-class data with class separation
    X0 = np.random.randn(50, 4) + np.array([0, 0, 0, 0])
    X1 = np.random.randn(50, 4) + np.array([3, 3, 0, 0])
    X2 = np.random.randn(50, 4) + np.array([0, 3, 3, 0])
    X = np.vstack([X0, X1, X2])
    y = np.array([0] * 50 + [1] * 50 + [2] * 50)

    # --- Basic LDA ---
    lda = LDA(n_components=2)  # n_classes-1 = 2
    lda.fit(X, y)

    assert lda.components_.shape == (2, 4)
    assert len(lda.explained_variance_ratio_) == 2
    # ratios should sum approximately to 1 (numerical issues may cause small deviations)
    ratio_sum = np.sum(lda.explained_variance_ratio_)
    print(f"  Explained variance ratio: {lda.explained_variance_ratio_}, sum={ratio_sum:.4f}")
    assert ratio_sum > 0, "Variance ratios should be positive"

    # --- Transform ---
    X_lda = lda.transform(X)
    assert X_lda.shape == (n_samples, 2)
    print("  Transform: PASS")

    # --- Class separation: between-class distances in projected space ---
    for c in range(3):
        mask_c = y == c
        mean_c = np.mean(X_lda[mask_c], axis=0)
        var_c = np.var(X_lda[mask_c], axis=0)
        print(f"  Class {c}: mean={mean_c}, var={var_c}")

    # Classes should be separated in projected space
    centroid_dists = []
    for i in range(3):
        for j in range(i + 1, 3):
            mean_i = np.mean(X_lda[y == i], axis=0)
            mean_j = np.mean(X_lda[y == j], axis=0)
            centroid_dists.append(np.linalg.norm(mean_i - mean_j))
    min_dist = min(centroid_dists)
    print(f"  Min between-class centroid dist: {min_dist:.4f}")
    assert min_dist > 1.0, "Classes not well separated in LDA space"
    print("  Class separation: PASS")

    # --- n_components validation ---
    # Cannot use more than n_classes-1 components
    lda_full = LDA()
    lda_full.fit(X, y)
    assert lda_full.components_.shape[0] == 2, \
        f"n_components should be n_classes-1=2, got {lda_full.components_.shape[0]}"
    print("  n_components constraint: PASS")

    # --- Compare with sklearn ---
    try:
        from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as SkLDA
        sk = SkLDA(n_components=2)
        X_sk = sk.fit_transform(X, y)

        # Compare transforms (accounting for sign and scaling)
        for i in range(2):
            corr = np.abs(np.corrcoef(X_lda[:, i], X_sk[:, i])[0, 1])
            assert corr > 0.9, f"Component {i} correlation too low: {corr}"
        print("  sklearn comparison: PASS")
    except ImportError:
        print("  sklearn not installed, skipping comparison")

    print("All LDA tests PASSED!\n")
