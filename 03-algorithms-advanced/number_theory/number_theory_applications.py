"""
Number theory applications.

Contains:
- Count primes in range (π function estimate + segmented sieve)
- Find all factors of a number
- Euler's totient function φ(n)
- Möbius function μ(n)
- Linear sieve (compute primes + smallest prime factor simultaneously)
"""

import math
from typing import List


# ======================================================================
# Count primes in range
# ======================================================================

def count_primes_in_range(lo: int, hi: int) -> int:
    """
    Count the number of primes in [lo, hi] using a segmented sieve.

    Args:
        lo: Lower bound (inclusive).
        hi: Upper bound (inclusive).

    Returns:
        Number of primes in the range.

    Time:  O((hi - lo) log log hi + sqrt(hi) log log sqrt(hi))
    Space: O(hi - lo + sqrt(hi))
    """
    if hi < 2:
        return 0
    if lo < 2:
        lo = 2

    limit = int(hi ** 0.5) + 1

    # Base sieve up to sqrt(hi)
    is_prime_small = [True] * (limit + 1)
    is_prime_small[0] = is_prime_small[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if is_prime_small[i]:
            for j in range(i * i, limit + 1, i):
                is_prime_small[j] = False

    base_primes = [i for i in range(2, limit + 1) if is_prime_small[i]]

    # Segment
    segment_size = hi - lo + 1
    is_prime_seg = [True] * segment_size

    for p in base_primes:
        start = max(p * p, ((lo + p - 1) // p) * p)
        for j in range(start, hi + 1, p):
            is_prime_seg[j - lo] = False

    return sum(is_prime_seg)


# ======================================================================
# Find all factors
# ======================================================================

def all_factors(n: int) -> List[int]:
    """
    Return all positive divisors (factors) of n in ascending order.

    Args:
        n: Positive integer.

    Returns:
        Sorted list of factors.

    Time:  O(sqrt(n))
    Space: O(number of factors)

    Example:
        all_factors(12) → [1, 2, 3, 4, 6, 12]
    """
    if n <= 0:
        return []

    small = []
    large = []

    for d in range(1, int(math.isqrt(n)) + 1):
        if n % d == 0:
            small.append(d)
            if d != n // d:
                large.append(n // d)

    return small + large[::-1]


# ======================================================================
# Euler's totient function
# ======================================================================

def euler_totient(n: int) -> int:
    """
    Compute Euler's totient function φ(n).

    φ(n) = number of integers 1 ≤ k ≤ n such that gcd(k, n) = 1.

    Using the product formula: φ(n) = n * ∏_{p|n} (1 - 1/p)

    Args:
        n: Positive integer.

    Returns:
        φ(n)

    Time:  O(sqrt(n))
    Space: O(1)

    Example:
        euler_totient(12) → 4  (1, 5, 7, 11)
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1

    result = n
    temp = n

    # Trial division for prime factors
    if temp % 2 == 0:
        result -= result // 2
        while temp % 2 == 0:
            temp //= 2

    d = 3
    while d * d <= temp:
        if temp % d == 0:
            result -= result // d
            while temp % d == 0:
                temp //= d
        d += 2

    if temp > 1:
        result -= result // temp

    return result


def euler_totient_sieve(n: int) -> List[int]:
    """
    Compute φ(i) for all i from 1 to n using a sieve-like approach.

    Args:
        n: Upper bound (inclusive).

    Returns:
        List phi where phi[i] = φ(i) for 1 ≤ i ≤ n (phi[0] = 0).

    Time:  O(n log log n)
    Space: O(n)
    """
    phi = list(range(n + 1))
    for i in range(2, n + 1):
        if phi[i] == i:  # i is prime
            for j in range(i, n + 1, i):
                phi[j] -= phi[j] // i
    return phi


# ======================================================================
# Möbius function
# ======================================================================

def mobius_function(n: int) -> int:
    """
    Compute the Möbius function μ(n).

    μ(n) =  1 if n = 1
    μ(n) =  0 if n has a squared prime factor
    μ(n) = (-1)^k if n is the product of k distinct primes

    Args:
        n: Positive integer.

    Returns:
        μ(n): one of -1, 0, or 1.

    Time:  O(sqrt(n))
    Space: O(1)

    Example:
        mobius_function(6) → 1   (2*3, k=2 → (-1)^2 = 1)
        mobius_function(4) → 0   (has squared factor 2^2)
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1

    p = 0
    temp = n

    # Check factor 2
    if temp % 2 == 0:
        p += 1
        temp //= 2
        if temp % 2 == 0:  # squared factor
            return 0

    d = 3
    while d * d <= temp:
        if temp % d == 0:
            p += 1
            temp //= d
            if temp % d == 0:
                return 0
        d += 2

    if temp > 1:
        p += 1

    return -1 if p % 2 == 1 else 1


def mobius_sieve(n: int) -> List[int]:
    """
    Compute μ(i) for all i from 1 to n using a sieve.

    Args:
        n: Upper bound.

    Returns:
        List mu where mu[i] = μ(i) for 1 ≤ i ≤ n (mu[0] = 0).

    Time:  O(n log log n)
    Space: O(n)
    """
    mu = [0] * (n + 1)
    mu[1] = 1

    is_composite = [False] * (n + 1)
    primes: List[int] = []

    for i in range(2, n + 1):
        if not is_composite[i]:
            primes.append(i)
            mu[i] = -1

        for p in primes:
            if i * p > n:
                break
            is_composite[i * p] = True
            if i % p == 0:
                mu[i * p] = 0  # squared factor
                break
            else:
                mu[i * p] = -mu[i]

    return mu


# ======================================================================
# Linear sieve (compute primes + smallest prime factor simultaneously)
# ======================================================================

def linear_sieve(n: int) -> tuple:
    """
    Linear sieve: compute primes, smallest prime factor (spf), and
    optionally Euler's totient and Möbius values for all numbers up to n.

    Args:
        n: Upper bound.

    Returns:
        (primes, spf) where primes is the list of primes ≤ n and
        spf[i] is the smallest prime factor of i (spf[0] = spf[1] = 0).

    Time:  O(n)
    Space: O(n)
    """
    spf = [0] * (n + 1)
    primes: List[int] = []

    for i in range(2, n + 1):
        if spf[i] == 0:
            spf[i] = i
            primes.append(i)

        for p in primes:
            if p > spf[i] or i * p > n:
                break
            spf[i * p] = p

    return primes, spf


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    import sys

    all_pass = True

    # --- Count primes in range ---
    cnt = count_primes_in_range(1, 30)
    if cnt != 10:  # 2,3,5,7,11,13,17,19,23,29
        print(f"FAIL count_primes 1-30: {cnt}")
        all_pass = False

    cnt2 = count_primes_in_range(90, 100)
    if cnt2 != 1:  # only 97
        print(f"FAIL count_primes 90-100: {cnt2}")
        all_pass = False

    # --- All factors ---
    factors_12 = all_factors(12)
    if factors_12 != [1, 2, 3, 4, 6, 12]:
        print(f"FAIL factors 12: {factors_12}")
        all_pass = False

    factors_1 = all_factors(1)
    if factors_1 != [1]:
        print(f"FAIL factors 1: {factors_1}")
        all_pass = False

    factors_16 = all_factors(16)
    if factors_16 != [1, 2, 4, 8, 16]:
        print(f"FAIL factors 16: {factors_16}")
        all_pass = False

    # --- Euler's totient ---
    if euler_totient(1) != 1:
        print(f"FAIL phi(1): {euler_totient(1)}")
        all_pass = False
    if euler_totient(12) != 4:
        print(f"FAIL phi(12): {euler_totient(12)}")
        all_pass = False
    if euler_totient(13) != 12:  # prime
        print(f"FAIL phi(13): {euler_totient(13)}")
        all_pass = False

    # Sieve totient
    phi_sieve = euler_totient_sieve(12)
    for i in range(1, 13):
        if phi_sieve[i] != euler_totient(i):
            print(f"FAIL phi_sieve[{i}]: {phi_sieve[i]} vs {euler_totient(i)}")
            all_pass = False

    # --- Möbius ---
    if mobius_function(1) != 1:
        print(f"FAIL mu(1): {mobius_function(1)}")
        all_pass = False
    if mobius_function(2) != -1:  # prime
        print(f"FAIL mu(2): {mobius_function(2)}")
        all_pass = False
    if mobius_function(4) != 0:  # square
        print(f"FAIL mu(4): {mobius_function(4)}")
        all_pass = False
    if mobius_function(6) != 1:  # 2*3
        print(f"FAIL mu(6): {mobius_function(6)}")
        all_pass = False

    # Möbius sieve
    mu_sieve = mobius_sieve(20)
    for i in range(1, 21):
        if mu_sieve[i] != mobius_function(i):
            print(f"FAIL mu_sieve[{i}]: {mu_sieve[i]} vs {mobius_function(i)}")
            all_pass = False

    # --- Linear sieve ---
    primes, spf = linear_sieve(20)
    if primes != [2, 3, 5, 7, 11, 13, 17, 19]:
        print(f"FAIL linear_sieve primes: {primes}")
        all_pass = False
    if spf[12] != 2 or spf[9] != 3 or spf[7] != 7:
        print(f"FAIL linear_sieve spf: spf[12]={spf[12]}, spf[9]={spf[9]}, spf[7]={spf[7]}")
        all_pass = False

    if all_pass:
        print("All number theory applications tests PASSED")
    sys.exit(0 if all_pass else 1)
