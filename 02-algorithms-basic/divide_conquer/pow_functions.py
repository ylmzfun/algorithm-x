"""
Fast Exponentiation and Matrix Power Functions
===============================================

Fast exponentiation (binary exponentiation) reduces the number of
multiplications from O(n) to O(log n) by exploiting the binary
representation of the exponent.

Functions:
- fast_pow               : Iterative fast power (x^n).
- fast_pow_recursive     : Recursive fast power for clarity.
- fast_pow_mod           : (x^n) % mod — handles large numbers.
- matrix_fast_pow        : Raise a square matrix to a power.
- fibonacci_matrix       : Nth Fibonacci number via matrix exponentiation.
"""

from typing import List


# ---------------------------------------------------------------------------
# Fast Power (iterative)
# ---------------------------------------------------------------------------

def fast_pow(x: float, n: int) -> float:
    """
    Compute x^n using iterative binary exponentiation.

    Parameters
    ----------
    x : float
        Base.
    n : int
        Exponent (may be negative).

    Returns
    -------
    float
        x raised to the power n.

    Time  : O(log n)
    Space : O(1)

    Example
    -------
    >>> fast_pow(2, 10)
    1024.0
    >>> fast_pow(2, -2)
    0.25
    """
    if n < 0:
        x = 1.0 / x
        n = -n
    result = 1.0
    while n:
        if n & 1:
            result *= x
        x *= x
        n >>= 1
    return result


# ---------------------------------------------------------------------------
# Fast Power (recursive)
# ---------------------------------------------------------------------------

