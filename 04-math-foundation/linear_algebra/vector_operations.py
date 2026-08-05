"""
Vector Operations for ML/AI Linear Algebra Foundation.

Implements fundamental vector operations including:
- Addition, scalar multiplication
- Dot product, cross product (3D)
- Norms (L1, L2, L-infinity)
- Cosine similarity, vector projection
- Gram-Schmidt orthogonalization

All implementations use numpy arrays and include comprehensive tests.
"""

import numpy as np
from numpy.typing import NDArray
from typing import Tuple, List


def vector_add(v1: NDArray[np.float64], v2: NDArray[np.float64]) -> NDArray[np.float64]:
    """Add two vectors element-wise.

    Args:
        v1: First vector of shape (n,) or (n, 1).
        v2: Second vector of shape (n,) or (n, 1).

    Returns:
        Element-wise sum as a numpy array.

    Raises:
        ValueError: If vectors have different shapes.

    Complexity: O(n) time, O(n) space.
    """
    if v1.shape != v2.shape:
        raise ValueError(f"Shape mismatch: {v1.shape} vs {v2.shape}")
    return v1 + v2


def scalar_multiply(v: NDArray[np.float64], scalar: float) -> NDArray[np.float64]:
    """Multiply a vector by a scalar.

    Args:
        v: Input vector of shape (n,).
        scalar: Scalar multiplier.

    Returns:
        Scaled vector.

    Complexity: O(n) time, O(n) space.
    """
    return v * scalar


def dot_product(v1: NDArray[np.float64], v2: NDArray[np.float64]) -> float:
    """Compute the dot (inner) product of two vectors.

    The dot product is defined as sum(v1_i * v2_i) for i = 1..n.
    Geometrically, it equals ||v1|| * ||v2|| * cos(theta), where theta
    is the angle between v1 and v2.

    Args:
        v1, v2: Input vectors of shape (n,).

    Returns:
        Scalar dot product.

    Raises:
        ValueError: If vectors have different shapes.

    Complexity: O(n) time, O(1) space.

    Example:
        >>> dot_product(np.array([1, 2, 3]), np.array([4, 5, 6]))
        32  # 1*4 + 2*5 + 3*6 = 4 + 10 + 18 = 32
    """
    if v1.shape != v2.shape:
        raise ValueError(f"Shape mismatch: {v1.shape} vs {v2.shape}")
    return float(np.dot(v1, v2))


def cross_product(v1: NDArray[np.float64], v2: NDArray[np.float64]) -> NDArray[np.float64]:
    """Compute the cross product of two 3D vectors.

    The cross product a × b is a vector perpendicular to both a and b,
    with magnitude ||a|| ||b|| sin(theta).
    Direction follows the right-hand rule.

    Formula: a × b = (a₂b₃ - a₃b₂, a₃b₁ - a₁b₃, a₁b₂ - a₂b₁)

    Args:
        v1, v2: 3D vectors of shape (3,).

    Returns:
        Cross product vector of shape (3,).

    Raises:
        ValueError: If vectors are not 3-dimensional.

    Complexity: O(1) time, O(1) space.

    Example:
        >>> cross_product(np.array([1, 0, 0]), np.array([0, 1, 0]))
        array([0, 0, 1])
    """
    if v1.shape != (3,) or v2.shape != (3,):
        raise ValueError("Cross product only defined for 3D vectors")
    return np.cross(v1, v2)


def l1_norm(v: NDArray[np.float64]) -> float:
    """Compute the L1 (Manhattan/taxicab) norm of a vector.

    ||v||₁ = Σ|vᵢ|

    Args:
        v: Input vector of shape (n,).

    Returns:
        L1 norm (non-negative scalar).

    Complexity: O(n) time, O(1) space.
    """
    return float(np.sum(np.abs(v)))


