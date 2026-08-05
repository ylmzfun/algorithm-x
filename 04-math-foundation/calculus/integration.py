"""
Numerical Integration Methods for ML/AI Foundations.

Implements:
- Riemann sum (left, right, midpoint)
- Trapezoidal rule
- Simpson's rule (1/3 rule)
- Monte Carlo integration

All methods approximate ∫ₐᵇ f(x) dx for scalar functions.
"""

import numpy as np
from numpy.typing import NDArray
from typing import Callable, Tuple


# ============================================================
# Riemann Sums
# ============================================================

def riemann_left(
    f: Callable[[float], float],
    a: float,
    b: float,
    n: int = 1000
) -> float:
    """Approximate ∫ₐᵇ f(x) dx using left Riemann sum.

    ∫ₐᵇ f(x) dx ≈ Σᵢ₌₀ⁿ⁻¹ f(xᵢ) * Δx,  where xᵢ = a + i·Δx

    Error: O(1/n) for smooth functions.

    Args:
        f: Integrand f: R → R.
        a: Lower limit.
        b: Upper limit.
        n: Number of subintervals.

    Returns:
        Approximate integral.

    Complexity: O(n) function evaluations.
    """
    dx = (b - a) / n
    total = 0.0
    for i in range(n):
        x = a + i * dx
        total += f(x)
    return total * dx


def riemann_right(
    f: Callable[[float], float],
    a: float,
    b: float,
    n: int = 1000
) -> float:
    """Approximate ∫ₐᵇ f(x) dx using right Riemann sum.

    ∫ₐᵇ f(x) dx ≈ Σᵢ₌₁ⁿ f(xᵢ) * Δx,  where xᵢ = a + i·Δx

    Error: O(1/n).

    Args:
        f: Integrand.
        a, b: Integration limits.
        n: Number of subintervals.

    Returns:
        Approximate integral.
    """
    dx = (b - a) / n
    total = 0.0
    for i in range(1, n + 1):
        x = a + i * dx
        total += f(x)
    return total * dx


def riemann_midpoint(
    f: Callable[[float], float],
    a: float,
    b: float,
    n: int = 1000
) -> float:
    """Approximate ∫ₐᵇ f(x) dx using midpoint rule.

    ∫ₐᵇ f(x) dx ≈ Σᵢ₌₀ⁿ⁻¹ f(xᵢ + Δx/2) * Δx

    Error: O(1/n²) — second-order accurate, better than left/right.

    Args:
        f: Integrand.
        a, b: Integration limits.
        n: Number of subintervals.

    Returns:
        Approximate integral.
    """
    dx = (b - a) / n
    total = 0.0
    for i in range(n):
        x_mid = a + (i + 0.5) * dx
        total += f(x_mid)
    return total * dx


# ============================================================
# Trapezoidal Rule
# ============================================================

def trapezoidal(
    f: Callable[[float], float],
    a: float,
    b: float,
    n: int = 1000
) -> float:
    """Approximate ∫ₐᵇ f(x) dx using the composite trapezoidal rule.

    ∫ₐᵇ f(x) dx ≈ (Δx/2) * [f(x₀) + 2f(x₁) + ... + 2f(xₙ₋₁) + f(xₙ)]

    Error: O(1/n²) for smooth functions.

    Geometrically: approximates area under curve with trapezoids.

    Args:
        f: Integrand.
        a, b: Integration limits.
        n: Number of subintervals.

    Returns:
        Approximate integral.

    Complexity: O(n) function evaluations.
    """
    dx = (b - a) / n
    total = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        x = a + i * dx
        total += f(x)
    return total * dx


# ============================================================
# Simpson's Rule (1/3 Rule)
# ============================================================

def simpson(
    f: Callable[[float], float],
    a: float,
    b: float,
    n: int = 1000
) -> float:
    """Approximate ∫ₐᵇ f(x) dx using Simpson's 1/3 rule.

    ∫ₐᵇ f(x) dx ≈ (Δx/3) * [f(x₀) + 4f(x₁) + 2f(x₂) + 4f(x₃) + ... + f(xₙ)]

    Pattern: endpoints ×1, odd indices ×4, even indices ×2.

    Error: O(1/n⁴) — fourth-order accurate. Much more accurate than
    trapezoidal for the same number of points. Requires n to be even.

    Based on fitting quadratic polynomials to pairs of subintervals.

    Args:
        f: Integrand.
        a, b: Integration limits.
        n: Number of subintervals (must be even; will be adjusted if odd).

    Returns:
        Approximate integral.

    Complexity: O(n) function evaluations.

    Example:
        >>> simpson(lambda x: x**2, 0, 1, n=100)
        0.3333333333333333  # ∫₀¹ x² dx = 1/3
    """
    if n % 2 != 0:
        n += 1  # Simpson's rule requires even n

    dx = (b - a) / n
    total = f(a) + f(b)

    for i in range(1, n):
        x = a + i * dx
        if i % 2 == 0:
            total += 2.0 * f(x)
        else:
            total += 4.0 * f(x)

    return total * dx / 3.0


# ============================================================
# Monte Carlo Integration
# ============================================================

