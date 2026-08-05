#pragma once

#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace advanced {

// 可持久化线段树（主席树）— 单点更新，区间求和，多版本。
class PersistentSegmentTree {
    struct Node {
        int left = -1, right = -1;
        int sum = 0;
    };

public:
    // 用 arr 构建版本 0。
    explicit PersistentSegmentTree(const std::vector<int>& arr) : n_(arr.size()) {
        nodes_.reserve(4 * n_ + 1);
        nodes_.emplace_back();  // node 0 = empty
        roots_.push_back(build(arr, 0, n_));
    }

    // 在版本 ver 基础上将 pos 位置值设为 val，返回新版本号。
    int update(int ver, std::size_t pos, int val) {
        int new_root = update_impl(roots_[static_cast<std::size_t>(ver)],
                                    0, n_, pos, val);
        roots_.push_back(new_root);
        return static_cast<int>(roots_.size()) - 1;
    }

    // 查询版本 ver 中 [l, r) 的区间和。
    int query(int ver, std::size_t l, std::size_t r) const {
        return query_impl(roots_[static_cast<std::size_t>(ver)], 0, n_, l, r);
    }

    int version_count() const { return static_cast<int>(roots_.size()); }

private:
    int build(const std::vector<int>& arr, std::size_t l, std::size_t r) {
        int idx = static_cast<int>(nodes_.size());
        nodes_.emplace_back();
        if (r - l == 1) {
            nodes_[static_cast<std::size_t>(idx)].sum = arr[l];
            return idx;
        }
        std::size_t mid = l + (r - l) / 2;
        nodes_[static_cast<std::size_t>(idx)].left = build(arr, l, mid);
        nodes_[static_cast<std::size_t>(idx)].right = build(arr, mid, r);
        nodes_[static_cast<std::size_t>(idx)].sum =
            nodes_[static_cast<std::size_t>(
                       nodes_[static_cast<std::size_t>(idx)].left)]
                .sum +
            nodes_[static_cast<std::size_t>(
                       nodes_[static_cast<std::size_t>(idx)].right)]
                .sum;
        return idx;
    }

    int update_impl(int prev, std::size_t l, std::size_t r,
                    std::size_t pos, int val) {
        int idx = static_cast<int>(nodes_.size());
        nodes_.push_back(nodes_[static_cast<std::size_t>(prev)]);
        if (r - l == 1) {
            nodes_[static_cast<std::size_t>(idx)].sum = val;
            return idx;
        }
        std::size_t mid = l + (r - l) / 2;
        if (pos < mid) {
            nodes_[static_cast<std::size_t>(idx)].left =
                update_impl(nodes_[static_cast<std::size_t>(prev)].left,
                            l, mid, pos, val);
        } else {
            nodes_[static_cast<std::size_t>(idx)].right =
                update_impl(nodes_[static_cast<std::size_t>(prev)].right,
                            mid, r, pos, val);
        }
        nodes_[static_cast<std::size_t>(idx)].sum =
            nodes_[static_cast<std::size_t>(
                       nodes_[static_cast<std::size_t>(idx)].left)]
                .sum +
            nodes_[static_cast<std::size_t>(
                       nodes_[static_cast<std::size_t>(idx)].right)]
                .sum;
        return idx;
    }

    int query_impl(int node, std::size_t l, std::size_t r,
                   std::size_t ql, std::size_t qr) const {
        if (node == -1 || ql >= r || qr <= l) return 0;
        if (ql <= l && r <= qr) {
            return nodes_[static_cast<std::size_t>(node)].sum;
        }
        std::size_t mid = l + (r - l) / 2;
        return query_impl(nodes_[static_cast<std::size_t>(node)].left,
                          l, mid, ql, qr) +
               query_impl(nodes_[static_cast<std::size_t>(node)].right,
                          mid, r, ql, qr);
    }

    std::size_t n_;
    std::vector<Node> nodes_;
    std::vector<int> roots_;
};

}  // namespace advanced
}  // namespace algorithm_x
