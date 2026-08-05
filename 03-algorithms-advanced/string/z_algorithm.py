"""
Z-Algorithm for pattern matching.

The Z-array z[i] for a string S is the length of the longest substring
starting at position i that matches a prefix of S.

Contains:
- z_algorithm: Compute the Z-array.
- z_algorithm_search: Find pattern occurrences using Z-algorithm.
"""

from typing import List


def z_algorithm(s: str) -> List[int]:
    """
    Compute the Z-array for a string using the linear-time Z-algorithm.

    z[i] = length of the longest common prefix between s and s[i:].

    Special case: z[0] is conventionally 0 (or len(s), but we use 0).

    Args:
        s: Input string.

    Returns:
        Z-array of length len(s).

    Time:  O(n), where n = len(s)
    Space: O(n)

    Example:
        s = "aabxaabxsaab"
        z =  [0, 1, 0, 0, 4, 1, 0, 0, 0, 2, 1, 0]
    """
    n = len(s)
    z = [0] * n
    l, r = 0, 0  # [l, r) is the rightmost Z-box

    for i in range(1, n):
        if i < r:
            # We are inside a Z-box, can use previously computed value
            z[i] = min(r - i, z[i - l])

        # Explicit comparison
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1

        # Update Z-box boundaries
        if i + z[i] > r:
            l, r = i, i + z[i]

    return z


def z_algorithm_search(text: str, pattern: str) -> List[int]:
    """
    Find all occurrences of pattern in text using the Z-algorithm.

    Constructs the concatenated string P + "$" + T and looks for positions
    where z[i] == len(P).

    Args:
        text: The text to search in.
        pattern: The pattern to find.

    Returns:
        List of starting indices where pattern occurs in text.

    Time:  O(n + m), where n = len(text), m = len(pattern)
    Space: O(n + m)

    Example:
        z_algorithm_search("ABABDABACDABABCABAB", "ABABCABAB") → [10]
    """
    if not pattern:
        return list(range(len(text) + 1))

    m = len(pattern)
    concat = pattern + "$" + text
    z = z_algorithm(concat)

    result = []
    for i in range(m + 1, len(concat)):
        if z[i] == m:
            result.append(i - m - 1)

    return result


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    import sys

    all_pass = True

    # --- Z-array ---
    # Known example
    s = "aabxaabxsaab"
    z = z_algorithm(s)
    expected_z = [0, 1, 0, 0, 4, 1, 0, 0, 0, 3, 1, 0]
    if z != expected_z:
        print(f"FAIL z_algorithm: expected {expected_z}, got {z}")
        all_pass = False

    z2 = z_algorithm("aaaaa")
    if z2 != [0, 4, 3, 2, 1]:
        print(f"FAIL z_algorithm 'aaaaa': {z2}")
        all_pass = False

    z3 = z_algorithm("ababab")
    if z3 != [0, 0, 4, 0, 2, 0]:
        print(f"FAIL z_algorithm 'ababab': {z3}")
        all_pass = False

    # Single char
    z4 = z_algorithm("a")
    if z4 != [0]:
        print(f"FAIL z_algorithm 'a': {z4}")
        all_pass = False

    # --- Z search ---
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    result = z_algorithm_search(text, pattern)
    if result != [10]:
        print(f"FAIL z_search: expected [10], got {result}")
        all_pass = False

    result2 = z_algorithm_search("AAAAA", "AA")
    if result2 != [0, 1, 2, 3]:
        print(f"FAIL z_search overlapping: {result2}")
        all_pass = False

    result3 = z_algorithm_search("HELLO", "X")
    if result3 != []:
        print(f"FAIL z_search no match: {result3}")
        all_pass = False

    result4 = z_algorithm_search("ABC", "")
    if result4 != [0, 1, 2, 3]:
        print(f"FAIL z_search empty pattern: {result4}")
        all_pass = False

    if all_pass:
        print("All Z-Algorithm tests PASSED")
    sys.exit(0 if all_pass else 1)
