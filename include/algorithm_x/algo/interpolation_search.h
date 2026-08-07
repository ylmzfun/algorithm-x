#pragma once

#include <cstddef>
#include <iterator>

namespace algorithm_x {
namespace algo {

// 插值查找 — O(log log n) 期望，适用于均匀分布的已排序数组。
// 返回第一个匹配元素的迭代器，未找到返回 last。
template <typename It, typename T>
It interpolation_search(It first, It last, const T& value) {
    if (first == last) return last;

    auto lo = first;
    auto hi = std::prev(last);

    while (lo <= hi) {
        auto lo_val = *lo;
        auto hi_val = *hi;
        if (value < lo_val || value > hi_val) break;

        auto n = static_cast<long>(std::distance(first, last));
        if (hi_val == lo_val) {
            return (*lo == value) ? lo : last;
        }

        // Interpolation formula.
        double fraction =
            static_cast<double>(value - lo_val) /
            static_cast<double>(hi_val - lo_val);
        auto pos = lo + static_cast<long>(fraction * (n - 1));
        if (pos < first) pos = first;
        if (pos >= last) pos = std::prev(last);

        if (*pos < value) {
            lo = std::next(pos);
        } else if (*pos > value) {
            hi = std::prev(pos);
        } else {
            return pos;
        }
    }
    return last;
}

}  // namespace algo
}  // namespace algorithm_x
