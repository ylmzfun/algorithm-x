"""
Maximum Likelihood Estimation for ML/AI Foundations.

Implements:
- MLE for Bernoulli distribution
- MLE for Poisson distribution
- MLE for Gaussian distribution
- Gradient ascent for MLE of logistic regression parameters
"""

import numpy as np
from numpy.typing import NDArray
from typing import Tuple, Dict


# ============================================================
# MLE for Bernoulli
# ============================================================

def mle_bernoulli(data: NDArray[np.int64]) -> Tuple[float, float]:
    """Compute MLE for Bernoulli parameter p.

    Likelihood: L(p) = Πᵢ p^{xᵢ} (1-p)^{1-xᵢ}
    Log-likelihood: ℓ(p) = Σᵢ [xᵢ log(p) + (1-xᵢ) log(1-p)]

    Derivative: ∂ℓ/∂p = Σ xᵢ/p - Σ (1-xᵢ)/(1-p) = 0
    ⇒ p̂ = (1/n) Σ xᵢ = sample mean

    Args:
        data: Binary data (0s and 1s).

    Returns:
        Tuple (p_hat, log_likelihood_at_mle).

    Complexity: O(n).
    """
    n = len(data)
    p_hat = float(np.mean(data))

    # Log-likelihood at MLE
    if p_hat == 0 or p_hat == 1:
        log_lik = 0.0
    else:
        log_lik = float(
            np.sum(data) * np.log(p_hat) +
            (n - np.sum(data)) * np.log(1.0 - p_hat)
        )

    return p_hat, log_lik


# ============================================================
# MLE for Poisson
# ============================================================

def mle_poisson(data: NDArray[np.int64]) -> Tuple[float, float]:
    """Compute MLE for Poisson rate parameter λ.

    Likelihood: L(λ) = Πᵢ λ^{xᵢ} e^{-λ} / xᵢ!
    Log-likelihood: ℓ(λ) = Σᵢ [xᵢ log(λ) - λ - log(xᵢ!)]

    Derivative: ∂ℓ/∂λ = Σ xᵢ/λ - n = 0
    ⇒ λ̂ = (1/n) Σ xᵢ = sample mean

    Args:
        data: Non-negative integer count data.

    Returns:
        Tuple (lambda_hat, log_likelihood_at_mle).

    Complexity: O(n).
    """
    n = len(data)
    lambda_hat = float(np.mean(data))

    from scipy.special import gammaln
    # Log-likelihood at MLE
    log_lik = float(
        np.sum(data) * np.log(lambda_hat) -
        n * lambda_hat -
        np.sum(gammaln(data.astype(float) + 1))
    )

    return lambda_hat, log_lik


# ============================================================
# MLE for Gaussian
# ============================================================

def mle_gaussian(data: NDArray[np.float64]) -> Tuple[float, float, float]:
    """Compute MLE for Gaussian parameters (μ, σ²).

    Likelihood: L(μ, σ²) = Πᵢ (1/√(2πσ²)) exp(-(xᵢ-μ)²/(2σ²))
    Log-likelihood: ℓ(μ, σ²) = -(n/2)log(2π) - (n/2)log(σ²) - (1/(2σ²)) Σ (xᵢ-μ)²

    ∂ℓ/∂μ = 0 ⇒ μ̂ = (1/n) Σ xᵢ (sample mean)
    ∂ℓ/∂σ² = 0 ⇒ σ̂² = (1/n) Σ (xᵢ - μ̂)² (sample variance, biased)

    Note: The MLE for σ² is the biased estimator (divide by n, not n-1).
    The unbiased estimator (n-1 denominator) is not the MLE.

    Args:
        data: Continuous data.

    Returns:
        Tuple (mu_hat, sigma_sq_hat, log_likelihood_at_mle).

    Complexity: O(n).
    """
    n = len(data)
    mu_hat = float(np.mean(data))
    sigma_sq_hat = float(np.mean((data - mu_hat) ** 2))

    # Log-likelihood at MLE
    log_lik = float(
        -0.5 * n * np.log(2.0 * np.pi) -
        0.5 * n * np.log(sigma_sq_hat) -
        0.5 * n  # since Σ(xᵢ-μ̂)²/σ̂² = n
    )

    return mu_hat, sigma_sq_hat, log_lik


