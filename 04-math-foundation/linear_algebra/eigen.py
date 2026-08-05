"""
Eigenvalues, Eigenvectors, SVD, and PCA for ML/AI Foundations.

Implements:
- Power iteration for dominant eigenvalue/eigenvector
- QR algorithm (simplified)
- Singular Value Decomposition (SVD) explanation + usage
- Principal Component Analysis (PCA) via SVD

All implementations use numpy and include comprehensive tests.
"""

import numpy as np
from numpy.typing import NDArray
from typing import Tuple, Optional


# ============================================================
# Power Iteration
# ============================================================

def power_iteration(
    A: NDArray[np.float64],
    max_iter: int = 1000,
    tol: float = 1e-10
) -> Tuple[float, NDArray[np.float64], int]:
    """Find the dominant eigenvalue and eigenvector using power iteration.

    Given a square matrix A with a unique dominant eigenvalue, the power
    iteration converges to the eigenvector associated with the largest
    eigenvalue (in absolute value).

    Algorithm:
        1. Start with random vector v₀
        2. v_{k+1} = A @ v_k / ||A @ v_k||
        3. λ_{k+1} = (v_{k+1}^T @ A @ v_{k+1}) / (v_{k+1}^T @ v_{k+1})  (Rayleigh quotient)

    The dominant eigenvalue λ₁ satisfies |λ₁| > |λᵢ| for all i > 1.
    Convergence rate depends on |λ₂/λ₁|.

    Args:
        A: Square matrix of shape (n, n).
        max_iter: Maximum iterations.
        tol: Convergence tolerance.

    Returns:
        Tuple (eigenvalue, eigenvector, num_iterations):
            eigenvalue: Dominant eigenvalue (float).
            eigenvector: Associated eigenvector, normalized to unit L2 norm.
            num_iterations: Number of iterations performed.

    Raises:
        ValueError: If A is not square.

    Complexity: O(n²) per iteration (O(n²) overall assuming fixed iterations).
    """
    n = A.shape[0]
    if A.shape[0] != A.shape[1]:
        raise ValueError(f"Matrix must be square, got {A.shape}")

    # Initialize random vector
    np.random.seed(42)
    v = np.random.randn(n)
    v = v / np.linalg.norm(v)

    prev_eigval = 0.0

    for it in range(max_iter):
        # Power step
        Av = A @ v
        v_next = Av / np.linalg.norm(Av)

        # Rayleigh quotient for eigenvalue
        eigval = float(v_next @ (A @ v_next))

        # Check convergence
        if abs(eigval - prev_eigval) < tol:
            return eigval, v_next, it + 1

        v = v_next
        prev_eigval = eigval

    # Max iterations reached
    eigval = float(v @ (A @ v))
    return eigval, v, max_iter


def rayleigh_quotient(A: NDArray[np.float64], v: NDArray[np.float64]) -> float:
    """Compute the Rayleigh quotient: R(A, v) = (v^T A v) / (v^T v).

    For an eigenvector v, R(A, v) gives the corresponding eigenvalue.
    For approximate eigenvectors, it gives the best eigenvalue estimate
    in the least-squares sense.

    Args:
        A: Square matrix (n, n).
        v: Non-zero vector (n,).

    Returns:
        Rayleigh quotient (scalar).

    Complexity: O(n²) time, O(1) space.
    """
    return float((v @ (A @ v)) / (v @ v))


# ============================================================
# QR Algorithm (Simplified)
# ============================================================

