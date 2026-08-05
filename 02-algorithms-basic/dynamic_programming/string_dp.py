"""
String Dynamic Programming
============================

DP problems on strings: LCS, edit distance, pattern matching, etc.

Functions:
- longest_common_subsequence    : LCS length.
- longest_common_substring      : Longest contiguous common substring.
- edit_distance                 : Levenshtein distance (min insert/delete/replace).
- shortest_common_supersequence : SCS length.
- wildcard_matching             : '?' matches any char, '*' matches any sequence.
- regular_expression_matching   : '.' matches any char, '*' repeats preceding char.
- distinct_subsequences         : Count ways to form target from source.
"""

from typing import List


# ---------------------------------------------------------------------------
# Longest Common Subsequence (LCS)
# ---------------------------------------------------------------------------

def longest_common_subsequence(text1: str, text2: str) -> int:
    """
    Length of the longest common subsequence of two strings.

    dp[i][j] = LCS of text1[0:i] and text2[0:j].

    Parameters
    ----------
    text1, text2 : str

    Returns
    -------
    int
        LCS length.

    Time  : O(m·n)
    Space : O(min(m, n)) — 1D space-optimised.

    Example
    -------
    >>> longest_common_subsequence("abcde", "ace")
    3   # "ace"
    """
    m, n = len(text1), len(text2)
    if m < n:
        text1, text2, m, n = text2, text1, m, n
    prev = [0] * (n + 1)
    for i in range(1, m + 1):
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev = cur
    return prev[n]


# ---------------------------------------------------------------------------
# Longest Common Substring
# ---------------------------------------------------------------------------

def longest_common_substring(s1: str, s2: str) -> int:
    """
    Length of the longest common **contiguous** substring.

    dp[i][j] = length of common suffix of s1[0:i] and s2[0:j].

    Parameters
    ----------
    s1, s2 : str

    Returns
    -------
    int
        Longest common substring length.

    Time  : O(m·n)
    Space : O(min(m, n))

    Example
    -------
    >>> longest_common_substring("abcdef", "zbcdf")
    3   # "bcd"
    """
    m, n = len(s1), len(s2)
    if m < n:
        s1, s2, m, n = s2, s1, m, n
    prev = [0] * (n + 1)
    max_len = 0
    for i in range(1, m + 1):
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                cur[j] = prev[j - 1] + 1
                max_len = max(max_len, cur[j])
        prev = cur
    return max_len


# ---------------------------------------------------------------------------
# Edit Distance (Levenshtein)
# ---------------------------------------------------------------------------

def edit_distance(word1: str, word2: str) -> int:
    """
    Minimum number of operations (insert, delete, replace) to convert
    word1 to word2 (Levenshtein distance).

    dp[i][j] = edit distance for word1[0:i] and word2[0:j].

    Parameters
    ----------
    word1, word2 : str

    Returns
    -------
    int
        Minimum operations.

    Time  : O(m·n)
    Space : O(min(m, n))

    Example
    -------
    >>> edit_distance("horse", "ros")
    3   # horse -> rorse -> rose -> ros
    """
    m, n = len(word1), len(word2)
    if m < n:
        word1, word2, m, n = word2, word1, m, n
    prev = list(range(n + 1))
    for i in range(1, m + 1):
        cur = [i] + [0] * n
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                cur[j] = prev[j - 1]
            else:
                cur[j] = 1 + min(prev[j - 1], prev[j], cur[j - 1])
        prev = cur
    return prev[n]


# ---------------------------------------------------------------------------
# Shortest Common Supersequence
# ---------------------------------------------------------------------------

def shortest_common_supersequence(str1: str, str2: str) -> int:
    """
    Length of the shortest string that has both str1 and str2 as
    subsequences.

    Formula: len(str1) + len(str2) - LCS(str1, str2).

    Parameters
    ----------
    str1, str2 : str

    Returns
    -------
    int
        SCS length.

    Time  : O(m·n)
    Space : O(min(m, n))
    """
    lcs = longest_common_subsequence(str1, str2)
    return len(str1) + len(str2) - lcs


# ---------------------------------------------------------------------------
# Wildcard Matching
# ---------------------------------------------------------------------------

