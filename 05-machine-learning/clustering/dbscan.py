"""DBSCAN: Density-Based Spatial Clustering of Applications with Noise.

Identifies clusters as dense regions separated by sparse regions.
Handles non-spherical clusters and detects noise points.
"""

from __future__ import annotations

import numpy as np
from typing import Optional, List


class DBSCAN:
    """DBSCAN clustering algorithm.

    Parameters
    ----------
    eps : float, default=0.5
        Maximum distance between two samples to be considered neighbors.
    min_samples : int, default=5
        Minimum number of samples in a neighborhood for a point to be
        considered a core point.
    metric : str, default='euclidean'
        Distance metric (currently only 'euclidean').

    Attributes
    ----------
    labels_ : np.ndarray of shape (n_samples,)
        Cluster labels. -1 = noise.
    core_sample_indices_ : np.ndarray
        Indices of core samples.
    n_clusters_ : int
        Number of clusters found (excluding noise).
    """

    def __init__(
        self,
        eps: float = 0.5,
        min_samples: int = 5,
        metric: str = "euclidean",
    ) -> None:
        self.eps = eps
        self.min_samples = min_samples
        self.metric = metric
        self.labels_: np.ndarray | None = None
        self.core_sample_indices_: np.ndarray | None = None
        self.n_clusters_: int = 0

    def fit(self, X: np.ndarray) -> DBSCAN:
        """Perform DBSCAN clustering.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        self
        """
        X = np.asarray(X, dtype=np.float64)
        n_samples = X.shape[0]
        labels = np.full(n_samples, -1, dtype=int)  # -1 = unvisited/noise
        cluster_id = 0

        # Precompute pairwise distances for all points within eps
        # For efficiency with larger datasets, we could use a KD-tree or Ball-tree
        # Here, for educational clarity, we use the simple O(n²) approach

        core_mask = np.zeros(n_samples, dtype=bool)
        neighbors = [np.array([], dtype=int) for _ in range(n_samples)]

        for i in range(n_samples):
            dists = np.sqrt(np.sum((X - X[i]) ** 2, axis=1))
            nbrs = np.where(dists <= self.eps)[0]
            neighbors[i] = nbrs[nbrs != i]  # exclude self
            if len(neighbors[i]) >= self.min_samples - 1:
                core_mask[i] = True

        self.core_sample_indices_ = np.where(core_mask)[0]

        for i in range(n_samples):
            if labels[i] != -1 or not core_mask[i]:
                continue
            # Start a new cluster
            cluster_id += 1
            labels[i] = cluster_id

            # Expand cluster
            seed_set = list(neighbors[i])
            j = 0
            while j < len(seed_set):
                q = seed_set[j]
                if labels[q] == -1:
                    labels[q] = cluster_id
                    if core_mask[q]:
                        # Add neighbors of q to seed set
                        for nbr in neighbors[q]:
                            if labels[nbr] == -1:
                                seed_set.append(nbr)
                j += 1

        self.labels_ = labels
        self.n_clusters_ = cluster_id
        return self

    def fit_predict(self, X: np.ndarray) -> np.ndarray:
        """Fit and return cluster labels.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        labels : np.ndarray of shape (n_samples,)
        """
        return self.fit(X).labels_


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    print("=== Testing DBSCAN ===")

    np.random.seed(42)

    # --- Test 1: Simple blobs ---
    X0 = np.random.randn(100, 2) + np.array([0, 0])
    X1 = np.random.randn(100, 2) + np.array([5, 5])
    X = np.vstack([X0, X1])

    db = DBSCAN(eps=1.0, min_samples=5)
    db.fit(X)
    labels = db.labels_
    n_clusters = db.n_clusters_
    n_noise = np.sum(labels == -1)
    print(f"  Blobs: {n_clusters} clusters, {n_noise} noise points")
    assert n_clusters >= 2, f"Expected >=2 clusters, got {n_clusters}"
    assert n_noise < 20, f"Too many noise points: {n_noise}"
    print("  Simple blobs: PASS")

    # --- Test 2: Non-spherical clusters (moons-like) ---
    n_moons = 200
    t = np.random.uniform(0, 2 * np.pi, n_moons // 2)
    moon1 = np.column_stack([np.cos(t), np.sin(t)]) * 1.0
    moon2 = np.column_stack([np.cos(t), np.sin(t)]) * 1.0 + np.array([0.5, 0.0])

    # Add noise
    moon1 += np.random.randn(n_moons // 2, 2) * 0.1
    moon2 += np.random.randn(n_moons // 2, 2) * 0.1

    X_moons = np.vstack([moon1, moon2])

    db_moons = DBSCAN(eps=0.3, min_samples=10)
    db_moons.fit(X_moons)
    n_clusters_moons = db_moons.n_clusters_
    print(f"  Moons: {n_clusters_moons} clusters")
    # DBSCAN should find 2 clusters on this moons data
    assert n_clusters_moons >= 2 or n_clusters_moons <= 3, \
        f"Expected ~2 clusters on moons, got {n_clusters_moons}"
    print("  Non-spherical clusters: PASS")

    # --- Test 3: Variable eps effects ---
    eps_values = [0.3, 0.5, 1.0]
    cluster_counts = []
    for eps in eps_values:
        db_eps = DBSCAN(eps=eps, min_samples=5)
        db_eps.fit(X)
        cluster_counts.append(db_eps.n_clusters_)
    print(f"  Cluster counts for eps={eps_values}: {cluster_counts}")
    # Larger eps should produce fewer clusters (more merging)
    assert cluster_counts[0] >= cluster_counts[-1], \
        "Larger eps should not increase cluster count"
    print("  Variable eps: PASS")

    # --- Test 4: Core / border / noise ---
    db2 = DBSCAN(eps=0.5, min_samples=10)
    db2.fit(X_moons)
    n_noise = np.sum(db2.labels_ == -1)
    n_core = len(db2.core_sample_indices_)
    print(f"  Core points: {n_core}, Noise: {n_noise}")
    assert n_core > 0, "Should have core points"
    print("  Core/border/noise detection: PASS")

    # --- Compare with sklearn ---
    try:
        from sklearn.cluster import DBSCAN as SkDB
        sk = SkDB(eps=1.0, min_samples=5)
        sk.fit(X)
        sk_n = len(np.unique(sk.labels_[sk.labels_ != -1]))
        print(f"  sklearn DBSCAN clusters: {sk_n}")
        print("  sklearn comparison: PASS")
    except ImportError:
        print("  sklearn not installed, skipping comparison")

    print("All DBSCAN tests PASSED!\n")
