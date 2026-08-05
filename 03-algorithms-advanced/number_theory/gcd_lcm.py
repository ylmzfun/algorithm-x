"""
GCD, LCM, and related algorithms.

Contains:
- Euclidean algorithm (recursive + iterative)
- Extended Euclidean algorithm
- Modular inverse
- Linear Diophantine equation solver
- Chinese Remainder Theorem
"""

import math
from typing import Optional, Tuple


# ======================================================================
# GCD (Greatest Common Divisor)
# ======================================================================

def gcd(a: int, b: int) -> int:
    """
    Compute GCD using the iterative Euclidean algorithm.

    Args:
        a, b: Non-negative integers.

    Returns:
        Greatest common divisor of a and b.

    Time:  O(log min(a, b))
    Space: O(1)
    """
    while b:
        a, b = b, a % b
    return a


def gcd_recursive(a: int, b: int) -> int:
    """
    Compute GCD using the recursive Euclidean algorithm.

    Args:
        a, b: Non-negative integers.

    Returns:
        Greatest common divisor of a and b.

    Time:  O(log min(a, b))
    Space: O(log min(a, b)) recursion depth
    """
    if b == 0:
        return a
    return gcd_recursive(b, a % b)


# ======================================================================
# LCM (Least Common Multiple)
# ======================================================================

def lcm(a: int, b: int) -> int:
    """
    Compute the least common multiple of a and b.

    Args:
        a, b: Positive integers.

    Returns:
        LCM(a, b).  Returns 0 if either is 0.

    Time:  O(log min(a, b))
    """
    if a == 0 or b == 0:
        return 0
    return a // gcd(a, b) * b  # divide first to avoid overflow


# ======================================================================
# Extended Euclidean Algorithm
# ======================================================================

