#pragma once

#include <algorithm>
#include <cstddef>
#include <limits>
#include <vector>

namespace algorithm_x {
namespace graph {

// KM 算法 — O(n³) 最大权二分图完美匹配。
// cost: n×n 矩阵，cost[i][j] 为左部 i 到右部 j 的权重（整数）。
// Returns {matchL, total_cost}, matchL[i] = 匹配的右部编号。
inline std::pair<std::vector<int>, int>
km_algorithm(const std::vector<std::vector<int>>& cost) {
    std::size_t n = cost.size();
    if (n == 0) return {{}, 0};

    const int INF = std::numeric_limits<int>::max();
    std::vector<int> matchL(n, -1), matchR(n, -1);
    std::vector<int> labelL(n, 0), labelR(n, 0);

    // Initialize labels.
    for (std::size_t i = 0; i < n; ++i) {
        labelL[i] = *std::max_element(cost[i].begin(), cost[i].end());
    }

    auto dfs = [&](auto&& self, std::size_t u, std::vector<bool>& visL,
                    std::vector<bool>& visR, std::vector<int>& slack) -> bool {
        visL[u] = true;
        for (std::size_t v = 0; v < n; ++v) {
            if (visR[v]) continue;
            int delta = labelL[u] + labelR[v] -
                        cost[u][v];
            if (delta == 0) {
                visR[v] = true;
                if (matchR[v] == -1 ||
                    self(self, static_cast<std::size_t>(matchR[v]),
                         visL, visR, slack)) {
                    matchL[u] = static_cast<int>(v);
                    matchR[v] = static_cast<int>(u);
                    return true;
                }
            } else if (delta < slack[v]) {
                slack[v] = delta;
            }
        }
        return false;
    };

    for (std::size_t i = 0; i < n; ++i) {
        std::vector<int> slack(n, INF);
        while (true) {
            std::vector<bool> visL(n, false), visR(n, false);
            if (dfs(dfs, i, visL, visR, slack)) break;

            int d = INF;
            for (std::size_t j = 0; j < n; ++j) {
                if (!visR[j]) d = std::min(d, slack[j]);
            }
            for (std::size_t j = 0; j < n; ++j) {
                if (visL[j]) labelL[j] -= d;
                if (visR[j]) labelR[j] += d;
                else slack[j] -= d;
            }
        }
    }

    int total = 0;
    for (std::size_t i = 0; i < n; ++i) {
        total += cost[i][static_cast<std::size_t>(matchL[i])];
    }
    return {matchL, total};
}

}  // namespace graph
}  // namespace algorithm_x
