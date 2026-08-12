#pragma once

#include <algorithm>
#include <cstddef>
#include <limits>
#include <vector>

namespace algorithm_x {
namespace algo {

// Maximum subarray sum (Kadane's algorithm, O(n)).
// Handles all-negative arrays by returning the largest single element.
template <typename T>
T max_subarray_sum(const std::vector<T>& arr) {
    if (arr.empty()) return {};
    T best = arr[0];
    T cur = arr[0];
    for (std::size_t i = 1; i < arr.size(); ++i) {
        cur = std::max(arr[i], cur + arr[i]);
        best = std::max(best, cur);
    }
    return best;
}

// Divide-and-conquer version for range [l, r).
template <typename T>
T max_subarray_dc(const std::vector<T>& arr,
                  std::size_t l, std::size_t r) {
    if (r - l == 0) return {};
    if (r - l == 1) return arr[l];

    std::size_t mid = l + (r - l) / 2;
    T left_max = max_subarray_dc(arr, l, mid);
    T right_max = max_subarray_dc(arr, mid, r);

    // Crossing midpoint.
    T left_sum = std::numeric_limits<T>::lowest();
    T sum = {};
    for (std::size_t i = mid; i-- > l;) {
        sum += arr[i];
        if (sum > left_sum) left_sum = sum;
    }

    T right_sum = std::numeric_limits<T>::lowest();
    sum = {};
    for (std::size_t i = mid; i < r; ++i) {
        sum += arr[i];
        if (sum > right_sum) right_sum = sum;
    }

    return std::max({left_max, right_max, left_sum + right_sum});
}

template <typename T>
T max_subarray_dc(const std::vector<T>& arr) {
    return max_subarray_dc(arr, 0, arr.size());
}

// ---- Quickselect (k-th smallest element, 0-indexed) ----

template <typename It, typename Cmp = std::less<>>
It quickselect(It first, It last, std::size_t k, Cmp cmp = {}) {
    auto n = static_cast<std::size_t>(std::distance(first, last));
    if (n == 0) return last;
    if (n == 1) return first;

    // Median-of-three pivot selection.
    auto mid = std::next(first, static_cast<long>(n / 2));
    auto last_elem = std::prev(last);
    if (cmp(*mid, *first)) std::iter_swap(first, mid);
    if (cmp(*last_elem, *first)) std::iter_swap(first, last_elem);
    if (cmp(*last_elem, *mid)) std::iter_swap(mid, last_elem);
    std::iter_swap(mid, last_elem);

    auto& pivot = *last_elem;
    auto i = first;
    for (auto j = first; j != last_elem; ++j) {
        if (cmp(*j, pivot)) std::iter_swap(i++, j);
    }
    std::iter_swap(i, last_elem);

    auto pivot_idx = static_cast<std::size_t>(std::distance(first, i));
    if (pivot_idx == k) return i;
    if (pivot_idx > k) return quickselect(first, i, k, cmp);
    return quickselect(std::next(i), last, k - pivot_idx - 1, cmp);
}

}  // namespace algo
}  // namespace algorithm_x
