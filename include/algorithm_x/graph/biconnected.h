#pragma once

#include <algorithm>
#include <cstddef>
#include <stack>
#include <vector>

namespace algorithm_x {
namespace graph {

// Tarjan 算法求双连通分量 (Biconnected Components / Blocks).
// 每个分量是一个点集（不含割点的极大双连通子图）。
inline std::vector<std::vector<std::size_t>>
biconnected_components(const std::vector<std::vector<std::size_t>>& adj) {
    std::size_t n = adj.size();
    std::vector<std::size_t> dfn(n, 0), low(n, 0);
    std::vector<std::pair<std::size_t, std::size_t>> stk;
    std::vector<std::vector<std::size_t>> result;
    std::size_t timer = 0;

    auto dfs = [&](auto&& self, std::size_t u, std::size_t parent) -> void {
        dfn[u] = low[u] = ++timer;
        for (std::size_t v : adj[u]) {
            if (v == parent) continue;
            if (!dfn[v]) {
                stk.emplace_back(u, v);
                self(self, v, u);
                low[u] = std::min(low[u], low[v]);
                if (low[v] >= dfn[u]) {
                    // Found a BCC.
                    std::vector<std::size_t> comp;
                    while (true) {
                        auto [a, b] = stk.back();
                        stk.pop_back();
                        comp.push_back(a);
                        comp.push_back(b);
                        if (a == u && b == v) break;
                    }
                    std::sort(comp.begin(), comp.end());
                    comp.erase(std::unique(comp.begin(), comp.end()), comp.end());
                    result.push_back(std::move(comp));
                }
            } else if (dfn[v] < dfn[u]) {
                low[u] = std::min(low[u], dfn[v]);
                stk.emplace_back(u, v);
            }
        }
    };

    for (std::size_t u = 0; u < n; ++u) {
        if (!dfn[u]) dfs(dfs, u, n);
    }
    return result;
}

}  // namespace graph
}  // namespace algorithm_x
