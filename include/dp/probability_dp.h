#pragma once

#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace dp {

// 掷硬币概率 — DP[i][j] = i 次投掷恰好 j 次正面的概率（公平硬币 p=0.5）。
inline double coin_toss_probability(int n, int k) {
    if (k < 0 || k > n) return 0.0;
    std::vector<double> dp(static_cast<std::size_t>(k) + 1, 0.0);
    dp[0] = 1.0;
    for (int i = 1; i <= n; ++i) {
        for (int j = std::min(i, k); j >= 1; --j) {
            dp[static_cast<std::size_t>(j)] =
                0.5 * dp[static_cast<std::size_t>(j)] +
                0.5 * dp[static_cast<std::size_t>(j - 1)];
        }
        dp[0] *= 0.5;
    }
    return dp[static_cast<std::size_t>(k)];
}

// 随机游走 — 从 0 出发，n 步后到达位置 pos 的概率。
inline double random_walk_probability(int n, int pos) {
    return coin_toss_probability(n, (n + pos) / 2);
}

}  // namespace dp
}  // namespace algorithm_x
