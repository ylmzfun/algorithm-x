#pragma once

#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace graph {

// 哈密顿路径 — Held-Karp DP O(n² · 2ⁿ)，n ≤ 20。
// adj: 邻接矩阵（true = 有边）。返回顶点序列或空。
inline std::vector<std::size_t> hamiltonian_path(
    const std::vector<std::vector<bool>>& adj) {
    std::size_t n = adj.size();
    if (n == 0) return {};
    if (n == 1) return {0};

    std::size_t total = std::size_t{1} << n;
    // dp[mask][i] = whether path ending at i covering mask exists
    std::vector<std::vector<bool>> dp(total, std::vector<bool>(n, false));
    std::vector<std::vector<std::size_t>> prev(total,
        std::vector<std::size_t>(n, static_cast<std::size_t>(-1)));

    for (std::size_t i = 0; i < n; ++i) {
        dp[std::size_t{1} << i][i] = true;
    }

    for (std::size_t mask = 0; mask < total; ++mask) {
        for (std::size_t i = 0; i < n; ++i) {
            if (!dp[mask][i]) continue;
            for (std::size_t j = 0; j < n; ++j) {
                if (mask & (std::size_t{1} << j)) continue;
                if (!adj[i][j]) continue;
                std::size_t new_mask = mask | (std::size_t{1} << j);
                dp[new_mask][j] = true;
                prev[new_mask][j] = i;
            }
        }
    }

    // Find any full mask
    std::size_t full = total - 1;
    for (std::size_t i = 0; i < n; ++i) {
        if (dp[full][i]) {
            std::vector<std::size_t> path;
            std::size_t cur = i, mask = full;
            while (cur != static_cast<std::size_t>(-1)) {
                path.push_back(cur);
                std::size_t p = prev[mask][cur];
                if (p == static_cast<std::size_t>(-1)) break;
                mask ^= (std::size_t{1} << cur);
                cur = p;
            }
            std::reverse(path.begin(), path.end());
            return path;
        }
    }
    return {};
}

}  // namespace graph
}  // namespace algorithm_x
