"""
Probability Distributions for ML/AI Foundations.

Implements key discrete and continuous distributions:
- Discrete: Bernoulli, Binomial, Poisson, Discrete Uniform
- Continuous: Gaussian (Normal), Exponential, Continuous Uniform

Each distribution provides: PMF/PDF, CDF, mean, variance, random sampling.
"""

import numpy as np
from numpy.typing import NDArray
from typing import Tuple, Union
from math import factorial, exp, sqrt, pi, log


# ============================================================
# Bernoulli Distribution
# ============================================================

class Bernoulli:
    """Bernoulli distribution: single binary trial with success probability p.

    PMF: P(X = k) = p^k * (1-p)^(1-k),  k ∈ {0, 1}
    Mean: p
    Variance: p * (1 - p)

    Example uses: coin flip, binary classification label, click-through.
    """

    def __init__(self, p: float):
        """
        Args:
            p: Probability of success, 0 ≤ p ≤ 1.

        Raises:
            ValueError: If p is not in [0, 1].
        """
        if not 0 <= p <= 1:
            raise ValueError(f"p must be in [0, 1], got {p}")
        self.p = p

    def pmf(self, k: int) -> float:
        """Probability mass function: P(X = k).

        Args:
            k: 0 or 1.

        Returns:
            P(X = k).
        """
        if k == 0:
            return 1.0 - self.p
        elif k == 1:
            return self.p
        else:
            return 0.0

    def cdf(self, k: int) -> float:
        """Cumulative distribution function: P(X ≤ k).

        Args:
            k: Value to evaluate CDF at.

        Returns:
            P(X ≤ k).
        """
        if k < 0:
            return 0.0
        elif k < 1:
            return 1.0 - self.p
        else:
            return 1.0

    def mean(self) -> float:
        """Expected value: E[X] = p."""
        return self.p

    def variance(self) -> float:
        """Variance: Var[X] = p(1-p)."""
        return self.p * (1.0 - self.p)

    def sample(self, size: int = 1) -> NDArray[np.int64]:
        """Generate random samples.

        Args:
            size: Number of samples.

        Returns:
            Array of 0s and 1s of shape (size,).
        """
        return np.random.binomial(1, self.p, size=size)


# ============================================================
# Binomial Distribution
# ============================================================

class Binomial:
    """Binomial distribution: n independent Bernoulli trials.

    PMF: P(X = k) = C(n,k) * p^k * (1-p)^(n-k),  k = 0, 1, ..., n
    where C(n,k) = n! / (k! * (n-k)!)

    Mean: n * p
    Variance: n * p * (1 - p)

    Example: number of heads in n coin flips, number of successes in n trials.
    """

    def __init__(self, n: int, p: float):
        """
        Args:
            n: Number of trials (positive integer).
            p: Success probability, 0 ≤ p ≤ 1.
        """
        if n <= 0:
            raise ValueError(f"n must be positive, got {n}")
        if not 0 <= p <= 1:
            raise ValueError(f"p must be in [0, 1], got {p}")
        self.n = n
        self.p = p

    def pmf(self, k: int) -> float:
        """Probability mass function: P(X = k).

        Args:
            k: Number of successes (0 ≤ k ≤ n).

        Returns:
            P(X = k). Returns 0 if k is out of range.
        """
        if k < 0 or k > self.n:
            return 0.0
        from math import comb
        return comb(self.n, k) * (self.p ** k) * ((1.0 - self.p) ** (self.n - k))

    def cdf(self, k: float) -> float:
        """Cumulative distribution function: P(X ≤ k).

        Uses summation of PMF values.

        Args:
            k: Upper bound.

        Returns:
            P(X ≤ k).
        """
        k_floor = int(np.floor(k))
        if k_floor < 0:
            return 0.0
        if k_floor >= self.n:
            return 1.0
        return sum(self.pmf(i) for i in range(k_floor + 1))

    def mean(self) -> float:
        """E[X] = n * p."""
        return self.n * self.p

    def variance(self) -> float:
        """Var[X] = n * p * (1 - p)."""
        return self.n * self.p * (1.0 - self.p)

    def sample(self, size: int = 1) -> NDArray[np.int64]:
        """Generate random samples.

        Args:
            size: Number of samples.

        Returns:
            Array of shape (size,).
        """
        return np.random.binomial(self.n, self.p, size=size)


# ============================================================
# Poisson Distribution
# ============================================================

