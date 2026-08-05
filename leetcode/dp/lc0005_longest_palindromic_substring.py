"""
LeetCode 5: Longest Palindromic Substring

Given a string s, return the longest palindromic substring in s.

Constraints:
- 1 <= s.length <= 1000
- s consist of only digits and English letters.
"""

from typing import Tuple


class Solution:
    # ── Approach 1: Dynamic Programming O(n²) time, O(n²) space ──────────────
    def longestPalindrome_dp(self, s: str) -> str:
        """DP: dp[i][j] = True if s[i:j+1] is palindrome."""
        n = len(s)
        if n < 2:
            return s

        dp = [[False] * n for _ in range(n)]
        start, max_len = 0, 1

        # All single characters are palindromes
        for i in range(n):
            dp[i][i] = True

        # Check substrings of length >= 2
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] == s[j]:
                    if length == 2 or dp[i + 1][j - 1]:
                        dp[i][j] = True
                        if length > max_len:
                            start, max_len = i, length

        return s[start:start + max_len]

    # ── Approach 2: Expand Around Center O(n²) time, O(1) space ──────────────
    def longestPalindrome_expand(self, s: str) -> str:
        """Expand around each center (single char or pair)."""
        n = len(s)
        if n < 2:
            return s

        def expand(left: int, right: int) -> Tuple[int, int]:
            while left >= 0 and right < n and s[left] == s[right]:
                left -= 1
                right += 1
            return left + 1, right - 1

        start, max_len = 0, 0
        for i in range(n):
            # Odd length
            l1, r1 = expand(i, i)
            if r1 - l1 + 1 > max_len:
                start, max_len = l1, r1 - l1 + 1
            # Even length
            l2, r2 = expand(i, i + 1)
            if r2 - l2 + 1 > max_len:
                start, max_len = l2, r2 - l2 + 1

        return s[start:start + max_len]

    # ── Approach 3: Manacher's Algorithm O(n) time, O(n) space ───────────────
    def longestPalindrome_manacher(self, s: str) -> str:
        """Manacher's algorithm — linear time."""
        if not s:
            return ""

        # Transform: "abc" -> "^#a#b#c#$"
        T = ['^']
        for ch in s:
            T.append('#')
            T.append(ch)
        T.append('#')
        T.append('$')

        n = len(T)
        P = [0] * n  # radius array
        center = right = 0
        max_len = max_center = 0

        for i in range(1, n - 1):
            mirror = 2 * center - i
            if i < right:
                P[i] = min(right - i, P[mirror])

            # Expand
            while T[i + P[i] + 1] == T[i - P[i] - 1]:
                P[i] += 1

            if i + P[i] > right:
                center, right = i, i + P[i]

            if P[i] > max_len:
                max_len, max_center = P[i], i

        start = (max_center - max_len) // 2
        return s[start:start + max_len]

    # Default
    def longestPalindrome(self, s: str) -> str:
        return self.longestPalindrome_expand(s)


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ("babad", ["bab", "aba"]),
        ("cbbd", ["bb"]),
        ("a", ["a"]),
        ("aaaa", ["aaaa"]),
        ("abcba", ["abcba"]),
    ]

    for s, expected_set in tests:
        r1 = sol.longestPalindrome_dp(s)
        r2 = sol.longestPalindrome_expand(s)
        r3 = sol.longestPalindrome_manacher(s)
        ok = r1 in expected_set and r2 in expected_set and r3 in expected_set
        print(f"Input: {s!r} → DP={r1!r}, Expand={r2!r}, Manacher={r3!r} | {'✓' if ok else '✗'}")
        if not ok:
            print(f"  Expected one of: {expected_set}")
