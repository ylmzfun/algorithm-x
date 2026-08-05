"""
Statistics for ML/AI Foundations.

Implements:
- Descriptive statistics: mean, median, mode, variance, std, covariance, correlation
- Central Limit Theorem demonstration
- Confidence intervals (z-interval, t-interval)
- Hypothesis testing (z-test, t-test, chi-squared test)
"""

import numpy as np
from numpy.typing import NDArray
from typing import Tuple, Dict, Optional
from math import sqrt, gamma as math_gamma


# ============================================================
# Descriptive Statistics
# ============================================================

def mean(data: NDArray[np.float64]) -> float:
    """Compute the arithmetic mean.

    x̄ = (1/n) * Σ xᵢ

    Args:
        data: 1D array of values.

    Returns:
        Sample mean.

    Complexity: O(n).
    """
    return float(np.mean(data))


def median(data: NDArray[np.float64]) -> float:
    """Compute the median (50th percentile).

    For odd n: the middle value.
    For even n: average of the two middle values.

    Args:
        data: 1D array of values.

    Returns:
        Median value.

    Complexity: O(n log n) due to sorting.
    """
    return float(np.median(data))


def mode(data: NDArray[np.float64]) -> Tuple[float, int]:
    """Find the most frequent value(s).

    Returns the first mode found and its frequency.
    For multiple modes, only the first (lowest value) is returned.

    Args:
        data: 1D array of values.

    Returns:
        Tuple (mode_value, frequency).

    Complexity: O(n).
    """
    values, counts = np.unique(data, return_counts=True)
    idx = np.argmax(counts)
    return float(values[idx]), int(counts[idx])


def variance(data: NDArray[np.float64], ddof: int = 1) -> float:
    """Compute the sample variance.

    s² = (1 / (n - ddof)) * Σ (xᵢ - x̄)²

    ddof=1 (default) gives the unbiased sample variance estimator.
    ddof=0 gives the population variance.

    Args:
        data: 1D array of values.
        ddof: Delta degrees of freedom (1 for sample, 0 for population).

    Returns:
        Variance.

    Complexity: O(n).
    """
    return float(np.var(data, ddof=ddof))


def std_dev(data: NDArray[np.float64], ddof: int = 1) -> float:
    """Compute the sample standard deviation.

    s = sqrt(variance(data, ddof))

    Args:
        data: 1D array of values.
        ddof: Delta degrees of freedom.

    Returns:
        Standard deviation.

    Complexity: O(n).
    """
    return float(np.std(data, ddof=ddof))


def covariance(x: NDArray[np.float64], y: NDArray[np.float64],
               ddof: int = 1) -> float:
    """Compute the sample covariance between two variables.

    cov(x, y) = (1 / (n - ddof)) * Σ (xᵢ - x̄)(yᵢ - ȳ)

    Measures how two variables vary together:
    - cov > 0: x and y tend to increase together.
    - cov < 0: as x increases, y tends to decrease.
    - cov ≈ 0: no linear relationship.

    Args:
        x, y: 1D arrays of same length.
        ddof: Delta degrees of freedom.

    Returns:
        Covariance.

    Raises:
        ValueError: If lengths differ.

    Complexity: O(n).
    """
    if len(x) != len(y):
        raise ValueError(f"Length mismatch: {len(x)} vs {len(y)}")
    n = len(x)
    return float(np.sum((x - np.mean(x)) * (y - np.mean(y))) / (n - ddof))


def correlation(x: NDArray[np.float64], y: NDArray[np.float64]) -> float:
    """Compute the Pearson correlation coefficient.

    r = cov(x, y) / (s_x * s_y)

    r ∈ [-1, 1]:
    - r = 1: perfect positive linear relationship.
    - r = -1: perfect negative linear relationship.
    - r = 0: no linear correlation.

    Args:
        x, y: 1D arrays of same length.

    Returns:
        Correlation coefficient in [-1, 1].

    Raises:
        ValueError: If lengths differ or std dev is 0.

    Complexity: O(n).
    """
    if len(x) != len(y):
        raise ValueError(f"Length mismatch: {len(x)} vs {len(y)}")
    cov_xy = covariance(x, y, ddof=1)
    sx = std_dev(x, ddof=1)
    sy = std_dev(y, ddof=1)
    if sx == 0 or sy == 0:
        raise ValueError("Correlation undefined when std dev is zero")
    return cov_xy / (sx * sy)


# ============================================================
# Central Limit Theorem Demo
# ============================================================

