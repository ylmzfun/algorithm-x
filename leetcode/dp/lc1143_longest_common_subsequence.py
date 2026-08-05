"""
LeetCode 1143: Longest Common Subsequence

Given two strings text1 and text2, return the length of their longest
common subsequence. If there is no common subsequence, return 0.

A subsequence of a string is a new string generated from the original
string with some characters (can be none) deleted without changing the
relative order of the remaining characters.

Constraints:
- 1 <= text1.length, text2.length <= 1000
- text1 and text2 consist of only lowercase English characters.
"""


class Solution:
    # ── 2D DP O(m·n) time, O(n) space (1D optimized) ──────────────────────
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        """
        dp[i][j] = LCS of text1[:i] and text2[:j].
        If chars match: dp[i][j] = 1 + dp[i-1][j-1]
        Else:           dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        Space optimized to O(n).
        """
        m, n = len(text1), len(text2)
        prev = [0] * (n + 1)  # dp[i-1]
        curr = [0] * (n + 1)  # dp[i]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    curr[j] = prev[j - 1] + 1
                else:
                    curr[j] = max(prev[j], curr[j - 1])
            prev, curr = curr, [0] * (n + 1)

        return prev[n]

    # ── 2D DP (readable) O(m·n) time, O(m·n) space ───────────────────────
    def longestCommonSubsequence_2d(self, text1: str, text2: str) -> int:
        """Full table for debugging / reconstructing the LCS."""
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        # Reconstruct the LCS
        lcs_chars = []
        i, j = m, n
        while i > 0 and j > 0:
            if text1[i - 1] == text2[j - 1]:
                lcs_chars.append(text1[i - 1])
                i -= 1
                j -= 1
            elif dp[i - 1][j] > dp[i][j - 1]:
                i -= 1
            else:
                j -= 1

        return dp[m][n]


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ("abcde", "ace", 3),
        ("abc", "abc", 3),
        ("abc", "def", 0),
        ("bsbininm", "jmjkbkjkv", 1),
        ("oxcpqrsvwf", "shmtulqrypy", 2),
        ("abcba", "abcbcba", 5),
    ]

    for text1, text2, expected in tests:
        r1 = sol.longestCommonSubsequence(text1, text2)
        r2 = sol.longestCommonSubsequence_2d(text1, text2)
        ok = r1 == r2 == expected
        print(f"({text1!r}, {text2!r}) → 1D={r1}, 2D={r2} | {'✓' if ok else '✗'}")
