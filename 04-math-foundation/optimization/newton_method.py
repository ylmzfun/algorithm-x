"""
Newton's Method for Root Finding and Optimization.

Implements:
- Newton's method for finding roots (f(x) = 0)
- Newton's method for 1D optimization (find f'(x) = 0)
- Newton's method for 2D optimization (multivariate)
- Comparison with gradient descent
"""

import numpy as np
from numpy.typing import NDArray
from typing import Callable, Tuple, List, Optional, Dict
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'calculus'))
from derivatives import gradient as numerical_gradient


# ============================================================
# Newton's Method for Root Finding (1D)
# ============================================================

def newton_root_1d(
    f: Callable[[float], float],
    f_prime: Callable[[float], float],
    x0: float,
    max_iter: int = 100,
    tol: float = 1e-10
) -> Tuple[float, int, List[float]]:
    """Find a root of f(x) = 0 using Newton's method.

    Update: x_{k+1} = x_k - f(x_k) / f'(x_k)

    Convergence: quadratic near the root (very fast) when f'(root) ≠ 0.
    Requires: f is differentiable, f'(root) ≠ 0, good initial guess.

    Args:
        f: Function whose root we seek.
        f_prime: Derivative of f.
        x0: Initial guess.
        max_iter: Maximum iterations.
        tol: Convergence tolerance on |f(x)|.

    Returns:
        Tuple (root, num_iterations, x_history):
            root: Approximate root.
            num_iterations: Number of iterations.
            x_history: Sequence of x values.

    Raises:
        ValueError: If derivative near zero causes divergence.

    Complexity: O(1) per iteration (1 function + 1 derivative evaluation).

    Example:
        >>> newton_root_1d(lambda x: x**2 - 2, lambda x: 2*x, 1.5)
        (1.4142135623..., 4, [...])  # √2
    """
    x = x0
    history = [x]

    for it in range(max_iter):
        fx = f(x)
        fpx = f_prime(x)

        if abs(fx) < tol:
            return x, it + 1, history

        if abs(fpx) < 1e-15:
            raise ValueError(f"Derivative near zero at x={x}; Newton fails")

        x_new = x - fx / fpx
        history.append(x_new)

        if abs(x_new - x) < tol:
            return x_new, it + 1, history

        x = x_new

    return x, max_iter, history


# ============================================================
# Newton's Method for Optimization (1D)
# ============================================================

def newton_opt_1d(
    f: Callable[[float], float],
    f_prime: Callable[[float], float],
    f_double_prime: Callable[[float], float],
    x0: float,
    max_iter: int = 100,
    tol: float = 1e-10
) -> Tuple[float, int, List[float]]:
    """Find a local minimum of f(x) using Newton's method.

    Apply Newton's root-finding to f'(x) = 0:

    x_{k+1} = x_k - f'(x_k) / f''(x_k)

    Convergence: quadratic near the minimum for well-conditioned functions.
    This is much faster than gradient descent near the optimum.

    Each iteration fits a quadratic approximation to f at x_k and jumps
    to its minimum.

    Args:
        f: Objective function.
        f_prime: First derivative f'.
        f_double_prime: Second derivative f'' (must be > 0 near minimum).
        x0: Initial guess.
        max_iter: Maximum iterations.
        tol: Convergence tolerance on |f'(x)|.

    Returns:
        Tuple (x_min, num_iterations, x_history).

    Complexity: O(1) per iteration (1 func + 1 first deriv + 1 second deriv).

    Example:
        >>> f = lambda x: x**4 - 4*x**2 + 2*x + 5
        >>> fp = lambda x: 4*x**3 - 8*x + 2
        >>> fpp = lambda x: 12*x**2 - 8
        >>> newton_opt_1d(f, fp, fpp, 0.0)
    """
    x = x0
    history = [x]

    for it in range(max_iter):
        fpx = f_prime(x)
        fppx = f_double_prime(x)

        if abs(fpx) < tol:
            return x, it + 1, history

        if abs(fppx) < 1e-15:
            raise ValueError(f"Second derivative near zero at x={x}; "
                             "Newton method for optimization fails")

        x_new = x - fpx / fppx
        history.append(x_new)

        if abs(x_new - x) < tol:
            return x_new, it + 1, history

        x = x_new

    return x, max_iter, history


# ============================================================
# Newton's Method for Optimization (2D / Multivariate)
# ============================================================

