"""
Numerical Derivatives and Differentiation for ML/AI Foundations.

Implements:
- Numerical derivatives (forward difference, central difference)
- Gradient computation in multiple variables
- Partial derivatives
- Chain rule via finite differences
"""

import numpy as np
from numpy.typing import NDArray
from typing import Callable, Tuple


# ============================================================
# Scalar Derivatives
# ============================================================

def forward_difference(
    f: Callable[[float], float],
    x: float,
    h: float = 1e-6
) -> float:
    """Compute the first derivative using forward difference.

    f'(x) ≈ (f(x + h) - f(x)) / h

    Error: O(h) — first-order accurate.

    Easy to implement, but asymmetric (not great for optimization).

    Args:
        f: Scalar function f: R → R.
        x: Point at which to evaluate the derivative.
        h: Step size (default 1e-6).

    Returns:
        Approximate derivative f'(x).

    Complexity: O(1) function evaluations.
    """
    return (f(x + h) - f(x)) / h


def central_difference(
    f: Callable[[float], float],
    x: float,
    h: float = 1e-6
) -> float:
    """Compute the first derivative using central difference.

    f'(x) ≈ (f(x + h) - f(x - h)) / (2h)

    Error: O(h²) — second-order accurate.
    This is the preferred method for numerical differentiation.

    Args:
        f: Scalar function f: R → R.
        x: Point to evaluate.
        h: Step size.

    Returns:
        Approximate derivative f'(x).

    Complexity: O(1) function evaluations.

    Example:
        >>> central_difference(lambda x: x**2, 3.0)
        6.0  # d/dx x² = 2x, at x=3 → 6
    """
    return (f(x + h) - f(x - h)) / (2.0 * h)


def second_derivative_central(
    f: Callable[[float], float],
    x: float,
    h: float = 1e-5
) -> float:
    """Compute the second derivative using central difference.

    f''(x) ≈ (f(x + h) - 2f(x) + f(x - h)) / h²

    Error: O(h²).

    Args:
        f: Scalar function.
        x: Point to evaluate.
        h: Step size.

    Returns:
        Approximate second derivative f''(x).

    Complexity: O(1) function evaluations.
    """
    return (f(x + h) - 2.0 * f(x) + f(x - h)) / (h ** 2)


# ============================================================
# Multivariate: Gradient
# ============================================================

def gradient(
    f: Callable[[NDArray[np.float64]], float],
    x: NDArray[np.float64],
    h: float = 1e-6
) -> NDArray[np.float64]:
    """Compute the gradient ∇f(x) using central differences.

    ∇f(x) = (∂f/∂x₁, ∂f/∂x₂, ..., ∂f/∂xₙ)

    Each partial derivative is approximated via central difference:
        ∂f/∂xᵢ ≈ (f(x + h·eᵢ) - f(x - h·eᵢ)) / (2h)

    where eᵢ is the i-th standard basis vector.

    Args:
        f: Scalar-valued function f: Rⁿ → R.
        x: Point (n,) at which to evaluate.
        h: Step size.

    Returns:
        Gradient vector of shape (n,).

    Complexity: O(n) function evaluations (2n for central diff).

    Example:
        >>> f = lambda x: x[0]**2 + x[1]**3
        >>> gradient(f, np.array([1.0, 2.0]))
        array([2.0, 12.0])  # ∂/∂x₁ = 2x₁ = 2, ∂/∂x₂ = 3x₂² = 12
    """
    x = np.asarray(x, dtype=np.float64)
    n = len(x)
    grad = np.zeros(n, dtype=np.float64)

    for i in range(n):
        x_plus = x.copy()
        x_minus = x.copy()
        x_plus[i] += h
        x_minus[i] -= h
        grad[i] = (f(x_plus) - f(x_minus)) / (2.0 * h)

    return grad


