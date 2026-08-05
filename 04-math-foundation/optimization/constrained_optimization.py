"""
Constrained Optimization for ML/AI Foundations.

Implements:
- Lagrange multipliers (solved via gradient descent on Lagrangian)
- KKT conditions explanation with examples
- Projected gradient descent for box constraints

Constrained optimization is fundamental to:
- Support Vector Machines (quadratic programming with constraints)
- Resource allocation problems
- Regularized ML models (L1/L2 constraints)
"""

import numpy as np
from numpy.typing import NDArray
from typing import Callable, Tuple, List, Dict
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'calculus'))


# ============================================================
# Lagrange Multipliers
# ============================================================

def lagrange_multiplier_solve(
    f: Callable[[NDArray[np.float64]], float],
    constraints: List[Callable[[NDArray[np.float64]], float]],
    x0: NDArray[np.float64],
    learning_rate: float = 0.01,
    max_iter: int = 5000,
    tol: float = 1e-6
) -> Tuple[NDArray[np.float64], NDArray[np.float64], float]:
    """Solve constrained optimization using Lagrange multipliers.

    Problem: minimize f(x) subject to g_i(x) = 0 for i = 1..m.

    Lagrangian: L(x, λ) = f(x) + Σᵢ λᵢ * g_i(x)

    We solve ∇L = 0 using gradient descent on x (minimizing) and
    gradient ascent on λ (maximizing), finding a saddle point.

    This demonstrates the primal-dual approach. For equality-constrained
    convex problems, the saddle point gives the global optimum.

    Args:
        f: Objective function f: Rⁿ → R.
        constraints: List of equality constraint functions g_i: Rⁿ → R.
                     Each must satisfy g_i(x) = 0 at the optimum.
        x0: Initial guess for primal variables x.
        learning_rate: Step size.
        max_iter: Maximum iterations.
        tol: Convergence tolerance.

    Returns:
        Tuple (x_opt, lambda_opt, lagrangian_value):
            x_opt: Optimal primal variables.
            lambda_opt: Lagrange multipliers.
            lagrangian_value: Final Lagrangian value.

    Complexity: O(n + m) per iteration.

    Example:
        minimize f(x, y) = x² + y²  subject to x + y = 1
        Solution: x = y = 0.5 (use analytical gradient or numerical)
    """
    from derivatives import gradient as numerical_gradient

    x = x0.astype(np.float64).copy()
    n = len(x)
    m = len(constraints)
    lam = np.zeros(m, dtype=np.float64)  # Lagrange multipliers

    def lagrangian(x_vec: NDArray[np.float64]) -> float:
        val = f(x_vec)
        for i in range(m):
            val += lam[i] * constraints[i](x_vec)
        return val

    for it in range(max_iter):
        # Gradient of Lagrangian w.r.t. x (descent)
        grad_L_x = numerical_gradient(lagrangian, x, h=1e-6)

        # Gradient of Lagrangian w.r.t. λ (ascent = gradient of constraints)
        grad_L_lam = np.array([g(x) for g in constraints], dtype=np.float64)

        # Check convergence
        grad_norm = float(
            np.linalg.norm(grad_L_x) + np.linalg.norm(grad_L_lam)
        )
        if grad_norm < tol:
            break

        # Update: minimize w.r.t. x, maximize w.r.t. λ
        x = x - learning_rate * grad_L_x
        lam = lam + learning_rate * grad_L_lam  # gradient ascent

    return x, lam, lagrangian(x)