def qr_decomposition(A: NDArray[np.float64]) -> Tuple[NDArray[np.float64],
                                                       NDArray[np.float64]]:
    """Compute QR decomposition using Gram-Schmidt process.

    Decomposes A into orthogonal Q and upper triangular R such that A = Q @ R.

    Q: Orthogonal matrix (Q^T @ Q = I), whose columns form an orthonormal basis.
    R: Upper triangular matrix.

    Args:
        A: Matrix of shape (m, n) with linearly independent columns.

    Returns:
        Tuple (Q, R):
            Q: Orthogonal matrix (m, n).
            R: Upper triangular (n, n).

    Complexity: O(mn²) time, O(mn) space.
    """
    m, n = A.shape
    Q = np.zeros((m, n), dtype=np.float64)
    R = np.zeros((n, n), dtype=np.float64)

    for j in range(n):
        v = A[:, j].astype(np.float64).copy()

        # Subtract projections onto previous q vectors
        for i in range(j):
            R[i, j] = float(Q[:, i] @ A[:, j])
            v = v - R[i, j] * Q[:, i]

        R[j, j] = float(np.linalg.norm(v))
        if R[j, j] < 1e-15:
            Q[:, j] = v
        else:
            Q[:, j] = v / R[j, j]

    return Q, R


def qr_algorithm(
    A: NDArray[np.float64],
    max_iter: int = 500,
    tol: float = 1e-10
) -> Tuple[NDArray[np.float64], NDArray[np.float64], int]:
    """Compute all eigenvalues using the QR algorithm (without shifts).

    The basic (unshifted) QR algorithm:
        A₀ = A
        For k = 0, 1, ...:
            Q_k, R_k = QR(A_k)
            A_{k+1} = R_k @ Q_k

    As k → ∞, A_k converges to an upper triangular matrix T whose
    diagonal entries are the eigenvalues of A. This version works
    well for symmetric matrices; for non-symmetric matrices, the
    shifted QR algorithm is preferred.

    Args:
        A: Square matrix of shape (n, n).
        max_iter: Maximum iterations.
        tol: Convergence tolerance (off-diagonal entries).

    Returns:
        Tuple (eigenvalues, eigenvectors_approx, num_iterations):
            eigenvalues: Diagonal entries of the converged matrix (n,).
            eigenvectors_approx: Product of Q matrices ≈ eigenvectors (n, n).
            num_iterations: Number of iterations performed.

    Complexity: O(n³) per iteration, O(n³) overall.
    """
    n = A.shape[0]
    if A.shape[0] != A.shape[1]:
        raise ValueError(f"Matrix must be square, got {A.shape}")

    Ak = A.astype(np.float64).copy()
    Q_accum = np.eye(n, dtype=np.float64)

    for it in range(max_iter):
        Q, R = qr_decomposition(Ak)
        Ak = R @ Q
        Q_accum = Q_accum @ Q

        # Check convergence: sum of absolute off-diagonal entries
        off_diag = np.sum(np.abs(Ak - np.diag(np.diag(Ak))))
        if off_diag < tol:
            return np.diag(Ak), Q_accum, it + 1

    return np.diag(Ak), Q_accum, max_iter


# ============================================================
# SVD — Explanation & Usage
# ============================================================

def svd_explained() -> str:
    """Return an educational explanation of Singular Value Decomposition (SVD).

    Returns:
        String explaining SVD concepts and uses.
    """
    return """
=== Singular Value Decomposition (SVD) ===

SVD factorizes any m×n matrix A into three matrices:
    A = U @ Σ @ Vᵀ

Where:
- U: m×m orthogonal matrix (left singular vectors).
     Columns are eigenvectors of AAᵀ.
- Σ: m×n diagonal matrix of singular values σ₁ ≥ σ₂ ≥ ... ≥ σᵣ > 0.
     σᵢ = sqrt(eigenvalues of AᵀA) = sqrt(eigenvalues of AAᵀ).
- V: n×n orthogonal matrix (right singular vectors).
     Columns are eigenvectors of AᵀA.

Key Properties:
1. Rank r = number of non-zero singular values.
2. ||A||₂ = σ₁ (spectral norm).
3. ||A||_F = sqrt(Σ σᵢ²) (Frobenius norm).
4. Condition number κ(A) = σ₁ / σᵣ.

Applications in ML/AI:
- PCA: dimensionality reduction via truncated SVD
- Latent Semantic Analysis (LSA/LSI)
- Recommender systems (collaborative filtering)
- Pseudo-inverse for least squares
- Image compression: keep top-k singular values
- Noise reduction / denoising
"""


