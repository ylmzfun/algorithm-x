"""
Convexity Analysis for ML/AI Foundations.

Implements:
- Checking convexity of functions
- Common convex functions (log-sum-exp, max)
- Convex set projection
- Duality concept with simple LP example

Convexity is the central property that makes optimization tractable
in machine learning: any local minimum of a convex function is global.
"""

import numpy as np
from numpy.typing import NDArray
from typing import Callable, Tuple, List
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'calculus'))


# ============================================================
# Checking Convexity
# ============================================================

def is_convex_1d(
    f: Callable[[float], float],
    a: float,
    b: float,
    n_points: int = 100
) -> Tuple[bool, str]:
    """Check if a 1D function appears convex on [a, b] using two conditions:

    1. Midpoint convexity: f((x+y)/2) ≤ (f(x) + f(y))/2
       (necessary + sufficient for continuous functions)
    2. Second derivative non-negative: f''(x) ≥ 0 (for twice-diff'ble functions)

    This is a numerical check, not a proof! For reliable results,
    use analytical verification.

    Args:
        f: Function f: R → R.
        a, b: Interval bounds.
        n_points: Number of test points.

    Returns:
        Tuple (is_convex_from_test, explanation):
            is_convex_from_test: True if all checks pass.
            explanation: String with reasoning.
    """
    xs = np.linspace(a, b, n_points)
    from derivatives import central_difference, second_derivative_central

    # Check midpoint convexity at random pairs
    np.random.seed(42)
    mid_ok = True
    for _ in range(50):
        i, j = np.random.randint(0, n_points, size=2)
        x_i, x_j = xs[i], xs[j]
        mid = (x_i + x_j) / 2.0
        if f(mid) > (f(x_i) + f(x_j)) / 2.0 + 1e-8:
            mid_ok = False
            break

    # Check second derivative
    second_deriv_ok = True
    negative_count = 0
    for x in xs:
        fpp = second_derivative_central(f, x, h=1e-4)
        if fpp < -1e-6:
            negative_count += 1
            if negative_count > 5:
                second_deriv_ok = False
                break

    checks = []
    checks.append(f"Midpoint convexity: {'PASS' if mid_ok else 'FAIL'}")
    checks.append(f"Second derivative ≥ 0: {'PASS' if second_deriv_ok else 'FAIL'}")

    return mid_ok and second_deriv_ok, "; ".join(checks)


def is_convex_2d(
    f: Callable[[NDArray[np.float64]], float],
    bounds: NDArray[np.float64],
    n_points: int = 30
) -> Tuple[bool, str]:
    """Check convexity numerically for a 2D function via Hessian eigenvalues.

    For a twice-differentiable function f: R² → R, convexity requires
    the Hessian to be positive semi-definite (PSD) everywhere. This is
    equivalent to all eigenvalues being ≥ 0.

    This checks eigenvalues of the numerical Hessian on a grid.

    Args:
        f: Function f: R² → R.
        bounds: [[x_min, x_max], [y_min, y_max]].
        n_points: Grid points per dimension.

    Returns:
        Tuple (appears_convex, explanation).
    """
    from derivatives import gradient as numerical_gradient

    x_vals = np.linspace(bounds[0, 0], bounds[0, 1], n_points)
    y_vals = np.linspace(bounds[1, 0], bounds[1, 1], n_points)

    min_eig = float('inf')
    for x in x_vals:
        for y in y_vals:
            pt = np.array([x, y])

            # Compute Hessian using numerical differentiation of gradient
            def grad_wrapper(v: NDArray[np.float64]) -> NDArray[np.float64]:
                return numerical_gradient(f, v, h=1e-5)

            H = np.zeros((2, 2))
            h = 1e-4
            for i in range(2):
                for j in range(2):
                    pt_plus_i = pt.copy(); pt_plus_i[i] += h
                    pt_plus_j = pt.copy(); pt_plus_j[j] += h
                    pt_plus_ij = pt.copy(); pt_plus_ij[i] += h; pt_plus_ij[j] += h

                    if i == j:
                        # Diagonal: f(x+2h) - 2f(x+h) + f(x) / h²
                        # Using gradient: (g_i(x+he_i) - g_i(x-he_i))/2h
                        g_plus = grad_wrapper(pt_plus_i)[i]
                        g_minus = grad_wrapper(pt - (np.eye(2)[i] * h))[i]
                        H[i, j] = (g_plus - g_minus) / (2 * h)
                    else:
                        g_i_plus = grad_wrapper(pt_plus_j)[i]
                        g_i_minus = grad_wrapper(pt - (np.eye(2)[j] * h))[i]
                        H[i, j] = (g_i_plus - g_i_minus) / (2 * h)

            # Symmetrize
            H = (H + H.T) / 2.0

            # Check eigenvalues
            eigvals = np.linalg.eigvalsh(H)
            min_eig = min(min_eig, np.min(eigvals))

    is_convex = min_eig >= -1e-6
    return is_convex, f"Minimum Hessian eigenvalue ≈ {min_eig:.6f}"


