#pragma once

#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace ds {

// 树状数组 (Fenwick Tree / BIT) — 单点加、前缀和 O(log n)。
template <typename T>
class FenwickTree {
public:
    explicit FenwickTree(std::size_t n) : n_(n), tree_(n + 1, T{}) {}

    // 由数组 O(n) 建树。
    explicit FenwickTree(const std::vector<T>& arr)
        : n_(arr.size()), tree_(arr.size() + 1, T{}) {
        for (std::size_t i = 0; i < n_; ++i) {
            tree_[i + 1] = arr[i];
        }
        for (std::size_t i = 1; i <= n_; ++i) {
            std::size_t j = i + (i & (~i + 1));  // i + lowbit(i)
            if (j <= n_) tree_[j] += tree_[i];
        }
    }

    // 位置 idx（0-indexed）加上 delta。
    void add(std::size_t idx, const T& delta) {
        for (std::size_t i = idx + 1; i <= n_; i += i & (~i + 1)) {
            tree_[i] += delta;
        }
    }

    // 前缀和 sum[0..idx]。
    T sum(std::size_t idx) const {
        T s = T{};
        for (std::size_t i = idx + 1; i > 0; i -= i & (~i + 1)) {
            s += tree_[i];
        }
        return s;
    }

    // 区间和 sum[l..r]。
    T range_sum(std::size_t l, std::size_t r) const {
        return sum(r) - (l > 0 ? sum(l - 1) : T{});
    }

    std::size_t size() const { return n_; }

private:
    std::size_t n_;
    std::vector<T> tree_;
};

}  // namespace ds
}  // namespace algorithm_x