class Poisson:
    """Poisson distribution: counts of events in fixed interval.

    PMF: P(X = k) = (λ^k * e^(-λ)) / k!,  k = 0, 1, 2, ...

    Mean: λ
    Variance: λ

    When λ is large, Poisson approximates Normal(λ, λ).
    The Poisson is the limit of Binomial(n, p) as n → ∞ with np = λ constant.

    Example: website visits per hour, radioactive decay counts,
             number of mutations in DNA strand.
    """

    def __init__(self, lam: float):
        """
        Args:
            lam: Rate parameter λ > 0.
        """
        if lam <= 0:
            raise ValueError(f"λ must be positive, got {lam}")
        self.lam = lam

    def pmf(self, k: int) -> float:
        """Probability mass function: P(X = k) = λ^k e^{-λ} / k!.

        Uses log-computation for numerical stability with large k.

        Args:
            k: Count value (non-negative integer).

        Returns:
            P(X = k).
        """
        if k < 0:
            return 0.0
        # log(PMF) = k * log(λ) - λ - log(k!)
        # Use log-gamma for factorial stability
        from math import lgamma
        log_pmf = k * log(self.lam) - self.lam - lgamma(k + 1)
        return exp(log_pmf)

    def cdf(self, k: float) -> float:
        """Cumulative distribution function via summation.

        Args:
            k: Upper bound.

        Returns:
            P(X ≤ k).
        """
        k_floor = int(np.floor(k))
        if k_floor < 0:
            return 0.0
        return sum(self.pmf(i) for i in range(k_floor + 1))

    def mean(self) -> float:
        """E[X] = λ."""
        return self.lam

    def variance(self) -> float:
        """Var[X] = λ."""
        return self.lam

    def sample(self, size: int = 1) -> NDArray[np.int64]:
        """Generate random samples.

        Args:
            size: Number of samples.

        Returns:
            Array of shape (size,).
        """
        return np.random.poisson(self.lam, size=size)


# ============================================================
# Gaussian (Normal) Distribution
# ============================================================

class Gaussian:
    """Gaussian (Normal) distribution: the bell curve.

    PDF: f(x) = (1 / (σ√(2π))) * exp(-(x - μ)² / (2σ²))

    Mean: μ
    Variance: σ²

    Central role in ML: noise model, prior distribution, latent variables,
    and the foundation of the Central Limit Theorem.

    The standard normal has μ = 0, σ = 1.
    """

    def __init__(self, mu: float = 0.0, sigma: float = 1.0):
        """
        Args:
            mu: Mean μ.
            sigma: Standard deviation σ > 0.
        """
        if sigma <= 0:
            raise ValueError(f"σ must be positive, got {sigma}")
        self.mu = mu
        self.sigma = sigma
        self._norm_const = 1.0 / (sigma * sqrt(2.0 * pi))

    def pdf(self, x: Union[float, NDArray[np.float64]]) -> NDArray[np.float64]:
        """Probability density function.

        Args:
            x: Value(s) to evaluate PDF at. Scalar or numpy array.

        Returns:
            PDF value(s).
        """
        x = np.asarray(x, dtype=np.float64)
        z = (x - self.mu) / self.sigma
        return self._norm_const * np.exp(-0.5 * z ** 2)

    def cdf(self, x: Union[float, NDArray[np.float64]]) -> NDArray[np.float64]:
        """Cumulative distribution function using the error function.

        Φ(x) = (1/2) * [1 + erf((x - μ) / (σ√2))]

        Args:
            x: Value(s) to evaluate CDF at.

        Returns:
            CDF value(s).
        """
        from math import erf
        x = np.asarray(x, dtype=np.float64)
        return 0.5 * (1.0 + np.vectorize(erf)((x - self.mu) / (self.sigma * sqrt(2.0))))

    def mean(self) -> float:
        """E[X] = μ."""
        return self.mu

    def variance(self) -> float:
        """Var[X] = σ²."""
        return self.sigma ** 2

    def sample(self, size: int = 1) -> NDArray[np.float64]:
        """Generate random samples.

        Args:
            size: Number of samples.

        Returns:
            Array of shape (size,).
        """
        return np.random.normal(self.mu, self.sigma, size=size)

    def z_score(self, x: float) -> float:
        """Compute z-score (standardization): z = (x - μ) / σ.

        Args:
            x: Value to standardize.

        Returns:
            z-score.
        """
        return (x - self.mu) / self.sigma


# ============================================================
# Exponential Distribution
# ============================================================

