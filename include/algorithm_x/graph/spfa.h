#pragma once

#include <cstddef>
#include <limits>
#include <queue>
#include <vector>

namespace algorithm_x {
namespace graph {

// SPFA — Shortest Path Faster Algorithm (queue-based Bellman-Ford).
// Returns {distances, has_negative_cycle}.
template <typename T>
std::pair<std::vector<T>, bool>
spfa(const std::vector<std::vector<std::pair<std::size_t, T>>>& adj,
     std::size_t src) {
    const T INF = std::numeric_limits<T>::max();
    std::size_t n = adj.size();
    std::vector<T> dist(n, INF);
    std::vector<bool> in_queue(n, false);
    std::vector<std::size_t> cnt(n, 0);
    std::queue<std::size_t> q;

    dist[src] = T{};
    q.push(src);
    in_queue[src] = true;

    while (!q.empty()) {
        std::size_t u = q.front();
        q.pop();
        in_queue[u] = false;
        for (auto& [v, w] : adj[u]) {
            if (dist[u] != INF && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                if (!in_queue[v]) {
                    q.push(v);
                    in_queue[v] = true;
                    ++cnt[v];
                    if (cnt[v] > n) return {dist, true};  // negative cycle
                }
            }
        }
    }
    return {dist, false};
}

}  // namespace graph
}  // namespace algorithm_x
