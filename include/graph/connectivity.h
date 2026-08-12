#pragma once

#include <algorithm>
#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace graph {

// ---- Tarjan SCC, O(V+E) ----

// Returns {component_id, component_count}.
// Component IDs are in reverse topological order (lower id = later in topo).
inline std::pair<std::vector<std::size_t>, std::size_t>
tarjan_scc(const std::vector<std::vector<std::size_t>>& adj) {
    std::size_t n = adj.size();
    std::vector<std::size_t> comp(n, n);
    std::vector<std::size_t> dfn(n, 0), low(n, 0);
    std::vector<std::size_t> stk;
    std::vector<bool> in_stack(n, false);
    std::size_t timer = 0, comp_cnt = 0;

    auto dfs = [&](auto&& self, std::size_t u) -> void {
        dfn[u] = low[u] = ++timer;
        stk.push_back(u);
        in_stack[u] = true;
        for (std::size_t v : adj[u]) {
            if (!dfn[v]) {
                self(self, v);
                low[u] = std::min(low[u], low[v]);
            } else if (in_stack[v]) {
                low[u] = std::min(low[u], dfn[v]);
            }
        }
        if (dfn[u] == low[u]) {
            std::size_t v;
            do {
                v = stk.back();
                stk.pop_back();
                in_stack[v] = false;
                comp[v] = comp_cnt;
            } while (v != u);
            ++comp_cnt;
        }
    };

    for (std::size_t u = 0; u < n; ++u) {
        if (!dfn[u]) dfs(dfs, u);
    }
    return {comp, comp_cnt};
}

// ---- Articulation Points (Cut Vertices) ----

inline std::vector<std::size_t> articulation_points(
    const std::vector<std::vector<std::size_t>>& adj) {
    std::size_t n = adj.size();
    std::vector<std::size_t> dfn(n, 0), low(n, 0);
    std::vector<bool> is_cut(n, false);
    std::size_t timer = 0;

    auto dfs = [&](auto&& self, std::size_t u, std::size_t parent) -> void {
        dfn[u] = low[u] = ++timer;
        std::size_t children = 0;
        for (std::size_t v : adj[u]) {
            if (!dfn[v]) {
                ++children;
                self(self, v, u);
                low[u] = std::min(low[u], low[v]);
                if (parent != n && low[v] >= dfn[u]) is_cut[u] = true;
            } else if (v != parent) {
                low[u] = std::min(low[u], dfn[v]);
            }
        }
        if (parent == n && children > 1) is_cut[u] = true;
    };

    for (std::size_t u = 0; u < n; ++u) {
        if (!dfn[u]) dfs(dfs, u, n);
    }

    std::vector<std::size_t> result;
    for (std::size_t u = 0; u < n; ++u) {
        if (is_cut[u]) result.push_back(u);
    }
    return result;
}

// ---- Bridges ----

inline std::vector<std::pair<std::size_t, std::size_t>> bridges(
    const std::vector<std::vector<std::size_t>>& adj) {
    std::size_t n = adj.size();
    std::vector<std::size_t> dfn(n, 0), low(n, 0);
    std::vector<std::pair<std::size_t, std::size_t>> result;
    std::size_t timer = 0;

    auto dfs = [&](auto&& self, std::size_t u, std::size_t parent) -> void {
        dfn[u] = low[u] = ++timer;
        for (std::size_t v : adj[u]) {
            if (!dfn[v]) {
                self(self, v, u);
                low[u] = std::min(low[u], low[v]);
                if (low[v] > dfn[u]) result.emplace_back(u, v);
            } else if (v != parent) {
                low[u] = std::min(low[u], dfn[v]);
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
