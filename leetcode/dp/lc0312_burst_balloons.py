"""
LeetCode 312: Burst Balloons

You are given n balloons, indexed from 0 to n - 1. Each balloon is
painted with a number on it represented by an array nums. You are
asked to burst all the balloons.

If you burst the i-th balloon, you will get nums[i-1] * nums[i] *
nums[i+1] coins. If i - 1 or i + 1 goes out of bounds of the array,
then treat it as if there is a balloon with a 1 painted on it.

Return the maximum coins you can collect by bursting the balloons
wisely.

Constraints:
- n == nums.length
- 1 <= n <= 300
- 0 <= nums[i] <= 100
"""

from typing import List


class Solution:
    # ── Interval DP (Reverse Thinking) O(n³) time, O(n²) space ────────────
    def maxCoins(self, nums: List[int]) -> int:
        """
        Reverse thinking: instead of choosing which balloon to burst first,
        consider which balloon is the LAST one to burst in each interval.
        Add sentinel 1's at both ends.
        dp[left][right] = max coins from bursting all balloons in (left, right).
        """
        # Pad with 1 at both ends
        balloons = [1] + nums + [1]
        n = len(balloons)

        # dp[i][j] = max coins in open interval (i, j)
        dp = [[0] * n for _ in range(n)]

        # Interval length from 2 (smallest with one balloon) to n-1
        for length in range(2, n):
            for left in range(0, n - length):
                right = left + length
                # k is the LAST balloon to burst in (left, right)
                for k in range(left + 1, right):
                    coins = (balloons[left] * balloons[k] * balloons[right]
                             + dp[left][k] + dp[k][right])
                    dp[left][right] = max(dp[left][right], coins)

        return dp[0][n - 1]


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([3, 1, 5, 8], 167),
        ([1, 5], 10),
        ([1], 1),
        ([9, 76, 64, 21], 116718),
        ([1, 2, 3, 4, 5], 110),
    ]

    for nums, expected in tests:
        result = sol.maxCoins(nums)
        status = "✓" if result == expected else "✗"
        print(f"{nums} → {result} (expected {expected}) {status}")