def fast_pow_recursive(x: float, n: int) -> float:
    """
    Compute x^n using recursive binary exponentiation.

    Parameters
    ----------
    x : float
        Base.
    n : int
        Exponent (must be >= 0).

    Returns
    -------
    float
        x^n.

    Time  : O(log n)
    Space : O(log n) recursion

    Raises
    ------
    ValueError
        If n is negative.
    """
    if n < 0:
        raise ValueError("fast_pow_recursive expects n >= 0; use fast_pow for negative exponents")
    if n == 0:
        return 1.0
    half = fast_pow_recursive(x, n // 2)
    if n % 2 == 0:
        return half * half
    else:
        return half * half * x


# ---------------------------------------------------------------------------
# Fast Power with Modulo
# ---------------------------------------------------------------------------

def fast_pow_mod(x: int, n: int, mod: int) -> int:
    """
    Compute (x^n) % mod using modular binary exponentiation.

    Parameters
    ----------
    x : int
        Base (non-negative).
    n : int
        Exponent (non-negative).
    mod : int
        Modulus (positive).

    Returns
    -------
    int
        (x^n) % mod.

    Time  : O(log n)
    Space : O(1)

    Example
    -------
    >>> fast_pow_mod(2, 10, 1000)
    24   # 2^10 = 1024, 1024 % 1000 = 24
    """
    result = 1
    x %= mod
    while n:
        if n & 1:
            result = (result * x) % mod
        x = (x * x) % mod
        n >>= 1
    return result


# ---------------------------------------------------------------------------
# Matrix Fast Power
# ---------------------------------------------------------------------------

def _mat_mul(A: List[List[int]], B: List[List[int]], mod: int) -> List[List[int]]:
    """Multiply two square matrices modulo `mod`."""
    size = len(A)
    C = [[0] * size for _ in range(size)]
    for i in range(size):
        for k in range(size):
            if A[i][k] == 0:
                continue
            aik = A[i][k]
            for j in range(size):
                C[i][j] = (C[i][j] + aik * B[k][j]) % mod
    return C


def matrix_fast_pow(mat: List[List[int]], n: int, mod: int = 10**9 + 7) -> List[List[int]]:
    """
    Raise a square matrix to the power n using binary exponentiation.

    Parameters
    ----------
    mat : List[List[int]]
        Square matrix.
    n : int
        Exponent (non-negative).
    mod : int
        Modulus for intermediate results (default 1e9+7).

    Returns
    -------
    List[List[int]]
        mat^n (mod mod).

    Time  : O(m³ log n) where m is the matrix dimension.
    Space : O(m²)
    """
    size = len(mat)
    # Identity matrix
    result = [[int(i == j) for j in range(size)] for i in range(size)]
    base = [row[:] for row in mat]

    while n:
        if n & 1:
            result = _mat_mul(result, base, mod)
        base = _mat_mul(base, base, mod)
        n >>= 1
    return result


# ---------------------------------------------------------------------------
# Fibonacci via Matrix Fast Power
# ---------------------------------------------------------------------------

def fibonacci_matrix(n: int, mod: int = 10**9 + 7) -> int:
    """
    Compute the n-th Fibonacci number using matrix exponentiation.

    Uses the identity:
        [[F_{n+1}, F_n    ],
         [F_n    , F_{n-1}]] = [[1, 1], [1, 0]]^n

    Parameters
    ----------
    n : int
        Index (0-based: F₀ = 0, F₁ = 1).
    mod : int
        Modulus.

    Returns
    -------
    int
        F_n % mod.

    Time  : O(log n)
    Space : O(1)

    Example
    -------
    >>> fibonacci_matrix(10)
    55
    >>> fibonacci_matrix(50)
    586268941   # (12586269025 % 1e9+7)
    """
    if n <= 1:
        return n
    base = [[1, 1], [1, 0]]
    result = matrix_fast_pow(base, n - 1, mod)
    return result[0][0]  # F_n


# ===========================================================================
# Tests
# ===========================================================================

if __name__ == "__main__":
    print("=== Fast Power Tests ===\n")

    # fast_pow
    cases = [
        (2, 10, 1024.0),
        (3, 5, 243.0),
        (2, -2, 0.25),
        (5, 0, 1.0),
        (2, 1, 2.0),
    ]
    ok = True
    for x, n, exp in cases:
        res = fast_pow(x, n)
        if abs(res - exp) > 1e-12:
            print(f"  FAIL fast_pow {x}^{n} = {res} != {exp}")
            ok = False
    print(f"  {'PASS' if ok else 'FAIL'} fast_pow (iterative)")

    # fast_pow_recursive
    ok = True
    for x, n, exp in [(2, 10, 1024.0), (3, 5, 243.0), (5, 0, 1.0)]:
        res = fast_pow_recursive(x, n)
        if abs(res - exp) > 1e-12:
            print(f"  FAIL fast_pow_recursive {x}^{n} = {res} != {exp}")
            ok = False
    print(f"  {'PASS' if ok else 'FAIL'} fast_pow_recursive")

    # fast_pow_mod
    ok = True
    cases = [
        (2, 10, 1000, 24),
        (3, 7, 5, 2),   # 3^7=2187, 2187%5=2
        (7, 256, 13, 9),
    ]
    for x, n, mod, exp in cases:
        res = fast_pow_mod(x, n, mod)
        if res != exp:
            print(f"  FAIL fast_pow_mod {x}^{n} % {mod} = {res} != {exp}")
            ok = False
    print(f"  {'PASS' if ok else 'FAIL'} fast_pow_mod")

    # matrix_fast_pow
    base = [[1, 2], [3, 4]]
    # Verify M^3 manually (simple)
    m2 = _mat_mul(base, base, 10**9 + 7)
    m3 = _mat_mul(m2, base, 10**9 + 7)
    res = matrix_fast_pow(base, 3)
    ok = res == m3
    print(f"  {'PASS' if ok else 'FAIL'} matrix_fast_pow")

    # fibonacci_matrix
    fibs = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
    ok = True
    for i, expected in enumerate(fibs):
        res = fibonacci_matrix(i, 10**9 + 7)
        if res != expected:
            print(f"  FAIL fibonacci_matrix F({i}) = {res} != {expected}")
            ok = False
    # Large n test
    f50 = fibonacci_matrix(50)  # should be 12586269025 % 1e9+7
    assert f50 == 12586269025 % (10**9 + 7)
    print(f"  {'PASS' if ok else 'FAIL'} fibonacci_matrix")
    print("  PASS fibonacci_matrix large n (F50)")

    print("\nAll fast power tests completed!")
