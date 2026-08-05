"""
Knuth-Morris-Pratt (KMP) string matching algorithm.

Contains:
- build_lps: Build the Longest-Prefix-Suffix (LPS / π) array.
- kmp_search: Find all occurrences of a pattern in text.
- kmp_count_occurrences: Count occurrences of pattern in text.
"""

from typing import List


def build_lps(pattern: str) -> List[int]:
    """
    Build the Longest-Prefix-Suffix (LPS) array for a pattern.

    lps[i] = length of the longest proper prefix of pattern[0..i]
             that is also a suffix of pattern[0..i].

    Args:
        pattern: The pattern string.

    Returns:
        LPS array of the same length as pattern.

    Time:  O(m), where m = len(pattern)
    Space: O(m)

    Example:
        pattern = "ABABCABAB"
        lps =     [0,0,1,2,0,1,2,3,4]
    """
    m = len(pattern)
    lps = [0] * m
    length = 0  # length of previous longest prefix-suffix
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(text: str, pattern: str) -> List[int]:
    """
    Find all starting indices of pattern in text using the KMP algorithm.

    Args:
        text: The text to search in.
        pattern: The pattern to search for.

    Returns:
        List of starting indices (0-based) where pattern occurs in text.

    Time:  O(n + m), where n = len(text), m = len(pattern)
    Space: O(m)

    Example:
        kmp_search("ABABDABACDABABCABAB", "ABABCABAB") → [10]
    """
    if not pattern:
        return list(range(len(text) + 1))  # empty pattern matches everywhere

    n, m = len(text), len(pattern)
    lps = build_lps(pattern)
    result: List[int] = []

    i = 0  # index for text
    j = 0  # index for pattern

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1

        if j == m:
            result.append(i - j)
            j = lps[j - 1]
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return result


def kmp_count_occurrences(text: str, pattern: str) -> int:
    """
    Count the number of (possibly overlapping) occurrences of pattern in text.

    Args:
        text: The text to search in.
        pattern: The pattern to search for.

    Returns:
        Number of occurrences.

    Time:  O(n + m)
    Space: O(m)
    """
    return len(kmp_search(text, pattern))


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    import sys

    all_pass = True

    # --- LPS ---
    lps = build_lps("ABABCABAB")
    expected_lps = [0, 0, 1, 2, 0, 1, 2, 3, 4]
    if lps != expected_lps:
        print(f"FAIL build_lps: expected {expected_lps}, got {lps}")
        all_pass = False

    # AAA pattern
    lps2 = build_lps("AAAA")
    if lps2 != [0, 1, 2, 3]:
        print(f"FAIL build_lps 'AAAA': {lps2}")
        all_pass = False

    # --- KMP Search ---
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    result = kmp_search(text, pattern)
    if result != [10]:
        print(f"FAIL kmp_search: expected [10], got {result}")
        all_pass = False

    # Multiple occurrences
    result2 = kmp_search("AAAAA", "AA")
    if result2 != [0, 1, 2, 3]:
        print(f"FAIL kmp_search overlapping: {result2}")
        all_pass = False

    # No match
    result3 = kmp_search("HELLO", "X")
    if result3 != []:
        print(f"FAIL kmp_search no match: {result3}")
        all_pass = False

    # Pattern longer than text
    result4 = kmp_search("AB", "ABC")
    if result4 != []:
        print(f"FAIL kmp_search longer pattern: {result4}")
        all_pass = False

    # Empty pattern
    result5 = kmp_search("ABC", "")
    if result5 != [0, 1, 2, 3]:
        print(f"FAIL kmp_search empty pattern: {result5}")
        all_pass = False

    # --- Count occurrences ---
    count = kmp_count_occurrences("AAAAA", "AA")
    if count != 4:
        print(f"FAIL kmp_count: expected 4, got {count}")
        all_pass = False

    if all_pass:
        print("All KMP tests PASSED")
    sys.exit(0 if all_pass else 1)
