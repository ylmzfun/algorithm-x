#pragma once

#include <algorithm>
#include <cstddef>
#include <limits>
#include <vector>

namespace algorithm_x {
namespace dp {

// 最优二叉搜索树 (Optimal BST) — Knuth 优化 O(n²)。
// freq[i]: 键 i 的访问频率 (0-indexed)。
inline int optimal_bst(const std::vector<int>& freq) {
    std::size_t n = freq.size();
    if (n == 0) return 0;

    // 前缀和
    std::vector<int> sum(n + 1, 0);
    for (std::size_t i = 0; i < n; ++i) sum[i + 1] = sum[i] + freq[i];

    // dp[i][j] = min cost for keys [i, j]
    std::vector<std::vector<int>> dp(n, std::vector<int>(n, 0));
    // opt[i][j] = optimal root for [i, j] (for Knuth optimization)
    std::vector<std::vector<int>> opt(n, std::vector<int>(n, 0));

    for (std::size_t i = 0; i < n; ++i) {
        dp[i][i] = freq[i];
        opt[i][i] = static_cast<int>(i);
    }

    for (std::size_t len = 2; len <= n; ++len) {
        for (std::size_t i = 0; i + len - 1 < n; ++i) {
            std::size_t j = i + len - 1;
            dp[i][j] = std::numeric_limits<int>::max();
            int cost = sum[j + 1] - sum[i];

            std::size_t l = static_cast<std::size_t>(opt[i][j - 1]);
            std::size_t r = static_cast<std::size_t>(opt[i + 1][j]);
            for (std::size_t k = l; k <= r && k <= j; ++k) {
                int val = cost;
                if (k > i) val += dp[i][k - 1];
                if (k < j) val += dp[k + 1][j];
                if (val < dp[i][j]) {
                    dp[i][j] = val;
                    opt[i][j] = static_cast<int>(k);
                }
            }
        }
    }
    return dp[0][n - 1];
}

}  // namespace dp
}  // namespace algorithm_x
