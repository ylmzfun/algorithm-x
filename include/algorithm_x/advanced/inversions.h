#pragma once

#include <cstddef>
#include <cstdint>
#include <vector>

namespace algorithm_x {
namespace advanced {

// 归并排序求逆序对 — O(n log n)。
template <typename T>
int64_t count_inversions(const std::vector<T>& arr) {
    if (arr.size() <= 1) return 0;
    auto copy = arr;

    auto merge = [&](auto&& self, std::size_t l, std::size_t mid,
                     std::size_t r) -> int64_t {
        std::vector<T> left(copy.begin() + static_cast<long>(l),
                             copy.begin() + static_cast<long>(mid));
        std::vector<T> right(copy.begin() + static_cast<long>(mid),
                              copy.begin() + static_cast<long>(r));
        int64_t inv = 0;
        std::size_t i = 0, j = 0, k = l;
        while (i < left.size() && j < right.size()) {
            if (left[i] <= right[j]) {
                copy[k++] = left[i++];
            } else {
                copy[k++] = right[j++];
                inv += static_cast<int64_t>(left.size() - i);
            }
        }
        while (i < left.size()) copy[k++] = left[i++];
        while (j < right.size()) copy[k++] = right[j++];
        return inv;
    };

    auto sort_count = [&](auto&& self, std::size_t l,
                           std::size_t r) -> int64_t {
        if (r - l <= 1) return 0;
        std::size_t mid = l + (r - l) / 2;
        int64_t inv = self(self, l, mid) + self(self, mid, r);
        inv += merge(merge, l, mid, r);
        return inv;
    };

    return sort_count(sort_count, 0, arr.size());
}

}  // namespace advanced
}  // namespace algorithm_x
