#pragma once

#include <cstddef>
#include <limits>
#include <queue>
#include <tuple>
#include <vector>

namespace algorithm_x {
namespace graph {

// Dijkstra — non-negative single-source shortest path, O((V+E) log V).
// Returns dist[v]; unreachable vertices get INF.
template <typename T>
std::vector<T> dijkstra(
    const std::vector<std::vector<std::pair<std::size_t, T>>>& adj,
    std::size_t src) {
    const T INF = std::numeric_limits<T>::max();
    std::size_t n = adj.size();
    std::vector<T> dist(n, INF);
    using State = std::pair<T, std::size_t>;
    std::priority_queue<State, std::vector<State>, std::greater<>> pq;

    dist[src] = T{};
    pq.emplace(T{}, src);

    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d != dist[u]) continue;
        for (auto& [v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.emplace(dist[v], v);
            }
        }
    }
    return dist;
}

// Bellman-Ford — handles negative edge weights, O(VE).
// Returns {dist_vec, has_negative_cycle}.
template <typename T>
std::pair<std::vector<T>, bool> bellman_ford(
    const std::vector<std::tuple<std::size_t, std::size_t, T>>& edges,
    std::size_t n, std::size_t src) {
    const T INF = std::numeric_limits<T>::max();
    std::vector<T> dist(n, INF);
    dist[src] = T{};

    for (std::size_t i = 1; i < n; ++i) {
        bool updated = false;
        for (auto& [u, v, w] : edges) {
            if (dist[u] != INF && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                updated = true;
            }
        }
        if (!updated) break;
    }

    bool neg_cycle = false;
    for (auto& [u, v, w] : edges) {
        if (dist[u] != INF && dist[u] + w < dist[v]) {
            neg_cycle = true;
            break;
        }
    }
    return {dist, neg_cycle};
}

// Floyd-Warshall — all-pairs shortest path, O(V^3).
// Returns {dist_matrix, has_negative_cycle}.
// dist[i][i] must be 0 initially; dist[i][j] = INF if no edge.
template <typename T>
std::pair<std::vector<std::vector<T>>, bool> floyd_warshall(
    std::vector<std::vector<T>> dist) {
    const T INF = std::numeric_limits<T>::max();
    std::size_t n = dist.size();

    for (std::size_t k = 0; k < n; ++k) {
        for (std::size_t i = 0; i < n; ++i) {
            if (dist[i][k] == INF) continue;
            for (std::size_t j = 0; j < n; ++j) {
                if (dist[k][j] == INF) continue;
                if (dist[i][k] + dist[k][j] < dist[i][j]) {
                    dist[i][j] = dist[i][k] + dist[k][j];
                }
            }
        }
    }

    bool neg_cycle = false;
    for (std::size_t i = 0; i < n; ++i) {
        if (dist[i][i] < T{}) neg_cycle = true;
    }
    return {dist, neg_cycle};
}

}  // namespace graph
}  // namespace algorithm_x