class Exponential:
    """Exponential distribution: time between events in a Poisson process.

    PDF: f(x) = λ * e^(-λx),  x ≥ 0
    CDF: F(x) = 1 - e^(-λx),  x ≥ 0

    Mean: 1/λ
    Variance: 1/λ²

    Memoryless property: P(X > s + t | X > s) = P(X > t).

    Example: time until next bus arrival, lifetime of electronic components,
             inter-arrival times in queuing systems.
    """

    def __init__(self, lam: float):
        """
        Args:
            lam: Rate parameter λ > 0.
        """
        if lam <= 0:
            raise ValueError(f"λ must be positive, got {lam}")
        self.lam = lam

    def pdf(self, x: Union[float, NDArray[np.float64]]) -> NDArray[np.float64]:
        """Probability density function: f(x) = λ e^(-λx), x ≥ 0.

        Args:
            x: Value(s).

        Returns:
            PDF value(s). Returns 0 for x < 0.
        """
        x = np.asarray(x, dtype=np.float64)
        result = np.where(x >= 0, self.lam * np.exp(-self.lam * x), 0.0)
        return result

    def cdf(self, x: Union[float, NDArray[np.float64]]) -> NDArray[np.float64]:
        """CDF: F(x) = 1 - e^(-λx), x ≥ 0.

        Args:
            x: Value(s).

        Returns:
            CDF value(s).
        """
        x = np.asarray(x, dtype=np.float64)
        result = np.where(x >= 0, 1.0 - np.exp(-self.lam * x), 0.0)
        return result

    def mean(self) -> float:
        """E[X] = 1/λ."""
        return 1.0 / self.lam

    def variance(self) -> float:
        """Var[X] = 1/λ²."""
        return 1.0 / (self.lam ** 2)

    def sample(self, size: int = 1) -> NDArray[np.float64]:
        """Generate random samples using inverse CDF method.

        Args:
            size: Number of samples.

        Returns:
            Array of shape (size,).
        """
        return np.random.exponential(1.0 / self.lam, size=size)


# ============================================================
# Uniform Distribution
# ============================================================

class UniformContinuous:
    """Continuous uniform distribution on [a, b].

    PDF: f(x) = 1 / (b - a),  a ≤ x ≤ b
    CDF: F(x) = (x - a) / (b - a),  a ≤ x ≤ b

    Mean: (a + b) / 2
    Variance: (b - a)² / 12

    Example: random number generation, prior for Bayesian models.
    """

    def __init__(self, a: float = 0.0, b: float = 1.0):
        """
        Args:
            a: Lower bound.
            b: Upper bound (b > a).
        """
        if b <= a:
            raise ValueError(f"Must have a < b, got a={a}, b={b}")
        self.a = a
        self.b = b
        self._pdf_val = 1.0 / (b - a)

    def pdf(self, x: Union[float, NDArray[np.float64]]) -> NDArray[np.float64]:
        """PDF: f(x) = 1/(b-a) for x in [a, b], 0 otherwise.

        Args:
            x: Value(s).

        Returns:
            PDF value(s).
        """
        x = np.asarray(x, dtype=np.float64)
        result = np.where((x >= self.a) & (x <= self.b), self._pdf_val, 0.0)
        return result

    def cdf(self, x: Union[float, NDArray[np.float64]]) -> NDArray[np.float64]:
        """CDF: F(x) = (x - a)/(b - a) for x in [a, b].

        Args:
            x: Value(s).

        Returns:
            CDF value(s).
        """
        x = np.asarray(x, dtype=np.float64)
        result = np.where(x < self.a, 0.0,
                          np.where(x > self.b, 1.0,
                                   (x - self.a) / (self.b - self.a)))
        return result

    def mean(self) -> float:
        """E[X] = (a + b) / 2."""
        return (self.a + self.b) / 2.0

    def variance(self) -> float:
        """Var[X] = (b - a)² / 12."""
        return (self.b - self.a) ** 2 / 12.0

    def sample(self, size: int = 1) -> NDArray[np.float64]:
        """Generate random samples.

        Args:
            size: Number of samples.

        Returns:
            Array of shape (size,).
        """
        return np.random.uniform(self.a, self.b, size=size)


class UniformDiscrete:
    """Discrete uniform distribution on {a, a+1, ..., b}.

    PMF: P(X = k) = 1 / (b - a + 1),  k = a, ..., b
    Mean: (a + b) / 2
    Variance: (n² - 1) / 12 where n = b - a + 1

    Example: fair die roll, random integer generation.
    """

    def __init__(self, a: int, b: int):
        """
        Args:
            a: Lower bound (inclusive).
            b: Upper bound (inclusive), b ≥ a.
        """
        if b < a:
            raise ValueError(f"Must have a ≤ b, got a={a}, b={b}")
        self.a = a
        self.b = b
        self.n = b - a + 1
        self._pmf_val = 1.0 / self.n

    def pmf(self, k: int) -> float:
        """PMF: P(X = k) = 1/n for k in {a, ..., b}."""
        if self.a <= k <= self.b:
            return self._pmf_val
        return 0.0

    def cdf(self, k: float) -> float:
        """CDF: P(X ≤ k)."""
        k_floor = int(np.floor(k))
        if k_floor < self.a:
            return 0.0
        if k_floor >= self.b:
            return 1.0
        return (k_floor - self.a + 1) / self.n

    def mean(self) -> float:
        """E[X] = (a + b) / 2."""
        return (self.a + self.b) / 2.0

    def variance(self) -> float:
        """Var[X] = (n² - 1) / 12."""
        return (self.n ** 2 - 1) / 12.0

    def sample(self, size: int = 1) -> NDArray[np.int64]:
        """Generate random samples.

        Args:
            size: Number of samples.

        Returns:
            Array of shape (size,).
        """
        return np.random.randint(self.a, self.b + 1, size=size)


