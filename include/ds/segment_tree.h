#pragma once

#include <algorithm>
#include <cstddef>
#include <functional>
#include <vector>

namespace algorithm_x {
namespace ds {

// SegmentTree — 区间求和线段树（可扩展为 min/max/gcd 等）。
// 支持 O(log n) 单点更新和区间查询。
// // 调用示例：
//   SegmentTree<int> st({1, 3, 5, 7, 9});
//   st.query(1, 3);  // sum of arr[1..3) = 3 + 5 + 7 = 15
//   st.update(2, 10); // arr[2] = 10
template <typename T>
class SegmentTree {
public:
    SegmentTree() = default;

    explicit SegmentTree(const std::vector<T>& arr) : n_(arr.size()) {
        tree_.resize(4 * n_);
        build(arr, 1, 0, n_);
    }

    void update(std::size_t idx, const T& value) {
        update(1, 0, n_, idx, value);
    }

    T query(std::size_t l, std::size_t r) const {
        return query(1, 0, n_, l, r);
    }

    std::size_t size() const { return n_; }

private:
    void build(const std::vector<T>& arr, std::size_t node,
               std::size_t tl, std::size_t tr) {
        if (tr - tl == 1) {
            tree_[node] = arr[tl];
            return;
        }
        std::size_t tm = tl + (tr - tl) / 2;
        build(arr, node * 2, tl, tm);
        build(arr, node * 2 + 1, tm, tr);
        tree_[node] = tree_[node * 2] + tree_[node * 2 + 1];
    }

    void update(std::size_t node, std::size_t tl, std::size_t tr,
                std::size_t idx, const T& value) {
        if (tr - tl == 1) {
            tree_[node] = value;
            return;
        }
        std::size_t tm = tl + (tr - tl) / 2;
        if (idx < tm)
            update(node * 2, tl, tm, idx, value);
        else
            update(node * 2 + 1, tm, tr, idx, value);
        tree_[node] = tree_[node * 2] + tree_[node * 2 + 1];
    }

    T query(std::size_t node, std::size_t tl, std::size_t tr,
            std::size_t l, std::size_t r) const {
        if (l >= r) return T{};
        if (tl == l && tr == r) return tree_[node];
        std::size_t tm = tl + (tr - tl) / 2;
        T left = query(node * 2, tl, tm, l, std::min(r, tm));
        T right = query(node * 2 + 1, tm, tr, std::max(l, tm), r);
        return left + right;
    }

    std::vector<T> tree_;
    std::size_t n_ = 0;
};

}  // namespace ds
}  // namespace algorithm_x