def newton_opt_2d(
    f: Callable[[NDArray[np.float64]], float],
    grad: Callable[[NDArray[np.float64]], NDArray[np.float64]],
    hessian: Callable[[NDArray[np.float64]], NDArray[np.float64]],
    x0: NDArray[np.float64],
    max_iter: int = 100,
    tol: float = 1e-10
) -> Tuple[NDArray[np.float64], int, List[float]]:
    """Find a local minimum of a multivariate function using Newton's method.

    x_{k+1} = x_k - H(x_k)⁻¹ * ∇f(x_k)

    where H is the Hessian matrix (matrix of second partial derivatives).

    Newton's method in multiple dimensions:
    - Fits a quadratic to the function at each step.
    - Jumps directly to the minimum of the quadratic approximation.
    - Converges quadratically near the minimum.

    Requires: Hessian is positive definite near the minimum.
    Computational cost: O(n³) per iteration for Hessian inversion.
    This makes it impractical for high-dimensional problems (n > 1000).

    Args:
        f: Objective function f: Rⁿ → R.
        grad: Gradient function ∇f: Rⁿ → Rⁿ.
        hessian: Hessian function H: Rⁿ → R^{n×n}.
        x0: Initial guess.
        max_iter: Maximum iterations.
        tol: Convergence tolerance on gradient norm.

    Returns:
        Tuple (x_min, num_iterations, grad_norm_history):
            x_min: Approximate minimum.
            num_iterations: Number of iterations.
            grad_norm_history: ||∇f|| at each iteration.
    """
    x = x0.astype(np.float64).copy()
    grad_norms: List[float] = []

    for it in range(max_iter):
        g = grad(x)
        gnorm = float(np.linalg.norm(g))
        grad_norms.append(gnorm)

        if gnorm < tol:
            return x, it + 1, grad_norms

        H = hessian(x)

        try:
            # Solve H @ dx = -g  (Newton step)
            dx = np.linalg.solve(H, -g)
        except np.linalg.LinAlgError:
            raise ValueError(f"Hessian singular at x={x}; cannot compute Newton step")

        x_new = x + dx

        # Divergence check: if function value increases, add damping
        if f(x_new) > f(x) + 1e-8:
            # Simple backtracking line search
            alpha = 1.0
            for _ in range(20):
                alpha *= 0.5
                x_try = x + alpha * dx
                if f(x_try) < f(x) or alpha < 1e-10:
                    x_new = x_try
                    break

        if np.linalg.norm(x_new - x) < tol:
            x = x_new
            g = grad(x)
            grad_norms.append(float(np.linalg.norm(g)))
            return x, it + 1, grad_norms

        x = x_new

    g = grad(x)
    grad_norms.append(float(np.linalg.norm(g)))
    return x, max_iter, grad_norms


# ============================================================
# Comparison: Newton vs Gradient Descent
# ============================================================

def compare_newton_vs_gd_1d() -> Dict[str, List[float]]:
    """Compare Newton's method and gradient descent for 1D optimization.

    Minimizes f(x) = x⁴ - 4x² + 2x + 5.
    This function has two local minima; we start near x=1.

    Returns:
        Dict with convergence histories.
    """
    f = lambda x: x**4 - 4*x**2 + 2*x + 5
    fp = lambda x: 4*x**3 - 8*x + 2
    fpp = lambda x: 12*x**2 - 8

    x0 = -2.0
    results: Dict[str, List[float]] = {}

    # Newton's method
    x_newt, iters, x_hist = newton_opt_1d(f, fp, fpp, x0, max_iter=50)
    newton_vals = [abs(fp(x)) for x in x_hist]
    results[f'Newton ({iters} iters)'] = newton_vals

    # Gradient descent with different learning rates
    for lr in [0.01, 0.1]:
        x = x0
        gd_vals = []
        for _ in range(200):
            g = fp(x)
            gd_vals.append(abs(g))
            x = x - lr * g
        results[f'GD lr={lr}'] = gd_vals

    return results


def compare_newton_vs_gd_2d() -> Dict[str, List[float]]:
    """Compare Newton's method and gradient descent for 2D optimization.

    Minimizes f(x, y) = (x-1)² + 100*(y-x²)²  (Rosenbrock-like at shifted min).
    Uses a simpler quadratic: f(x, y) = x² + 10y² (convex, well-conditioned).

    Returns:
        Dict with gradient norm histories.
    """
    f = lambda v: v[0]**2 + 10.0 * v[1]**2
    grad = lambda v: np.array([2.0 * v[0], 20.0 * v[1]])
    hess = lambda v: np.array([[2.0, 0.0], [0.0, 20.0]])

    x0 = np.array([5.0, 5.0])
    results: Dict[str, List[float]] = {}

    # Newton
    _, iters, n_hist = newton_opt_2d(f, grad, hess, x0.copy(), max_iter=50)
    results[f'Newton ({iters} iters)'] = n_hist

    # Gradient descent
    x = x0.copy()
    gd_hist = []
    for _ in range(200):
        g = grad(x)
        gd_hist.append(np.linalg.norm(g))
        x = x - 0.05 * g
    results['GD lr=0.05'] = gd_hist

    return results