def monte_carlo_1d(
    f: Callable[[float], float],
    a: float,
    b: float,
    n: int = 10000
) -> Tuple[float, float]:
    """Approximate ∫ₐᵇ f(x) dx using Monte Carlo integration.

    ∫ₐᵇ f(x) dx ≈ (b - a) * (1/n) * Σᵢ f(xᵢ)

    where xᵢ ~ Uniform(a, b).

    Error: O(1/√n) — converges slowly but works for ANY dimension.
    The strength of Monte Carlo is that the convergence rate does NOT
    depend on the dimension, unlike grid-based methods.

    Args:
        f: Integrand.
        a, b: Integration limits.
        n: Number of random samples.

    Returns:
        Tuple (estimate, standard_error):
            estimate: Approximate integral.
            standard_error: Estimated error σ/√n.

    Complexity: O(n) function evaluations.
    """
    np.random.seed(42)
    samples = np.random.uniform(a, b, size=n)
    values = np.array([f(x) for x in samples])

    volume = b - a
    estimate = volume * np.mean(values)

    # Standard error of the mean
    std_error = volume * np.std(values, ddof=1) / np.sqrt(n)

    return float(estimate), float(std_error)


def monte_carlo_nd(
    f: Callable[[NDArray[np.float64]], float],
    bounds: NDArray[np.float64],
    n: int = 10000
) -> Tuple[float, float]:
    """Approximate multidimensional integral using Monte Carlo.

    ∫_{bounds} f(x) dx ≈ volume * (1/n) * Σᵢ f(xᵢ)

    where xᵢ ~ Uniform in the hyper-rectangle defined by bounds.

    Args:
        f: Integrand f: Rᵈ → R.
        bounds: Array of shape (d, 2) where bounds[i] = [lower_i, upper_i].
        n: Number of random samples.

    Returns:
        Tuple (estimate, standard_error).

    Complexity: O(nd) function evaluations (d = dimension).
    """
    np.random.seed(42)
    d = bounds.shape[0]

    # Volume of the hyper-rectangle
    volume = np.prod(bounds[:, 1] - bounds[:, 0])

    # Generate uniform samples
    samples = np.random.uniform(
        bounds[:, 0], bounds[:, 1], size=(n, d)
    )
    values = np.array([f(samples[i]) for i in range(n)])

    estimate = volume * np.mean(values)
    std_error = volume * np.std(values, ddof=1) / np.sqrt(n)

    return float(estimate), float(std_error)


# ============================================================
# Tests
# ============================================================

def _test_riemann() -> None:
    f = lambda x: x**2
    a, b, n = 0.0, 1.0, 10000

    approx_left = riemann_left(f, a, b, n)
    approx_right = riemann_right(f, a, b, n)
    approx_mid = riemann_midpoint(f, a, b, n)

    true_val = 1.0 / 3.0  # ∫₀¹ x² dx = 1/3
    assert abs(approx_left - true_val) < 1e-3, f"FAIL left: {approx_left}"
    assert abs(approx_right - true_val) < 1e-3, f"FAIL right: {approx_right}"
    assert abs(approx_mid - true_val) < 1e-5, \
        f"FAIL midpoint: {approx_mid} (should be more accurate)"

    # Midpoint should be more accurate than left/right
    assert (abs(approx_mid - true_val) < abs(approx_left - true_val))
    print("  PASS: Riemann sums (left, right, midpoint)")


def _test_trapezoidal() -> None:
    import math
    f = math.sin
    a, b, n = 0.0, math.pi, 10000
    approx = trapezoidal(f, a, b, n)
    true_val = 2.0  # ∫₀^π sin(x) dx = 2
    assert abs(approx - true_val) < 1e-7, f"FAIL: {approx}"
    print("  PASS: trapezoidal")


def _test_simpson() -> None:
    import math
    # ∫₀¹ x² dx = 1/3
    approx1 = simpson(lambda x: x**2, 0, 1, n=100)
    assert abs(approx1 - 1.0/3.0) < 1e-10, f"FAIL x²: {approx1}"

    # ∫₀^π sin(x) dx = 2
    approx2 = simpson(math.sin, 0, math.pi, n=500)
    assert abs(approx2 - 2.0) < 1e-10, f"FAIL sin: {approx2}"

    # ∫₀¹ e^x dx = e - 1 ≈ 1.71828
    approx3 = simpson(math.exp, 0, 1, n=100)
    assert abs(approx3 - (math.e - 1.0)) < 1e-10, f"FAIL exp: {approx3}"

    print("  PASS: Simpson's rule")


def _test_monte_carlo() -> None:
    import math
    f = lambda x: math.sin(x)
    estimate, se = monte_carlo_1d(f, 0, math.pi, n=50000)
    true_val = 2.0
    # Should be within ~3 standard errors
    assert abs(estimate - true_val) < 3 * se + 0.05, \
        f"FAIL MC: estimate={estimate:.4f}, se={se:.4f}"

    # 2D Monte Carlo: ∫₀¹∫₀¹ x*y dx dy = 1/4
    f2d = lambda v: v[0] * v[1]
    bounds = np.array([[0.0, 1.0], [0.0, 1.0]])
    est2d, se2d = monte_carlo_nd(f2d, bounds, n=20000)
    true_2d = 0.25
    assert abs(est2d - true_2d) < 0.02, f"FAIL MC 2D: {est2d}"
    print(f"  PASS: Monte Carlo (1D est={estimate:.4f}, 2D est={est2d:.4f})")


if __name__ == "__main__":
    import math
    from typing import Tuple
    print("Testing integration.py ...")
    _test_riemann()
    _test_trapezoidal()
    _test_simpson()
    _test_monte_carlo()
    print("All integration tests PASSED!")
