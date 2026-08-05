#pragma once

#include <algorithm>
#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace graph {

// Kosaraju 强连通分量 — O(V+E)。
// 返回 {comp, comp_cnt}，comp[u] 为 u 所属分量编号。
inline std::pair<std::vector<std::size_t>, std::size_t>
kosaraju_scc(const std::vector<std::vector<std::size_t>>& adj) {
    std::size_t n = adj.size();
    std::vector<bool> visited(n, false);
    std::vector<std::size_t> order;

    // 第一遍 DFS：记录出栈序
    auto dfs1 = [&](auto&& self, std::size_t u) -> void {
        visited[u] = true;
        for (std::size_t v : adj[u]) {
            if (!visited[v]) self(self, v);
        }
        order.push_back(u);
    };

    for (std::size_t u = 0; u < n; ++u) {
        if (!visited[u]) dfs1(dfs1, u);
    }

    // 反转图
    std::vector<std::vector<std::size_t>> rev(n);
    for (std::size_t u = 0; u < n; ++u) {
        for (std::size_t v : adj[u]) {
            rev[v].push_back(u);
        }
    }

    // 第二遍 DFS：在逆图上按出栈逆序染色
    std::fill(visited.begin(), visited.end(), false);
    std::vector<std::size_t> comp(n, n);
    std::size_t comp_cnt = 0;

    auto dfs2 = [&](auto&& self, std::size_t u) -> void {
        visited[u] = true;
        comp[u] = comp_cnt;
        for (std::size_t v : rev[u]) {
            if (!visited[v]) self(self, v);
        }
    };

    for (auto it = order.rbegin(); it != order.rend(); ++it) {
        if (!visited[*it]) {
            dfs2(dfs2, *it);
            ++comp_cnt;
        }
    }

    return {comp, comp_cnt};
}

}  // namespace graph
}  // namespace algorithm_x