def log_likelihood_gaussian(
    data: NDArray[np.float64],
    mu: float,
    sigma_sq: float
) -> float:
    """Compute the log-likelihood of data under N(μ, σ²).

    Args:
        data: Observed data.
        mu: Mean parameter.
        sigma_sq: Variance parameter (> 0).

    Returns:
        Log-likelihood value.

    Complexity: O(n).
    """
    n = len(data)
    if sigma_sq <= 0:
        return -np.inf
    return float(
        -0.5 * n * np.log(2.0 * np.pi) -
        0.5 * n * np.log(sigma_sq) -
        0.5 * np.sum((data - mu) ** 2) / sigma_sq
    )


# ============================================================
# MLE for Logistic Regression via Gradient Ascent
# ============================================================

def sigmoid(z: NDArray[np.float64]) -> NDArray[np.float64]:
    """Sigmoid (logistic) function: σ(z) = 1 / (1 + e^{-z}).

    Maps real values to (0, 1), used as probability in logistic regression.

    Args:
        z: Real-valued input(s).

    Returns:
        σ(z) ∈ (0, 1).
    """
    # Clip to avoid overflow
    z = np.clip(z, -500, 500)
    return 1.0 / (1.0 + np.exp(-z))


def logistic_regression_mle(
    X: NDArray[np.float64],
    y: NDArray[np.int64],
    learning_rate: float = 0.01,
    max_iter: int = 5000,
    tol: float = 1e-6,
    verbose: bool = False
) -> Tuple[NDArray[np.float64], float, list]:
    """Fit logistic regression using gradient ascent on the log-likelihood.

    Model: P(y=1 | x) = σ(βᵀx), where σ is the sigmoid function.

    Log-likelihood:
        ℓ(β) = Σᵢ [yᵢ log(σ(βᵀxᵢ)) + (1-yᵢ) log(1 - σ(βᵀxᵢ))]

    Gradient:
        ∇ℓ = Xᵀ (y - σ(Xβ))

    This is gradient ASCENT (maximizing log-likelihood), equivalent to
    minimizing negative log-likelihood (the standard logistic loss).

    Args:
        X: Feature matrix (n_samples, n_features). Assumes bias column
           is already included (column of 1s).
        y: Binary labels (0 or 1), shape (n_samples,).
        learning_rate: Step size for gradient ascent.
        max_iter: Maximum iterations.
        tol: Convergence tolerance on log-likelihood change.
        verbose: Print progress if True.

    Returns:
        Tuple (beta, final_log_lik, log_lik_history):
            beta: Fitted coefficients (n_features,).
            final_log_lik: Log-likelihood at convergence.
            log_lik_history: List of log-likelihood values per iteration.
    """
    n, p = X.shape
    beta = np.zeros(p, dtype=np.float64)
    log_lik_history = []

    for it in range(max_iter):
        # Predictions
        z = X @ beta
        prob = sigmoid(z)

        # Log-likelihood
        eps = 1e-15  # prevent log(0)
        log_lik = float(
            np.sum(y * np.log(prob + eps) + (1 - y) * np.log(1 - prob + eps))
        )
        log_lik_history.append(log_lik)

        # Gradient
        grad = X.T @ (y - prob)  # gradient ASCENT: we add, not subtract

        # Update
        beta_new = beta + learning_rate * grad

        # Check convergence
        if np.max(np.abs(beta_new - beta)) < tol:
            beta = beta_new
            if verbose:
                print(f"  Converged at iteration {it+1}, log-lik = {log_lik:.4f}")
            return beta, log_lik, log_lik_history

        beta = beta_new

    final_z = X @ beta
    final_prob = sigmoid(final_z)
    eps = 1e-15
    final_log_lik = float(
        np.sum(y * np.log(final_prob + eps) + (1 - y) * np.log(1 - final_prob + eps))
    )
    return beta, final_log_lik, log_lik_history