def l2_norm(v: NDArray[np.float64]) -> float:
    """Compute the L2 (Euclidean) norm of a vector.

    ||v||₂ = sqrt(Σ vᵢ²)

    Args:
        v: Input vector of shape (n,).

    Returns:
        L2 norm (non-negative scalar).

    Complexity: O(n) time, O(1) space.
    """
    return float(np.linalg.norm(v))


def l_infinity_norm(v: NDArray[np.float64]) -> float:
    """Compute the L∞ (max/supremum) norm of a vector.

    ||v||∞ = max(|vᵢ|)

    Args:
        v: Input vector of shape (n,).

    Returns:
        L∞ norm (non-negative scalar).

    Complexity: O(n) time, O(1) space.
    """
    return float(np.max(np.abs(v)))


def cosine_similarity(v1: NDArray[np.float64], v2: NDArray[np.float64]) -> float:
    """Compute the cosine similarity between two vectors.

    cos(θ) = (v1 · v2) / (||v1||₂ * ||v2||₂)

    Measures the cosine of the angle between vectors. Returns:
    - 1 if vectors point in the same direction
    - 0 if orthogonal
    - -1 if opposite directions

    Args:
        v1, v2: Input vectors of shape (n,).

    Returns:
        Cosine similarity in [-1, 1].

    Raises:
        ValueError: If either vector is zero-length.

    Complexity: O(n) time, O(1) space.

    Example:
        >>> cosine_similarity(np.array([1, 0]), np.array([1, 0]))
        1.0
        >>> cosine_similarity(np.array([1, 0]), np.array([0, 1]))
        0.0
        >>> cosine_similarity(np.array([1, 0]), np.array([-1, 0]))
        -1.0
    """
    dot = dot_product(v1, v2)
    n1 = l2_norm(v1)
    n2 = l2_norm(v2)
    if n1 == 0 or n2 == 0:
        raise ValueError("Cannot compute cosine similarity with zero-length vector")
    return dot / (n1 * n2)


def vector_projection(v_target: NDArray[np.float64],
                      v_onto: NDArray[np.float64]) -> NDArray[np.float64]:
    """Compute the projection of v_target onto v_onto.

    proj_u(v) = (v · u / u · u) * u

    This gives the component of v_target that lies along v_onto.

    Args:
        v_target: The vector to project.
        v_onto: The direction vector to project onto.

    Returns:
        Projection vector parallel to v_onto.

    Raises:
        ValueError: If v_onto is zero-length.

    Complexity: O(n) time, O(n) space.
    """
    dot_vu = dot_product(v_target, v_onto)
    dot_uu = dot_product(v_onto, v_onto)
    if dot_uu == 0:
        raise ValueError("Cannot project onto a zero-length vector")
    return (dot_vu / dot_uu) * v_onto


def scalar_projection(v_target: NDArray[np.float64],
                      v_onto: NDArray[np.float64]) -> float:
    """Compute the scalar projection (component) of v_target onto v_onto.

    comp_u(v) = (v · u) / ||u||₂

    This is the signed length of the projection.

    Args:
        v_target: The vector to project.
        v_onto: The direction vector.

    Returns:
        Scalar projection (signed magnitude).

    Complexity: O(n) time, O(1) space.
    """
    dot_vu = dot_product(v_target, v_onto)
    norm_u = l2_norm(v_onto)
    if norm_u == 0:
        raise ValueError("Cannot project onto a zero-length vector")
    return dot_vu / norm_u


