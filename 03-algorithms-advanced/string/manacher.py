"""
Manacher's algorithm for palindromic substrings.

Contains:
- longest_palindromic_substring: Find the longest palindromic substring.
- count_palindromic_substrings: Count all palindromic substrings.
"""

from typing import Tuple


def _manacher_radii(s: str) -> list:
    """
    Compute palindrome radii using Manacher's algorithm.

    Transforms the string by inserting '#' between characters and at ends,
    then computes the radius of the longest palindrome centered at each
    position in the transformed string.

    Args:
        s: Input string.

    Returns:
        List of radii for the transformed string.

    Time:  O(n)
    Space: O(n)
    """
    # Transform: "abc" → "^#a#b#c#$"
    t = ["^"]
    for ch in s:
        t.append("#")
        t.append(ch)
    t.append("#")
    t.append("$")

    n = len(t)
    p = [0] * n  # p[i] = radius of palindrome centered at i in t
    center = 0
    right = 0

    for i in range(1, n - 1):
        mirror = 2 * center - i
        if i < right:
            p[i] = min(right - i, p[mirror])

        # Expand around i
        while t[i + p[i] + 1] == t[i - p[i] - 1]:
            p[i] += 1

        # Update center and right
        if i + p[i] > right:
            center = i
            right = i + p[i]

    return p


def _transformed_to_original(index: int, radii: list) -> Tuple[int, int]:
    """
    Map a center in the transformed string back to the original.
    Assumes transform pattern "^#a#b#c#$".

    Args:
        index: Center index in transformed string.
        radii: Radius array from Manacher.

    Returns:
        (start, length) in the original string.
    """
    # Remove the leading '^#' → index 0 = '^', index 1 = '#'
    # For original char at i, its position in t is 2*i + 2.
    # The palindrome length in original is p[index].
    start = (index - radii[index] - 1) // 2
    length = radii[index]
    return start, length


def longest_palindromic_substring(s: str) -> str:
    """
    Find the longest palindromic substring using Manacher's algorithm.

    Args:
        s: Input string.

    Returns:
        The longest palindromic substring. If multiple exist, returns the
        first one encountered. Returns empty string if input is empty.

    Time:  O(n)
    Space: O(n)

    Example:
        longest_palindromic_substring("babad") → "bab" (or "aba")
    """
    if not s:
        return ""

    p = _manacher_radii(s)
    max_len = 0
    center_idx = 0

    for i in range(len(p)):
        if p[i] > max_len:
            max_len = p[i]
            center_idx = i

    start, length = _transformed_to_original(center_idx, p)
    return s[start : start + length]


def count_palindromic_substrings(s: str) -> int:
    """
    Count the total number of palindromic substrings using Manacher's algorithm.

    Each radius r at a transformed center i corresponds to (r + 1) // 2
    palindromic substrings centered at i (in the original string).

    Args:
        s: Input string.

    Returns:
        Total count of palindromic substrings.

    Time:  O(n)
    Space: O(n)

    Example:
        count_palindromic_substrings("aaa") → 6  (a, a, a, aa, aa, aaa)
    """
    if not s:
        return 0

    p = _manacher_radii(s)
    total = 0
    for radius in p:
        total += (radius + 1) // 2
    return total


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    import sys

    all_pass = True

    # --- Longest palindromic substring ---
    lps = longest_palindromic_substring("babad")
    if lps not in ("bab", "aba"):
        print(f"FAIL longest 'babad': {lps}")
        all_pass = False

    lps2 = longest_palindromic_substring("cbbd")
    if lps2 != "bb":
        print(f"FAIL longest 'cbbd': {lps2}")
        all_pass = False

    lps3 = longest_palindromic_substring("a")
    if lps3 != "a":
        print(f"FAIL longest 'a': {lps3}")
        all_pass = False

    lps4 = longest_palindromic_substring("")
    if lps4 != "":
        print(f"FAIL longest empty: '{lps4}'")
        all_pass = False

    lps5 = longest_palindromic_substring("racecar")
    if lps5 != "racecar":
        print(f"FAIL longest 'racecar': {lps5}")
        all_pass = False

    # --- Count palindromic substrings ---
    c1 = count_palindromic_substrings("abc")
    if c1 != 3:
        print(f"FAIL count 'abc': expected 3, got {c1}")
        all_pass = False

    c2 = count_palindromic_substrings("aaa")
    if c2 != 6:
        print(f"FAIL count 'aaa': expected 6, got {c2}")
        all_pass = False

    c3 = count_palindromic_substrings("")
    if c3 != 0:
        print(f"FAIL count empty: {c3}")
        all_pass = False

    c4 = count_palindromic_substrings("a")
    if c4 != 1:
        print(f"FAIL count 'a': {c4}")
        all_pass = False

    if all_pass:
        print("All Manacher tests PASSED")
    sys.exit(0 if all_pass else 1)