def wildcard_matching(s: str, p: str) -> bool:
    """
    Wildcard pattern matching where '?' matches any single character and
    '*' matches any sequence of characters (including empty).

    Parameters
    ----------
    s : str
        Input string.
    p : str
        Pattern with wildcards.

    Returns
    -------
    bool
        True if s matches p.

    Time  : O(m·n)
    Space : O(n)

    Example
    -------
    >>> wildcard_matching("adceb", "*a*b")
    True
    """
    m, n = len(s), len(p)
    prev = [False] * (n + 1)
    prev[0] = True
    # Handle leading '*' in pattern
    for j in range(1, n + 1):
        if p[j - 1] == '*':
            prev[j] = prev[j - 1]
        else:
            break

    for i in range(1, m + 1):
        cur = [False] * (n + 1)
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                cur[j] = cur[j - 1] or prev[j]
            elif p[j - 1] == '?' or s[i - 1] == p[j - 1]:
                cur[j] = prev[j - 1]
        prev = cur
    return prev[n]


# ---------------------------------------------------------------------------
# Regular Expression Matching
# ---------------------------------------------------------------------------

def regular_expression_matching(s: str, p: str) -> bool:
    """
    Regular expression matching with '.' and '*'.

    '.' matches any single character.
    '*' matches zero or more of the preceding element.

    Parameters
    ----------
    s : str
        Input string.
    p : str
        Pattern.

    Returns
    -------
    bool
        True if the whole string s matches p.

    Time  : O(m·n)
    Space : O(m·n)

    Example
    -------
    >>> regular_expression_matching("aab", "c*a*b")
    True   # c* = zero c, a* = two a, b = b
    """
    m, n = len(s), len(p)
    # dp[i][j] = s[0:i] matches p[0:j]
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    # Patterns like a*, a*b*, a*b*c* can match empty string
    for j in range(2, n + 1, 2):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                # Zero occurrences of preceding char
                dp[i][j] = dp[i][j - 2]
                # One or more: preceding char matches s[i-1]
                if p[j - 2] == '.' or p[j - 2] == s[i - 1]:
                    dp[i][j] = dp[i][j] or dp[i - 1][j]
            elif p[j - 1] == '.' or s[i - 1] == p[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]

    return dp[m][n]


# ---------------------------------------------------------------------------
# Distinct Subsequences
# ---------------------------------------------------------------------------

def distinct_subsequences(s: str, t: str) -> int:
    """
    Number of distinct subsequences of s that equal t.

    dp[i][j] = number of ways to form t[0:j] from s[0:i].

    Parameters
    ----------
    s : str
        Source string.
    t : str
        Target string.

    Returns
    -------
    int
        Number of distinct subsequences.

    Time  : O(m·n)
    Space : O(n)

    Example
    -------
    >>> distinct_subsequences("rabbbit", "rabbit")
    3
    """
    m, n = len(s), len(t)
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(1, m + 1):
        for j in range(n, 0, -1):
            if s[i - 1] == t[j - 1]:
                dp[j] += dp[j - 1]
    return dp[n]


# ===========================================================================
# Tests
# ===========================================================================

if __name__ == "__main__":
    print("=== String DP Tests ===\n")

    # LCS
    assert longest_common_subsequence("abcde", "ace") == 3
    assert longest_common_subsequence("abc", "abc") == 3
    assert longest_common_subsequence("abc", "def") == 0
    print("  PASS longest_common_subsequence")

    # Longest common substring
    assert longest_common_substring("abcdef", "zbcdf") == 3
    assert longest_common_substring("abc", "abc") == 3
    assert longest_common_substring("a", "b") == 0
    print("  PASS longest_common_substring")

    # Edit distance
    assert edit_distance("horse", "ros") == 3
    assert edit_distance("intention", "execution") == 5
    assert edit_distance("", "abc") == 3
    print("  PASS edit_distance")

    # SCS
    assert shortest_common_supersequence("abac", "cab") == 5  # "cabac"
    print("  PASS shortest_common_supersequence")

    # Wildcard matching
    assert wildcard_matching("aa", "a") == False
    assert wildcard_matching("aa", "*") == True
    assert wildcard_matching("cb", "?a") == False
    assert wildcard_matching("adceb", "*a*b") == True
    assert wildcard_matching("", "*") == True
    print("  PASS wildcard_matching")

    # Regex matching
    assert regular_expression_matching("aa", "a") == False
    assert regular_expression_matching("aa", "a*") == True
    assert regular_expression_matching("ab", ".*") == True
    assert regular_expression_matching("aab", "c*a*b") == True
    assert regular_expression_matching("mississippi", "mis*is*p*.") == False
    print("  PASS regular_expression_matching")

    # Distinct subsequences
    assert distinct_subsequences("rabbbit", "rabbit") == 3
    assert distinct_subsequences("babgbag", "bag") == 5
    print("  PASS distinct_subsequences")

    print("\nAll string DP tests completed!")