def gram_schmidt(vectors: List[NDArray[np.float64]]) -> List[NDArray[np.float64]]:
    """Orthogonalize a set of vectors using the Gram-Schmidt process.

    Given a set of linearly independent vectors {v₁, ..., vₖ}, produces
    an orthogonal set {u₁, ..., uₖ} spanning the same subspace.

    Algorithm:
        u₁ = v₁
        uᵢ = vᵢ - Σⱼ₌₁ⁱ⁻¹ proj_uⱼ(vᵢ)  for i = 2..k

    Args:
        vectors: List of (n,) numpy arrays, linearly independent.

    Returns:
        List of orthogonalized vectors (not normalized). Use gram_schmidt_orthonormal
        for orthonormal basis.

    Complexity: O(k²n) time (k vectors, dimension n), O(kn) space.
    """
    if not vectors:
        return []

    n = len(vectors[0])
    for v in vectors:
        if v.shape != (n,) and v.shape != (n, 1):
            raise ValueError(f"All vectors must have shape ({n},); got {v.shape}")

    orthogonal: List[NDArray[np.float64]] = [vectors[0].astype(np.float64).copy()]

    for i in range(1, len(vectors)):
        v_i = vectors[i].astype(np.float64).copy()
        u_i = v_i.copy()
        for j in range(i):
            # Project v_i onto u_j and subtract
            proj = vector_projection(v_i, orthogonal[j])
            u_i = u_i - proj
        orthogonal.append(u_i)

    return orthogonal


def gram_schmidt_orthonormal(
    vectors: List[NDArray[np.float64]]
) -> List[NDArray[np.float64]]:
    """Produce an orthonormal basis using Gram-Schmidt + normalization.

    Args:
        vectors: List of linearly independent vectors.

    Returns:
        List of orthonormal vectors (unit length, mutually orthogonal).

    Complexity: O(k²n) time, O(kn) space.
    """
    orthogonal = gram_schmidt(vectors)
    orthonormal: List[NDArray[np.float64]] = []
    for u in orthogonal:
        norm_u = l2_norm(u)
        if norm_u > 1e-12:
            orthonormal.append(u / norm_u)
        else:
            orthonormal.append(u)  # near-zero vector, keep as-is
    return orthonormal


# ============================================================
# Tests
# ============================================================

def _test_vector_add() -> None:
    v1 = np.array([1.0, 2.0, 3.0])
    v2 = np.array([4.0, 5.0, 6.0])
    result = vector_add(v1, v2)
    assert np.allclose(result, np.array([5.0, 7.0, 9.0])), f"FAIL: {result}"
    print("  PASS: vector_add")


def _test_scalar_multiply() -> None:
    v = np.array([1.0, -2.0, 3.0])
    result = scalar_multiply(v, 2.0)
    assert np.allclose(result, np.array([2.0, -4.0, 6.0])), f"FAIL: {result}"
    print("  PASS: scalar_multiply")


def _test_dot_product() -> None:
    v1 = np.array([1.0, 2.0, 3.0])
    v2 = np.array([4.0, 5.0, 6.0])
    assert abs(dot_product(v1, v2) - 32.0) < 1e-10, f"FAIL: {dot_product(v1, v2)}"
    # Orthogonal vectors
    v3 = np.array([1.0, 0.0])
    v4 = np.array([0.0, 1.0])
    assert abs(dot_product(v3, v4) - 0.0) < 1e-10
    print("  PASS: dot_product")


def _test_cross_product() -> None:
    # Standard basis: i × j = k
    i = np.array([1.0, 0.0, 0.0])
    j = np.array([0.0, 1.0, 0.0])
    k = np.array([0.0, 0.0, 1.0])
    assert np.allclose(cross_product(i, j), k), f"FAIL i×j: {cross_product(i, j)}"
    assert np.allclose(cross_product(j, k), i), f"FAIL j×k: {cross_product(j, k)}"
    assert np.allclose(cross_product(k, i), j), f"FAIL k×i: {cross_product(k, i)}"
    # Anti-commutative: i × j = -(j × i)
    assert np.allclose(cross_product(j, i), -k), "FAIL anti-commutative"
    print("  PASS: cross_product")