# ============================================================
# Tests
# ============================================================

def _test_bernoulli() -> None:
    b = Bernoulli(p=0.3)
    assert b.pmf(1) == 0.3
    assert b.pmf(0) == 0.7
    assert b.mean() == 0.3
    assert abs(b.variance() - 0.21) < 1e-10
    samples = b.sample(1000)
    assert np.all((samples == 0) | (samples == 1))
    assert abs(np.mean(samples) - 0.3) < 0.1  # probabilistic
    print("  PASS: Bernoulli")


def _test_binomial() -> None:
    binom = Binomial(n=10, p=0.5)
    # P(X = 5) = C(10,5) * 0.5^10 = 252/1024 ≈ 0.246
    assert abs(binom.pmf(5) - 252 / 1024) < 1e-10
    assert binom.mean() == 5.0
    assert binom.variance() == 2.5
    assert binom.pmf(-1) == 0.0
    assert binom.pmf(11) == 0.0
    samples = binom.sample(2000)
    assert 4.5 < np.mean(samples) < 5.5
    print("  PASS: Binomial")


def _test_poisson() -> None:
    pois = Poisson(lam=4.0)
    # P(X = 0) = e^{-4} ≈ 0.0183
    assert abs(pois.pmf(0) - exp(-4.0)) < 1e-10
    # P(X = 2) = 4^2 * e^{-4} / 2! = 8 * e^{-4} ≈ 0.1465
    expected_2 = 8.0 * exp(-4.0)
    assert abs(pois.pmf(2) - expected_2) < 1e-10
    assert pois.mean() == 4.0
    assert pois.variance() == 4.0
    samples = pois.sample(2000)
    assert 3.5 < np.mean(samples) < 4.5
    print("  PASS: Poisson")


def _test_gaussian() -> None:
    g = Gaussian(mu=2.0, sigma=0.5)
    # PDF at mean: 1/(σ√(2π)) = 1/(0.5 * √(2π)) ≈ 0.7979
    pdf_mean = 1.0 / (0.5 * sqrt(2 * pi))
    assert abs(g.pdf(2.0) - pdf_mean) < 1e-10
    # CDF at mean should be 0.5
    assert abs(g.cdf(2.0) - 0.5) < 1e-10
    assert g.mean() == 2.0
    assert g.variance() == 0.25
    assert abs(g.z_score(2.5) - 1.0) < 1e-10
    samples = g.sample(5000)
    assert 1.8 < np.mean(samples) < 2.2
    assert 0.4 < np.std(samples) < 0.6
    print("  PASS: Gaussian")


def _test_exponential() -> None:
    exp_dist = Exponential(lam=2.0)
    assert exp_dist.mean() == 0.5
    assert exp_dist.variance() == 0.25
    # PDF at 0 = λ = 2.0
    assert abs(exp_dist.pdf(0.0) - 2.0) < 1e-10
    # PDF for x < 0 = 0
    assert exp_dist.pdf(-1.0) == 0.0
    # CDF at 0 = 0
    assert abs(exp_dist.cdf(0.0)) < 1e-10
    samples = exp_dist.sample(5000)
    assert 0.4 < np.mean(samples) < 0.6
    print("  PASS: Exponential")


def _test_uniform() -> None:
    uc = UniformContinuous(a=2.0, b=5.0)
    assert uc.pdf(3.0) == 1.0 / 3.0
    assert uc.pdf(1.0) == 0.0
    assert uc.pdf(6.0) == 0.0
    assert uc.cdf(2.0) == 0.0
    assert uc.cdf(5.0) == 1.0
    assert uc.cdf(3.5) == 0.5
    assert uc.mean() == 3.5
    assert abs(uc.variance() - 9.0 / 12.0) < 1e-10

    ud = UniformDiscrete(a=1, b=6)  # fair die
    assert ud.pmf(3) == 1.0 / 6.0
    assert ud.pmf(7) == 0.0
    assert ud.mean() == 3.5
    assert abs(ud.variance() - 35.0 / 12.0) < 1e-10
    samples = ud.sample(6000)
    assert 3.3 < np.mean(samples) < 3.7
    print("  PASS: Uniform (continuous + discrete)")


if __name__ == "__main__":
    print("Testing distributions.py ...")
    _test_bernoulli()
    _test_binomial()
    _test_poisson()
    _test_gaussian()
    _test_exponential()
    _test_uniform()
    print("All distribution tests PASSED!")