def lagrange_example_demo() -> None:
    """Demonstrate Lagrange multipliers on a classic problem.

    minimize f(x, y) = x² + y²  subject to x + y = 1

    Analytical solution: x = y = 0.5
    Lagrangian: L = x² + y² + λ(x + y - 1)

    ∇_x L = 2x + λ = 0  →  x = -λ/2
    ∇_y L = 2y + λ = 0  →  y = -λ/2
    ∇_λ L = x + y - 1 = 0 → -λ = 1 → λ = -1

    Therefore: x = 0.5, y = 0.5, λ = -1, f_min = 0.5
    """
    f = lambda v: v[0]**2 + v[1]**2
    g1 = lambda v: v[0] + v[1] - 1.0  # x + y = 1

    x0 = np.array([2.0, -1.0])
    x_opt, lam_opt, L_val = lagrange_multiplier_solve(
        f, [g1], x0, learning_rate=0.1, max_iter=5000
    )

    print("--- Lagrange Multiplier Demo ---")
    print(f"  Problem: min x²+y²  s.t. x+y=1")
    print(f"  Analytical: x=y=0.5, λ=-1, f_min=0.5")
    print(f"  Numerical:  x={np.round(x_opt, 4)}, λ={np.round(lam_opt, 4)}, "
          f"f={f(x_opt):.4f}")
    print(f"  Constraint satisfaction: x+y-1 = {x_opt[0]+x_opt[1]-1:.2e}")
    print()


# ============================================================
# KKT Conditions
# ============================================================

def kkt_conditions_explanation() -> str:
    """Return an educational explanation of KKT conditions.

    The Karush-Kuhn-Tucker (KKT) conditions are necessary conditions
    for a solution to be optimal in a constrained optimization problem.

    Returns:
        String explanation.
    """
    return """
=== KKT (Karush-Kuhn-Tucker) Conditions ===

For the problem:
    minimize  f(x)
    subject to  g_i(x) ≤ 0,  i = 1..m   (inequality constraints)
                h_j(x) = 0,  j = 1..p   (equality constraints)

The KKT conditions at optimal x* with multipliers μ (inequality) and λ (equality):

1. Stationarity:
   ∇f(x*) + Σᵢ μᵢ ∇gᵢ(x*) + Σⱼ λⱼ ∇hⱼ(x*) = 0

2. Primal feasibility:
   g_i(x*) ≤ 0  for all i
   h_j(x*) = 0  for all j

3. Dual feasibility (inequality multipliers non-negative):
   μᵢ ≥ 0  for all i

4. Complementary slackness:
   μᵢ * g_i(x*) = 0  for all i
   (Either the constraint is active g_i=0 OR μ_i=0)

Key insights:
- If a constraint is inactive (g_i(x*) < 0), its multiplier μ_i = 0.
- If μ_i > 0, then g_i(x*) = 0 (constraint is binding/active).
- For convex problems, KKT conditions are necessary AND sufficient.

In ML:
- SVM dual formulation comes from KKT conditions.
- The support vectors are precisely the points where the margin
  constraint is active (μ_i > 0).
"""


def check_kkt_for_simple_qp() -> Dict[str, bool]:
    """Verify KKT conditions for a simple quadratic program.

    minimize  (x-1)² + (y-2)²  subject to  x + y ≤ 3

    This has inequality constraint g(x,y) = x + y - 3 ≤ 0.
    The unconstrained minimum is (1, 2), which satisfies 1+2=3,
    so the constraint is active at the optimum.

    Analytical: Lagrangian L = (x-1)²+(y-2)² + μ(x+y-3)
    KKT: 2(x-1)+μ=0, 2(y-2)+μ=0, x+y-3=0, μ≥0
    → x=1-μ/2, y=2-μ/2 → (1-μ/2)+(2-μ/2)=3 → 3-μ=3 → μ=0
    → x=1, y=2 (unconstrained min coincides with boundary)

    Returns:
        Dict with verification results.
    """
    x_opt = np.array([1.0, 2.0])
    mu = 0.0  # μ = 0 since constraint is exactly active at unconstrained min

    # 1. Stationarity: ∇f + μ∇g = 0
    grad_f = np.array([2*(x_opt[0]-1), 2*(x_opt[1]-2)])  # [0, 0]
    grad_g = np.array([1.0, 1.0])
    stationarity = np.allclose(grad_f + mu * grad_g, 0.0)

    # 2. Primal feasibility: g(x) ≤ 0
    g_val = x_opt[0] + x_opt[1] - 3.0
    primal_feasible = g_val <= 1e-10

    # 3. Dual feasibility: μ ≥ 0
    dual_feasible = mu >= 0

    # 4. Complementary slackness: μ * g(x) = 0
    comp_slack = abs(mu * g_val) < 1e-10

    return {
        'stationarity': stationarity,
        'primal_feasible': primal_feasible,
        'dual_feasible': dual_feasible,
        'complementary_slackness': comp_slack,
    }


