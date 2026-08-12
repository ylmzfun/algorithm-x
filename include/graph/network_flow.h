#pragma once

#include <algorithm>
#include <cstddef>
#include <limits>
#include <queue>
#include <vector>

namespace algorithm_x {
namespace graph {

// ---- Dinic Max Flow ----

// Usage:
//   DinicGraph g(V);
//   g.add_edge(u, v, cap);
//   int max_flow = g.max_flow(src, sink);
class DinicGraph {
public:
    struct Edge {
        std::size_t to, rev;
        int cap;
    };

    explicit DinicGraph(std::size_t n) : adj_(n), level_(n), iter_(n) {}

    void add_edge(std::size_t u, std::size_t v, int cap) {
        adj_[u].push_back({v, adj_[v].size(), cap});
        adj_[v].push_back({u, adj_[u].size() - 1, 0});
    }

    int max_flow(std::size_t s, std::size_t t) {
        int flow = 0;
        const int INF = std::numeric_limits<int>::max();
        while (bfs(s, t)) {
            std::fill(iter_.begin(), iter_.end(), 0);
            int f;
            while ((f = dfs(s, t, INF)) > 0) flow += f;
        }
        return flow;
    }

private:
    bool bfs(std::size_t s, std::size_t t) {
        std::fill(level_.begin(), level_.end(), -1);
        std::queue<std::size_t> q;
        level_[s] = 0;
        q.push(s);
        while (!q.empty()) {
            std::size_t u = q.front();
            q.pop();
            for (auto& e : adj_[u]) {
                if (e.cap > 0 && level_[e.to] < 0) {
                    level_[e.to] = level_[u] + 1;
                    q.push(e.to);
                }
            }
        }
        return level_[t] >= 0;
    }

    int dfs(std::size_t u, std::size_t t, int f) {
        if (u == t) return f;
        for (std::size_t& i = iter_[u]; i < adj_[u].size(); ++i) {
            auto& e = adj_[u][i];
            if (e.cap > 0 && level_[u] < level_[e.to]) {
                int d = dfs(e.to, t, std::min(f, e.cap));
                if (d > 0) {
                    e.cap -= d;
                    adj_[e.to][e.rev].cap += d;
                    return d;
                }
            }
        }
        return 0;
    }

    std::vector<std::vector<Edge>> adj_;
    std::vector<int> level_;
    std::vector<std::size_t> iter_;
};

// ---- Bipartite Matching (Hungarian / DFS augmenting path), O(VE) ----

// Returns matchL[u] = v, or -1 if unmatched.
inline std::vector<long> bipartite_matching(
    std::size_t L, std::size_t R,
    const std::vector<std::vector<std::size_t>>& adj) {
    std::vector<long> matchL(L, -1), matchR(R, -1);
    std::vector<bool> visited;

    auto dfs = [&](auto&& self, std::size_t u) -> bool {
        for (std::size_t v : adj[u]) {
            if (visited[v]) continue;
            visited[v] = true;
            if (matchR[v] == -1 ||
                self(self, static_cast<std::size_t>(matchR[v]))) {
                matchL[u] = static_cast<long>(v);
                matchR[v] = static_cast<long>(u);
                return true;
            }
        }
        return false;
    };

    for (std::size_t u = 0; u < L; ++u) {
        visited.assign(R, false);
        dfs(dfs, u);
    }
    return matchL;
}

}  // namespace graph
}  // namespace algorithm_x