def central_limit_theorem_demo(
    distribution: str = "uniform",
    sample_size: int = 30,
    n_samples: int = 5000
) -> Dict[str, NDArray[np.float64]]:
    """Demonstrate the Central Limit Theorem (CLT).

    CLT: The distribution of sample means approaches a Normal distribution
    as the sample size increases, REGARDLESS of the original distribution
    (given finite variance).

    This function:
    1. Draws n_samples batches, each of size sample_size, from the
       specified distribution.
    2. Computes the mean of each batch.
    3. Returns the distribution of sample means.

    Args:
        distribution: Original distribution ("uniform", "exponential",
                      "bernoulli", "poisson").
        sample_size: Size of each sample (n in CLT).
        n_samples: Number of sample means to compute.

    Returns:
        Dictionary with keys:
            - 'sample_means': Array of sample means (n_samples,).
            - 'population_mean': True population mean μ.
            - 'population_std': True population std σ.
            - 'expected_mean_of_means': μ (should equal population_mean).
            - 'expected_std_of_means': σ / √n (standard error).
            - 'observed_mean_of_means': Actual mean of sample_means.
            - 'observed_std_of_means': Actual std of sample_means.
    """
    np.random.seed(42)

    # Define distribution parameters
    if distribution == "uniform":
        # Uniform[0, 1]
        pop_mean = 0.5
        pop_std = sqrt(1.0 / 12.0)
        samples = np.random.uniform(0, 1, size=(n_samples, sample_size))

    elif distribution == "exponential":
        # Exponential(λ=1), μ=1, σ=1
        pop_mean = 1.0
        pop_std = 1.0
        samples = np.random.exponential(1.0, size=(n_samples, sample_size))

    elif distribution == "bernoulli":
        # Bernoulli(p=0.3), μ=0.3, σ=√(0.21) ≈ 0.458
        p = 0.3
        pop_mean = p
        pop_std = sqrt(p * (1 - p))
        samples = np.random.binomial(1, p, size=(n_samples, sample_size))

    elif distribution == "poisson":
        # Poisson(λ=5), μ=5, σ=√5 ≈ 2.236
        lam = 5.0
        pop_mean = lam
        pop_std = sqrt(lam)
        samples = np.random.poisson(lam, size=(n_samples, sample_size))

    else:
        raise ValueError(f"Unknown distribution: {distribution}")

    sample_means = np.mean(samples, axis=1)

    return {
        'sample_means': sample_means,
        'population_mean': pop_mean,
        'population_std': pop_std,
        'expected_mean_of_means': pop_mean,
        'expected_std_of_means': pop_std / sqrt(sample_size),
        'observed_mean_of_means': float(np.mean(sample_means)),
        'observed_std_of_means': float(np.std(sample_means, ddof=1)),
    }


# ============================================================
# Confidence Intervals
# ============================================================

def z_confidence_interval(
    data: NDArray[np.float64],
    confidence: float = 0.95,
    population_std: Optional[float] = None
) -> Tuple[float, float, float]:
    """Compute a z-confidence interval for the population mean.

    Assumes the population is normally distributed OR the sample size
    is large enough (n ≥ 30) by CLT. Uses known population std or
    estimates from large samples.

    CI = x̄ ± z_{α/2} * σ / √n

    Args:
        data: 1D array of sample values.
        confidence: Confidence level (default 0.95 for 95% CI).
        population_std: Known population std. If None, uses sample std
                        (valid for n ≥ 30).

    Returns:
        Tuple (lower_bound, upper_bound, margin_of_error).

    Complexity: O(n).
    """
    n = len(data)
    x_bar = mean(data)

    # z-critical value for given confidence
    alpha = 1.0 - confidence
    # z_{α/2}: two-tailed
    from scipy.stats import norm
    z_crit = norm.ppf(1.0 - alpha / 2.0)

    sigma = population_std if population_std is not None else std_dev(data, ddof=1)
    margin = z_crit * sigma / sqrt(n)

    return x_bar - margin, x_bar + margin, margin


def t_confidence_interval(
    data: NDArray[np.float64],
    confidence: float = 0.95
) -> Tuple[float, float, float]:
    """Compute a t-confidence interval for the population mean.

    Used when population std is unknown (estimated from sample).
    Appropriate for small samples (n < 30) from a normal population.

    CI = x̄ ± t_{α/2, n-1} * s / √n

    where s is the sample standard deviation and t uses n-1 degrees of freedom.

    Args:
        data: 1D array of sample values.
        confidence: Confidence level (default 0.95 for 95% CI).

    Returns:
        Tuple (lower_bound, upper_bound, margin_of_error).

    Complexity: O(n).
    """
    n = len(data)
    x_bar = mean(data)
    s = std_dev(data, ddof=1)

    from scipy.stats import t as t_dist
    alpha = 1.0 - confidence
    t_crit = t_dist.ppf(1.0 - alpha / 2.0, df=n - 1)

    margin = t_crit * s / sqrt(n)

    return x_bar - margin, x_bar + margin, margin


# ============================================================
# Hypothesis Testing
# ============================================================