def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Compute (g, x, y) such that a*x + b*y = g = gcd(a, b).

    Args:
        a, b: Integers.

    Returns:
        (g, x, y) where g = gcd(a, b) and a*x + b*y = g.

    Time:  O(log min(|a|, |b|))
    Space: O(1)
    """
    if b == 0:
        return (a, 1, 0)

    g, x1, y1 = extended_gcd(b, a % b)
    # a*x + b*y = g
    # b*x1 + (a % b)*y1 = g
    # a % b = a - (a // b) * b
    # => b*x1 + (a - (a//b)*b)*y1 = g
    # => a*y1 + b*(x1 - (a//b)*y1) = g
    x = y1
    y = x1 - (a // b) * y1
    return (g, x, y)


# ======================================================================
# Modular Inverse
# ======================================================================

def mod_inverse(a: int, m: int) -> Optional[int]:
    """
    Compute the modular multiplicative inverse of a modulo m.

    a * x ≡ 1 (mod m).  The inverse exists iff gcd(a, m) == 1.

    Args:
        a: The integer to invert.
        m: The modulus.

    Returns:
        The modular inverse x (0 < x < m), or None if it does not exist.

    Time:  O(log min(a, m))
    """
    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        return None  # inverse does not exist
    return x % m


# ======================================================================
# Linear Diophantine Equation
# ======================================================================

def solve_linear_diophantine(
    a: int, b: int, c: int
) -> Optional[Tuple[int, int, int, int]]:
    """
    Find one integer solution (x0, y0) to the equation a*x + b*y = c.

    General solution:
        x = x0 + k * (b / g)
        y = y0 - k * (a / g)

    Args:
        a, b, c: Integer coefficients.

    Returns:
        (x0, y0, dx, dy) where (x0, y0) is one solution and
        (dx, dy) = (b/g, a/g) gives the step for generating all solutions.
        Returns None if no solution exists (g does not divide c).

    Time:  O(log min(|a|, |b|))
    """
    g, x, y = extended_gcd(abs(a), abs(b))
    if c % g != 0:
        return None

    # Scale the solution
    factor = c // g
    x0 = x * factor
    y0 = y * factor

    # Adjust for negative a, b
    if a < 0:
        x0 = -x0
    if b < 0:
        y0 = -y0

    dx = b // g
    dy = a // g

    return (x0, y0, dx, dy)


# ======================================================================
# Chinese Remainder Theorem
# ======================================================================

def chinese_remainder(
    remainders: list, moduli: list
) -> Optional[Tuple[int, int]]:
    """
    Solve the system of congruences:
        x ≡ r_i (mod m_i) for all i

    using the Chinese Remainder Theorem (pairwise coprime moduli).

    Args:
        remainders: List of r_i values.
        moduli: List of pairwise coprime m_i values.

    Returns:
        (x, M) where x is the unique solution modulo M = ∏ m_i.
        Returns None if moduli are not pairwise coprime.

    Time:  O(n * log M)
    """
    if len(remainders) != len(moduli) or len(moduli) == 0:
        return None

    # Check pairwise coprime
    for i in range(len(moduli)):
        for j in range(i + 1, len(moduli)):
            if gcd(moduli[i], moduli[j]) != 1:
                return None

    M = 1
    for m in moduli:
        M *= m

    x = 0
    for r, m in zip(remainders, moduli):
        Mi = M // m
        inv = mod_inverse(Mi, m)
        if inv is None:
            return None
        x = (x + r * Mi * inv) % M

    return x % M, M


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    import sys

    all_pass = True

    # --- GCD ---
    if gcd(48, 18) != 6:
        print(f"FAIL gcd(48,18): {gcd(48,18)}")
        all_pass = False
    if gcd_recursive(48, 18) != 6:
        print(f"FAIL gcd_recursive: {gcd_recursive(48,18)}")
        all_pass = False
    if gcd(0, 5) != 5:
        print(f"FAIL gcd(0,5): {gcd(0,5)}")
        all_pass = False

    # --- LCM ---
    if lcm(12, 18) != 36:
        print(f"FAIL lcm(12,18): {lcm(12,18)}")
        all_pass = False
    if lcm(0, 5) != 0:
        print("FAIL lcm(0,5)")
        all_pass = False

    # --- Extended GCD ---
    g, x, y = extended_gcd(48, 18)
    if g != 6 or 48 * x + 18 * y != 6:
        print(f"FAIL extended_gcd: g={g}, 48*{x}+18*{y}={48*x+18*y}")
        all_pass = False

    # --- Modular Inverse ---
    inv = mod_inverse(3, 7)  # 3*5 = 15 ≡ 1 mod 7
    if inv != 5:
        print(f"FAIL mod_inverse(3,7): {inv}")
        all_pass = False

    inv2 = mod_inverse(2, 4)
    if inv2 is not None:
        print("FAIL mod_inverse(2,4): should be None")
        all_pass = False

    # --- Linear Diophantine ---
    sol = solve_linear_diophantine(3, 5, 1)  # 3*(-2) + 5*(1) = -1 wait
    # 3*2 + 5*(-1) = 1 ✓
    if sol is None:
        print("FAIL diophantine: no solution")
        all_pass = False
    else:
        x0, y0, dx, dy = sol
        if 3 * x0 + 5 * y0 != 1:
            print(f"FAIL diophantine check: 3*{x0}+5*{y0}={3*x0+5*y0}")
            all_pass = False

    # No solution case
    if solve_linear_diophantine(2, 4, 1) is not None:
        print("FAIL diophantine: should have no solution")
        all_pass = False

    # --- Chinese Remainder ---
    crt = chinese_remainder([2, 3, 1], [3, 5, 7])
    if crt is None:
        print("FAIL CRT: no solution")
        all_pass = False
    else:
        x, M = crt
        if M != 105 or x % 3 != 2 or x % 5 != 3 or x % 7 != 1:
            print(f"FAIL CRT: x={x}, M={M}")
            all_pass = False

    # Non-coprime moduli
    crt2 = chinese_remainder([0, 1], [2, 4])
    if crt2 is not None:
        print("FAIL CRT: should detect non-coprime")
        all_pass = False

    if all_pass:
        print("All GCD/LCM tests PASSED")
    sys.exit(0 if all_pass else 1)
