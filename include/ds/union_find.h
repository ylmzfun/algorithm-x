#pragma once

#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace ds {

// UnionFind — 并查集（Disjoint Set Union）。
// 路径压缩 + 按秩合并，均摊 O(α(n))。
// // 调用示例：
//   UnionFind uf(5);
//   uf.unite(0, 2);
//   uf.connected(0, 2);  // true
//   uf.connected(0, 1);  // false
//   uf.count();
// 4 groups
class UnionFind {
public:
    explicit UnionFind(std::size_t n)
        : parent_(n), rank_(n, 0), count_(n) {
        for (std::size_t i = 0; i < n; ++i) {
            parent_[i] = i;
        }
    }

    std::size_t find(std::size_t x) {
        if (parent_[x] != x) {
            parent_[x] = find(parent_[x]);  // path compression
        }
        return parent_[x];
    }

    void unite(std::size_t x, std::size_t y) {
        std::size_t rx = find(x);
        std::size_t ry = find(y);
        if (rx == ry) return;
        // union by rank
        if (rank_[rx] < rank_[ry]) {
            parent_[rx] = ry;
        } else if (rank_[rx] > rank_[ry]) {
            parent_[ry] = rx;
        } else {
            parent_[ry] = rx;
            ++rank_[rx];
        }
        --count_;
    }

    bool connected(std::size_t x, std::size_t y) {
        return find(x) == find(y);
    }

    std::size_t count() const { return count_; }
    std::size_t size() const { return parent_.size(); }

private:
    std::vector<std::size_t> parent_;
    std::vector<int> rank_;
    std::size_t count_;
};

}  // namespace ds
}  // namespace algorithm_x
