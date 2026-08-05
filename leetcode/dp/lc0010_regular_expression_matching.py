"""
LeetCode 10: Regular Expression Matching

Given an input string s and a pattern p, implement regular expression
matching with support for '.' and '*':
- '.' Matches any single character.
- '*' Matches zero or more of the preceding element.
The matching should cover the entire input string (not partial).

Constraints:
- 1 <= s.length <= 20
- 1 <= p.length <= 20
- s contains only lowercase English letters.
- p contains only lowercase English letters, '.', and '*'.
- It is guaranteed for each appearance of the character '*',
  there will be a previous valid character to match.
"""


class Solution:
    # ── DP Bottom-Up O(m·n) time, O(m·n) space ─────────────────────────────
    def isMatch(self, s: str, p: str) -> bool:
        m, n = len(s), len(p)

        # dp[i][j] = does s[:i] match p[:j]?
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[0][0] = True  # empty matches empty

        # Handle patterns like a*, a*b*, a*b*c* matching empty string
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                dp[0][j] = dp[0][j - 2]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if p[j - 1] == '*':
                    # Zero occurrence: skip "x*"
                    dp[i][j] = dp[i][j - 2]
                    # One or more: if char before * matches s[i-1]
                    if p[j - 2] == '.' or p[j - 2] == s[i - 1]:
                        dp[i][j] |= dp[i - 1][j]
                else:
                    # Direct match or '.'
                    if p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                        dp[i][j] = dp[i - 1][j - 1]

        return dp[m][n]


# ── Tests ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    tests = [
        ("aa", "a", False),
        ("aa", "a*", True),
        ("ab", ".*", True),
        ("aab", "c*a*b", True),
        ("mississippi", "mis*is*p*.", False),
        ("", ".*", True),
        ("ab", ".*c", False),
        ("aaa", "a*a", True),
        ("aaa", "ab*a*c*a", True),
    ]

    for s, p, expected in tests:
        result = sol.isMatch(s, p)
        status = "✓" if result == expected else "✗"
        print(f"isMatch({s!r}, {p!r}) = {result} (expected {expected}) {status}")