# ============================================================
# Projected Gradient Descent
# ============================================================

def projected_gradient_descent(
    f_grad: Callable[[NDArray[np.float64]], NDArray[np.float64]],
    projection: Callable[[NDArray[np.float64]], NDArray[np.float64]],
    x0: NDArray[np.float64],
    learning_rate: float = 0.01,
    max_iter: int = 1000,
    tol: float = 1e-8
) -> Tuple[NDArray[np.float64], List[float]]:
    """Projected Gradient Descent for box-constrained optimization.

    Solves: minimize f(x) subject to x ∈ C (convex set)

    Algorithm:
        x_{k+1} = P_C(x_k - α ∇f(x_k))

    where P_C is the projection onto the feasible set C.

    For box constraints l ≤ x ≤ u:
        P_C(x)_i = max(l_i, min(x_i, u_i))  (clipping)

    Args:
        f_grad: Gradient function ∇f: Rⁿ → Rⁿ.
        projection: Projection function P_C: Rⁿ → Rⁿ.
        x0: Initial feasible point (must satisfy constraints).
        learning_rate: Step size.
        max_iter: Maximum iterations.
        tol: Convergence tolerance on gradient mapping norm.

    Returns:
        Tuple (x_opt, grad_norm_history):
            x_opt: Optimal point (feasible).
            grad_norm_history: ||x - P_C(x - ∇f(x))|| at each iteration
                               (gradient mapping norm).

    Complexity: O(n) per iteration plus gradient cost.
    """
    x = x0.astype(np.float64).copy()
    grad_norms: List[float] = []

    for _ in range(max_iter):
        grad = f_grad(x)

        # Gradient mapping: x - P_C(x - ∇f(x))
        x_tentative = x - learning_rate * grad
        x_projected = projection(x_tentative)
        grad_map = x - x_projected
        gnorm = float(np.linalg.norm(grad_map))
        grad_norms.append(gnorm)

        if gnorm < tol:
            return x_projected, grad_norms

        x = x_projected

    return x, grad_norms


def box_projection(
    x: NDArray[np.float64],
    lower: NDArray[np.float64],
    upper: NDArray[np.float64]
) -> NDArray[np.float64]:
    """Project x onto box constraints lower ≤ x ≤ upper.

    P_C(x)_i = max(lower_i, min(x_i, upper_i))

    Args:
        x: Point to project.
        lower: Lower bounds (same shape as x).
        upper: Upper bounds (same shape as x).

    Returns:
        Projected point satisfying all box constraints.
    """
    return np.clip(x, lower, upper)


