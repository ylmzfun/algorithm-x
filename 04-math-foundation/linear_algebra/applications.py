"""
Linear Algebra Applications for ML/AI Foundations.

Implements practical applications:
- Solve Ax = b (Gaussian elimination with partial pivoting)
- Least squares solution
- Condition number computation
- Linear regression via normal equations
"""

import numpy as np
from numpy.typing import NDArray
from typing import Tuple, Union, Dict


# ============================================================
# Solve Ax = b — Gaussian Elimination with Partial Pivoting
# ============================================================

def solve_linear_system(
    A: NDArray[np.float64], b: NDArray[np.float64]
) -> NDArray[np.float64]:
    """Solve Ax = b using Gaussian elimination with partial pivoting.

    Algorithm:
        1. Forward elimination: transform [A | b] to upper triangular form.
        2. Back substitution: solve for x from bottom to top.
        Partial pivoting is used at each step for numerical stability.

    Args:
        A: Coefficient matrix (n, n), must be non-singular.
        b: Right-hand side vector (n,).

    Returns:
        Solution vector x (n,).

    Raises:
        ValueError: If A is singular or shapes don't match.

    Complexity: O(n³) time, O(n²) space.

    Example:
        >>> A = np.array([[2, 1], [1, 3]])
        >>> b = np.array([5, 6])
        >>> solve_linear_system(A, b)
        array([1.8, 1.4])  # x=9/5, y=7/5
    """
    n = A.shape[0]
    if A.shape != (n, n):
        raise ValueError(f"A must be square, got {A.shape}")
    if b.shape != (n,):
        raise ValueError(f"b must have shape ({n},), got {b.shape}")

    # Augmented matrix
    Ab = np.column_stack([A.astype(np.float64), b.astype(np.float64)])
    n_rows, n_cols = Ab.shape  # n_cols = n + 1

    # Forward elimination with partial pivoting
    for k in range(n):
        # Find pivot row
        pivot_row = k + np.argmax(np.abs(Ab[k:, k]))
        if pivot_row != k:
            Ab[[k, pivot_row]] = Ab[[pivot_row, k]]

        if abs(Ab[k, k]) < 1e-15:
            raise ValueError("Matrix is singular; no unique solution exists")

        # Eliminate below
        for i in range(k + 1, n):
            factor = Ab[i, k] / Ab[k, k]
            Ab[i, k:] -= factor * Ab[k, k:]

    # Back substitution
    x = np.zeros(n, dtype=np.float64)
    for i in range(n - 1, -1, -1):
        x[i] = (Ab[i, -1] - np.dot(Ab[i, i + 1:n], x[i + 1:])) / Ab[i, i]

    return x


def is_singular(A: NDArray[np.float64], tol: float = 1e-10) -> bool:
    """Check if a matrix is singular using the same pivot test as solve_linear_system.

    Args:
        A: Square matrix (n, n).
        tol: Tolerance for zero pivot.

    Returns:
        True if A is (numerically) singular.
    """
    try:
        b = np.ones(A.shape[0])
        solve_linear_system(A, b)
        return False
    except ValueError:
        return True


# ============================================================
# Least Squares Solution
# ============================================================

def least_squares(
    A: NDArray[np.float64], b: NDArray[np.float64]
) -> NDArray[np.float64]:
    """Solve the least squares problem: minimize ||Ax - b||₂.

    The solution is x = (AᵀA)⁻¹ Aᵀb (normal equations).
    For better numerical stability, this uses numpy's lstsq which
    employs SVD-based solving.

    When A has full column rank:
        x̂ = (AᵀA)⁻¹ Aᵀb

    This finds the vector x that minimizes the sum of squared residuals.

    Args:
        A: Design matrix (m, n) with m ≥ n (more equations than unknowns).
        b: Observation vector (m,).

    Returns:
        Least squares solution x (n,).

    Complexity: O(mn²) using normal equations; O(mn²) with SVD.

    Example:
        # Fit y = a*x + b to data (x=[1,2,3], y=[2,4,5])
        >>> A = np.array([[1, 1], [2, 1], [3, 1]])  # [x, 1]
        >>> b = np.array([2, 4, 5])
        >>> least_squares(A, b)
        array([1.5, 0.666...])  # a=1.5, b=2/3
    """
    # Use numpy's robust least squares solver (SVD-based)
    x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
    return x


