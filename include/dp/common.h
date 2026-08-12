#pragma once

#include <algorithm>
#include <climits>
#include <cstddef>
#include <string>
#include <vector>

namespace algorithm_x {
namespace dp {

// 矩阵链乘法：返回最小乘法次数。
// dims[i] 为矩阵 i 的行数，dims[i+1] 为列数。n 个矩阵需要 n+1 维。
inline int matrix_chain_order(const std::vector<int>& dims) {
    std::size_t n = dims.size() - 1;
    if (n == 0) return 0;

    // dp[i][j] = 从矩阵 i 乘到 j 的最小代价
    std::vector<std::vector<int>> dp(n, std::vector<int>(n, 0));
    for (std::size_t len = 2; len <= n; ++len) {
        for (std::size_t i = 0; i + len - 1 < n; ++i) {
            std::size_t j = i + len - 1;
            dp[i][j] = INT_MAX;
            for (std::size_t k = i; k < j; ++k) {
                int cost = dp[i][k] + dp[k + 1][j] +
                           dims[i] * dims[k + 1] * dims[j + 1];
                dp[i][j] = std::min(dp[i][j], cost);
            }
        }
    }
    return dp[0][n - 1];
}

// 硬币找零（最少硬币数）— DP 版本，支持任意硬币系统。
// 返回所需最少硬币数，无解返回 -1。
inline int coin_change_dp(const std::vector<int>& coins, int amount) {
    const int INF = amount + 1;
    std::vector<int> dp(static_cast<std::size_t>(amount) + 1, INF);
    dp[0] = 0;
    for (int a = 1; a <= amount; ++a) {
        for (int c : coins) {
            if (a >= c) {
                dp[static_cast<std::size_t>(a)] = std::min(
                    dp[static_cast<std::size_t>(a)],
                    dp[static_cast<std::size_t>(a - c)] + 1);
            }
        }
    }
    return dp[static_cast<std::size_t>(amount)] > amount
               ? -1
               : dp[static_cast<std::size_t>(amount)];
}

// 戳气球（Burst Balloons）— 区间 DP 经典题。
// nums[i] 戳破得分 = nums[left] * nums[i] * nums[right]。
inline int burst_balloons(std::vector<int> nums) {
    // 在首尾加上 1
    nums.insert(nums.begin(), 1);
    nums.push_back(1);
    std::size_t n = nums.size();
    std::vector<std::vector<int>> dp(n, std::vector<int>(n, 0));

    for (std::size_t len = 2; len < n; ++len) {
        for (std::size_t l = 0; l + len < n; ++l) {
            std::size_t r = l + len;
            for (std::size_t k = l + 1; k < r; ++k) {
                dp[l][r] = std::max(dp[l][r],
                    nums[l] * nums[k] * nums[r] + dp[l][k] + dp[k][r]);
            }
        }
    }
    return dp[0][n - 1];
}

}  // namespace dp
}  // namespace algorithm_x
