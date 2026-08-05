"""
LeetCode 72: Edit Distance (Levenshtein Distance)

Given two strings word1 and word2, return the minimum number of
operations required to convert word1 to word2.

You have the following three operations permitted on a word:
- Insert a character
- Delete a character
- Replace a character

Constraints:
- 0 <= word1.length, word2.length <= 500
- word1 and word2 consist of lowercase English letters.
"""


class Solution:
    # ── DP O(m·n) time, O(n) space (1D optimized) ──────────────────────────
    def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)

        # Space optimization: use two rows
        prev = list(range(n + 1))  # dp[0][j] = j
        curr = [0] * (n + 1)

        for i in range(1, m + 1):
            curr[0] = i  # dp[i][0] = i
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    curr[j] = prev[j - 1]
                else:
                    curr[j] = 1 + min(
                        prev[j],       # delete
                        curr[j - 1],   # insert
                        prev[j - 1],   # replace
                    )
            prev, curr = curr, prev

        return prev[n]

    # ── 2D DP (readable) O(m·n) time, O(m·n) space ────────────────────────
    def minDistance_2d(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

        return dp[m][n]


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ("horse", "ros", 3),
        ("intention", "execution", 5),
        ("", "abc", 3),
        ("abc", "", 3),
        ("", "", 0),
        ("abc", "abc", 0),
        ("kitten", "sitting", 3),
    ]

    for w1, w2, expected in tests:
        r1 = sol.minDistance(w1, w2)
        r2 = sol.minDistance_2d(w1, w2)
        ok = r1 == r2 == expected
        print(f"({w1!r} → {w2!r}) → 1D={r1}, 2D={r2} | {'✓' if ok else '✗'}")
