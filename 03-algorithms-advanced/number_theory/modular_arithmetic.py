"""
Modular arithmetic algorithms.

Contains:
- Modular exponentiation (fast power)
- nCr modulo p (factorial precomputation)
- nCr modulo p for large n (Lucas theorem)
"""

from typing import List


# ======================================================================
# Modular exponentiation (binary exponentiation)
# ======================================================================

def mod_pow(base: int, exp: int, mod: int) -> int:
    """
    Compute (base^exp) % mod using binary exponentiation.

    Args:
        base: The base.
        exp: The exponent (non-negative).
        mod: The modulus (positive).

    Returns:
        base^exp modulo mod.

    Time:  O(log exp)
    Space: O(1)

    Example:
        mod_pow(2, 10, 1000) → 24  (2^10 = 1024, 1024 % 1000 = 24)
    """
    if mod == 1:
        return 0

    result = 1 % mod
    base %= mod

    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1

    return result


# ======================================================================
# nCr mod p (factorial precomputation)
# ======================================================================

class NCRMod:
    """
    Precompute factorials and inverse factorials modulo a prime p
    to answer nCr queries in O(1) time (after O(n) precomputation).
    """

    def __init__(self, max_n: int, mod: int) -> None:
        """
        Precompute factorials up to max_n modulo mod.

        Args:
            max_n: Maximum n for nCr queries.
            mod: A prime modulus.

        Time: O(max_n)
        """
        self.mod = mod
        self.max_n = max_n

        self.fact = [1] * (max_n + 1)
        self.inv_fact = [1] * (max_n + 1)

        for i in range(1, max_n + 1):
            self.fact[i] = (self.fact[i - 1] * i) % mod

        # Fermat's little theorem: inv_fact[max_n] = fact[max_n]^(mod-2) mod mod
        self.inv_fact[max_n] = mod_pow(self.fact[max_n], mod - 2, mod)

        for i in range(max_n, 0, -1):
            self.inv_fact[i - 1] = (self.inv_fact[i] * i) % mod

    def ncr(self, n: int, r: int) -> int:
        """
        Compute C(n, r) modulo p.

        Args:
            n: Total items.
            r: Items to choose.

        Returns:
            C(n, r) % mod.  0 if r < 0 or r > n.

        Time: O(1) after precomputation.
        """
        if r < 0 or r > n:
            return 0
        return (
            self.fact[n] * self.inv_fact[r] % self.mod * self.inv_fact[n - r]
        ) % self.mod


def ncr_mod(n: int, r: int, mod: int) -> int:
    """
    Compute C(n, r) % mod for small n (no precomputation needed).

    Uses the multiplicative formula: C(n, r) = ∏_{i=1}^{r} (n - r + i) / i

    Args:
        n: Total items.
        r: Items to choose.
        mod: Prime modulus.

    Returns:
        C(n, r) % mod.

    Time: O(r) or O(min(r, n-r)) — whichever is smaller
    Space: O(1)
    """
    if r < 0 or r > n:
        return 0
    if r > n - r:
        r = n - r

    numerator = 1
    denominator = 1

    for i in range(r):
        numerator = (numerator * (n - i)) % mod
        denominator = (denominator * (i + 1)) % mod

    return (numerator * mod_pow(denominator, mod - 2, mod)) % mod


# ======================================================================
# Lucas Theorem for nCr mod p with large n
# ======================================================================

def ncr_mod_lucas(n: int, r: int, p: int) -> int:
    """
    Compute C(n, r) modulo a prime p using Lucas's theorem.

    C(n, r) ≡ ∏ C(n_i, r_i) (mod p)
    where n_i, r_i are the base-p digits of n and r.

    Works for large n and r (not limited by p) as long as p is prime.

    Args:
        n: Total items (can be very large).
        r: Items to choose.
        p: A prime modulus.

    Returns:
        C(n, r) % p.

    Time:  O(log_p n * min(n_i, p))
    Space: O(1)
    """
    if r < 0 or r > n:
        return 0

    def _ncr_small(ni: int, ri: int) -> int:
        """Compute C(ni, ri) % p using the multiplicative formula (ni < p)."""
        if ri > ni:
            return 0
        if ri > ni - ri:
            ri = ni - ri
        num = 1
        den = 1
        for i in range(ri):
            num = (num * (ni - i)) % p
            den = (den * (i + 1)) % p
        return (num * mod_pow(den, p - 2, p)) % p

    result = 1
    while n > 0 or r > 0:
        ni = n % p
        ri = r % p
        if ri > ni:
            return 0
        result = (result * _ncr_small(ni, ri)) % p
        n //= p
        r //= p

    return result


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    import sys

    all_pass = True

    MOD = 1000000007  # prime

    # --- mod_pow ---
    if mod_pow(2, 10, 1000) != 24:
        print(f"FAIL mod_pow: {mod_pow(2, 10, 1000)}")
        all_pass = False
    if mod_pow(3, 0, 100) != 1:
        print(f"FAIL mod_pow zero exp: {mod_pow(3, 0, 100)}")
        all_pass = False
    if mod_pow(0, 5, 100) != 0:
        print(f"FAIL mod_pow zero base: {mod_pow(0, 5, 100)}")
        all_pass = False

    # --- nCr mod (multiplicative) ---
    c1 = ncr_mod(5, 2, MOD)  # C(5,2) = 10
    if c1 != 10:
        print(f"FAIL ncr_mod(5,2): {c1}")
        all_pass = False

    c2 = ncr_mod(10, 3, MOD)  # 120
    if c2 != 120:
        print(f"FAIL ncr_mod(10,3): {c2}")
        all_pass = False

    # Edge cases
    if ncr_mod(5, 0, MOD) != 1:
        print("FAIL ncr_mod(5,0)")
        all_pass = False
    if ncr_mod(5, 5, MOD) != 1:
        print("FAIL ncr_mod(5,5)")
        all_pass = False
    if ncr_mod(5, 6, MOD) != 0:
        print("FAIL ncr_mod(5,6)")
        all_pass = False

    # --- NCRMod class ---
    ncr_calc = NCRMod(10, MOD)
    if ncr_calc.ncr(5, 2) != 10:
        print(f"FAIL NCRMod.ncr(5,2): {ncr_calc.ncr(5, 2)}")
        all_pass = False
    if ncr_calc.ncr(10, 5) != 252:
        print(f"FAIL NCRMod.ncr(10,5): {ncr_calc.ncr(10, 5)}")
        all_pass = False

    # --- Lucas Theorem ---
    p = 13  # small prime for easy verification
    # C(10, 3) = 120 ≡ 120 % 13 = 3
    if ncr_mod_lucas(10, 3, p) != 120 % 13:
        print(f"FAIL lucas(10,3,13): {ncr_mod_lucas(10, 3, p)}")
        all_pass = False

    # C(14, 5) % 7 = 2002 % 7 = 0
    if ncr_mod_lucas(14, 5, 7) != 0:
        print(f"FAIL lucas(14,5,7): {ncr_mod_lucas(14, 5, 7)}")
        all_pass = False

    # Large n Lucas
    # Should match direct computation
    for n in [5, 10, 20]:
        for r in range(n + 1):
            if ncr_mod_lucas(n, r, MOD) != ncr_mod(n, r, MOD):
                print(f"FAIL lucas vs direct: n={n}, r={r}")
                all_pass = False

    if all_pass:
        print("All modular arithmetic tests PASSED")
    sys.exit(0 if all_pass else 1)