def _test_norms() -> None:
    v = np.array([3.0, -4.0])
    assert abs(l1_norm(v) - 7.0) < 1e-10, f"FAIL L1: {l1_norm(v)}"
    assert abs(l2_norm(v) - 5.0) < 1e-10, f"FAIL L2: {l2_norm(v)}"
    assert abs(l_infinity_norm(v) - 4.0) < 1e-10, f"FAIL Linf: {l_infinity_norm(v)}"
    # Zero vector
    z = np.array([0.0, 0.0])
    assert abs(l2_norm(z) - 0.0) < 1e-10
    print("  PASS: norms")


def _test_cosine_similarity() -> None:
    # Same direction
    assert abs(cosine_similarity(np.array([2.0, 0.0]), np.array([5.0, 0.0])) - 1.0) < 1e-10
    # Orthogonal
    assert abs(cosine_similarity(np.array([1.0, 0.0]), np.array([0.0, 1.0])) - 0.0) < 1e-10
    # Opposite
    assert abs(cosine_similarity(np.array([1.0, 0.0]), np.array([-2.0, 0.0])) + 1.0) < 1e-10
    # Acute angle: v1=[1,1], v2=[1,0], dot=1, norms=√2,1 → cos=1/√2 ≈ 0.7071
    sim = cosine_similarity(np.array([1.0, 1.0]), np.array([1.0, 0.0]))
    assert abs(sim - 1.0 / np.sqrt(2)) < 1e-10, f"FAIL: {sim}"
    print("  PASS: cosine_similarity")


def _test_vector_projection() -> None:
    # Project [2, 2] onto [1, 0] → [2, 0]
    v = np.array([2.0, 2.0])
    u = np.array([1.0, 0.0])
    proj = vector_projection(v, u)
    assert np.allclose(proj, np.array([2.0, 0.0])), f"FAIL vector_proj: {proj}"

    # Scalar projection
    s = scalar_projection(v, u)
    assert abs(s - 2.0) < 1e-10, f"FAIL scalar_proj: {s}"

    # Project [3, 4] onto [1, 0]
    v2 = np.array([3.0, 4.0])
    u2 = np.array([1.0, 0.0])
    proj2 = vector_projection(v2, u2)
    assert np.allclose(proj2, np.array([3.0, 0.0])), f"FAIL: {proj2}"
    print("  PASS: vector_projection")


def _test_gram_schmidt() -> None:
    # Simple 2D case: [(1,1), (1,0)]
    v1 = np.array([1.0, 1.0])
    v2 = np.array([1.0, 0.0])
    ortho = gram_schmidt([v1, v2])
    # u1 should equal v1
    assert np.allclose(ortho[0], v1), f"FAIL u1: {ortho[0]}"
    # u2 should be orthogonal to u1
    dot_check = dot_product(ortho[0], ortho[1])
    assert abs(dot_check) < 1e-10, f"FAIL ortho: dot={dot_check}"

    # Orthonormal version
    on_basis = gram_schmidt_orthonormal([v1, v2])
    for u in on_basis:
        assert abs(l2_norm(u) - 1.0) < 1e-10, f"FAIL unit norm: {l2_norm(u)}"
    # Check orthogonality
    assert abs(dot_product(on_basis[0], on_basis[1])) < 1e-10

    # Standard basis — should stay the same after orthonormalization
    std = [np.array([1.0, 0.0, 0.0]),
           np.array([0.0, 1.0, 0.0]),
           np.array([0.0, 0.0, 1.0])]
    on_std = gram_schmidt_orthonormal(std)
    for i, u in enumerate(on_std):
        assert np.allclose(u, std[i]), f"FAIL std {i}: {u}"
    print("  PASS: gram_schmidt")


if __name__ == "__main__":
    print("Testing vector_operations.py ...")
    _test_vector_add()
    _test_scalar_multiply()
    _test_dot_product()
    _test_cross_product()
    _test_norms()
    _test_cosine_similarity()
    _test_vector_projection()
    _test_gram_schmidt()
    print("All vector_operations tests PASSED!")
