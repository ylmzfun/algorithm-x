"""Naive Bayes classifiers: Gaussian and Multinomial.

GaussianNB: Assumes features follow a Gaussian distribution per class.
MultinomialNB: Suitable for discrete features (e.g., word counts).
"""

from __future__ import annotations

import numpy as np
from typing import Optional


class GaussianNB:
    """Gaussian Naive Bayes classifier.

    Assumes that features within each class follow a Gaussian distribution.

    P(x_i | y) = N(μ_{y,i}, σ²_{y,i})

    Parameters
    ----------
    var_smoothing : float, default=1e-9
        Portion of the largest variance to add to variances for stability.

    Attributes
    ----------
    classes_ : np.ndarray
        Unique class labels.
    class_prior_ : np.ndarray of shape (n_classes,)
        Prior probabilities P(y).
    theta_ : np.ndarray of shape (n_classes, n_features)
        Mean of each feature per class.
    var_ : np.ndarray of shape (n_classes, n_features)
        Variance of each feature per class.
    """

    def __init__(self, var_smoothing: float = 1e-9) -> None:
        self.var_smoothing = var_smoothing
        self.classes_: np.ndarray | None = None
        self.class_prior_: np.ndarray | None = None
        self.theta_: np.ndarray | None = None
        self.var_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> GaussianNB:
        """Fit Gaussian Naive Bayes.

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

        self.theta_ = np.zeros((n_classes, n_features))
        self.var_ = np.zeros((n_classes, n_features))
        self.class_prior_ = np.zeros(n_classes)

        for i, c in enumerate(self.classes_):
            X_c = X[y == c]
            self.class_prior_[i] = len(X_c) / n_samples
            self.theta_[i] = np.mean(X_c, axis=0)
            self.var_[i] = np.var(X_c, axis=0, ddof=1)

        # Smoothing
        self.var_ += self.var_smoothing * np.max(self.var_)

        return self

    def _log_likelihood(self, X: np.ndarray) -> np.ndarray:
        """Compute log-likelihood log P(X|y) for each class.

        Returns
        -------
        log_lik : np.ndarray of shape (n_samples, n_classes)
        """
        n_samples, n_features = X.shape
        n_classes = len(self.classes_)
        log_lik = np.zeros((n_samples, n_classes))

        for i in range(n_classes):
            # log(2πσ²)
            log_var = np.log(2 * np.pi * self.var_[i])
            # (x - μ)² / σ²
            diff_sq = (X - self.theta_[i]) ** 2 / self.var_[i]
            # sum over features
            log_lik[:, i] = -0.5 * np.sum(log_var + diff_sq, axis=1)

        return log_lik

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Compute class posterior probabilities.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        proba : np.ndarray of shape (n_samples, n_classes)
        """
        self._check_fitted()
        X = np.asarray(X, dtype=np.float64)
        log_lik = self._log_likelihood(X)
        log_prior = np.log(self.class_prior_)
        log_joint = log_lik + log_prior

        # Log-sum-exp trick
        log_joint_max = np.max(log_joint, axis=1, keepdims=True)
        joint_exp = np.exp(log_joint - log_joint_max)
        return joint_exp / np.sum(joint_exp, axis=1, keepdims=True)

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

    def _check_fitted(self) -> None:
        if self.classes_ is None:
            raise ValueError("Model not fitted.")

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Mean accuracy."""
        return float(np.mean(self.predict(X) == y))


class MultinomialNB:
    """Multinomial Naive Bayes classifier.

    Suitable for discrete features (e.g., word counts in text classification).
    Assumes features follow a multinomial distribution.

    P(x | y) = (Σ x_i)! / Π(x_i!) * Π(p_{y,i}^{x_i})

    Parameters
    ----------
    alpha : float, default=1.0
        Laplace smoothing parameter.

    Attributes
    ----------
    classes_ : np.ndarray
    class_prior_ : np.ndarray
    feature_log_prob_ : np.ndarray of shape (n_classes, n_features)
        Log of P(x_i|y).
    """

    def __init__(self, alpha: float = 1.0) -> None:
        self.alpha = alpha
        self.classes_: np.ndarray | None = None
        self.class_prior_: np.ndarray | None = None
        self.feature_log_prob_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> MultinomialNB:
        """Fit Multinomial Naive Bayes.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
            Non-negative feature counts.
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

        self.feature_log_prob_ = np.zeros((n_classes, n_features))
        self.class_prior_ = np.zeros(n_classes)

        for i, c in enumerate(self.classes_):
            X_c = X[y == c]
            self.class_prior_[i] = len(X_c) / n_samples
            # P(x_j | y) = (count(x_j, y) + α) / (count(y) + α * n_features)
            count = np.sum(X_c, axis=0) + self.alpha
            self.feature_log_prob_[i] = np.log(
                count / (np.sum(count, axis=0))
            )

        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Compute class probabilities.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        proba : np.ndarray of shape (n_samples, n_classes)
        """
        self._check_fitted()
        X = np.asarray(X, dtype=np.float64)
        log_joint = X @ self.feature_log_prob_.T + np.log(self.class_prior_)

        # Log-sum-exp
        log_joint_max = np.max(log_joint, axis=1, keepdims=True)
        joint_exp = np.exp(log_joint - log_joint_max)
        return joint_exp / np.sum(joint_exp, axis=1, keepdims=True)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict class labels."""
        proba = self.predict_proba(X)
        return self.classes_[np.argmax(proba, axis=1)]

    def _check_fitted(self) -> None:
        if self.classes_ is None:
            raise ValueError("Model not fitted.")

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Mean accuracy."""
        return float(np.mean(self.predict(X) == y))


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    print("=== Testing Naive Bayes ===")

    np.random.seed(42)

    # --- GaussianNB on Iris-like data ---
    n_samples = 150
    # Class 0
    X0 = np.random.randn(n_samples // 3, 4) + np.array([5, 3.5, 1.5, 0.3])
    # Class 1
    X1 = np.random.randn(n_samples // 3, 4) + np.array([6, 3, 4.5, 1.5])
    # Class 2
    X2 = np.random.randn(n_samples // 3, 4) + np.array([6.5, 3.5, 5.5, 2.0])
    X = np.vstack([X0, X1, X2])
    y = np.array([0] * (n_samples // 3) + [1] * (n_samples // 3) + [2] * (n_samples // 3))
    idx = np.random.permutation(n_samples)
    X, y = X[idx], y[idx]
    split = int(0.8 * n_samples)

    gnb = GaussianNB()
    gnb.fit(X[:split], y[:split])
    acc = gnb.score(X[split:], y[split:])
    print(f"  GaussianNB accuracy: {acc:.4f}")
    assert acc >= 0.7, f"Accuracy too low: {acc}"

    proba = gnb.predict_proba(X[:5])
    assert np.allclose(np.sum(proba, axis=1), 1.0)
    print("  GaussianNB: PASS")

    # --- MultinomialNB on text-like data ---
    # Simulate word counts per document
    rng = np.random.RandomState(42)
    n_docs, n_words = 100, 20
    X_text = rng.randint(0, 5, size=(n_docs, n_words))
    # Class 0: more words in first half; Class 1: more in second half
    y_text = np.array([0] * (n_docs // 2) + [1] * (n_docs // 2))
    # Make features slightly discriminative
    X_text[y_text == 0, :10] += 3
    X_text[y_text == 1, 10:] += 3

    idx = rng.permutation(n_docs)
    X_text, y_text = X_text[idx], y_text[idx]
    split = int(0.8 * n_docs)

    mnb = MultinomialNB(alpha=1.0)
    mnb.fit(X_text[:split], y_text[:split])
    acc_mnb = mnb.score(X_text[split:], y_text[split:])
    print(f"  MultinomialNB accuracy: {acc_mnb:.4f}")
    assert acc_mnb > 0.7
    print("  MultinomialNB: PASS")

    # --- Compare with sklearn ---
    try:
        from sklearn.naive_bayes import GaussianNB as SkGNB, MultinomialNB as SkMNB
        sk_gnb = SkGNB()
        sk_gnb.fit(X[:split], y[:split])
        sk_acc = sk_gnb.score(X[split:], y[split:])
        print(f"  sklearn GaussianNB accuracy: {sk_acc:.4f}")
        diff = np.abs(acc - sk_acc)
        assert diff < 0.1, f"Large discrepancy: {diff:.4f}"
        print("  sklearn comparison: PASS")
    except ImportError:
        print("  sklearn not installed, skipping comparison")

    print("All Naive Bayes tests PASSED!\n")