def z_test(
    data: NDArray[np.float64],
    mu0: float,
    population_std: Optional[float] = None,
    alternative: str = "two-sided"
) -> Dict[str, float]:
    """Perform a one-sample z-test.

    H₀: μ = μ₀ (null hypothesis: population mean equals μ₀)
    H₁: μ ≠ μ₀, μ > μ₀, or μ < μ₀ (alternative)

    Test statistic: z = (x̄ - μ₀) / (σ / √n)

    Args:
        data: Sample data.
        mu0: Null hypothesis mean value.
        population_std: Known population std. If None, uses sample std.
        alternative: "two-sided", "greater", or "less".

    Returns:
        Dictionary with keys: 'z_statistic', 'p_value', 'reject' (bool at α=0.05),
        'conclusion'.

    Complexity: O(n).
    """
    from scipy.stats import norm

    n = len(data)
    x_bar = mean(data)
    sigma = population_std if population_std is not None else std_dev(data, ddof=1)

    z = (x_bar - mu0) / (sigma / sqrt(n))

    if alternative == "two-sided":
        p_value = 2.0 * (1.0 - norm.cdf(abs(z)))
    elif alternative == "greater":
        p_value = 1.0 - norm.cdf(z)
    elif alternative == "less":
        p_value = norm.cdf(z)
    else:
        raise ValueError(f"Unknown alternative: {alternative}")

    reject = p_value < 0.05

    return {
        'z_statistic': z,
        'p_value': p_value,
        'reject': reject,
        'conclusion': (
            f"Reject H₀ at α=0.05" if reject
            else f"Fail to reject H₀ at α=0.05"
        ),
        'sample_mean': x_bar,
        'sample_size': n,
    }


def t_test(
    data: NDArray[np.float64],
    mu0: float,
    alternative: str = "two-sided"
) -> Dict[str, float]:
    """Perform a one-sample t-test.

    Uses Student's t-distribution (n-1 degrees of freedom).
    Appropriate when population std is unknown.

    H₀: μ = μ₀
    Test statistic: t = (x̄ - μ₀) / (s / √n),  df = n - 1

    Args:
        data: Sample data.
        mu0: Null hypothesis mean.
        alternative: "two-sided", "greater", or "less".

    Returns:
        Dictionary with keys: 't_statistic', 'p_value', 'reject',
        'degrees_of_freedom', 'conclusion'.

    Complexity: O(n).
    """
    from scipy.stats import t as t_dist

    n = len(data)
    x_bar = mean(data)
    s = std_dev(data, ddof=1)

    t_stat = (x_bar - mu0) / (s / sqrt(n))
    df = n - 1

    if alternative == "two-sided":
        p_value = 2.0 * (1.0 - t_dist.cdf(abs(t_stat), df=df))
    elif alternative == "greater":
        p_value = 1.0 - t_dist.cdf(t_stat, df=df)
    elif alternative == "less":
        p_value = t_dist.cdf(t_stat, df=df)
    else:
        raise ValueError(f"Unknown alternative: {alternative}")

    reject = p_value < 0.05
    return {
        't_statistic': t_stat,
        'p_value': p_value,
        'degrees_of_freedom': df,
        'reject': reject,
        'conclusion': (
            f"Reject H₀ at α=0.05" if reject
            else f"Fail to reject H₀ at α=0.05"
        ),
        'sample_mean': x_bar,
        'sample_size': n,
    }


def chi_squared_test(
    observed: NDArray[np.float64],
    expected: NDArray[np.float64]
) -> Dict[str, float]:
    """Perform a chi-squared goodness-of-fit test.

    Tests whether observed frequencies differ significantly from
    expected frequencies under the null hypothesis.

    H₀: The data follow the expected distribution.
    H₁: The data do NOT follow the expected distribution.

    Test statistic: χ² = Σ (Oᵢ - Eᵢ)² / Eᵢ
    Degrees of freedom: k - 1 (where k = number of categories)

    Args:
        observed: Observed frequencies.
        expected: Expected frequencies under H₀ (same shape).

    Returns:
        Dictionary with keys: 'chi2_statistic', 'p_value', 'reject',
        'degrees_of_freedom', 'conclusion'.

    Complexity: O(k) where k = number of categories.
    """
    from scipy.stats import chi2

    observed = np.asarray(observed, dtype=np.float64)
    expected = np.asarray(expected, dtype=np.float64)

    if observed.shape != expected.shape:
        raise ValueError("Observed and expected must have same shape")
    if np.any(expected == 0):
        raise ValueError("Expected frequencies must be non-zero")

    chi2_stat = float(np.sum((observed - expected) ** 2 / expected))
    df = len(observed) - 1

    p_value = 1.0 - chi2.cdf(chi2_stat, df=df)
    reject = p_value < 0.05

    return {
        'chi2_statistic': chi2_stat,
        'p_value': p_value,
        'degrees_of_freedom': df,
        'reject': reject,
        'conclusion': (
            f"Reject H₀ at α=0.05 (data does NOT fit expected distribution)"
            if reject
            else f"Fail to reject H₀ at α=0.05 (data fits expected distribution)"
        ),
    }


