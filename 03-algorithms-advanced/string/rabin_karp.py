"""
Rabin-Karp string matching with rolling hash.

Contains:
- rabin_karp_search: Single pattern search.
- rabin_karp_multi_pattern: Multi-pattern search using rolling hash.
- RollingHash: Helper class for computing rolling hash values.
"""

from typing import List, Dict, Set


class RollingHash:
    """
    Rolling hash (polynomial hash) with fixed base and modulus.

    Supports:
      - Computing hash of a string
      - Rolling (sliding-window) hash update: append char, remove leading char
      - Quickly recompute hashes for all substrings of a given length
    """

    def __init__(self, base: int = 256, mod: int = 10**9 + 7) -> None:
        """
        Initialize the rolling hash.

        Args:
            base: Base for the polynomial hash (default 256).
            mod: Modulus (large prime for low collision probability).
        """
        self.base = base
        self.mod = mod

    def hash(self, s: str) -> int:
        """
        Compute the polynomial hash of string s.

        hash(s) = (s[0] * base^(len-1) + s[1] * base^(len-2) + … + s[-1]) % mod

        Args:
            s: Input string.

        Returns:
            Integer hash value.

        Time: O(len(s))
        """
        h = 0
        for ch in s:
            h = (h * self.base + ord(ch)) % self.mod
        return h

    def _precompute_powers(self, length: int) -> List[int]:
        """Precompute base^i % mod for i = 0..length."""
        powers = [1] * (length + 1)
        for i in range(1, length + 1):
            powers[i] = (powers[i - 1] * self.base) % self.mod
        return powers

    def all_hashes(self, text: str, window_len: int) -> List[int]:
        """
        Compute rolling hash for every window of length `window_len` in text.

        Args:
            text: The text string.
            window_len: Length of each window.

        Returns:
            List of hashes; hashes[i] = hash(text[i : i+window_len]).

        Time: O(n), where n = len(text)
        Space: O(n)
        """
        n = len(text)
        if n < window_len:
            return []

        powers = self._precompute_powers(window_len)
        result = [0] * (n - window_len + 1)

        # First window
        h = self.hash(text[:window_len])
        result[0] = h

        for i in range(1, n - window_len + 1):
            # Remove leftmost char, add new rightmost char
            left_char_val = ord(text[i - 1])
            right_char_val = ord(text[i + window_len - 1])
            h = (h * self.base - left_char_val * powers[window_len] + right_char_val) % self.mod
            result[i] = h

        return result


# ======================================================================
# Single pattern Rabin-Karp
# ======================================================================

def rabin_karp_search(
    text: str, pattern: str, base: int = 256, mod: int = 10**9 + 7
) -> List[int]:
    """
    Find all occurrences of pattern in text using the Rabin-Karp algorithm.

    Uses a rolling hash to achieve expected O(n + m) time.  Hash collisions
    are resolved by explicit string comparison.

    Args:
        text: The text to search in.
        pattern: The pattern to find.
        base: Hash base (default 256).
        mod: Hash modulus (default 1e9+7).

    Returns:
        List of starting indices where pattern occurs.

    Time:  Expected O(n + m), worst-case O(n*m) with many collisions
    Space: O(1) (incremental) or O(n) (precomputed all-hashes)
    """
    if not pattern:
        return list(range(len(text) + 1))

    n, m = len(text), len(pattern)
    if n < m:
        return []

    rh = RollingHash(base, mod)
    pattern_hash = rh.hash(pattern)
    powers = rh._precompute_powers(m)
    text_hash = rh.hash(text[:m])

    result: List[int] = []

    for i in range(n - m + 1):
        if text_hash == pattern_hash and text[i : i + m] == pattern:
            result.append(i)
        if i < n - m:
            text_hash = (
                text_hash * base
                - ord(text[i]) * powers[m]
                + ord(text[i + m])
            ) % mod

    return result


# ======================================================================
# Multi-pattern Rabin-Karp
# ======================================================================

def rabin_karp_multi_pattern(
    text: str, patterns: List[str], base: int = 256, mod: int = 10**9 + 7
) -> Dict[str, List[int]]:
    """
    Search for multiple patterns simultaneously using Rabin-Karp.

    Precomputes hashes for all patterns, then slides a single window
    over the text, checking against each pattern of matching length.

    Args:
        text: The text to search in.
        patterns: List of pattern strings.
        base: Hash base.
        mod: Hash modulus.

    Returns:
        Dictionary mapping each pattern to its list of starting indices.

    Time:  O(n * max_pattern_len + total_pattern_len) expected
    Space: O(total_pattern_len + result)
    """
    result: Dict[str, List[int]] = {p: [] for p in patterns}

    if not patterns:
        return result

    # Group patterns by length
    by_length: Dict[int, List[tuple]] = {}
    for p in patterns:
        m = len(p)
        if m == 0:
            result[p] = list(range(len(text) + 1))
            continue
        by_length.setdefault(m, []).append(p)

    if not by_length:
        return result

    rh = RollingHash(base, mod)
    n = len(text)

    # For each pattern length, precompute text hashes and check
    for m, pats in by_length.items():
        if n < m:
            continue
        # Precompute hashes of all patterns of this length
        pat_hashes = {rh.hash(p): p for p in pats}
        # Compute all text window hashes
        powers = rh._precompute_powers(m)
        h = rh.hash(text[:m])
        for i in range(n - m + 1):
            if h in pat_hashes:
                p = pat_hashes[h]
                if text[i : i + m] == p:
                    result[p].append(i)
            if i < n - m:
                h = (h * base - ord(text[i]) * powers[m] + ord(text[i + m])) % mod

    return result


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    import sys

    all_pass = True

    # --- RollingHash ---
    rh = RollingHash()
    h1 = rh.hash("hello")
    h2 = rh.hash("hello")
    if h1 != h2:
        print("FAIL hash consistency")
        all_pass = False

    # --- Single-pattern ---
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    result = rabin_karp_search(text, pattern)
    if result != [10]:
        print(f"FAIL rabin_karp: expected [10], got {result}")
        all_pass = False

    # Multiple matches
    result2 = rabin_karp_search("AAAAA", "AA")
    if result2 != [0, 1, 2, 3]:
        print(f"FAIL rabin_karp overlapping: {result2}")
        all_pass = False

    # Pattern not in text
    result3 = rabin_karp_search("HELLO", "Z")
    if result3 != []:
        print(f"FAIL rabin_karp no match: {result3}")
        all_pass = False

    # Empty pattern
    result4 = rabin_karp_search("ABC", "")
    if result4 != [0, 1, 2, 3]:
        print(f"FAIL rabin_karp empty pattern: {result4}")
        all_pass = False

    # Pattern longer than text
    result5 = rabin_karp_search("AB", "ABC")
    if result5 != []:
        print(f"FAIL rabin_karp longer pattern: {result5}")
        all_pass = False

    # --- Multi-pattern ---
    mp = rabin_karp_multi_pattern(
        "abababcab", ["aba", "bab", "abc", "zz"]
    )
    if mp["aba"] != [0, 2] or mp["bab"] != [1, 3] or mp["abc"] != [4] or mp["zz"] != []:
        print(f"FAIL multi-pattern: {mp}")
        all_pass = False

    # Empty patterns handling
    mp2 = rabin_karp_multi_pattern("abc", ["", "a"])
    if len(mp2[""]) != 4:
        print(f"FAIL multi-pattern empty: {mp2}")
        all_pass = False

    if all_pass:
        print("All Rabin-Karp tests PASSED")
    sys.exit(0 if all_pass else 1)