def logistic_regression_predict(
    X: NDArray[np.float64], beta: NDArray[np.float64],
    threshold: float = 0.5
) -> NDArray[np.int64]:
    """Make binary predictions using fitted logistic regression.

    Args:
        X: Feature matrix (n_samples, n_features).
        beta: Fitted coefficients.
        threshold: Classification threshold (default 0.5).

    Returns:
        Predicted labels (0 or 1).
    """
    prob = sigmoid(X @ beta)
    return (prob >= threshold).astype(np.int64)


# ============================================================
# Tests
# ============================================================

def _test_mle_bernoulli() -> None:
    data = np.array([1, 0, 1, 1, 0, 1, 1, 1, 0, 1], dtype=np.int64)
    p_hat, log_lik = mle_bernoulli(data)
    # 7 out of 10 = 0.7
    assert abs(p_hat - 0.7) < 1e-10, f"FAIL: {p_hat}"
    assert log_lik < 0  # log-likelihood is negative
    print(f"  PASS: mle_bernoulli (p̂={p_hat:.3f})")


def _test_mle_poisson() -> None:
    data = np.array([2, 4, 3, 5, 1, 3, 4, 2, 3, 3], dtype=np.int64)
    lambda_hat, log_lik = mle_poisson(data)
    # mean = 30/10 = 3.0
    assert abs(lambda_hat - 3.0) < 1e-10, f"FAIL: {lambda_hat}"
    print(f"  PASS: mle_poisson (λ̂={lambda_hat:.3f})")


def _test_mle_gaussian() -> None:
    data = np.array([2.0, 4.0, 3.0, 5.0, 1.0, 3.0, 4.0, 2.0, 3.0, 3.0])
    mu_hat, sigma_sq_hat, log_lik = mle_gaussian(data)

    # mean = 3.0, var = (1+1+0+4+4+0+1+1+0+0)/10 = 12/10 = 1.2 (biased)
    assert abs(mu_hat - 3.0) < 1e-10, f"FAIL mu: {mu_hat}"
    assert abs(sigma_sq_hat - 1.2) < 1e-10, f"FAIL sigma_sq: {sigma_sq_hat}"

    # Check that MLE is indeed the maximum
    ll_mle = log_likelihood_gaussian(data, mu_hat, sigma_sq_hat)
    ll_other = log_likelihood_gaussian(data, 2.5, 1.5)
    assert ll_mle >= ll_other, f"MLE not maximum: {ll_mle} < {ll_other}"
    print(f"  PASS: mle_gaussian (μ̂={mu_hat:.3f}, σ̂²={sigma_sq_hat:.3f})")


def _test_logistic_regression_mle() -> None:
    np.random.seed(42)
    n = 200
    # Generate separable data
    X_class0 = np.random.randn(n // 2, 2) + np.array([-2.0, -2.0])
    X_class1 = np.random.randn(n // 2, 2) + np.array([2.0, 2.0])
    X_data = np.vstack([X_class0, X_class1])
    y_data = np.hstack([np.zeros(n // 2), np.ones(n // 2)]).astype(np.int64)

    # Add bias column
    X_with_bias = np.column_stack([np.ones(n), X_data])

    beta, log_lik, history = logistic_regression_mle(
        X_with_bias, y_data, learning_rate=0.1, max_iter=1000
    )

    # Check log-likelihood is increasing
    for i in range(1, len(history)):
        assert history[i] >= history[i - 1] - 1e-10, \
            f"Log-lik not monotonic at {i}: {history[i-1]:.6f} → {history[i]:.6f}"

    # Check accuracy
    y_pred = logistic_regression_predict(X_with_bias, beta)
    accuracy = np.mean(y_pred == y_data)
    assert accuracy > 0.9, f"Accuracy too low: {accuracy:.3f}"
    print(f"  PASS: logistic_regression_mle (accuracy={accuracy:.3f})")


if __name__ == "__main__":
    print("Testing mle.py ...")
    _test_mle_bernoulli()
    _test_mle_poisson()
    _test_mle_gaussian()
    _test_logistic_regression_mle()
    print("All MLE tests PASSED!")
