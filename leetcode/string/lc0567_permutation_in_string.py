"""
567. Permutation in String
https://leetcode.com/problems/permutation-in-string/

Given two strings s1 and s2, return true if s2 contains a permutation of s1,
or false otherwise. In other words, return true if one of s1's permutations
is a substring of s2.
"""

from __future__ import annotations
from collections import Counter


# ──────────────────────────────────────────────────────────────────────────────
# Approach 1: Sliding Window with Frequency Arrays
# Maintain a fixed-size window of length len(s1). Compare frequency arrays.
# Time: O(N) where N = len(s2)
# Space: O(1) — two arrays of size 26.
# ──────────────────────────────────────────────────────────────────────────────
def check_inclusion_array(s1: str, s2: str) -> bool:
    """Sliding window with frequency arrays (size 26)."""
    if len(s1) > len(s2):
        return False

    target = [0] * 26
    window = [0] * 26

    for ch in s1:
        target[ord(ch) - ord("a")] += 1

    for i, ch in enumerate(s2):
        window[ord(ch) - ord("a")] += 1
        if i >= len(s1):
            window[ord(s2[i - len(s1)]) - ord("a")] -= 1
        if window == target:
            return True

    return False


# ──────────────────────────────────────────────────────────────────────────────
# Approach 2: Sliding Window with Counter
# Time: O(N × 26) ≈ O(N) — Counter comparison is O(26).
# Space: O(1)
# ──────────────────────────────────────────────────────────────────────────────
def check_inclusion_counter(s1: str, s2: str) -> bool:
    """Sliding window with Python Counter."""
    if len(s1) > len(s2):
        return False

    target = Counter(s1)
    window = Counter(s2[:len(s1)])

    if window == target:
        return True

    for i in range(len(s1), len(s2)):
        window[s2[i]] += 1
        window[s2[i - len(s1)]] -= 1
        if window[s2[i - len(s1)]] == 0:
            del window[s2[i - len(s1)]]
        if window == target:
            return True

    return False


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, s1: str, s2: str, expected: bool):
        methods = [
            ("Array", check_inclusion_array),
            ("Counter", check_inclusion_counter),
        ]
        for name, fn in methods:
            result = fn(s1, s2)
            ok = result == expected
            print(f"[{label}] {name}: {'✓' if ok else '✗'} (got {result}, expected {expected})")

    test("Example 1", "ab", "eidbaooo", True)
    test("Example 2", "ab", "eidboaoo", False)
    test("Same length exact match", "abc", "cba", True)
    test("s1 longer", "ab", "a", False)
    print("\nAll permutation in string tests completed.")