def partial_derivative(
    f: Callable[[NDArray[np.float64]], float],
    x: NDArray[np.float64],
    var_idx: int,
    h: float = 1e-6
) -> float:
    """Compute a single partial derivative ∂f/∂x_i using central difference.

    Args:
        f: Scalar-valued function f: Rⁿ → R.
        x: Point (n,).
        var_idx: Index of the variable to differentiate with respect to.
        h: Step size.

    Returns:
        Approximate partial derivative ∂f/∂x_var_idx.
    """
    x = np.asarray(x, dtype=np.float64)
    x_plus = x.copy()
    x_minus = x.copy()
    x_plus[var_idx] += h
    x_minus[var_idx] -= h
    return (f(x_plus) - f(x_minus)) / (2.0 * h)


# ============================================================
# Chain Rule: Numerical Verification
# ============================================================

def chain_rule_1d(
    f: Callable[[float], float],
    g: Callable[[float], float],
    x: float,
    h: float = 1e-6
) -> Tuple[float, float]:
    """Numerically verify the chain rule: d/dx f(g(x)) = f'(g(x)) * g'(x).

    Computes:
    1. Direct derivative of h(x) = f(g(x)) via central difference.
    2. Chain rule formula: f'(g(x)) * g'(x).

    Args:
        f: Outer function.
        g: Inner function.
        x: Point to evaluate.
        h: Step size.

    Returns:
        Tuple (direct_derivative, chain_rule_derivative).

    Complexity: O(1).
    """
    # Direct: compute h(x) = f(g(x)) and differentiate
    def h_func(x_val: float) -> float:
        return f(g(x_val))

    direct = central_difference(h_func, x, h)

    # Chain rule: f'(g(x)) * g'(x)
    gx = g(x)
    fp = central_difference(f, gx, h)
    gp = central_difference(g, x, h)
    chain = fp * gp

    return direct, chain


