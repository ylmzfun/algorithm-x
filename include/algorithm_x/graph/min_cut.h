#pragma once

#include <cstddef>
#include <limits>
#include <queue>
#include <utility>
#include <vector>

namespace algorithm_x {
namespace graph {

// Min-Cut via Dinic. Returns {max_flow_value, S_side_vertices}.
// S_side[u] = true if vertex u is reachable from src in residual graph.
inline std::pair<int, std::vector<bool>>
min_cut(std::vector<std::vector<int>>& capacity, std::size_t src, std::size_t sink) {
    std::size_t n = capacity.size();
    if (n == 0) return {0, {}};

    // Build adjacency with reverse edges
    struct Edge {
        std::size_t to, rev;
        int cap;
    };
    std::vector<std::vector<Edge>> adj(n);
    for (std::size_t u = 0; u < n; ++u) {
        for (std::size_t v = 0; v < n; ++v) {
            if (capacity[u][v] > 0) {
                adj[u].push_back({v, adj[v].size(), capacity[u][v]});
                adj[v].push_back({u, adj[u].size() - 1, 0});
            }
        }
    }

    // Dinic max flow
    std::vector<int> level(n);
    std::vector<std::size_t> iter(n);
    const int INF = std::numeric_limits<int>::max();

    auto bfs = [&]() {
        std::fill(level.begin(), level.end(), -1);
        std::queue<std::size_t> q;
        level[src] = 0;
        q.push(src);
        while (!q.empty()) {
            std::size_t u = q.front(); q.pop();
            for (auto& e : adj[u]) {
                if (e.cap > 0 && level[e.to] < 0) {
                    level[e.to] = level[u] + 1;
                    q.push(e.to);
                }
            }
        }
        return level[sink] >= 0;
    };

    std::function<int(std::size_t, int)> dfs = [&](std::size_t u, int f) {
        if (u == sink) return f;
        for (std::size_t& i = iter[u]; i < adj[u].size(); ++i) {
            auto& e = adj[u][i];
            if (e.cap > 0 && level[u] < level[e.to]) {
                int d = dfs(e.to, std::min(f, e.cap));
                if (d > 0) {
                    e.cap -= d;
                    adj[e.to][e.rev].cap += d;
                    return d;
                }
            }
        }
        return 0;
    };

    int flow = 0;
    while (bfs()) {
        std::fill(iter.begin(), iter.end(), 0);
        int f;
        while ((f = dfs(src, INF)) > 0) flow += f;
    }

    // Find S-side: vertices reachable from src in residual graph
    std::vector<bool> s_side(n, false);
    std::queue<std::size_t> q;
    q.push(src);
    s_side[src] = true;
    while (!q.empty()) {
        std::size_t u = q.front(); q.pop();
        for (auto& e : adj[u]) {
            if (e.cap > 0 && !s_side[e.to]) {
                s_side[e.to] = true;
                q.push(e.to);
            }
        }
    }

    return {flow, s_side};
}

}  // namespace graph
}  // namespace algorithm_x
