"""
Prime number algorithms.

Contains:
- Sieve of Eratosthenes
- Segmented sieve
- Miller-Rabin primality test
- Prime factorization (trial division + Pollard's Rho)
"""

import math
import random
from typing import List, Tuple


# ======================================================================
# Sieve of Eratosthenes
# ======================================================================

def sieve_of_eratosthenes(n: int) -> List[int]:
    """
    Return all prime numbers up to n using the Sieve of Eratosthenes.

    Args:
        n: Upper bound (inclusive).

    Returns:
        List of primes ≤ n.

    Time:  O(n log log n)
    Space: O(n)
    """
    if n < 2:
        return []

    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            step = i
            start = i * i
            for j in range(start, n + 1, step):
                is_prime[j] = False

    return [i for i in range(2, n + 1) if is_prime[i]]


# ======================================================================
# Segmented Sieve
# ======================================================================

def segmented_sieve(lo: int, hi: int) -> List[int]:
    """
    Return all primes in the range [lo, hi].

    Uses a base sieve up to sqrt(hi) and a segment sieve.

    Args:
        lo: Lower bound (inclusive).
        hi: Upper bound (inclusive).

    Returns:
        List of primes in [lo, hi].

    Time:  O((hi - lo) log log hi + sqrt(hi) log log sqrt(hi))
    Space: O(hi - lo + sqrt(hi))
    """
    if hi < 2:
        return []
    if lo < 2:
        lo = 2

    limit = int(hi ** 0.5) + 1
    base_primes = sieve_of_eratosthenes(limit)

    segment_size = hi - lo + 1
    is_prime_seg = [True] * segment_size

    for p in base_primes:
        # Find first multiple of p in [lo, hi]
        start = max(p * p, ((lo + p - 1) // p) * p)
        for j in range(start, hi + 1, p):
            is_prime_seg[j - lo] = False

    return [lo + i for i in range(segment_size) if is_prime_seg[i]]


# ======================================================================
# Miller-Rabin primality test
# ======================================================================

def miller_rabin(n: int, k: int = 10) -> bool:
    """
    Miller-Rabin probabilistic primality test.

    Args:
        n: The integer to test.
        k: Number of rounds (higher = more accurate). Default 10.

    Returns:
        True if n is probably prime, False if composite.

    Time:  O(k * log^3 n)
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # Write n - 1 = d * 2^s
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    def _check_composite(a: int) -> bool:
        """Returns True if n is definitely composite using witness a."""
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return False
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return False
        return True

    # Deterministic witnesses for n < 2^64
    if n < 2 ** 64:
        witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    else:
        witnesses = [random.randrange(2, n - 1) for _ in range(k)]

    for a in witnesses:
        if a % n == 0:
            continue
        if _check_composite(a):
            return False

    return True


# ======================================================================
# Trial division factorization
# ======================================================================

def trial_division_factorization(n: int) -> List[int]:
    """
    Factorize n using trial division up to sqrt(n).

    Args:
        n: Positive integer.

    Returns:
        List of prime factors (not necessarily sorted).

    Time:  O(sqrt(n))
    """
    if n <= 1:
        return []

    factors = []
    temp = n

    # Factor out 2
    while temp % 2 == 0:
        factors.append(2)
        temp //= 2

    # Factor out odd numbers
    d = 3
    while d * d <= temp:
        while temp % d == 0:
            factors.append(d)
            temp //= d
        d += 2

    if temp > 1:
        factors.append(temp)

    return factors


# ======================================================================
# Pollard's Rho factorization
# ======================================================================

def _pollards_rho_factor(n: int) -> int:
    """
    Find a non-trivial factor of n using Pollard's Rho algorithm.

    Args:
        n: Composite integer.

    Returns:
        A non-trivial factor of n.

    Time: Expected O(sqrt(p)) where p is the smallest prime factor.
    """
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3

    while True:
        c = random.randrange(1, n)
        f = lambda x: (pow(x, 2, n) + c) % n
        x = random.randrange(2, n)
        y = x
        d = 1

        while d == 1:
            x = f(x)
            y = f(f(y))
            d = math.gcd(abs(x - y), n)

        if d != n:
            return d


def pollards_rho(n: int) -> List[int]:
    """
    Prime factorization of n using Pollard's Rho combined with Miller-Rabin.

    Args:
        n: Positive integer.

    Returns:
        List of prime factors (not necessarily sorted).

    Time: Expected O(n^(1/4) * log n)
    """
    factors: List[int] = []

    def _factorize(x: int) -> None:
        if x <= 1:
            return
        if miller_rabin(x):
            factors.append(x)
            return
        d = _pollards_rho_factor(x)
        _factorize(d)
        _factorize(x // d)

    _factorize(n)
    return factors


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    import sys

    all_pass = True

    # --- Sieve of Eratosthenes ---
    primes_30 = sieve_of_eratosthenes(30)
    if primes_30 != [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        print(f"FAIL sieve 30: {primes_30}")
        all_pass = False

    if sieve_of_eratosthenes(1) != []:
        print("FAIL sieve 1")
        all_pass = False

    # --- Segmented Sieve ---
    seg = segmented_sieve(10, 30)
    if seg != [11, 13, 17, 19, 23, 29]:
        print(f"FAIL segmented 10-30: {seg}")
        all_pass = False

    seg2 = segmented_sieve(0, 10)
    if seg2 != [2, 3, 5, 7]:
        print(f"FAIL segmented 0-10: {seg2}")
        all_pass = False

    # --- Miller-Rabin ---
    primes_small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in primes_small:
        if not miller_rabin(p):
            print(f"FAIL miller_rabin prime {p}")
            all_pass = False

    composites_small = [4, 6, 8, 9, 10, 12, 14, 15, 21, 25]
    for c in composites_small:
        if miller_rabin(c):
            print(f"FAIL miller_rabin composite {c}")
            all_pass = False

    # Large known primes
    if not miller_rabin(10**9 + 7):
        print("FAIL miller_rabin 1e9+7")
        all_pass = False
    if not miller_rabin(10**9 + 9):
        print("FAIL miller_rabin 1e9+9")
        all_pass = False

    # --- Trial division ---
    factors = trial_division_factorization(84)  # 2*2*3*7
    if sorted(factors) != [2, 2, 3, 7]:
        print(f"FAIL trial_div 84: {sorted(factors)}")
        all_pass = False

    if trial_division_factorization(1) != []:
        print("FAIL trial_div 1")
        all_pass = False

    if trial_division_factorization(13) != [13]:
        print(f"FAIL trial_div 13: {trial_division_factorization(13)}")
        all_pass = False

    # --- Pollard's Rho ---
    factors_rho = pollards_rho(84)
    if sorted(factors_rho) != [2, 2, 3, 7]:
        print(f"FAIL pollard_rho 84: {sorted(factors_rho)}")
        all_pass = False

    factors_rho2 = pollards_rho(10403)  # 101 * 103
    if sorted(factors_rho2) != [101, 103]:
        print(f"FAIL pollard_rho 10403: {sorted(factors_rho2)}")
        all_pass = False

    if all_pass:
        print("All primes tests PASSED")
    sys.exit(0 if all_pass else 1)