def low_rank_approximation(
    A: NDArray[np.float64], k: int
) -> NDArray[np.float64]:
    """Compute the best rank-k approximation of A via truncated SVD.

    By the Eckart-Young theorem, A_k = U[:, :k] @ Σ[:k, :k] @ V[:k, :]
    is the optimal rank-k approximation in both Frobenius and spectral norms.

    Args:
        A: Matrix of shape (m, n).
        k: Target rank (k ≤ min(m, n)).

    Returns:
        Rank-k approximation matrix of shape (m, n).

    Complexity: O(mn * min(m,n)) using numpy's SVD.
    """
    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    k = min(k, len(S))
    return U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]


# ============================================================
# PCA via SVD
# ============================================================

def pca_svd(
    X: NDArray[np.float64],
    n_components: Optional[int] = None
) -> Tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """Perform Principal Component Analysis (PCA) using SVD.

    PCA finds directions of maximum variance in the data. Using SVD:
        1. Center the data: X̂ = X - mean(X)
        2. Compute SVD: X̂ = U Σ Vᵀ
        3. Principal components = V columns (right singular vectors)
        4. Projected data = X̂ @ V[:, :k] = U[:, :k] @ Σ[:k, :k]
        5. Explained variance = σᵢ² / (n_samples - 1)

    Args:
        X: Data matrix of shape (n_samples, n_features).
        n_components: Number of principal components to keep.
                       If None, keeps all.

    Returns:
        Tuple (projected, components, explained_variance_ratio):
            projected: Transformed data (n_samples, n_components).
            components: Principal axes (n_components, n_features).
            explained_variance_ratio: Variance ratio per component (n_components,).

    Complexity: O(n_samples * n_features * min(n_samples, n_features)).
    """
    n_samples = X.shape[0]

    # 1. Center the data
    X_centered = X - np.mean(X, axis=0)

    # 2. SVD of centered data
    U, S, Vt = np.linalg.svd(X_centered, full_matrices=False)

    # 3. Explained variance (singular values squared divided by n-1)
    eigenvalues = S ** 2 / (n_samples - 1)
    total_var = np.sum(eigenvalues)
    explained_variance_ratio = eigenvalues / total_var

    # 4. Keep requested components
    if n_components is not None:
        Vt = Vt[:n_components, :]
        S = S[:n_components]
        explained_variance_ratio = explained_variance_ratio[:n_components]

    # 5. Project data
    projected = X_centered @ Vt.T  # (n_samples, n_components)

    return projected, Vt, explained_variance_ratio


def pca_transform(
    X: NDArray[np.float64],
    components: NDArray[np.float64]
) -> NDArray[np.float64]:
    """Transform new data using pre-computed PCA components.

    Args:
        X: Data matrix (n_samples, n_features).
        components: PCA components from pca_svd (n_components, n_features).

    Returns:
        Projected data (n_samples, n_components).
    """
    X_centered = X - np.mean(X, axis=0)
    return X_centered @ components.T


# ============================================================
# Tests
# ============================================================

def _test_power_iteration() -> None:
    # Test with a symmetric matrix with known dominant eigenvalue
    A = np.array([[4.0, 1.0], [1.0, 3.0]], dtype=np.float64)
    eigval, eigvec, iters = power_iteration(A)
    # True eigenvalues: (5 + √2)/2 ≈ 3.207..., and (5 - √2)/2 ≈ 1.793...
    # The dominant is ≈ 4.207... wait, let me compute properly.
    # det(A - λI) = (4-λ)(3-λ) - 1 = λ² - 7λ + 11 = 0
    # λ = (7 ± √(49-44))/2 = (7 ± √5)/2
    # λ₁ ≈ (7 + 2.236)/2 = 4.618, λ₂ ≈ (7 - 2.236)/2 = 2.382
    true_eigvals = np.sort(np.linalg.eigvals(A))[::-1]
    assert abs(eigval - true_eigvals[0]) < 1e-6, \
        f"FAIL: got {eigval}, expected {true_eigvals[0]}"
    # Verify eigenpair: A v = λ v
    assert np.allclose(A @ eigvec, eigval * eigvec, atol=1e-6), \
        "FAIL: Av != λv"
    print(f"  PASS: power_iteration (converged in {iters} iters)")


