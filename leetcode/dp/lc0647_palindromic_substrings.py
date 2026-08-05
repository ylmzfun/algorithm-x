"""
LeetCode 647: Palindromic Substrings

Given a string s, return the number of palindromic substrings in it.
A string is a palindrome when it reads the same backward as forward.
A substring is a contiguous sequence of characters within the string.

Constraints:
- 1 <= s.length <= 1000
- s consists of lowercase English letters.
"""


class Solution:
    # ── Expand Around Center O(n²) time, O(1) space ───────────────────────
    def countSubstrings(self, s: str) -> int:
        """For each center (odd and even), expand and count."""
        n = len(s)
        count = 0

        def expand(left: int, right: int) -> int:
            cnt = 0
            while left >= 0 and right < n and s[left] == s[right]:
                cnt += 1
                left -= 1
                right += 1
            return cnt

        for i in range(n):
            count += expand(i, i)      # odd length
            count += expand(i, i + 1)  # even length

        return count

    # ── DP O(n²) time, O(n²) space ────────────────────────────────────────
    def countSubstrings_dp(self, s: str) -> int:
        """dp[i][j] = True if s[i:j+1] is a palindrome."""
        n = len(s)
        dp = [[False] * n for _ in range(n)]
        count = 0

        for length in range(1, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] == s[j]:
                    if length <= 2 or dp[i + 1][j - 1]:
                        dp[i][j] = True
                        count += 1

        return count

    # ── Manacher O(n) time, O(n) space ────────────────────────────────────
    def countSubstrings_manacher(self, s: str) -> int:
        """Use Manacher's radius array: each radius contributes palindromes."""
        T = ['^']
        for ch in s:
            T.append('#')
            T.append(ch)
        T.append('#')
        T.append('$')

        n = len(T)
        P = [0] * n
        center = right = 0

        for i in range(1, n - 1):
            mirror = 2 * center - i
            if i < right:
                P[i] = min(right - i, P[mirror])

            while T[i + P[i] + 1] == T[i - P[i] - 1]:
                P[i] += 1

            if i + P[i] > right:
                center, right = i, i + P[i]

        # Each radius r contributes r palindromes (rounded to integer count)
        # In the transformed string, each palindrome center at '#'
        # contributes floor((radius+1)/2), at letters contributes floor(radius/2)+1
        count = 0
        for r in P:
            count += (r + 1) // 2
        return count


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ("abc", 3),
        ("aaa", 6),
        ("a", 1),
        ("abca", 4),
    ]

    for s, expected in tests:
        r1 = sol.countSubstrings(s)
        r2 = sol.countSubstrings_dp(s)
        r3 = sol.countSubstrings_manacher(s)
        ok = r1 == r2 == r3 == expected
        print(f"{s!r} → Expand={r1}, DP={r2}, Manacher={r3} | {'✓' if ok else '✗'}")
