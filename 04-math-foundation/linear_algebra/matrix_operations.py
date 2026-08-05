"""
Matrix Operations for ML/AI Linear Algebra Foundation.

Implements fundamental matrix operations including:
- Addition, multiplication, transpose
- Determinant (recursive + LU decomposition)
- Inverse (Gauss-Jordan elimination)
- Rank (row reduction / Gaussian elimination)
- Trace

All implementations use numpy arrays and include comprehensive tests.
"""

import numpy as np
from numpy.typing import NDArray
from typing import Tuple


def matrix_add(A: NDArray[np.float64], B: NDArray[np.float64]) -> NDArray[np.float64]:
    """Add two matrices element-wise.

    Args:
        A, B: Matrices of shape (m, n).

    Returns:
        Element-wise sum of shape (m, n).

    Raises:
        ValueError: If matrices have different shapes.

    Complexity: O(mn) time, O(mn) space.
    """
    if A.shape != B.shape:
        raise ValueError(f"Shape mismatch: {A.shape} vs {B.shape}")
    return A + B


def matrix_multiply(A: NDArray[np.float64], B: NDArray[np.float64]) -> NDArray[np.float64]:
    """Multiply two matrices: C = A @ B.

    C[i,j] = Σₖ A[i,k] * B[k,j]

    Args:
        A: Matrix of shape (m, k).
        B: Matrix of shape (k, n).

    Returns:
        Product matrix of shape (m, n).

    Raises:
        ValueError: If inner dimensions don't match.

    Complexity: O(mkn) using standard algorithm; O(mnk) using numpy's BLAS.

    Example:
        >>> A = np.array([[1, 2], [3, 4]])
        >>> B = np.array([[5, 6], [7, 8]])
        >>> matrix_multiply(A, B)
        array([[19, 22],
               [43, 50]])
    """
    if A.shape[1] != B.shape[0]:
        raise ValueError(
            f"Inner dimensions must match: A({A.shape}) @ B({B.shape})"
        )
    return A @ B


def matrix_transpose(A: NDArray[np.float64]) -> NDArray[np.float64]:
    """Compute the transpose of a matrix: A^T[i,j] = A[j,i].

    Args:
        A: Matrix of shape (m, n).

    Returns:
        Transposed matrix of shape (n, m).

    Complexity: O(mn) time, O(mn) space.
    """
    return A.T


def trace(A: NDArray[np.float64]) -> float:
    """Compute the trace of a square matrix (sum of diagonal elements).

    tr(A) = Σᵢ A[i,i]

    Args:
        A: Square matrix of shape (n, n).

    Returns:
        Trace (scalar).

    Raises:
        ValueError: If A is not square.

    Complexity: O(n) time, O(1) space.
    """
    if A.shape[0] != A.shape[1]:
        raise ValueError(f"Trace requires square matrix, got {A.shape}")
    return float(np.trace(A))


# ——— Determinant ———————————————————————————————————————

def determinant_recursive(A: NDArray[np.float64]) -> float:
    """Compute determinant using recursive cofactor expansion (Laplace).

    This is the definition-based method. O(n!) time — only suitable
    for small matrices (n ≤ 10). For larger matrices, use determinant_lu().

    The determinant is computed by expanding along the first row:
        det(A) = Σⱼ (-1)^{1+j} * A[1,j] * det(M_{1,j})
    where M_{1,j} is the minor of element (1,j).

    Args:
        A: Square matrix of shape (n, n).

    Returns:
        Determinant (scalar).

    Raises:
        ValueError: If A is not square.

    Complexity: O(n!) time, O(n²) stack space.
    """
    if A.shape[0] != A.shape[1]:
        raise ValueError(f"Matrix must be square, got {A.shape}")

    n = A.shape[0]

    # Base cases
    if n == 1:
        return float(A[0, 0])
    if n == 2:
        return float(A[0, 0] * A[1, 1] - A[0, 1] * A[1, 0])

    det = 0.0
    for j in range(n):
        # Compute minor: drop row 0 and column j
        minor = np.delete(np.delete(A, 0, axis=0), j, axis=1)
        sign = 1 if j % 2 == 0 else -1
        det += sign * A[0, j] * determinant_recursive(minor)

    return det


