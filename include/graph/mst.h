#pragma once

#include <algorithm>
#include <cstddef>
#include <limits>
#include <numeric>
#include <utility>
#include <vector>

namespace algorithm_x {
namespace graph {

// ---- Types ----

struct Edge {
    std::size_t u;
    std::size_t v;
    int w;
};

// ---- Kruskal (edge-list, O(E log E)) ----

// Returns {mst_edges, total_weight}.
inline std::pair<std::vector<Edge>, int> kruskal(std::vector<Edge> edges,
                                                  std::size_t n) {
    std::sort(edges.begin(), edges.end(),
              [](const Edge& a, const Edge& b) { return a.w < b.w; });

    std::vector<std::size_t> parent(n);
    std::iota(parent.begin(), parent.end(), 0);

    auto find = [&](std::size_t x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    };

    auto unite = [&](std::size_t a, std::size_t b) {
        a = find(a);
        b = find(b);
        if (a != b) {
            parent[a] = b;
            return true;
        }
        return false;
    };

    std::vector<Edge> mst;
    int total = 0;
    for (auto& e : edges) {
        if (unite(e.u, e.v)) {
            mst.push_back(e);
            total += e.w;
            if (mst.size() == n - 1) break;
        }
    }
    return {mst, total};
}

// ---- Prim (adjacency-list, O(V^2)) ----

// Returns total MST weight; -1 if graph is disconnected.
inline int prim(
    const std::vector<std::vector<std::pair<std::size_t, int>>>& adj) {
    std::size_t n = adj.size();
    if (n == 0) return 0;

    std::vector<bool> visited(n, false);
    std::vector<int> min_edge(n, std::numeric_limits<int>::max());
    min_edge[0] = 0;

    int total = 0;
    for (std::size_t i = 0; i < n; ++i) {
        std::size_t u = n;
        int best = std::numeric_limits<int>::max();
        for (std::size_t v = 0; v < n; ++v) {
            if (!visited[v] && min_edge[v] < best) {
                best = min_edge[v];
                u = v;
            }
        }
        if (u == n) return -1;  // disconnected
        visited[u] = true;
        total += best;

        for (auto& [v, w] : adj[u]) {
            if (!visited[v] && w < min_edge[v]) {
                min_edge[v] = w;
            }
        }
    }
    return total;
}

}  // namespace graph
}  // namespace algorithm_x