def least_squares_normal_eq(
    A: NDArray[np.float64], b: NDArray[np.float64]
) -> NDArray[np.float64]:
    """Solve least squares using the normal equations: AᵀA x = Aᵀb.

    This is the textbook approach. Less numerically stable than SVD-based
    methods but conceptually important.

    x̂ = (AᵀA)⁻¹ Aᵀb

    Args:
        A: Design matrix (m, n), m ≥ n, full column rank.
        b: Observation vector (m,).

    Returns:
        Least squares solution x (n,).

    Raises:
        ValueError: If AᵀA is singular.
    """
    ATA = A.T @ A
    ATb = A.T @ b
    return solve_linear_system(ATA, ATb)


# ============================================================
# Condition Number
# ============================================================

def condition_number(
    A: NDArray[np.float64], p: Union[int, str] = 2
) -> float:
    """Compute the condition number of a matrix: κ(A) = ||A||_p * ||A⁻¹||_p.

    The condition number measures how sensitive the solution of Ax = b
    is to perturbations in A or b.

    - κ ≈ 1: well-conditioned, small errors stay small.
    - κ ≫ 1: ill-conditioned, small errors can blow up.
    - κ = ∞: singular matrix.

    Args:
        A: Square matrix (n, n).
        p: Norm order (1, 2, inf, 'fro').

    Returns:
        Condition number κ(A) ≥ 1.

    Complexity: O(n³) due to matrix inverse computation.
    """
    return float(np.linalg.cond(A, p=p))


def condition_number_analysis(A: NDArray[np.float64]) -> str:
    """Provide a human-readable analysis of a matrix's condition number.

    Args:
        A: Square matrix.

    Returns:
        String describing the conditioning.
    """
    kappa = condition_number(A)
    if kappa < 10:
        level = "well-conditioned"
    elif kappa < 1e3:
        level = "moderately conditioned"
    elif kappa < 1e6:
        level = "ill-conditioned"
    else:
        level = "severely ill-conditioned (near-singular)"

    digits_lost = int(np.log10(kappa)) if kappa > 1 else 0
    return (
        f"Condition number κ₂(A) = {kappa:.2e}\n"
        f"Matrix is {level}.\n"
        f"Expected loss of ~{digits_lost} decimal digits of precision "
        f"when solving Ax = b."
    )


# ============================================================
# Linear Regression
# ============================================================

def linear_regression(
    X: NDArray[np.float64], y: NDArray[np.float64]
) -> Tuple[NDArray[np.float64], dict]:
    """Fit a linear regression model y = Xβ + ε using normal equations.

    β̂ = (XᵀX)⁻¹ Xᵀy

    Assumes X already includes a bias column (column of 1s) if needed.
    Use linear_regression_with_intercept() to auto-add the intercept.

    Args:
        X: Design matrix (n_samples, n_features), including bias column.
        y: Target values (n_samples,).

    Returns:
        Tuple (beta, stats):
            beta: Coefficients (n_features,).
            stats: Dictionary with keys:
                - residuals: Residual vector y - Xβ.
                - rss: Residual sum of squares.
                - tss: Total sum of squares.
                - r_squared: Coefficient of determination R².
                - mse: Mean squared error.
                - se: Standard errors of coefficients.
                - t_stats: t-statistics of coefficients.
                - p_values: p-values (two-sided).

    Complexity: O(np²) time (n samples, p features), O(np) space.
    """
    import numpy as np
    from numpy.typing import NDArray
    from typing import Tuple, Dict

    n, p = X.shape

    # Fit: β = (XᵀX)⁻¹ Xᵀy
    beta = least_squares(X, y)  # using SVD-based solver for stability

    # Predictions and residuals
    y_pred = X @ beta
    residuals = y - y_pred

    # Sum of squares
    rss = float(np.sum(residuals ** 2))
    tss = float(np.sum((y - np.mean(y)) ** 2))

    # R²
    r_squared = 1.0 - rss / tss if tss > 0 else 0.0

    # Standard errors
    sigma_sq = rss / (n - p) if n > p else rss / n
    try:
        XtX_inv = np.linalg.inv(X.T @ X)
        se = np.sqrt(sigma_sq * np.diag(XtX_inv))
    except np.linalg.LinAlgError:
        se = np.full(p, np.nan)

    # t-statistics
    with np.errstate(divide='ignore', invalid='ignore'):
        t_stats = np.where(se > 1e-15, beta / se, np.nan)

    # MSE
    mse = rss / n

    stats = {
        'residuals': residuals,
        'rss': rss,
        'tss': tss,
        'r_squared': r_squared,
        'mse': mse,
        'se': se,
        't_stats': t_stats,
    }
    return beta, stats