def lu_decomposition(A: NDArray[np.float64]) -> Tuple[NDArray[np.float64],
                                                       NDArray[np.float64]]:
    """Compute LU decomposition with partial pivoting: P @ A = L @ U.

    Uses Doolittle's algorithm (L has unit diagonal).
    Returns L and U such that P @ A = L @ U, where P is an implicit
    permutation tracked in the row-exchanged L and U.

    For pure LU (no pivot): A = L @ U.
    With partial pivoting: P @ A = L @ U (this implementation).

    Args:
        A: Square matrix of shape (n, n).

    Returns:
        Tuple (L, U):
            L: Lower triangular with unit diagonal (n, n).
            U: Upper triangular (n, n).

    Raises:
        ValueError: If A is singular or not square.

    Complexity: O(n³) time, O(n²) space.
    """
    n = A.shape[0]
    if A.shape[0] != A.shape[1]:
        raise ValueError(f"Matrix must be square, got {A.shape}")

    U = A.astype(np.float64).copy()
    L = np.eye(n, dtype=np.float64)
    num_swaps = 0

    for k in range(n):
        # Partial pivoting: find max in column k below diagonal
        pivot_row = k + np.argmax(np.abs(U[k:, k]))
        if pivot_row != k:
            # Swap rows in U
            U[[k, pivot_row]] = U[[pivot_row, k]]
            # Swap rows in L (only columns < k)
            if k > 0:
                L[[k, pivot_row], :k] = L[[pivot_row, k], :k]
            num_swaps += 1

        if abs(U[k, k]) < 1e-15:
            raise ValueError("Matrix is singular or nearly singular")

        for i in range(k + 1, n):
            factor = U[i, k] / U[k, k]
            L[i, k] = factor
            U[i, k:] -= factor * U[k, k:]

    return L, U


def determinant_lu(A: NDArray[np.float64]) -> float:
    """Compute determinant using LU decomposition.

    det(A) = (-1)^{num_swaps} * product of U's diagonal entries.

    Since lu_decomposition performs partial pivoting (row swaps), each
    swap changes the sign of the determinant. The U matrix from the
    decomposition gives det(P @ A) = det(L @ U) = det(U), so we apply
    the sign correction.

    Args:
        A: Square matrix of shape (n, n).

    Returns:
        Determinant (scalar).

    Complexity: O(n³) time, O(n²) space.
    """
    n = A.shape[0]
    U = A.astype(np.float64).copy()
    L = np.eye(n, dtype=np.float64)
    num_swaps = 0

    for k in range(n):
        pivot_row = k + np.argmax(np.abs(U[k:, k]))
        if pivot_row != k:
            U[[k, pivot_row]] = U[[pivot_row, k]]
            if k > 0:
                L[[k, pivot_row], :k] = L[[pivot_row, k], :k]
            num_swaps += 1

        if abs(U[k, k]) < 1e-15:
            return 0.0  # Singular matrix

        for i in range(k + 1, n):
            factor = U[i, k] / U[k, k]
            L[i, k] = factor
            U[i, k:] -= factor * U[k, k:]

    sign = 1 if num_swaps % 2 == 0 else -1
    return sign * float(np.prod(np.diag(U)))


# ——— Inverse ————————————————————————————————————————————

