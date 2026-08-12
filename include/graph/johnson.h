#pragma once

#include <algorithm>
#include <cstddef>
#include <limits>
#include <queue>
#include <vector>

namespace algorithm_x {
namespace graph {

// Johnson 全源最短路径 O(V² log V + VE)。
// 支持负权边，无负环。返回 dist[i][j]。
template <typename T>
std::vector<std::vector<T>> johnson(
    const std::vector<std::vector<std::pair<std::size_t, T>>>& adj) {
    const T INF = std::numeric_limits<T>::max();
    std::size_t n = adj.size();

    // Step 1: 添加虚拟节点 n，到所有节点边权为 0
    std::vector<T> h(n + 1, INF);
    h[n] = T{};

    // Bellman-Ford from virtual node
    std::vector<std::tuple<std::size_t, std::size_t, T>> edges;
    for (std::size_t u = 0; u < n; ++u) {
        for (auto& [v, w] : adj[u]) {
            edges.emplace_back(u, v, w);
        }
        edges.emplace_back(n, u, T{});
    }

    for (std::size_t i = 0; i < n; ++i) {
        bool updated = false;
        for (auto& [u, v, w] : edges) {
            if (h[u] != INF && h[u] + w < h[v]) {
                h[v] = h[u] + w;
                updated = true;
            }
        }
        if (!updated) break;
    }

    // Step 2: 重赋权 + Dijkstra
    std::vector<std::vector<T>> dist(n, std::vector<T>(n, INF));
    for (std::size_t s = 0; s < n; ++s) {
        using State = std::pair<T, std::size_t>;
        std::priority_queue<State, std::vector<State>, std::greater<>> pq;
        dist[s][s] = T{};
        pq.emplace(T{}, s);

        while (!pq.empty()) {
            auto [d, u] = pq.top();
            pq.pop();
            if (d != dist[s][u]) continue;
            for (auto& [v, w] : adj[u]) {
                T new_d = d + w + h[u] - h[v];
                if (new_d < dist[s][v]) {
                    dist[s][v] = new_d;
                    pq.emplace(new_d, v);
                }
            }
        }

        // 恢复真实距离
        for (std::size_t v = 0; v < n; ++v) {
            if (dist[s][v] != INF) {
                dist[s][v] = dist[s][v] - h[s] + h[v];
            }
        }
    }
    return dist;
}

}  // namespace graph
}  // namespace algorithm_x
