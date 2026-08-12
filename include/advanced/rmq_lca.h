#pragma once

#include <algorithm>
#include <cmath>
#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace advanced {

// Sparse Table — 静态 RMQ（区间最小值查询）O(n log n) 建表，O(1) 查询。
template <typename T>
class SparseTable {
public:
    explicit SparseTable(const std::vector<T>& arr) : n_(arr.size()) {
        int k = static_cast<int>(std::log2(n_)) + 1;
        table_.assign(static_cast<std::size_t>(k),
                      std::vector<T>(n_));
        logs_.resize(n_ + 1, 0);
        for (std::size_t i = 2; i <= n_; ++i) {
            logs_[i] = logs_[i / 2] + 1;
        }

        table_[0] = arr;
        for (int j = 1; j < k; ++j) {
            std::size_t step = std::size_t{1} << static_cast<std::size_t>(j - 1);
            for (std::size_t i = 0; i + (std::size_t{1} << static_cast<std::size_t>(j)) <= n_; ++i) {
                table_[static_cast<std::size_t>(j)][i] =
                    std::min(table_[static_cast<std::size_t>(j - 1)][i],
                             table_[static_cast<std::size_t>(j - 1)][i + step]);
            }
        }
    }

    // 查询 [l, r]（闭区间）的最小值。
    T query(std::size_t l, std::size_t r) const {
        std::size_t len = r - l + 1;
        int j = logs_[len];
        return std::min(table_[static_cast<std::size_t>(j)][l],
                        table_[static_cast<std::size_t>(j)]
                              [r - (std::size_t{1} << static_cast<std::size_t>(j)) + 1]);
    }

    std::size_t size() const { return n_; }

private:
    std::size_t n_;
    std::vector<std::vector<T>> table_;
    std::vector<int> logs_;
};

// LCA（最近公共祖先）— 倍增法 O(n log n) 建表，O(log n) 查询。
// 输入：树以无向邻接表给出，root 为根节点。
class LCA {
public:
    LCA(const std::vector<std::vector<std::size_t>>& adj,
        std::size_t root = 0)
        : n_(adj.size()) {
        int k = static_cast<int>(std::log2(n_)) + 1;
        up_.assign(n_, std::vector<std::size_t>(static_cast<std::size_t>(k), 0));
        depth_.assign(n_, 0);

        auto dfs = [&](auto&& self, std::size_t u, std::size_t p) -> void {
            up_[u][0] = p;
            for (int j = 1; j < k; ++j) {
                up_[u][static_cast<std::size_t>(j)] =
                    up_[up_[u][static_cast<std::size_t>(j - 1)]]
                      [static_cast<std::size_t>(j - 1)];
            }
            for (std::size_t v : adj[u]) {
                if (v == p) continue;
                depth_[v] = depth_[u] + 1;
                self(self, v, u);
            }
        };
        dfs(dfs, root, root);
    }

    std::size_t query(std::size_t u, std::size_t v) const {
        if (depth_[u] < depth_[v]) std::swap(u, v);

        int k = static_cast<int>(std::log2(n_)) + 1;
        // 提升 u 到与 v 同深度
        int diff = depth_[u] - depth_[v];
        for (int j = 0; j < k; ++j) {
            if (diff & (1 << j)) {
                u = up_[u][static_cast<std::size_t>(j)];
            }
        }

        if (u == v) return u;

        for (int j = k - 1; j >= 0; --j) {
            if (up_[u][static_cast<std::size_t>(j)] !=
                up_[v][static_cast<std::size_t>(j)]) {
                u = up_[u][static_cast<std::size_t>(j)];
                v = up_[v][static_cast<std::size_t>(j)];
            }
        }
        return up_[u][0];
    }

private:
    std::size_t n_;
    std::vector<std::vector<std::size_t>> up_;
    std::vector<int> depth_;
};

}  // namespace advanced
}  // namespace algorithm_x
