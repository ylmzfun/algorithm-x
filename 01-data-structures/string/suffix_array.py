"""
Suffix Array Implementation
=============================

A suffix array is a sorted array of all suffixes of a string. It enables
efficient substring search and other string processing operations.

Two construction methods:
    1. Naive: O(n² log n) — Generate all suffixes, sort them.
    2. Prefix doubling: O(n log² n) — Sort suffixes by first 2^k characters.

LCP (Longest Common Prefix) array: LCP[i] = length of the longest common
prefix between suffix SA[i] and suffix SA[i-1]. Built using Kasai's algorithm.

Applications:
    - Substring search (binary search on suffix array)
    - Longest repeated substring
    - Longest common substring of two strings

Space Complexity: O(n) for n = length of string.
"""

from typing import List, Optional, Tuple


class SuffixArray:
    """Suffix array with LCP array for a given string.

    Examples:
        >>> sa = SuffixArray("banana")
        >>> sa.suffix_array
        [5, 3, 1, 0, 4, 2]
        >>> sa.lcp_array
        [0, 1, 3, 0, 0, 2]
        >>> sa.search("ana")
        True
        >>> sa.search("xyz")
        False
    """

    def __init__(self, s: str, method: str = "doubling") -> None:
        """Build suffix array and LCP array for string `s`.

        Args:
            s: Input string.
            method: Construction method — "naive" or "doubling" (default).

        Raises:
            ValueError: If method is not recognized.
        """
        self._s = s
        self._n = len(s)

        if method == "naive":
            self._sa = self._build_naive()
        elif method == "doubling":
            self._sa = self._build_doubling()
        else:
            raise ValueError(f"Unknown method: {method}. Use 'naive' or 'doubling'.")

        self._lcp = self._build_lcp()

    @property
    def suffix_array(self) -> List[int]:
        """Return the suffix array (list of starting indices)."""
        return self._sa

    @property
    def lcp_array(self) -> List[int]:
        """Return the LCP array."""
        return self._lcp

    # ── Naive Construction ───────────────────────────────────────────────────

    def _build_naive(self) -> List[int]:
        """Build suffix array naively: generate all suffixes and sort.

        Time Complexity: O(n² log n) — sorting n strings of average length n/2.
        """
        suffixes = [(self._s[i:], i) for i in range(self._n)]
        suffixes.sort(key=lambda x: x[0])
        return [idx for _, idx in suffixes]

    # ── Prefix Doubling Construction ─────────────────────────────────────────

    def _build_doubling(self) -> List[int]:
        """Build suffix array using prefix doubling.

        Sorts suffixes by first k characters, then doubles k each iteration.

        Time Complexity: O(n log² n) — log n iterations × O(n log n) sort.
        Space Complexity: O(n)
        """
        n = self._n
        s = self._s

        # Initialize: sort by first character
        sa = list(range(n))
        rank = [ord(c) for c in s]
        tmp = [0] * n
        k = 1

        while k < n:
            # Sort by (rank[i], rank[i+k])
            sa.sort(key=lambda i: (rank[i], rank[i + k] if i + k < n else -1))

            # Re-rank
            tmp[sa[0]] = 0
            for i in range(1, n):
                prev = sa[i - 1]
                curr = sa[i]
                prev_rank = (rank[prev], rank[prev + k] if prev + k < n else -1)
                curr_rank = (rank[curr], rank[curr + k] if curr + k < n else -1)
                tmp[curr] = tmp[prev] + (1 if curr_rank != prev_rank else 0)

            rank, tmp = tmp, rank
            if rank[sa[-1]] == n - 1:
                break  # All suffixes have distinct ranks
            k <<= 1

        return sa

    # ── LCP Array (Kasai's algorithm) ───────────────────────────────────────

    def _build_lcp(self) -> List[int]:
        """Build LCP array using Kasai's algorithm.

        LCP[i] = longest common prefix length between suffixes at
        SA[i] and SA[i-1].

        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        n = self._n
        s = self._s
        sa = self._sa

        # Inverse: rank[i] = position of suffix i in SA
        rank = [0] * n
        for i, suffix in enumerate(sa):
            rank[suffix] = i

        lcp = [0] * n
        h = 0

        for i in range(n):
            if rank[i] > 0:
                j = sa[rank[i] - 1]
                # Count common prefix between suffix i and suffix j
                while (i + h < n and j + h < n and
                       s[i + h] == s[j + h]):
                    h += 1
                lcp[rank[i]] = h
                if h > 0:
                    h -= 1

        return lcp

    # ── Search ───────────────────────────────────────────────────────────────

    def search(self, pattern: str) -> bool:
        """Check if `pattern` occurs as a substring.

        Uses binary search on the suffix array.

        Args:
            pattern: String to search for.

        Returns:
            True if pattern exists in the original string.

        Time Complexity: O(m log n) where m = len(pattern).
        """
        if not pattern:
            return True

        n = self._n
        m = len(pattern)
        sa = self._sa
        s = self._s

        # Binary search for lower bound
        lo, hi = 0, n

        while lo < hi:
            mid = (lo + hi) // 2
            suffix = s[sa[mid]:sa[mid] + m]
            if suffix < pattern:
                lo = mid + 1
            else:
                hi = mid

        if lo >= n:
            return False

        # Check if the suffix at `lo` starts with pattern
        start = sa[lo]
        return (start + m <= n and s[start:start + m] == pattern)

    def find_all(self, pattern: str) -> List[int]:
        """Find all occurrences of `pattern` in the string.

        Returns the starting indices of all matches.

        Args:
            pattern: String to search for.

        Returns:
            List of starting indices (may be empty).

        Time Complexity: O(m log n + k) where k = number of matches.
        """
        if not pattern:
            return list(range(self._n + 1))

        n = self._n
        m = len(pattern)
        sa = self._sa
        s = self._s

        # Binary search for range
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            suffix = s[sa[mid]:sa[mid] + m]
            if suffix < pattern:
                lo = mid + 1
            else:
                hi = mid

        left = lo
        hi = n
        while lo < hi:
            mid = (lo + hi) // 2
            suffix = s[sa[mid]:sa[mid] + m]
            if suffix[:m] <= pattern:
                lo = mid + 1
            else:
                hi = mid

        right = lo

        result = [sa[i] for i in range(left, right)]
        return result

    def longest_repeated_substring(self) -> str:
        """Return the longest repeated substring using LCP array.

        Returns:
            The longest substring that appears more than once.

        Time Complexity: O(n)
        """
        if self._n == 0:
            return ""

        # Find max LCP and its position
        max_lcp = max(self._lcp)
        if max_lcp == 0:
            return ""

        max_idx = self._lcp.index(max_lcp)
        start = self._sa[max_idx]
        return self._s[start:start + max_lcp]

    def __len__(self) -> int:
        return self._n

    def __repr__(self) -> str:
        return f"SuffixArray(n={self._n})"


# ─── Tests ────────────────────────────────────────────────────────────────────


def _run_tests() -> None:
    """Run all tests and report results."""
    import sys

    passed = 0
    failed = 0

    def check(description: str, condition: bool) -> None:
        nonlocal passed, failed
        if condition:
            passed += 1
            print(f"  ✓ {description}")
        else:
            failed += 1
            print(f"  ✗ {description}", file=sys.stderr)

    test_string = "banana"

    # ── Naive ─────────────────────────────────────────────────────────────────
    print("Naive Construction:")
    sa_naive = SuffixArray(test_string, method="naive")
    check("naive SA correct", sa_naive.suffix_array == [5, 3, 1, 0, 4, 2])
    check("naive LCP correct", sa_naive.lcp_array == [0, 1, 3, 0, 0, 2])

    # ── Prefix Doubling ──────────────────────────────────────────────────────
    print("\nDoubling Construction:")
    sa_double = SuffixArray(test_string, method="doubling")
    check("doubling SA correct", sa_double.suffix_array == [5, 3, 1, 0, 4, 2])
    check("doubling LCP correct", sa_double.lcp_array == [0, 1, 3, 0, 0, 2])

    # ── Search ────────────────────────────────────────────────────────────────
    print("\nSearch:")
    check("search 'ana'", sa_double.search("ana"))
    check("search 'ban'", sa_double.search("ban"))
    check("search 'na'", sa_double.search("na"))
    check("search 'nana'", sa_double.search("nana"))
    check("not search 'xyz'", not sa_double.search("xyz"))
    check("not search 'bananas'", not sa_double.search("bananas"))
    check("empty pattern", sa_double.search(""))

    # ── Find All ─────────────────────────────────────────────────────────────
    print("\nFind All:")
    check("find_all 'ana' indices", sorted(sa_double.find_all("ana")) == [1, 3])
    check("find_all 'a' indices", sorted(sa_double.find_all("a")) == [1, 3, 5])
    check("find_all 'xyz' empty", sa_double.find_all("xyz") == [])

    # ── Longest Repeated Substring ───────────────────────────────────────────
    print("\nLongest Repeated Substring:")
    check("LRS 'banana' == 'ana'", sa_double.longest_repeated_substring() == "ana")

    sa2 = SuffixArray("mississippi", method="doubling")
    check("LRS 'mississippi' == 'issi'", sa2.longest_repeated_substring() == "issi")

    sa_empty = SuffixArray("", method="doubling")
    check("LRS empty string == ''", sa_empty.longest_repeated_substring() == "")

    # ── Single char ──────────────────────────────────────────────────────────
    print("\nSingle character:")
    sa_single = SuffixArray("a", method="doubling")
    check("SA single char", sa_single.suffix_array == [0])
    check("LCP single char", sa_single.lcp_array == [0])

    # ── Summary ───────────────────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
