#pragma once

#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace graph {

// 2-SAT solver using Tarjan SCC.
// n variables. add_clause(u, u_neg, v, v_neg):
//   u_neg=true means NOT u. So (u OR v) = add_clause(u, false, v, false).
// Returns assignment (index by variable) or empty if unsatisfiable.
class TwoSAT {
public:
    explicit TwoSAT(std::size_t n) : n_(n), adj_(2 * n) {}

    void add_clause(std::size_t u, bool u_neg,
                    std::size_t v, bool v_neg) {
        std::size_t nu = 2 * u + (u_neg ? 1 : 0);
        std::size_t nv = 2 * v + (v_neg ? 1 : 0);
        adj_[nu ^ 1].push_back(nv);  // !u → v
        adj_[nv ^ 1].push_back(nu);  // !v → u
    }

    std::vector<bool> solve() {
        // Tarjan SCC
        std::vector<std::size_t> comp(2 * n_, 2 * n_);
        std::vector<std::size_t> dfn(2 * n_, 0), low(2 * n_, 0);
        std::vector<std::size_t> stk;
        std::vector<bool> in_stack(2 * n_, false);
        std::size_t timer = 0, comp_cnt = 0;

        auto dfs = [&](auto&& self, std::size_t u) -> void {
            dfn[u] = low[u] = ++timer;
            stk.push_back(u);
            in_stack[u] = true;
            for (std::size_t v : adj_[u]) {
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

        for (std::size_t i = 0; i < 2 * n_; ++i)
            if (!dfn[i]) dfs(dfs, i);

        // Check each variable is in different SCCs
        std::vector<bool> result(n_);
        for (std::size_t i = 0; i < n_; ++i) {
            if (comp[2 * i] == comp[2 * i + 1]) return {};
            result[i] = comp[2 * i] > comp[2 * i + 1];
        }
        return result;
    }

private:
    std::size_t n_;
    std::vector<std::vector<std::size_t>> adj_;
};

}  // namespace graph
}  // namespace algorithm_x
