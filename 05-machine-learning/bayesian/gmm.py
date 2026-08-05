"""Gaussian Mixture Model (GMM) with EM algorithm from scratch.

Features:
- EM algorithm for parameter estimation
- K-means++ initialization for better convergence
- Soft assignments (responsibilities)
- BIC for model selection
"""

from __future__ import annotations

import numpy as np
from typing import Optional, Tuple


class GaussianMixture:
    """Gaussian Mixture Model trained via Expectation-Maximization.

    Parameters
    ----------
    n_components : int, default=2
        Number of mixture components.
    covariance_type : {'full', 'diag'}, default='full'
        Type of covariance matrix. 'diag' = diagonal only.
    max_iter : int, default=100
        Maximum number of EM iterations.
    tol : float, default=1e-3
        Convergence threshold for log-likelihood.
    init_params : {'kmeans', 'random'}, default='kmeans'
        Method to initialize parameters.
    reg_covar : float, default=1e-6
        Regularization added to the diagonal of covariance matrices.
    random_state : int or None, default=None

    Attributes
    ----------
    weights_ : np.ndarray of shape (n_components,)
        Mixing weights (prior probabilities).
    means_ : np.ndarray of shape (n_components, n_features)
        Mean vectors.
    covariances_ : np.ndarray of shape (n_components, n_features, n_features) or
                   (n_components, n_features) for 'diag'
    converged_ : bool
        Whether EM converged.
    bic_ : float or None
        BIC score of the fitted model.
    """

    def __init__(
        self,
        n_components: int = 2,
        covariance_type: str = "full",
        max_iter: int = 100,
        tol: float = 1e-3,
        init_params: str = "kmeans",
        reg_covar: float = 1e-6,
        random_state: int | None = None,
    ) -> None:
        self.n_components = n_components
        self.covariance_type = covariance_type
        self.max_iter = max_iter
        self.tol = tol
        self.init_params = init_params
        self.reg_covar = reg_covar
        self.random_state = random_state
        self.weights_: np.ndarray | None = None
        self.means_: np.ndarray | None = None
        self.covariances_: np.ndarray | None = None
        self.converged_: bool = False
        self.bic_: float | None = None

    def _initialize_kmeans(self, X: np.ndarray, rng: np.random.RandomState) -> np.ndarray:
        """K-means++ initialization for cluster centers."""
        n_samples, n_features = X.shape
        centers = np.zeros((self.n_components, n_features))

        # First center: random point
        centers[0] = X[rng.randint(n_samples)]

        for k in range(1, self.n_components):
            # Compute squared distances to nearest center
            dists = np.min(
                np.sum((X[:, np.newaxis, :] - centers[:k]) ** 2, axis=2),
                axis=1,
            )
            # Choose next center with probability proportional to dist²
            probs = dists / np.sum(dists)
            centers[k] = X[rng.choice(n_samples, p=probs)]

        # Run a few iterations of k-means
        for _ in range(10):
            # Assign to nearest center
            dists = np.sum((X[:, np.newaxis, :] - centers) ** 2, axis=2)
            labels = np.argmin(dists, axis=1)
            for k in range(self.n_components):
                if np.sum(labels == k) > 0:
                    centers[k] = np.mean(X[labels == k], axis=0)

        return centers

    def fit(self, X: np.ndarray) -> GaussianMixture:
        """Fit the GMM using EM algorithm.

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

        # Initialize
        if self.init_params == "kmeans":
            self.means_ = self._initialize_kmeans(X, rng)
        else:
            self.means_ = X[rng.choice(n_samples, size=self.n_components, replace=False)]

        # Initialize weights equally
        self.weights_ = np.ones(self.n_components) / self.n_components

        # Initialize covariances as identity
        if self.covariance_type == "full":
            self.covariances_ = np.array(
                [np.eye(n_features) for _ in range(self.n_components)]
            )
        elif self.covariance_type == "diag":
            self.covariances_ = np.ones((self.n_components, n_features))
        else:
            raise ValueError(f"Unknown covariance_type: {self.covariance_type}")

        prev_log_lik = -float("inf")

        for iteration in range(self.max_iter):
            # E-step: compute responsibilities
            log_prob = self._estimate_log_prob(X)
            log_resp = self._estimate_log_weights() + log_prob
            resp = self._log_normalize(log_resp)

            # M-step: update parameters
            Nk = np.sum(resp, axis=0) + 1e-15
            self.weights_ = Nk / n_samples
            self.means_ = (resp.T @ X) / Nk.reshape(-1, 1)

            for k in range(self.n_components):
                diff = X - self.means_[k]
                if self.covariance_type == "full":
                    cov = (resp[:, k].reshape(-1, 1) * diff).T @ diff / Nk[k]
                    cov += self.reg_covar * np.eye(n_features)
                    self.covariances_[k] = cov
                elif self.covariance_type == "diag":
                    cov_diag = np.sum(resp[:, k].reshape(-1, 1) * diff ** 2, axis=0) / Nk[k]
                    cov_diag += self.reg_covar
                    self.covariances_[k] = cov_diag

            # Check convergence
            log_lik = np.sum(np.log(np.sum(np.exp(log_resp), axis=1)))
            if np.abs(log_lik - prev_log_lik) < self.tol:
                self.converged_ = True
                break
            prev_log_lik = log_lik

        # Compute BIC
        log_lik = np.sum(np.log(np.sum(
            np.exp(self._estimate_log_weights() + self._estimate_log_prob(X)),
            axis=1,
        )))
        # Number of parameters
        if self.covariance_type == "full":
            n_params = self.n_components * (
                n_features + n_features * (n_features + 1) // 2 + 1
            )
        else:
            n_params = self.n_components * (n_features + n_features + 1)
        n_params -= 1  # weights sum to 1
        self.bic_ = n_params * np.log(n_samples) - 2 * log_lik

        return self

    def _estimate_log_prob(self, X: np.ndarray) -> np.ndarray:
        """Log probability for each component: log N(X | μ_k, Σ_k)."""
        n_samples, n_features = X.shape
        log_prob = np.zeros((n_samples, self.n_components))

        for k in range(self.n_components):
            diff = X - self.means_[k]
            if self.covariance_type == "full":
                cov = self.covariances_[k]
                # log(2π)^d |Σ|
                sign, logdet = np.linalg.slogdet(cov)
                log_prob[:, k] = (
                    -0.5 * (n_features * np.log(2 * np.pi) + logdet
                            + np.sum(diff @ np.linalg.inv(cov) * diff, axis=1))
                )
            elif self.covariance_type == "diag":
                cov_diag = self.covariances_[k]
                log_prob[:, k] = (
                    -0.5 * (n_features * np.log(2 * np.pi)
                            + np.sum(np.log(cov_diag))
                            + np.sum(diff ** 2 / cov_diag, axis=1))
                )
        return log_prob

    def _estimate_log_weights(self) -> np.ndarray:
        """Log of mixing weights."""
        return np.log(self.weights_)

    def _log_normalize(self, log_resp: np.ndarray) -> np.ndarray:
        """Normalize responsibilities from log space."""
        log_resp_max = np.max(log_resp, axis=1, keepdims=True)
        resp = np.exp(log_resp - log_resp_max)
        return resp / np.sum(resp, axis=1, keepdims=True)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Soft assignment: posterior probability of each component.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        resp : np.ndarray of shape (n_samples, n_components)
        """
        self._check_fitted()
        X = np.asarray(X, dtype=np.float64)
        log_prob = self._estimate_log_prob(X)
        log_resp = self._estimate_log_weights() + log_prob
        return self._log_normalize(log_resp)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Hard assignment: predict the most likely component.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        labels : np.ndarray of shape (n_samples,)
        """
        return np.argmax(self.predict_proba(X), axis=1)

    def _check_fitted(self) -> None:
        if self.means_ is None:
            raise ValueError("Model not fitted.")

    def score(self, X: np.ndarray) -> float:
        """Average log-likelihood of X under the model.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        log_lik : float
        """
        self._check_fitted()
        X = np.asarray(X, dtype=np.float64)
        log_prob = self._estimate_log_prob(X)
        log_weights = self._estimate_log_weights()
        log_resp = log_weights + log_prob
        return float(np.mean(np.log(np.sum(np.exp(log_resp), axis=1))))


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    print("=== Testing GMM ===")

    np.random.seed(42)
    n_samples = 300

    # Generate 3 Gaussian clusters
    X0 = np.random.randn(100, 2) + np.array([0, 0])
    X1 = np.random.randn(100, 2) + np.array([5, 5])
    X2 = np.random.randn(100, 2) + np.array([0, 5])
    X = np.vstack([X0, X1, X2])
    idx = np.random.permutation(n_samples)
    X = X[idx]

    # --- Full covariance ---
    gmm = GaussianMixture(n_components=3, covariance_type="full",
                          init_params="kmeans", random_state=42)
    gmm.fit(X)
    labels = gmm.predict(X)
    assert len(np.unique(labels)) == 3, f"Expected 3 clusters, got {len(np.unique(labels))}"
    log_lik = gmm.score(X)
    print(f"  GMM (full) log-likelihood: {log_lik:.2f}")
    print(f"  BIC: {gmm.bic_:.2f}")
    print("  GMM full covariance: PASS")

    # --- Diagonal covariance ---
    gmm_diag = GaussianMixture(n_components=3, covariance_type="diag",
                               init_params="kmeans", random_state=42)
    gmm_diag.fit(X)
    log_lik_diag = gmm_diag.score(X)
    print(f"  GMM (diag) log-likelihood: {log_lik_diag:.2f}")
    print("  GMM diagonal covariance: PASS")

    # --- Probabilities sum to 1 ---
    proba = gmm.predict_proba(X[:10])
    assert np.allclose(np.sum(proba, axis=1), 1.0)
    print("  predict_proba: PASS")

    # --- BIC model selection ---
    bics = []
    for k in range(1, 6):
        gmm_k = GaussianMixture(n_components=k, covariance_type="full",
                                init_params="kmeans", random_state=42)
        gmm_k.fit(X)
        bics.append(gmm_k.bic_)
    best_k = np.argmin(bics) + 1
    print(f"  BIC values (k=1..5): {[f'{b:.0f}' for b in bics]}")
    print(f"  Best k by BIC: {best_k}")
    assert best_k == 3, f"BIC should select k=3, got {best_k}"
    print("  BIC model selection: PASS")

    # --- Compare with sklearn ---
    try:
        from sklearn.mixture import GaussianMixture as SkGMM
        sk_gmm = SkGMM(n_components=3, covariance_type="full",
                       init_params="kmeans", random_state=42)
        sk_gmm.fit(X)
        sk_labels = sk_gmm.predict(X)
        # Labels may differ by permutation, so check cluster purity is comparable
        from sklearn.metrics import adjusted_rand_score
        ari = adjusted_rand_score(labels, sk_labels)
        print(f"  Adjusted Rand Index vs sklearn: {ari:.4f}")
        assert ari > 0.7, f"Low agreement with sklearn: {ari}"
        print("  sklearn comparison: PASS")
    except ImportError:
        print("  sklearn not installed, skipping comparison")

    print("All GMM tests PASSED!\n")