# ============================================================
# Tests
# ============================================================

def _test_descriptive() -> None:
    data = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 5.0])
    assert abs(mean(data) - 20.0 / 6.0) < 1e-10
    assert abs(median(data) - 3.5) < 1e-10
    mode_val, mode_freq = mode(data)
    assert mode_val == 5.0 and mode_freq == 2

    # Variance and std
    var_s = variance(data, ddof=1)  # sample variance
    # mean=20/6=3.333, deviations: -2.333, -1.333, -0.333, 0.667, 1.667, 1.667
    # squared: 5.444, 1.778, 0.111, 0.444, 2.778, 2.778 → sum=13.333, /5=2.667
    assert abs(var_s - 13.333 / 5.0) < 1e-3
    assert abs(std_dev(data, ddof=1) - sqrt(var_s)) < 1e-10
    print("  PASS: descriptive statistics")


def _test_covariance_correlation() -> None:
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y = np.array([2.0, 4.0, 5.0, 4.0, 5.0])
    # Compare with numpy
    assert abs(covariance(x, y, ddof=1) - np.cov(x, y, ddof=1)[0, 1]) < 1e-10
    assert abs(correlation(x, y) - np.corrcoef(x, y)[0, 1]) < 1e-10

    # Perfect positive correlation
    z = 2 * x + 1
    assert abs(correlation(x, z) - 1.0) < 1e-10

    # Perfect negative
    w = -3 * x
    assert abs(correlation(x, w) + 1.0) < 1e-10
    print("  PASS: covariance and correlation")


def _test_clt() -> None:
    result = central_limit_theorem_demo("uniform", sample_size=30, n_samples=5000)
    # Observed mean of means should be close to population mean (0.5)
    assert abs(result['observed_mean_of_means'] - 0.5) < 0.03
    # Observed std of means should be close to σ/√n = (1/√12)/√30 ≈ 0.0527
    expected_se = sqrt(1.0 / 12.0) / sqrt(30)
    assert abs(result['observed_std_of_means'] - expected_se) < 0.01
    print("  PASS: central_limit_theorem")


def _test_confidence_intervals() -> None:
    np.random.seed(42)
    # Generate data from N(5, 2)
    data = np.random.normal(5.0, 2.0, size=100)

    # z-interval
    low_z, high_z, margin_z = z_confidence_interval(data, confidence=0.95)
    assert low_z < 5.0 < high_z, f"z-CI does not contain true mean: [{low_z}, {high_z}]"

    # t-interval
    low_t, high_t, margin_t = t_confidence_interval(data, confidence=0.95)
    assert low_t < 5.0 < high_t, f"t-CI does not contain true mean: [{low_t}, {high_t}]"
    print("  PASS: confidence_intervals")


def _test_hypothesis_testing() -> None:
    np.random.seed(42)
    # Generate data from N(5, 1), test H₀: μ = 5 (should not reject)
    data_h0 = np.random.normal(5.0, 1.0, size=50)
    result_z = z_test(data_h0, mu0=5.0)
    assert not result_z['reject'], f"Falsely rejected: {result_z}"

    result_t = t_test(data_h0, mu0=5.0)
    assert not result_t['reject'], f"Falsely rejected t-test"

    # Generate data from N(6, 1), test H₀: μ = 5 (should reject)
    data_h1 = np.random.normal(6.0, 1.0, size=50)
    result_z2 = z_test(data_h1, mu0=5.0)
    assert result_z2['reject'], f"Failed to reject: {result_z2}"

    # Chi-squared: fair die test
    observed = np.array([20.0, 18.0, 22.0, 15.0, 17.0, 28.0])
    expected = np.full(6, 120.0 / 6.0)
    chi2_result = chi_squared_test(observed, expected)
    assert 'chi2_statistic' in chi2_result
    # With these numbers, should not reject (p > 0.05)
    # 120 rolls, observed: 20,18,22,15,17,28; expected: 20 each
    # χ² = (0+4+4+25+9+64)/20 = 106/20 = 5.3, df=5, p ≈ 0.38
    assert not chi2_result['reject'], f"Chi2 falsely rejected: {chi2_result}"

    print("  PASS: hypothesis_testing (z-test, t-test, chi-squared)")


if __name__ == "__main__":
    print("Testing statistics.py ...")
    _test_descriptive()
    _test_covariance_correlation()
    _test_clt()
    _test_confidence_intervals()
    _test_hypothesis_testing()
    print("All statistics tests PASSED!")
