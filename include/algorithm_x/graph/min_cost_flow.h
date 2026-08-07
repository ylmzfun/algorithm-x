#pragma once

#include <algorithm>
#include <cstddef>
#include <limits>
#include <queue>
#include <vector>

namespace algorithm_x {
namespace graph {

// 最小费用最大流 — Successive Shortest Path with potentials (Dijkstra).
class MinCostMaxFlow {
    struct Edge {
        std::size_t to, rev;
        int cap, cost;
    };

public:
    MinCostMaxFlow(std::size_t n) : adj_(n), potential_(n), n_(n) {}

    void add_edge(std::size_t u, std::size_t v, int cap, int cost) {
        adj_[u].push_back({v, adj_[v].size(), cap, cost});
        adj_[v].push_back({u, adj_[u].size() - 1, 0, -cost});
    }

    // Returns {max_flow, min_cost}.
    std::pair<int, int> solve(std::size_t s, std::size_t t) {
        int flow = 0, cost = 0;
        const int INF = std::numeric_limits<int>::max();
        std::fill(potential_.begin(), potential_.end(), 0);

        while (true) {
            std::vector<int> dist(n_, INF);
            std::vector<int> prevv(n_, -1);
            std::vector<int> preve(n_, -1);
            dist[s] = 0;

            using State = std::pair<int, int>;
            std::priority_queue<State, std::vector<State>, std::greater<>> pq;
            pq.emplace(0, static_cast<int>(s));

            while (!pq.empty()) {
                auto [d, u] = pq.top();
                pq.pop();
                if (dist[static_cast<std::size_t>(u)] < d) continue;
                for (int i = 0; i < static_cast<int>(adj_[static_cast<std::size_t>(u)].size()); ++i) {
                    auto& e = adj_[static_cast<std::size_t>(u)][static_cast<std::size_t>(i)];
                    if (e.cap <= 0) continue;
                    int nd = d + e.cost +
                             potential_[static_cast<std::size_t>(u)] -
                             potential_[e.to];
                    if (nd < dist[e.to]) {
                        dist[e.to] = nd;
                        prevv[e.to] = u;
                        preve[e.to] = i;
                        pq.emplace(nd, static_cast<int>(e.to));
                    }
                }
            }
            if (dist[t] == INF) break;

            for (std::size_t v = 0; v < n_; ++v) {
                if (dist[v] < INF)
                    potential_[v] += dist[v];
            }

            // Augment.
            int add = INF;
            for (int v = static_cast<int>(t); v != static_cast<int>(s);
                 v = prevv[static_cast<std::size_t>(v)]) {
                int u = prevv[static_cast<std::size_t>(v)];
                int i = preve[static_cast<std::size_t>(v)];
                add = std::min(add,
                    adj_[static_cast<std::size_t>(u)][static_cast<std::size_t>(i)].cap);
            }

            for (int v = static_cast<int>(t); v != static_cast<int>(s);
                 v = prevv[static_cast<std::size_t>(v)]) {
                int u = prevv[static_cast<std::size_t>(v)];
                int i = preve[static_cast<std::size_t>(v)];
                auto& e = adj_[static_cast<std::size_t>(u)][static_cast<std::size_t>(i)];
                e.cap -= add;
                adj_[e.to][e.rev].cap += add;
                cost += add * e.cost;
            }
            flow += add;
        }
        return {flow, cost};
    }

private:
    std::vector<std::vector<Edge>> adj_;
    std::vector<int> potential_;
    std::size_t n_;
};

}  // namespace graph
}  // namespace algorithm_x