# ============================================================
# Common Convex Functions
# ============================================================

def log_sum_exp(x: NDArray[np.float64]) -> float:
    """Log-Sum-Exp function: f(x) = log(Σ exp(x_i)).

    This is a smooth approximation of the max function:
        max(x) ≤ log_sum_exp(x) ≤ max(x) + log(n)

    It is convex and is the log-partition function of the softmax distribution.
    Used extensively in ML for:
    - Log-softmax for numerical stability
    - Log-likelihood of exponential family distributions
    - Convex relaxation of max

    Args:
        x: Input vector of shape (n,).

    Returns:
        log(Σ exp(x_i)).

    Complexity: O(n).
    """
    x_max = np.max(x)
    # Shift for numerical stability: log(Σ exp(x_i)) = x_max + log(Σ exp(x_i - x_max))
    return float(x_max + np.log(np.sum(np.exp(x - x_max))))


def softmax(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """Softmax function: σ(x)_i = exp(x_i) / Σ_j exp(x_j).

    The gradient of log_sum_exp is the softmax.
    Maps Rⁿ → Δ^{n-1} (probability simplex).

    For numerical stability, we subtract max before exponentiating.

    Args:
        x: Input vector.

    Returns:
        Probability distribution over n classes.
    """
    x_shifted = x - np.max(x)
    exp_x = np.exp(x_shifted)
    return exp_x / np.sum(exp_x)


def hinge_loss_max(
    x: NDArray[np.float64], threshold: float = 0.0
) -> float:
    """Pointwise maximum: f(x) = max_i {0, x_i - threshold}.

    The max of linear functions is convex.
    This is related to the hinge loss: max(0, 1 - y·f(x)) in SVMs.

    Args:
        x: Input vector.
        threshold: Offset value.

    Returns:
        max(0, max_i(x_i - threshold)).
    """
    return float(np.maximum(0.0, np.max(x - threshold)))


# ============================================================
# Convex Set Projection
# ============================================================

def project_onto_l1_ball(
    x: NDArray[np.float64], radius: float = 1.0
) -> NDArray[np.float64]:
    """Project x onto the L1 ball {z: ||z||₁ ≤ radius}.

    This is the Euclidean projection onto the L1 ball, used in:
    - Lasso (L1-regularized regression) proximal operator
    - Sparse coding
    - Compressed sensing

    Algorithm: Duchi et al. (2008) O(n log n) projection.

    Args:
        x: Point to project.
        radius: L1 ball radius.

    Returns:
        Projected point with L1 norm ≤ radius.
    """
    if np.sum(np.abs(x)) <= radius:
        return x.copy()

    # Projection algorithm: sort |x| descending, find threshold
    u = np.abs(x)
    u_sorted = np.sort(u)[::-1]

    # Find the pivot via cumulative sum
    cumsum = np.cumsum(u_sorted)
    # Condition: u_sorted[j] >= (cumsum[j] - radius) / (j + 1)
    # Find largest j satisfying this
    rho = -1.0
    for j in range(len(u_sorted)):
        if u_sorted[j] > (cumsum[j] - radius) / (j + 1):
            rho = j

    theta = (cumsum[rho] - radius) / (rho + 1)

    # Soft-threshold
    return np.sign(x) * np.maximum(u - theta, 0.0)


def project_onto_l2_ball(
    x: NDArray[np.float64], radius: float = 1.0
) -> NDArray[np.float64]:
    """Project x onto the L2 ball {z: ||z||₂ ≤ radius}.

    If ||x||₂ ≤ radius: return x.
    Otherwise: return radius * x / ||x||₂  (scale to boundary).

    Args:
        x: Point to project.
        radius: L2 ball radius.

    Returns:
        Projected point.
    """
    norm_x = np.linalg.norm(x)
    if norm_x <= radius:
        return x.copy()
    return radius * x / norm_x


def project_onto_simplex(
    x: NDArray[np.float64]
) -> NDArray[np.float64]:
    """Project x onto the probability simplex Δ = {z: Σ z_i = 1, z_i ≥ 0}.

    Efficient O(n log n) algorithm (Wang & Carreira-Perpinan, 2013).

    This is used in ML for:
    - Softmax output projections
    - Portfolio optimization
    - Attention weight normalization

    Args:
        x: Input vector.

    Returns:
        Point on the simplex (non-negative, sums to 1).
    """
    n = len(x)
    u = np.sort(x)[::-1]
    cumsum = np.cumsum(u)

    # Find ρ = max{j: u_j - (cumsum_j - 1)/(j+1) > 0}
    rho = -1
    for j in range(n):
        if u[j] - (cumsum[j] - 1.0) / (j + 1) > 0:
            rho = j

    theta = (cumsum[rho] - 1.0) / (rho + 1)
    return np.maximum(x - theta, 0.0)


# ============================================================
# Duality: Simple LP Example
# ============================================================

def linear_program_duality_demo() -> None:
    """Demonstrate duality with a simple linear program.

    Primal (P):
        maximize  3x₁ + 2x₂
        subject to  x₁ + x₂ ≤ 4
                   2x₁ + x₂ ≤ 5
                   x₁, x₂ ≥ 0

    Dual (D):
        minimize  4y₁ + 5y₂
        subject to  y₁ + 2y₂ ≥ 3
                    y₁ + y₂ ≥ 2
                    y₁, y₂ ≥ 0

    Weak duality: primal_obj ≤ dual_obj for all feasible solutions.
    Strong duality: at optimality, primal_obj* = dual_obj* (for LPs).

    For this problem, the optimal values are:
    Primal: x₁=1, x₂=2, obj=7 (or x₁=2, x₂=1, obj=8... let me verify)
    Let's compute: feasible region is bounded by:
      x₁ + x₂ ≤ 4
      2x₁ + x₂ ≤ 5
      x₁, x₂ ≥ 0

    Intersections: (0,0)→0, (2.5,0)→7.5, (0,4)→8, (1,3)→let's check: 2*1+3=5✓,1+3=4✓,obj=9

    Hmm, let me use a simpler well-known example instead.
    """
    print("--- Linear Programming Duality Demo ---")
    print("""
Primal (P): maximize  x₁ + x₂
             subject to  x₁ + 2x₂ ≤ 4
                         4x₁ + 2x₂ ≤ 12
                         x₁, x₂ ≥ 0

Dual (D):   minimize  4y₁ + 12y₂
             subject to  y₁ + 4y₂ ≥ 1
                         2y₁ + 2y₂ ≥ 1
                         y₁, y₂ ≥ 0

Solving Primal graphically:
- Constraints: x₁+2x₂=4 → x₂ = 2-x₁/2
               4x₁+2x₂=12 → x₂ = 6-2x₁
- Intersection: 2-x₁/2 = 6-2x₁ → 1.5x₁ = 4 → x₁ = 8/3 ≈ 2.67, x₂ = 2/3 ≈ 0.67
- Objective: 8/3 + 2/3 = 10/3 ≈ 3.33

- Also check vertices: (0,0)→0, (0,2)→2, (3,0)→3, (8/3, 2/3)→10/3 ≈ 3.33
- Optimal: x* = (3, 0), obj = 3  (wait, (8/3,2/3) gives 10/3 > 3)
  Check constraint 2: 4*(8/3)+2*(2/3) = 32/3+4/3 = 12 ✓
  So optimal is x*=(8/3, 2/3), obj=10/3 ≈ 3.33

Weak duality: For any feasible primal x and dual y:
    cᵀx ≤ bᵀy = 4y₁ + 12y₂

Strong duality at optimum: max primal = min dual = 10/3

This is foundational to SVM dual formulation and many ML algorithms.
""")
    print()


# ============================================================
# Tests
# ============================================================

def _test_convexity_check() -> None:
    # f(x) = x² is convex
    is_conv, msg = is_convex_1d(lambda x: x**2, -5, 5)
    assert is_conv, f"x² should be convex: {msg}"

    # f(x) = -x² is NOT convex (concave)
    is_conv2, msg2 = is_convex_1d(lambda x: -(x**2), -5, 5)
    assert not is_conv2, f"-x² should not be convex: {msg2}"

    # f(x) = |x| is convex
    is_conv3, msg3 = is_convex_1d(lambda x: abs(x), -5, 5)
    assert is_conv3, f"|x| should be convex: {msg3}"

    print(f"  PASS: is_convex_1d (x²:{is_conv}, -x²:{is_conv2}, |x|:{is_conv3})")


def _test_log_sum_exp() -> None:
    x = np.array([1.0, 2.0, 3.0])
    # log_sum_exp should be close to max(1,2,3)=3
    lse = log_sum_exp(x)
    assert 3.0 < lse < 3.0 + np.log(3), f"LSE out of bounds: {lse}"  # 3 < LSE < 3+ln3 ≈ 4.099
    # log_sum_exp(x + c) = c + log_sum_exp(x)
    c = 5.0
    assert abs(log_sum_exp(x + c) - (c + lse)) < 1e-10, "Shift property failed"
    print(f"  PASS: log_sum_exp (value={lse:.4f})")


def _test_softmax() -> None:
    x = np.array([1.0, 2.0, 3.0])
    sm = softmax(x)
    assert len(sm) == 3
    assert abs(np.sum(sm) - 1.0) < 1e-10, f"Sums to {np.sum(sm)}, not 1"
    # Higher input → higher probability
    assert sm[2] > sm[1] > sm[0], f"Order wrong: {sm}"
    print(f"  PASS: softmax (probs={np.round(sm, 4)})")


def _test_projections() -> None:
    # L1 ball projection
    x = np.array([3.0, -1.0, 2.0])
    projected = project_onto_l1_ball(x, radius=2.0)
    assert np.sum(np.abs(projected)) <= 2.0 + 1e-10, \
        f"L1 norm violated: {np.sum(np.abs(projected))}"

    # L2 ball projection
    x2 = np.array([3.0, 4.0])
    proj2 = project_onto_l2_ball(x2, radius=1.0)
    assert np.linalg.norm(proj2) <= 1.0 + 1e-10

    # Simplex projection
    x3 = np.array([2.0, 1.0, -1.0])
    proj3 = project_onto_simplex(x3)
    assert abs(np.sum(proj3) - 1.0) < 1e-10, f"Simplex sum: {np.sum(proj3)}"
    assert np.all(proj3 >= -1e-10), f"Negative values: {proj3}"
    print(f"  PASS: projections (L1, L2, simplex)")


if __name__ == "__main__":
    print("Testing convexity.py ...")
    _test_convexity_check()
    _test_log_sum_exp()
    _test_softmax()
    _test_projections()

    # Check 2D convexity
    f = lambda v: v[0]**2 + v[1]**2  # convex
    bounds_2d = np.array([[-5, 5], [-5, 5]])
    is_conv, msg = is_convex_2d(f, bounds_2d, n_points=10)
    print(f"  2D convexity check (x²+y²): {is_conv} ({msg})")

    # Demo
    linear_program_duality_demo()

    print("All convexity tests PASSED!")
