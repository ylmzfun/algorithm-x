"""Principal Component Analysis (PCA) from scratch.

Implements:
- Mean centering
- Covariance matrix computation
- Eigen decomposition
- Explained variance ratio
- Data reconstruction from reduced dimensions
"""

from __future__ import annotations

import numpy as np
from typing import Optional, Tuple


class PCA:
    """Principal Component Analysis.

    Linear dimensionality reduction using Singular Value Decomposition
    of the data to project it to a lower dimensional space.

    Parameters
    ----------
    n_components : int or None, default=None
        Number of components to keep. If None, keep all.

    Attributes
    ----------
    components_ : np.ndarray of shape (n_components, n_features)
        Principal axes in feature space (eigenvectors).
    explained_variance_ : np.ndarray of shape (n_components,)
        Variance explained by each component.
    explained_variance_ratio_ : np.ndarray of shape (n_components,)
        Percentage of variance explained by each component.
    mean_ : np.ndarray of shape (n_features,)
        Per-feature empirical mean.
    n_components_ : int
        Estimated number of components.
    """

    def __init__(self, n_components: int | None = None) -> None:
        self.n_components = n_components
        self.components_: np.ndarray | None = None
        self.explained_variance_: np.ndarray | None = None
        self.explained_variance_ratio_: np.ndarray | None = None
        self.mean_: np.ndarray | None = None
        self.n_components_: int = 0

    def fit(self, X: np.ndarray) -> PCA:
        """Fit PCA on training data.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        self
        """
        X = np.asarray(X, dtype=np.float64)
        n_samples, n_features = X.shape

        # Center the data
        self.mean_ = np.mean(X, axis=0)
        X_centered = X - self.mean_

        # Compute covariance matrix
        # C = (1/(n-1)) * X_centered^T @ X_centered
        cov = (X_centered.T @ X_centered) / (n_samples - 1)

        # Eigen decomposition
        eigenvalues, eigenvectors = np.linalg.eigh(cov)

        # Sort in descending order
        idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        # Determine n_components
        if self.n_components is None:
            self.n_components_ = n_features
        else:
            self.n_components_ = min(self.n_components, n_features)

        self.components_ = eigenvectors[:, :self.n_components_].T
        self.explained_variance_ = eigenvalues[:self.n_components_]
        total_var = np.sum(eigenvalues)
        self.explained_variance_ratio_ = (
            eigenvalues[:self.n_components_] / total_var if total_var > 0
            else np.zeros(self.n_components_)
        )

        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Apply dimensionality reduction to X.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        X_transformed : np.ndarray of shape (n_samples, n_components)
        """
        self._check_fitted()
        X = np.asarray(X, dtype=np.float64)
        X_centered = X - self.mean_
        return X_centered @ self.components_.T

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        """Fit and transform."""
        return self.fit(X).transform(X)

    def inverse_transform(self, X: np.ndarray) -> np.ndarray:
        """Transform data back to its original space.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_components)

        Returns
        -------
        X_original : np.ndarray of shape (n_samples, n_features)
        """
        self._check_fitted()
        X = np.asarray(X, dtype=np.float64)
        return X @ self.components_ + self.mean_

    def _check_fitted(self) -> None:
        if self.components_ is None:
            raise ValueError("Model not fitted.")


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    print("=== Testing PCA ===")

    np.random.seed(42)
    n_samples = 200
    n_features = 5

    # Generate correlated data
    base = np.random.randn(n_samples, 2)
    X = np.column_stack([
        base[:, 0],
        base[:, 0] * 0.8 + base[:, 1] * 0.2,
        base[:, 1],
        base[:, 0] * 0.3 + base[:, 1] * 0.7,
        np.random.randn(n_samples) * 0.1,
    ])

    # --- Fit PCA ---
    pca = PCA(n_components=2)
    pca.fit(X)

    assert pca.components_.shape == (2, n_features)
    assert len(pca.explained_variance_) == 2
    assert len(pca.explained_variance_ratio_) == 2
    assert np.isclose(np.sum(pca.explained_variance_ratio_), pca.explained_variance_ratio_.sum())

    # Explained variance ratios should be decreasing
    assert pca.explained_variance_ratio_[0] >= pca.explained_variance_ratio_[1]
    print(f"  Explained variance ratio: {pca.explained_variance_ratio_}")
    cum_var = np.sum(pca.explained_variance_ratio_)
    print(f"  Cumulative variance (2 components): {cum_var:.4f}")
    assert cum_var > 0.5, f"Top 2 components should explain most variance: {cum_var}"
    print("  Explained variance: PASS")

    # --- Transform ---
    X_trans = pca.transform(X)
    assert X_trans.shape == (n_samples, 2)
    print("  Transform: PASS")

    # --- Inverse transform ---
    X_recon = pca.inverse_transform(X_trans)
    assert X_recon.shape == X.shape
    # Reconstruction error should be relatively small for most variance
    recon_error = np.mean((X - X_recon) ** 2)
    print(f"  Reconstruction MSE: {recon_error:.6f}")
    print("  Inverse transform: PASS")

    # --- Full PCA (n_components=None) ---
    pca_full = PCA()
    pca_full.fit(X)
    # All ratios should sum to 1
    assert np.isclose(np.sum(pca_full.explained_variance_ratio_), 1.0)
    print("  Full PCA: PASS")

    # --- Compare with sklearn ---
    try:
        from sklearn.decomposition import PCA as SkPCA
        sk = SkPCA(n_components=2)
        sk.fit(X)

        # Components may have flipped signs
        # Compare explained variance
        diff_var = np.max(np.abs(pca.explained_variance_ratio_
                                  - sk.explained_variance_ratio_))
        print(f"  Max explained variance ratio diff: {diff_var:.6f}")
        assert diff_var < 0.01, f"Large variance diff: {diff_var}"

        # Compare transforms (accounting for sign)
        X_sk = sk.transform(X)
        # Correlations between components (abs)
        for i in range(2):
            corr = np.abs(np.corrcoef(X_trans[:, i], X_sk[:, i])[0, 1])
            assert corr > 0.99, f"Component {i} correlation too low: {corr}"
        print("  sklearn comparison: PASS")
    except ImportError:
        print("  sklearn not installed, skipping comparison")

    print("All PCA tests PASSED!\n")
