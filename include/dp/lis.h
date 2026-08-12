#pragma once

#include <algorithm>
#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace dp {

// 最长递增子序列长度 — O(n log n) 耐心排序。
template <typename T>
std::size_t lis_length(const std::vector<T>& nums) {
    std::vector<T> tails;
    for (const auto& x : nums) {
        auto it = std::lower_bound(tails.begin(), tails.end(), x);
        if (it == tails.end()) {
            tails.push_back(x);
        } else {
            *it = x;
        }
    }
    return tails.size();
}

// 最长递增子序列具体内容 — O(n log n)。
template <typename T>
std::vector<T> lis_sequence(const std::vector<T>& nums) {
    std::size_t n = nums.size();
    if (n == 0) return {};

    std::vector<T> tails;
    std::vector<std::size_t> tail_idx;
    std::vector<std::size_t> prev(n, n);  // n = sentinel

    for (std::size_t i = 0; i < n; ++i) {
        auto it = std::lower_bound(tails.begin(), tails.end(), nums[i]);
        std::size_t pos = static_cast<std::size_t>(it - tails.begin());
        if (it == tails.end()) {
            tails.push_back(nums[i]);
            tail_idx.push_back(i);
        } else {
            *it = nums[i];
            tail_idx[pos] = i;
        }
        if (pos > 0) prev[i] = tail_idx[pos - 1];
    }

    std::vector<T> result;
    for (std::size_t i = tail_idx.back(); i != n; i = prev[i]) {
        result.push_back(nums[i]);
    }
    std::reverse(result.begin(), result.end());
    return result;
}

// 最大子数组和 — Kadane O(n)（同时在此提供，虽已在 divide_conquer 中）。
template <typename T>
T max_subarray_sum(const std::vector<T>& arr) {
    if (arr.empty()) return T{};
    T best = arr[0], cur = arr[0];
    for (std::size_t i = 1; i < arr.size(); ++i) {
        cur = std::max(arr[i], cur + arr[i]);
        best = std::max(best, cur);
    }
    return best;
}

}  // namespace dp
}  // namespace algorithm_x