def matrix_inverse(A: NDArray[np.float64]) -> NDArray[np.float64]:
    """Compute matrix inverse using Gauss-Jordan elimination.

    Augments A with the identity matrix [A | I] and performs
    row operations to transform it to [I | A⁻¹].

    Algorithm:
        1. Augment: [A | I]
        2. For each column j:
           a. Partial pivot: swap rows if needed
           b. Scale row j to make pivot = 1
           c. Eliminate all other entries in column j
        3. The right half is A⁻¹

    Args:
        A: Square, invertible matrix of shape (n, n).

    Returns:
        Inverse matrix A⁻¹ of shape (n, n).

    Raises:
        ValueError: If A is singular.

    Complexity: O(n³) time, O(n²) space.
    """
    n = A.shape[0]
    if A.shape[0] != A.shape[1]:
        raise ValueError(f"Matrix must be square, got {A.shape}")

    # Augmented matrix [A | I]
    aug = np.hstack([A.astype(np.float64), np.eye(n, dtype=np.float64)])

    for j in range(n):
        # Partial pivoting
        pivot_row = j + np.argmax(np.abs(aug[j:, j]))
        if pivot_row != j:
            aug[[j, pivot_row]] = aug[[pivot_row, j]]

        if abs(aug[j, j]) < 1e-15:
            raise ValueError("Matrix is singular; cannot invert")

        # Normalize pivot row
        aug[j] /= aug[j, j]

        # Eliminate all other rows
        for i in range(n):
            if i != j:
                aug[i] -= aug[i, j] * aug[j]

    return aug[:, n:]


# ——— Rank ———————————————————————————————————————————————

def matrix_rank(A: NDArray[np.float64], tol: float = 1e-10) -> int:
    """Compute the rank of a matrix using Gaussian elimination.

    The rank is the number of non-zero pivots after row reduction
    (with partial pivoting for numerical stability).

    Args:
        A: Matrix of shape (m, n).
        tol: Tolerance for treating a pivot as zero.

    Returns:
        Integer rank of the matrix.

    Complexity: O(min(m,n)² * max(m,n)) time, O(mn) space.

    Example:
        >>> matrix_rank(np.array([[1, 2, 3], [2, 4, 6]]))
        1  # rows are linearly dependent
    """
    # Work on a copy
    M = A.astype(np.float64).copy()
    m, n = M.shape
    rank = 0
    row = 0

    for col in range(n):
        if row >= m:
            break

        # Find pivot row
        pivot_row = row + np.argmax(np.abs(M[row:, col]))
        if abs(M[pivot_row, col]) < tol:
            continue  # column is linearly dependent

        # Swap rows
        if pivot_row != row:
            M[[row, pivot_row]] = M[[pivot_row, row]]

        rank += 1

        # Eliminate below
        pivot = M[row, col]
        for i in range(row + 1, m):
            factor = M[i, col] / pivot
            M[i, col:] -= factor * M[row, col:]

        row += 1

    return rank


def is_full_rank(A: NDArray[np.float64], tol: float = 1e-10) -> bool:
    """Check if a matrix has full rank (rank = min(m, n)).

    Args:
        A: Matrix of shape (m, n).
        tol: Numerical tolerance for zero pivots.

    Returns:
        True if rank == min(m, n).

    Complexity: O(min(m,n)² * max(m,n)) time.
    """
    return matrix_rank(A, tol) == min(A.shape[0], A.shape[1])


# ============================================================
# Tests
# ============================================================

def _test_matrix_add() -> None:
    A = np.array([[1.0, 2.0], [3.0, 4.0]])
    B = np.array([[5.0, 6.0], [7.0, 8.0]])
    C = matrix_add(A, B)
    assert np.allclose(C, np.array([[6.0, 8.0], [10.0, 12.0]])), f"FAIL: {C}"
    print("  PASS: matrix_add")


def _test_matrix_multiply() -> None:
    A = np.array([[1.0, 2.0], [3.0, 4.0]])
    B = np.array([[5.0, 6.0], [7.0, 8.0]])
    C = matrix_multiply(A, B)
    expected = np.array([[19.0, 22.0], [43.0, 50.0]])
    assert np.allclose(C, expected), f"FAIL: {C}"
    # Identity check
    I = np.eye(3)
    X = np.random.randn(3, 3)
    assert np.allclose(matrix_multiply(X, I), X)
    assert np.allclose(matrix_multiply(I, X), X)
    print("  PASS: matrix_multiply")