def _test_rayleigh_quotient() -> None:
    A = np.array([[4.0, 0.0], [0.0, 3.0]])
    # Eigenvector [1, 0] gives eigenvalue 4
    v = np.array([1.0, 0.0])
    rq = rayleigh_quotient(A, v)
    assert abs(rq - 4.0) < 1e-10, f"FAIL: {rq}"
    print("  PASS: rayleigh_quotient")


def _test_qr_decomposition() -> None:
    A = np.array([[12.0, -51.0, 4.0],
                  [6.0, 167.0, -68.0],
                  [-4.0, 24.0, -41.0]], dtype=np.float64)
    Q, R = qr_decomposition(A)
    # Check Q^T @ Q = I
    assert np.allclose(Q.T @ Q, np.eye(3), atol=1e-10), "Q not orthogonal"
    # Check A = Q @ R
    assert np.allclose(Q @ R, A, atol=1e-10), "A != QR"
    # Check R is upper triangular
    for i in range(3):
        for j in range(i):
            assert abs(R[i, j]) < 1e-10, f"R not upper triangular: R[{i},{j}]={R[i,j]}"
    print("  PASS: qr_decomposition")


def _test_qr_algorithm() -> None:
    # Symmetric matrix
    A = np.array([[4.0, 1.0, 2.0],
                  [1.0, 3.0, 1.0],
                  [2.0, 1.0, 5.0]], dtype=np.float64)
    eigvals, eigvecs, iters = qr_algorithm(A, max_iter=1000, tol=1e-8)
    true_eigvals = np.sort(np.linalg.eigvalsh(A))
    eigvals_sorted = np.sort(eigvals)
    assert np.allclose(eigvals_sorted, true_eigvals, atol=1e-6), \
        f"FAIL: {eigvals_sorted} vs {true_eigvals}"
    print(f"  PASS: qr_algorithm (converged in {iters} iters)")


def _test_low_rank_approximation() -> None:
    np.random.seed(42)
    A = np.random.randn(10, 8)
    A_r2 = low_rank_approximation(A, k=2)
    assert A_r2.shape == A.shape
    # Rank should be ≤ 2
    U, S, Vt = np.linalg.svd(A_r2)
    rank = np.sum(S > 1e-10)
    assert rank <= 2, f"Rank is {rank}"
    print("  PASS: low_rank_approximation")


def _test_pca() -> None:
    # Simple 2D dataset with known principal direction
    np.random.seed(42)
    n = 100
    # Generate data with strong correlation along [1, 1]
    t = np.random.randn(n)
    X = np.column_stack([3 * t + 0.1 * np.random.randn(n),
                         3 * t + 0.1 * np.random.randn(n)])
    projected, components, var_ratio = pca_svd(X, n_components=2)

    # First component should explain most variance
    assert var_ratio[0] > 0.9, f"PC1 ratio too low: {var_ratio[0]}"
    assert np.abs(np.sum(var_ratio) - 1.0) < 1e-10, "Not 100% variance"

    # First component should point roughly along [1, 1]/√2
    pc1 = components[0]
    direction = np.array([1.0, 1.0]) / np.sqrt(2)
    # PC1 should be ≈ ±[1/√2, 1/√2]
    sim = abs(np.dot(np.abs(pc1), direction))
    assert sim > 0.95, f"PC1 direction wrong: {pc1}, sim={sim}"

    # Transform test
    X_test = np.column_stack([2 * np.random.randn(20),
                              2 * np.random.randn(20)])
    proj_test = pca_transform(X_test, components)
    assert proj_test.shape == (20, 2)

    print("  PASS: PCA via SVD")


if __name__ == "__main__":
    print("Testing eigen.py ...")
    _test_power_iteration()
    _test_rayleigh_quotient()
    _test_qr_decomposition()
    _test_qr_algorithm()
    _test_low_rank_approximation()
    _test_pca()
    print("All eigen tests PASSED!")
