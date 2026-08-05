"""K-Means clustering: Lloyd's algorithm, k-means++ initialization, elbow method, silhouette score.

All implementations from scratch using numpy.
"""

from __future__ import annotations

import numpy as np
from typing import Optional, Tuple


def silhouette_score(X: np.ndarray, labels: np.ndarray) -> float:
    """Compute the mean silhouette score for all samples.

    The silhouette score measures how similar a point is to its own
    cluster compared to other clusters. Range: [-1, 1].

    Parameters
    ----------
    X : np.ndarray of shape (n_samples, n_features)
    labels : np.ndarray of shape (n_samples,)

    Returns
    -------
    score : float
        Mean silhouette score.
    """
    n_samples = X.shape[0]
    unique_labels = np.unique(labels)
    if len(unique_labels) <= 1:
        return -1.0

    # Precompute pairwise distances
    # We compute on-demand to avoid O(n²) memory for large datasets
    silhouettes = np.zeros(n_samples)

    for i in range(n_samples):
        # a_i: mean distance to points in same cluster
        same_cluster = labels == labels[i]
        if np.sum(same_cluster) <= 1:
            silhouettes[i] = 0.0
            continue
        a_i = np.mean(np.linalg.norm(X[i] - X[same_cluster], axis=1))

        # b_i: minimum mean distance to another cluster
        b_i = float("inf")
        for lbl in unique_labels:
            if lbl == labels[i]:
                continue
            other_cluster = labels == lbl
            mean_dist = np.mean(np.linalg.norm(X[i] - X[other_cluster], axis=1))
            if mean_dist < b_i:
                b_i = mean_dist

        silhouettes[i] = (b_i - a_i) / max(a_i, b_i) if max(a_i, b_i) > 0 else 0.0

    return float(np.mean(silhouettes))