def projected_gd_example_demo() -> None:
    """Demonstrate projected gradient descent on a box-constrained problem.

    minimize f(x, y) = (x-3)² + (y+2)²  subject to 0 ≤ x ≤ 2, -3 ≤ y ≤ 0
    """
    f_grad = lambda v: np.array([2*(v[0]-3), 2*(v[1]+2)])
    lower = np.array([0.0, -3.0])
    upper = np.array([2.0, 0.0])

    def proj(v: NDArray[np.float64]) -> NDArray[np.float64]:
        return box_projection(v, lower, upper)

    x0 = np.array([1.0, -1.0])  # feasible starting point
    x_opt, hist = projected_gradient_descent(f_grad, proj, x0,
                                             learning_rate=0.5, max_iter=500)

    # Unconstrained optimum: (3, -2)
    # Box constraints: x ≤ 2 → x* = 2, y ≥ -3 and y ≤ 0 → y* = -2 still
    # But y=-2 is within [-3, 0], so the constraint on y should not be active
    print("--- Projected Gradient Descent Demo ---")
    print(f"  Problem: min (x-3)²+(y+2)²  s.t. 0≤x≤2, -3≤y≤0")
    print(f"  Unconstrained min: (3, -2)")
    print(f"  Constrained min:   x=2 (boundary), y=-2 (interior)")
    print(f"  Numerical result:  x={np.round(x_opt, 4)}")
    # Check feasibility
    assert np.all(x_opt >= lower - 1e-10) and np.all(x_opt <= upper + 1e-10), \
        "Solution not feasible!"
    print(f"  Feasible: {np.all(x_opt >= lower) and np.all(x_opt <= upper)}")
    print()


# ============================================================
# Tests
# ============================================================

def _test_lagrange_multiplier() -> None:
    """Test Lagrange multiplier on min x²+y² s.t. x+y=1."""
    f = lambda v: v[0]**2 + v[1]**2
    g1 = lambda v: v[0] + v[1] - 1.0

    x0 = np.array([2.0, -1.0])
    x_opt, lam_opt, _ = lagrange_multiplier_solve(
        f, [g1], x0, learning_rate=0.1, max_iter=5000
    )

    # Should converge to (0.5, 0.5)
    assert abs(x_opt[0] - 0.5) < 0.05, f"x0 off: {x_opt[0]}"
    assert abs(x_opt[1] - 0.5) < 0.05, f"x1 off: {x_opt[1]}"
    # Constraint should be satisfied
    assert abs(x_opt[0] + x_opt[1] - 1.0) < 0.01, \
        f"Constraint not satisfied: {x_opt[0]+x_opt[1]}"
    print("  PASS: lagrange_multiplier")


def _test_kkt_conditions() -> None:
    result = check_kkt_for_simple_qp()
    assert all(result.values()), f"KKT check failed: {result}"
    print("  PASS: kkt_conditions")


def _test_projected_gradient_descent() -> None:
    """Test PGD on box-constrained quadratic."""
    f_grad = lambda v: np.array([2*(v[0]-3), 2*(v[1]+2)])
    lower = np.array([0.0, -3.0])
    upper = np.array([2.0, 0.0])

    def proj(v: NDArray[np.float64]) -> NDArray[np.float64]:
        return box_projection(v, lower, upper)

    x0 = np.array([1.0, -1.0])
    x_opt, hist = projected_gradient_descent(f_grad, proj, x0,
                                             learning_rate=0.5, max_iter=500)

    # Check feasibility
    assert np.all(x_opt >= lower - 1e-10), f"Lower bound violated: {x_opt}"
    assert np.all(x_opt <= upper + 1e-10), f"Upper bound violated: {x_opt}"

    # x should be near 2 (constrained), y near -2 (unconstrained)
    assert abs(x_opt[0] - 2.0) < 0.01, f"x0={x_opt[0]} should be ≈2"
    assert abs(x_opt[1] + 2.0) < 0.01, f"x1={x_opt[1]} should be ≈-2"

    # Gradient should be decreasing
    assert hist[-1] < hist[0], "Gradient not decreasing"
    print("  PASS: projected_gradient_descent")


if __name__ == "__main__":
    print("Testing constrained_optimization.py ...")
    _test_lagrange_multiplier()
    _test_kkt_conditions()
    _test_projected_gradient_descent()

    # Run demos
    lagrange_example_demo()
    print(kkt_conditions_explanation())
    projected_gd_example_demo()

    print("All constrained_optimization tests PASSED!")
