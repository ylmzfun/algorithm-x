"""
LeetCode 91: Decode Ways

A message containing letters from A-Z can be encoded into numbers
using the following mapping:
'A' -> "1", 'B' -> "2", ..., 'Z' -> "26"

To decode an encoded message, all the digits must be grouped then
mapped back into letters using the reverse of the mapping above.

Given a string s containing only digits, return the number of ways
to decode it.

Constraints:
- 1 <= s.length <= 100
- s contains only digits and may contain leading zero(s).
"""


class Solution:
    # ── 1D DP O(n) time, O(1) space ───────────────────────────────────────
    def numDecodings(self, s: str) -> int:
        if not s or s[0] == '0':
            return 0

        # dp[i] = ways to decode s[:i]
        # dp[0] = 1 (empty string), dp[1] = 1 if s[0] != '0'
        prev2, prev1 = 1, 1  # dp[i-2], dp[i-1]

        for i in range(1, len(s)):
            curr = 0
            # One-digit decode: s[i] alone
            if s[i] != '0':
                curr += prev1
            # Two-digit decode: s[i-1:i+1]
            two_digit = int(s[i - 1:i + 1])
            if 10 <= two_digit <= 26:
                curr += prev2

            prev2, prev1 = prev1, curr

        return prev1


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ("12", 2),       # "AB" (1 2) or "L" (12)
        ("226", 3),      # "BZ" (2 26), "VF" (22 6), "BBF" (2 2 6)
        ("06", 0),       # invalid leading 0
        ("0", 0),
        ("10", 1),       # "J" (10)
        ("27", 1),       # "BG" (2 7)
        ("11106", 2),    # "AAJF" (1 1 10 6), "KJF" (11 10 6)
        ("123456789", 3),
    ]

    for s, expected in tests:
        result = sol.numDecodings(s)
        status = "✓" if result == expected else "✗"
        print(f"numDecodings({s!r}) = {result} (expected {expected}) {status}")