class KMeans:
    """K-Means clustering algorithm.

    Parameters
    ----------
    n_clusters : int, default=8
        Number of clusters.
    init : {'random', 'k-means++'}, default='k-means++'
        Initialization method.
    max_iter : int, default=300
        Maximum iterations of Lloyd's algorithm.
    tol : float, default=1e-4
        Relative tolerance for convergence (inertia change).
    n_init : int, default=10
        Number of times to run with different initializations.
    random_state : int or None, default=None

    Attributes
    ----------
    cluster_centers_ : np.ndarray of shape (n_clusters, n_features)
    labels_ : np.ndarray of shape (n_samples,)
    inertia_ : float
        Sum of squared distances to closest centroid.
    n_iter_ : int
        Number of iterations run.
    """

    def __init__(
        self,
        n_clusters: int = 8,
        init: str = "k-means++",
        max_iter: int = 300,
        tol: float = 1e-4,
        n_init: int = 10,
        random_state: int | None = None,
    ) -> None:
        self.n_clusters = n_clusters
        self.init = init
        self.max_iter = max_iter
        self.tol = tol
        self.n_init = n_init
        self.random_state = random_state
        self.cluster_centers_: np.ndarray | None = None
        self.labels_: np.ndarray | None = None
        self.inertia_: float = 0.0
        self.n_iter_: int = 0

    def _init_centroids(self, X: np.ndarray, rng: np.random.RandomState) -> np.ndarray:
        """Initialize cluster centroids.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
        rng : RandomState

        Returns
        -------
        centroids : np.ndarray of shape (n_clusters, n_features)
        """
        n_samples = X.shape[0]

        if self.init == "random":
            indices = rng.choice(n_samples, size=self.n_clusters, replace=False)
            return X[indices].copy()

        elif self.init == "k-means++":
            centroids = np.zeros((self.n_clusters, X.shape[1]))
            # First centroid: random
            centroids[0] = X[rng.randint(n_samples)]

            for k in range(1, self.n_clusters):
                # Compute squared distances to nearest centroid
                dists = np.min(
                    np.sum((X[:, np.newaxis, :] - centroids[:k]) ** 2, axis=2),
                    axis=1,
                )
                # Choose with probability proportional to dist²
                probs = dists / np.sum(dists)
                centroids[k] = X[rng.choice(n_samples, p=probs)]

            return centroids
        else:
            raise ValueError(f"Unknown init method: {self.init}")

    def fit(self, X: np.ndarray) -> KMeans:
        """Fit k-means clustering.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        self
        """
        X = np.asarray(X, dtype=np.float64)
        n_samples, n_features = X.shape
        rng = np.random.RandomState(self.random_state)

        best_inertia = float("inf")
        best_centers = None
        best_labels = None
        best_n_iter = 0

        for _ in range(self.n_init):
            centers = self._init_centroids(X, rng)
            prev_inertia = float("inf")

            for it in range(self.max_iter):
                # Assignment step
                dists = np.sum((X[:, np.newaxis, :] - centers) ** 2, axis=2)
                labels = np.argmin(dists, axis=1)

                # Update step
                new_centers = np.zeros_like(centers)
                for k in range(self.n_clusters):
                    mask = labels == k
                    if np.any(mask):
                        new_centers[k] = np.mean(X[mask], axis=0)
                    else:
                        # Reinitialize empty cluster
                        new_centers[k] = X[rng.randint(n_samples)]

                # Compute inertia
                inertia = np.sum(
                    np.sum((X - new_centers[labels]) ** 2, axis=1)
                )

                if np.abs(prev_inertia - inertia) < self.tol * prev_inertia:
                    break
                prev_inertia = inertia
                centers = new_centers

            if inertia < best_inertia:
                best_inertia = inertia
                best_centers = centers
                best_labels = labels
                best_n_iter = it + 1

        self.cluster_centers_ = best_centers
        self.labels_ = best_labels
        self.inertia_ = best_inertia
        self.n_iter_ = best_n_iter
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict the closest cluster for each sample.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        labels : np.ndarray of shape (n_samples,)
        """
        if self.cluster_centers_ is None:
            raise ValueError("Model not fitted.")
        X = np.asarray(X, dtype=np.float64)
        dists = np.sum((X[:, np.newaxis, :] - self.cluster_centers_) ** 2, axis=2)
        return np.argmin(dists, axis=1)

    def fit_predict(self, X: np.ndarray) -> np.ndarray:
        """Fit and return cluster labels."""
        return self.fit(X).labels_


def elbow_method(X: np.ndarray, k_range: range,
                 random_state: int | None = None) -> list[float]:
    """Compute inertia for a range of k values (elbow method).

    Parameters
    ----------
    X : np.ndarray of shape (n_samples, n_features)
    k_range : range
        Range of k values to try.
    random_state : int or None

    Returns
    -------
    inertias : list of float
    """
    inertias = []
    for k in k_range:
        km = KMeans(n_clusters=k, init="k-means++", n_init=5,
                     random_state=random_state, max_iter=100)
        km.fit(X)
        inertias.append(km.inertia_)
    return inertias


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    print("=== Testing K-Means ===")

    np.random.seed(42)
    n_samples = 300

    # Generate 3 clusters
    X0 = np.random.randn(100, 2) + np.array([0, 0])
    X1 = np.random.randn(100, 2) + np.array([5, 5])
    X2 = np.random.randn(100, 2) + np.array([0, 5])
    X = np.vstack([X0, X1, X2])
    idx = np.random.permutation(n_samples)
    X = X[idx]

    # --- K-means++ ---
    km = KMeans(n_clusters=3, init="k-means++", n_init=10, random_state=42)
    km.fit(X)
    assert km.labels_ is not None
    assert km.cluster_centers_.shape == (3, 2)
    n_unique = len(np.unique(km.labels_))
    print(f"  Cluster centers: {km.cluster_centers_.shape}")
    print(f"  Inertia: {km.inertia_:.2f}, Iterations: {km.n_iter_}")
    print(f"  Unique clusters: {n_unique}")
    assert n_unique == 3, f"Expected 3 clusters, got {n_unique}"

    # --- Silhouette score ---
    sil = silhouette_score(X, km.labels_)
    print(f"  Silhouette score: {sil:.4f}")
    assert sil > 0.3, f"Silhouette score too low: {sil}"
    print("  K-means++ + silhouette: PASS")

    # --- Elbow method ---
    inertias = elbow_method(X, range(1, 7), random_state=42)
    print(f"  Elbow inertias (k=1..6): {[f'{i:.0f}' for i in inertias]}")
    # Inertia should decrease
    for i in range(len(inertias) - 1):
        assert inertias[i] > inertias[i + 1], "Inertia not monotonic"
    print("  Elbow method: PASS")

    # --- Random init ---
    km_rand = KMeans(n_clusters=3, init="random", n_init=10, random_state=42)
    km_rand.fit(X)
    assert len(np.unique(km_rand.labels_)) == 3
    print("  Random init: PASS")

    # --- Compare with sklearn ---
    try:
        from sklearn.cluster import KMeans as SkKM
        sk = SkKM(n_clusters=3, init="k-means++", n_init=10, random_state=42)
        sk.fit(X)
        from sklearn.metrics import adjusted_rand_score
        ari = adjusted_rand_score(km.labels_, sk.labels_)
        print(f"  Adjusted Rand Index vs sklearn: {ari:.4f}")
        assert ari > 0.7, f"Low agreement with sklearn: {ari}"
        print("  sklearn comparison: PASS")
    except ImportError:
        print("  sklearn not installed, skipping comparison")

    print("All K-Means tests PASSED!\n")