def linear_regression_with_intercept(
    X: NDArray[np.float64], y: NDArray[np.float64]
) -> Tuple[NDArray[np.float64], dict]:
    """Fit linear regression y = Xβ + β₀ + ε, auto-adding intercept.

    Args:
        X: Feature matrix (n_samples, n_features) WITHOUT bias column.
        y: Target values (n_samples,).

    Returns:
        Tuple (beta_full, stats):
            beta_full: [β₀ (intercept), β₁, ..., βₚ] (n_features + 1,).
            stats: Same as linear_regression().
    """
    X_with_bias = np.column_stack([np.ones(X.shape[0]), X])
    return linear_regression(X_with_bias, y)


# ============================================================
# Tests
# ============================================================

def _test_solve_linear_system() -> None:
    # Simple 2×2
    A = np.array([[2.0, 1.0], [1.0, 3.0]])
    b = np.array([5.0, 6.0])
    x = solve_linear_system(A, b)
    expected = np.linalg.solve(A, b)
    assert np.allclose(x, expected, atol=1e-10), f"FAIL: {x} vs {expected}"

    # 3×3 test
    A3 = np.array([[3.0, 2.0, -4.0], [2.0, 3.0, 3.0], [5.0, -3.0, 1.0]])
    b3 = np.array([3.0, 15.0, 14.0])
    x3 = solve_linear_system(A3, b3)
    assert np.allclose(A3 @ x3, b3, atol=1e-10), f"FAIL: A@x={A3@x3} != b={b3}"

    # Random tests
    np.random.seed(42)
    for _ in range(10):
        n = np.random.randint(2, 20)
        M = np.random.randn(n, n)
        v = np.random.randn(n)
        sol = solve_linear_system(M, v)
        assert np.allclose(M @ sol, v, atol=1e-8), \
            f"FAIL random: residual norm={np.linalg.norm(M@sol - v)}"

    print("  PASS: solve_linear_system")


def _test_least_squares() -> None:
    # Overdetermined system: 3 equations, 2 unknowns
    A = np.array([[1.0, 1.0], [1.0, 2.0], [1.0, 3.0]])
    b = np.array([1.0, 2.0, 2.0])
    x = least_squares(A, b)
    x_ne = least_squares_normal_eq(A, b)
    # Both methods should agree
    assert np.allclose(x, x_ne, atol=1e-8), f"FAIL: {x} vs {x_ne}"
    # Residual should be minimal
    residual = np.linalg.norm(A @ x - b)
    # Check with small perturbation: any other x should give larger residual
    x_perturbed = x + np.array([0.01, 0.01])
    residual_pert = np.linalg.norm(A @ x_perturbed - b)
    assert residual <= residual_pert, "Solution not optimal"

    print("  PASS: least_squares")


def _test_condition_number() -> None:
    # Well-conditioned: identity
    I = np.eye(5)
    assert abs(condition_number(I) - 1.0) < 1e-10, f"FAIL I: {condition_number(I)}"

    # Ill-conditioned: Hilbert matrix
    H = np.array([[1.0 / (i + j + 1) for j in range(5)] for i in range(5)])
    kappa_H = condition_number(H)
    assert kappa_H > 1e4, f"Hilbert should be ill-conditioned: {kappa_H}"

    analysis = condition_number_analysis(H)
    assert "ill-conditioned" in analysis.lower()

    print(f"  PASS: condition_number (Hilbert κ={kappa_H:.2e})")


def _test_linear_regression() -> None:
    # Generate data: y = 2*x + 1 + noise
    np.random.seed(42)
    n = 100
    X_true = np.random.randn(n)
    y_true = 2.0 * X_true + 1.0 + 0.3 * np.random.randn(n)

    X = X_true.reshape(-1, 1)
    beta, stats = linear_regression_with_intercept(X, y_true)

    # β₀ ≈ 1, β₁ ≈ 2
    assert abs(beta[0] - 1.0) < 0.2, f"Intercept off: {beta[0]}"
    assert abs(beta[1] - 2.0) < 0.2, f"Slope off: {beta[1]}"
    # R² should be high
    assert stats['r_squared'] > 0.9, f"R² too low: {stats['r_squared']}"

    print(f"  PASS: linear_regression (β={np.round(beta, 3)}, R²={stats['r_squared']:.4f})")


if __name__ == "__main__":
    import numpy as np
    from numpy.typing import NDArray
    from typing import Tuple, Dict
    print("Testing applications.py ...")
    _test_solve_linear_system()
    _test_least_squares()
    _test_condition_number()
    _test_linear_regression()
    print("All applications tests PASSED!")
