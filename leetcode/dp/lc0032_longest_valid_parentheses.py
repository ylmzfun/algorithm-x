"""
LeetCode 32: Longest Valid Parentheses

Given a string containing just the characters '(' and ')', return the
length of the longest valid (well-formed) parentheses substring.

Constraints:
- 0 <= s.length <= 3 * 10^4
- s[i] is '(', or ')'.
"""


class Solution:
    # ── Approach 1: Dynamic Programming O(n) time, O(n) space ──────────────
    def longestValidParentheses_dp(self, s: str) -> int:
        """dp[i] = length of longest valid substring ending at i."""
        n = len(s)
        if n < 2:
            return 0

        dp = [0] * n
        max_len = 0

        for i in range(1, n):
            if s[i] == ')':
                if s[i - 1] == '(':
                    # "...()" case
                    dp[i] = (dp[i - 2] if i >= 2 else 0) + 2
                elif i - dp[i - 1] - 1 >= 0 and s[i - dp[i - 1] - 1] == '(':
                    # "...))" case: check char before the previous valid segment
                    dp[i] = dp[i - 1] + 2
                    if i - dp[i - 1] - 2 >= 0:
                        dp[i] += dp[i - dp[i - 1] - 2]
                max_len = max(max_len, dp[i])

        return max_len

    # ── Approach 2: Stack O(n) time, O(n) space ────────────────────────────
    def longestValidParentheses_stack(self, s: str) -> int:
        """Use stack to track indices of unmatched parentheses."""
        stack = [-1]  # sentinel for the base
        max_len = 0

        for i, ch in enumerate(s):
            if ch == '(':
                stack.append(i)
            else:
                stack.pop()
                if not stack:
                    stack.append(i)  # new base
                else:
                    max_len = max(max_len, i - stack[-1])

        return max_len

    # ── Approach 3: Two-Pass O(n) time, O(1) space ─────────────────────────
    def longestValidParentheses(self, s: str) -> int:
        """Left-to-right then right-to-left scan."""
        left = right = max_len = 0

        # Left → Right
        for ch in s:
            if ch == '(':
                left += 1
            else:
                right += 1
            if left == right:
                max_len = max(max_len, 2 * right)
            elif right > left:
                left = right = 0

        # Right → Left
        left = right = 0
        for ch in reversed(s):
            if ch == ')':
                right += 1
            else:
                left += 1
            if left == right:
                max_len = max(max_len, 2 * left)
            elif left > right:
                left = right = 0

        return max_len


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ("(()", 2),
        (")()())", 4),
        ("", 0),
        ("()(()", 2),
        ("(()())", 6),
        ("()()()", 6),
        ("((()))", 6),
        ("())", 2),
    ]

    for s, expected in tests:
        r1 = sol.longestValidParentheses_dp(s)
        r2 = sol.longestValidParentheses_stack(s)
        r3 = sol.longestValidParentheses(s)
        ok = r1 == r2 == r3 == expected
        print(f"{s!r} → DP={r1}, Stack={r2}, TwoPass={r3} | {'✓' if ok else '✗'}")
