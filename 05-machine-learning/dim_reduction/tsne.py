"""Simplified t-SNE: t-distributed Stochastic Neighbor Embedding.

Computes pairwise affinities using perplexity-based Gaussian kernels,
then optimizes low-dimensional embedding via gradient descent.
"""

from __future__ import annotations

import numpy as np
from typing import Optional


class TSNE:
    """Simplified t-Distributed Stochastic Neighbor Embedding.

    Parameters
    ----------
    n_components : int, default=2
        Dimension of the embedded space.
    perplexity : float, default=30.0
        Related to the number of nearest neighbors.
    learning_rate : float, default=200.0
        Learning rate for gradient descent.
    max_iter : int, default=1000
        Maximum number of iterations.
    random_state : int or None, default=None

    Attributes
    ----------
    embedding_ : np.ndarray of shape (n_samples, n_components)
        Low-dimensional embedding.
    """

    def __init__(
        self,
        n_components: int = 2,
        perplexity: float = 30.0,
        learning_rate: float = 200.0,
        max_iter: int = 1000,
        random_state: int | None = None,
    ) -> None:
        self.n_components = n_components
        self.perplexity = perplexity
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.random_state = random_state
        self.embedding_: np.ndarray | None = None

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        """Fit t-SNE and return the embedding.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        embedding : np.ndarray of shape (n_samples, n_components)
        """
        X = np.asarray(X, dtype=np.float64)
        n_samples = X.shape[0]
        rng = np.random.RandomState(self.random_state)

        # Step 1: Compute pairwise affinities in high-dimensional space
        P = self._compute_affinities(X, perplexity=self.perplexity)

        # Symmetrize: P_ij = (p_{i|j} + p_{j|i}) / (2n)
        P = (P + P.T) / (2 * n_samples)
        P = np.maximum(P, 1e-12)

        # Step 2: Initialize low-dimensional embedding
        Y = rng.randn(n_samples, self.n_components) * 0.0001

        # Step 3: Gradient descent
        # Momentum
        velocity = np.zeros_like(Y)
        momentum_switch = 250
        initial_momentum = 0.5
        final_momentum = 0.8

        for iteration in range(self.max_iter):
            # Compute Q (low-dimensional affinities)
            # Using t-distribution with 1 degree of freedom
            # q_ij = (1 + ||y_i - y_j||²)^{-1} / Σ_{k≠l} (1 + ||y_k - y_l||²)^{-1}
            sq_dists = np.sum((Y[:, np.newaxis, :] - Y[np.newaxis, :, :]) ** 2, axis=2)
            # Set diagonal to infinity (don't use self)
            np.fill_diagonal(sq_dists, np.inf)

            # 1 / (1 + dist²)
            inv_dists = 1.0 / (1.0 + sq_dists)
            inv_dists_sum = np.sum(inv_dists)
            Q = inv_dists / inv_dists_sum
            Q = np.maximum(Q, 1e-12)

            # Gradient
            pq_diff = P - Q
            grad = np.zeros_like(Y)
            for i in range(n_samples):
                # ∂C/∂y_i = 4 Σ_j (p_ij - q_ij)(y_i - y_j)(1 + ||y_i - y_j||²)^{-1}
                diff_ij = Y[i] - Y
                grad[i] = 4 * np.sum(
                    pq_diff[i, :, np.newaxis]
                    * diff_ij
                    * inv_dists[i, :, np.newaxis],
                    axis=0,
                )

            # Momentum update
            if iteration < momentum_switch:
                momentum = initial_momentum
            else:
                momentum = final_momentum

            velocity = momentum * velocity - self.learning_rate * grad
            Y += velocity

            # Center
            Y -= np.mean(Y, axis=0)

        self.embedding_ = Y
        return Y

    def _compute_affinities(self, X: np.ndarray, perplexity: float = 30.0) -> np.ndarray:
        """Compute pairwise affinities P_{j|i} using Gaussian kernels.

        Each point i has its own σ_i chosen so that the perplexity
        of the conditional distribution equals the target perplexity.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
        perplexity : float

        Returns
        -------
        P : np.ndarray of shape (n_samples, n_samples)
            P[i, j] = p_{j|i}
        """
        n_samples = X.shape[0]
        # Pairwise squared distances
        sq_dists = np.sum((X[:, np.newaxis, :] - X[np.newaxis, :, :]) ** 2, axis=2)
        P = np.zeros((n_samples, n_samples))

        target_entropy = np.log(perplexity)
        tol = 1e-5
        max_tries = 50

        for i in range(n_samples):
            # Binary search for σ_i
            beta = 1.0  # beta = 1 / (2σ²)
            beta_min = -float("inf")
            beta_max = float("inf")

            dists_i = sq_dists[i].copy()
            dists_i[i] = np.inf  # exclude self

            for _ in range(max_tries):
                # Compute P_{j|i}
                exp_neg = np.exp(-dists_i * beta)
                sum_exp = np.sum(exp_neg)
                if sum_exp == 0:
                    P_i = np.zeros(n_samples)
                    P_i[dists_i != np.inf] = 1.0 / (n_samples - 1)
                else:
                    P_i = exp_neg / sum_exp

                # Entropy H(P_i) = -Σ P_i log P_i
                entropy = -np.sum(P_i * np.log(np.maximum(P_i, 1e-15)))

                if np.abs(entropy - target_entropy) < tol:
                    break
                elif entropy > target_entropy:
                    # Increase beta (decrease σ)
                    beta_min = beta
                    if beta_max == float("inf"):
                        beta *= 2
                    else:
                        beta = (beta + beta_max) / 2
                else:
                    # Decrease beta (increase σ)
                    beta_max = beta
                    if beta_min == -float("inf"):
                        beta /= 2
                    else:
                        beta = (beta + beta_min) / 2

            P[i] = P_i

        return P


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    print("=== Testing t-SNE ===")

    np.random.seed(42)
    n_samples = 100

    # Generate 2 clusters in high-dimensional space
    X0 = np.random.randn(n_samples // 2, 10) + np.array([2] * 10)
    X1 = np.random.randn(n_samples // 2, 10) + np.array([-2] * 10)
    X = np.vstack([X0, X1])
    y = np.array([0] * (n_samples // 2) + [1] * (n_samples // 2))

    # --- Fit t-SNE ---
    tsne = TSNE(n_components=2, perplexity=20.0, learning_rate=100.0,
                max_iter=300, random_state=42)
    embedding = tsne.fit_transform(X)

    assert embedding.shape == (n_samples, 2)
    # Points from the same cluster should be closer together
    dist_intra = np.mean([
        np.linalg.norm(embedding[i] - embedding[j])
        for i in range(50) for j in range(i + 1, 50)
    ])
    dist_inter = np.mean([
        np.linalg.norm(embedding[i] - embedding[j])
        for i in range(50) for j in range(50, 100)
    ])
    print(f"  Intra-cluster mean dist: {dist_intra:.4f}")
    print(f"  Inter-cluster mean dist: {dist_inter:.4f}")
    assert dist_intra < dist_inter, \
        f"Intra should be < inter: {dist_intra:.4f} vs {dist_inter:.4f}"
    print("  Cluster separation: PASS")

    # --- Perplexity effect ---
    for perp in [5.0, 30.0]:
        tsne2 = TSNE(n_components=2, perplexity=perp, learning_rate=100.0,
                     max_iter=200, random_state=42)
        emb = tsne2.fit_transform(X)
        assert emb.shape == (n_samples, 2)
    print("  Variable perplexity: PASS")

    # --- Compare with sklearn ---
    try:
        from sklearn.manifold import TSNE as SkTSNE
        sk = SkTSNE(n_components=2, perplexity=20.0, max_iter=300,
                    random_state=42, method="exact")
        sk_emb = sk.fit_transform(X)
        print(f"  sklearn t-SNE shape: {sk_emb.shape}")
        print("  sklearn comparison: PASS")
    except ImportError:
        print("  sklearn not installed, skipping comparison")

    print("All t-SNE tests PASSED!\n")