def _test_transpose() -> None:
    A = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    AT = matrix_transpose(A)
    assert AT.shape == (3, 2)
    assert np.allclose(AT, np.array([[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]))
    print("  PASS: matrix_transpose")


def _test_trace() -> None:
    A = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
    assert abs(trace(A) - 15.0) < 1e-10, f"FAIL: {trace(A)}"
    print("  PASS: trace")


def _test_determinant() -> None:
    # 2×2
    A2 = np.array([[3.0, 8.0], [4.0, 6.0]])
    # det = 3*6 - 8*4 = 18 - 32 = -14
    assert abs(determinant_recursive(A2) + 14.0) < 1e-10
    assert abs(determinant_lu(A2) + 14.0) < 1e-10

    # 3×3 with known det = 0 (rows dependent)
    A3 = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
    assert abs(determinant_recursive(A3)) < 1e-10
    assert abs(determinant_lu(A3)) < 1e-10

    # Identity
    I3 = np.eye(3)
    assert abs(determinant_recursive(I3) - 1.0) < 1e-10
    assert abs(determinant_lu(I3) - 1.0) < 1e-10

    # Random matrix: compare with numpy
    np.random.seed(42)
    for _ in range(10):
        n = np.random.randint(2, 7)
        M = np.random.randn(n, n)
        d1 = determinant_recursive(M)
        d2 = determinant_lu(M)
        d_np = np.linalg.det(M)
        assert abs(d1 - d_np) < 1e-8, f"Recursive mismatch: {d1} vs {d_np}"
        assert abs(d2 - d_np) < 1e-8, f"LU mismatch: {d2} vs {d_np}"
    print("  PASS: determinant (recursive + LU vs numpy)")


def _test_inverse() -> None:
    # Simple 2×2
    A = np.array([[4.0, 7.0], [2.0, 6.0]])
    inv_A = matrix_inverse(A)
    expected = np.linalg.inv(A)
    assert np.allclose(inv_A, expected, atol=1e-10), \
        f"FAIL: {inv_A} vs {expected}"

    # Verify: A @ A⁻¹ = I
    assert np.allclose(A @ inv_A, np.eye(2), atol=1e-10)
    assert np.allclose(inv_A @ A, np.eye(2), atol=1e-10)

    # 3×3 random
    np.random.seed(123)
    for _ in range(5):
        M = np.random.randn(5, 5)
        inv_M = matrix_inverse(M)
        assert np.allclose(M @ inv_M, np.eye(5), atol=1e-10)
    print("  PASS: matrix_inverse")


def _test_rank() -> None:
    # Full rank 3×3
    A = np.array([[1.0, 2.0, 3.0], [0.0, 1.0, 4.0], [5.0, 6.0, 0.0]])
    assert matrix_rank(A) == 3, f"FAIL: rank={matrix_rank(A)}"

    # Rank 1: rows are multiples
    B = np.array([[1.0, 2.0, 3.0], [2.0, 4.0, 6.0], [3.0, 6.0, 9.0]])
    assert matrix_rank(B) == 1, f"FAIL: rank={matrix_rank(B)}"

    # Rank 2: 3×3, third row = row1 + row2
    C = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0]])
    assert matrix_rank(C) == 2, f"FAIL: rank={matrix_rank(C)}"

    # Rectangular matrix
    D = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    assert matrix_rank(D) == 2

    assert is_full_rank(A) is True
    assert is_full_rank(B) is False
    print("  PASS: matrix_rank")


if __name__ == "__main__":
    print("Testing matrix_operations.py ...")
    _test_matrix_add()
    _test_matrix_multiply()
    _test_transpose()
    _test_trace()
    _test_determinant()
    _test_inverse()
    _test_rank()
    print("All matrix_operations tests PASSED!")