# ============================================================
# Tests
# ============================================================

def _test_newton_root() -> None:
    # Find √2: solve x² - 2 = 0
    f = lambda x: x**2 - 2
    fp = lambda x: 2 * x
    root, iters, hist = newton_root_1d(f, fp, 1.5)
    assert abs(root - np.sqrt(2)) < 1e-10, f"FAIL: {root}"
    assert iters < 10, f"Too many iterations: {iters}"
    print(f"  PASS: newton_root_1d (√2={root:.10f}, {iters} iters)")


def _test_newton_opt_1d() -> None:
    # Minimize f(x) = x⁴ - 4x² + 2x + 5
    f = lambda x: x**4 - 4*x**2 + 2*x + 5
    fp = lambda x: 4*x**3 - 8*x + 2
    fpp = lambda x: 12*x**2 - 8

    # Start near local minimum around x ≈ 1.2
    x_min, iters, hist = newton_opt_1d(f, fp, fpp, -2.0)
    # The minimum derivative should be near zero
    assert abs(fp(x_min)) < 1e-8, f"FAIL: f'({x_min}) = {fp(x_min)}"
    assert iters < 20, f"Too many iterations: {iters}"
    print(f"  PASS: newton_opt_1d (x*={x_min:.6f}, {iters} iters)")


def _test_newton_opt_2d() -> None:
    # f(x, y) = x² + 10y², minimum at (0, 0)
    f = lambda v: v[0]**2 + 10.0 * v[1]**2
    grad = lambda v: np.array([2.0 * v[0], 20.0 * v[1]])
    hess = lambda v: np.array([[2.0, 0.0], [0.0, 20.0]])

    x0 = np.array([5.0, 5.0])
    x_min, iters, hist = newton_opt_2d(f, grad, hess, x0)
    assert np.linalg.norm(x_min) < 1e-10, f"FAIL: x={x_min}"
    # Newton should converge in 1 iteration for quadratics!
    assert iters <= 2, f"Newton should need 1 iter for quadratic: {iters}"
    print(f"  PASS: newton_opt_2d (x={np.round(x_min, 3)}, {iters} iters)")


def _test_rosenbrock_newton() -> None:
    """Test Newton on Rosenbrock function."""
    f = lambda v: (1 - v[0])**2 + 100 * (v[1] - v[0]**2)**2

    def grad(v: NDArray[np.float64]) -> NDArray[np.float64]:
        dx = -2*(1 - v[0]) - 400*v[0]*(v[1] - v[0]**2)
        dy = 200*(v[1] - v[0]**2)
        return np.array([dx, dy])

    def hess(v: NDArray[np.float64]) -> NDArray[np.float64]:
        h11 = 2 - 400*v[1] + 1200*v[0]**2
        h12 = -400 * v[0]
        h21 = -400 * v[0]
        h22 = 200.0
        return np.array([[h11, h12], [h21, h22]])

    x0 = np.array([-1.0, 1.0])
    x_min, iters, hist = newton_opt_2d(f, grad, hess, x0, max_iter=100)
    dist = np.linalg.norm(x_min - np.array([1.0, 1.0]))
    start_dist = np.linalg.norm(x0 - np.array([1.0, 1.0]))
    assert dist < start_dist, f"No progress on Rosenbrock: {x_min}"
    print(f"  PASS: Newton on Rosenbrock (x={np.round(x_min, 4)}, {iters} iters)")


if __name__ == "__main__":
    print("Testing newton_method.py ...")
    _test_newton_root()
    _test_newton_opt_1d()
    _test_newton_opt_2d()
    _test_rosenbrock_newton()

    print("\nComparison: Newton vs Gradient Descent (1D)")
    results_1d = compare_newton_vs_gd_1d()
    for name, hist in results_1d.items():
        print(f"  {name:20s}: {len(hist):3d} iters, final |f'| = {hist[-1]:.2e}")

    print("\nComparison: Newton vs Gradient Descent (2D)")
    results_2d = compare_newton_vs_gd_2d()
    for name, hist in results_2d.items():
        print(f"  {name:20s}: {len(hist):3d} iters, final ||∇f|| = {hist[-1]:.2e}")

    print("\nAll newton_method tests PASSED!")
