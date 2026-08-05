#pragma once

#include <algorithm>
#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace dp {

// 0-1 背包：每件物品最多选一次。
// 返回最大价值。weights 和 values 长度相同。
inline int knapsack_01(const std::vector<int>& weights,
                        const std::vector<int>& values, int capacity) {
    std::vector<int> dp(static_cast<std::size_t>(capacity) + 1, 0);
    for (std::size_t i = 0; i < weights.size(); ++i) {
        for (int w = capacity; w >= weights[i]; --w) {
            dp[static_cast<std::size_t>(w)] = std::max(
                dp[static_cast<std::size_t>(w)],
                dp[static_cast<std::size_t>(w - weights[i])] + values[i]);
        }
    }
    return dp[static_cast<std::size_t>(capacity)];
}

// 0-1 背包（带回溯）：返回 {最大价值, 选中物品的下标}。
inline std::pair<int, std::vector<std::size_t>>
knapsack_01_with_items(const std::vector<int>& weights,
                        const std::vector<int>& values, int capacity) {
    std::size_t n = weights.size();
    std::size_t cap = static_cast<std::size_t>(capacity);
    std::vector<std::vector<int>> dp(n + 1, std::vector<int>(cap + 1, 0));

    for (std::size_t i = 1; i <= n; ++i) {
        int w = weights[i - 1], v = values[i - 1];
        for (std::size_t j = 0; j <= cap; ++j) {
            dp[i][j] = dp[i - 1][j];
            if (j >= static_cast<std::size_t>(w)) {
                dp[i][j] = std::max(dp[i][j],
                                     dp[i - 1][j - static_cast<std::size_t>(w)] + v);
            }
        }
    }

    // 回溯
    std::vector<std::size_t> items;
    std::size_t j = cap;
    for (std::size_t i = n; i > 0; --i) {
        if (dp[i][j] != dp[i - 1][j]) {
            items.push_back(i - 1);
            j -= static_cast<std::size_t>(weights[i - 1]);
        }
    }
    std::reverse(items.begin(), items.end());
    return {dp[n][cap], items};
}

// 完全背包：每件物品可选无限次。
inline int knapsack_complete(const std::vector<int>& weights,
                              const std::vector<int>& values, int capacity) {
    std::vector<int> dp(static_cast<std::size_t>(capacity) + 1, 0);
    for (std::size_t i = 0; i < weights.size(); ++i) {
        for (int w = weights[i]; w <= capacity; ++w) {
            dp[static_cast<std::size_t>(w)] = std::max(
                dp[static_cast<std::size_t>(w)],
                dp[static_cast<std::size_t>(w - weights[i])] + values[i]);
        }
    }
    return dp[static_cast<std::size_t>(capacity)];
}

// 多重背包（二进制拆分优化）：每件物品有 count 个。
inline int knapsack_multiple(const std::vector<int>& weights,
                              const std::vector<int>& values,
                              const std::vector<int>& counts, int capacity) {
    std::vector<int> dp(static_cast<std::size_t>(capacity) + 1, 0);
    for (std::size_t i = 0; i < weights.size(); ++i) {
        int w = weights[i], v = values[i], c = counts[i];
        // 二进制拆分
        for (int k = 1; k <= c; k <<= 1) {
            int kw = k * w, kv = k * v;
            for (int j = capacity; j >= kw; --j) {
                dp[static_cast<std::size_t>(j)] = std::max(
                    dp[static_cast<std::size_t>(j)],
                    dp[static_cast<std::size_t>(j - kw)] + kv);
            }
            c -= k;
        }
        if (c > 0) {
            int cw = c * w, cv = c * v;
            for (int j = capacity; j >= cw; --j) {
                dp[static_cast<std::size_t>(j)] = std::max(
                    dp[static_cast<std::size_t>(j)],
                    dp[static_cast<std::size_t>(j - cw)] + cv);
            }
        }
    }
    return dp[static_cast<std::size_t>(capacity)];
}

}  // namespace dp
}  // namespace algorithm_x