def chain_rule_multivariate(
    f: Callable[[float], float],
    g: Callable[[NDArray[np.float64]], float],
    x: NDArray[np.float64],
    h: float = 1e-6
) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Numerically verify multivariate chain rule: ∇ f(g(x)) = f'(g(x)) * ∇g(x).

    Args:
        f: Outer scalar function R → R.
        g: Inner function Rⁿ → R.
        x: Point (n,).
        h: Step size.

    Returns:
        Tuple (direct_gradient, chain_rule_gradient).
    """
    x = np.asarray(x, dtype=np.float64)

    # Direct gradient of F(x) = f(g(x))
    def F(x_vec: NDArray[np.float64]) -> float:
        return f(g(x_vec))

    direct_grad = gradient(F, x, h)

    # Chain rule: f'(g(x)) * ∇g(x)
    gx = g(x)
    fp = central_difference(f, gx, h)
    g_grad = gradient(g, x, h)
    chain_grad = fp * g_grad

    return direct_grad, chain_grad


# ============================================================
# Tests
# ============================================================

def _test_forward_difference() -> None:
    f = lambda x: x**2
    # f'(3) = 6
    approx = forward_difference(f, 3.0, h=1e-6)
    assert abs(approx - 6.0) < 1e-4, f"FAIL: {approx}"
    print("  PASS: forward_difference")


def _test_central_difference() -> None:
    f = lambda x: x**3
    # f'(2) = 12
    approx = central_difference(f, 2.0, h=1e-6)
    assert abs(approx - 12.0) < 1e-6, f"FAIL: {approx}"

    # sin'(π/4) = cos(π/4) = √2/2 ≈ 0.7071
    import math
    approx2 = central_difference(math.sin, math.pi / 4, h=1e-6)
    assert abs(approx2 - math.sqrt(2) / 2) < 1e-5, f"FAIL sin: {approx2}"
    print("  PASS: central_difference")


def _test_second_derivative() -> None:
    f = lambda x: x**3
    # f''(1) = 6 (since f'(x)=3x², f''(x)=6x, at x=1 → 6)
    approx = second_derivative_central(f, 1.0, h=1e-4)
    assert abs(approx - 6.0) < 1e-2, f"FAIL: {approx}"
    print("  PASS: second_derivative_central")


def _test_gradient() -> None:
    # f(x, y) = x² + y³
    f = lambda v: v[0]**2 + v[1]**3
    grad_f = gradient(f, np.array([2.0, 3.0]))
    # ∂f/∂x = 2x = 4, ∂f/∂y = 3y² = 27
    assert np.allclose(grad_f, np.array([4.0, 27.0]), atol=1e-5), f"FAIL: {grad_f}"

    # f(x, y, z) = sin(x) * cos(y) + z²
    import math
    f2 = lambda v: math.sin(v[0]) * math.cos(v[1]) + v[2]**2
    grad_f2 = gradient(f2, np.array([0.0, 0.0, 3.0]))
    # ∂/∂x = cos(0)*cos(0) = 1, ∂/∂y = sin(0)*(-sin(0)) = 0, ∂/∂z = 2*3 = 6
    expected = np.array([1.0, 0.0, 6.0])
    assert np.allclose(grad_f2, expected, atol=1e-5), f"FAIL: {grad_f2}"
    print("  PASS: gradient")


def _test_partial_derivative() -> None:
    f = lambda v: v[0]**2 * v[1]
    x = np.array([3.0, 4.0])
    # ∂/∂x₀ = 2*x₀*x₁ = 2*3*4 = 24
    pd0 = partial_derivative(f, x, 0)
    # ∂/∂x₁ = x₀² = 9
    pd1 = partial_derivative(f, x, 1)
    assert abs(pd0 - 24.0) < 1e-5, f"FAIL pd0: {pd0}"
    assert abs(pd1 - 9.0) < 1e-5, f"FAIL pd1: {pd1}"
    print("  PASS: partial_derivative")


def _test_chain_rule() -> None:
    # Chain rule: f(x)=sin(x), g(x)=x² → h(x)=sin(x²)
    # h'(x) = cos(x²) * 2x
    import math
    f = math.sin
    g = lambda x: x**2
    direct, chain = chain_rule_1d(f, g, 1.5)
    # h'(1.5) = cos(2.25) * 3 = -0.628... * 3 = -1.884...
    expected = math.cos(1.5**2) * 3.0
    assert abs(direct - expected) < 1e-5, f"FAIL direct: {direct} vs {expected}"
    assert abs(chain - expected) < 1e-5, f"FAIL chain: {chain} vs {expected}"

    # Multivariate: f(t) = t², g(x,y) = 2x + 3y
    # F(x,y) = (2x + 3y)²
    # ∇F = [2(2x+3y)*2, 2(2x+3y)*3] = [4(2x+3y), 6(2x+3y)]
    f_m = lambda t: t**2
    g_m = lambda v: 2*v[0] + 3*v[1]
    x_pt = np.array([1.0, 1.0])
    direct_grad, chain_grad = chain_rule_multivariate(f_m, g_m, x_pt)
    # g(1,1) = 5, f'(5) = 10
    # ∇g = [2, 3]
    # Chain: 10 * [2, 3] = [20, 30]
    # Direct: 2*(2x+3y)*[2,3] = 2*5*[2,3] = [20, 30]
    expected_grad = np.array([20.0, 30.0])
    assert np.allclose(direct_grad, expected_grad, atol=1e-5), \
        f"FAIL direct: {direct_grad}"
    assert np.allclose(chain_grad, expected_grad, atol=1e-5), \
        f"FAIL chain: {chain_grad}"
    print("  PASS: chain_rule (1D + multivariate)")


if __name__ == "__main__":
    import math
    from typing import Tuple
    print("Testing derivatives.py ...")
    _test_forward_difference()
    _test_central_difference()
    _test_second_derivative()
    _test_gradient()
    _test_partial_derivative()
    _test_chain_rule()
    print("All derivatives tests PASSED!")
