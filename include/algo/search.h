#pragma once

#include <algorithm>
#include <cstddef>
#include <iterator>

namespace algorithm_x {
namespace algo {

// Linear search — O(n).
// Returns iterator to first element equal to value, or last if not found.
template <typename It, typename T>
It linear_search(It first, It last, const T& value) {
    for (; first != last; ++first) {
        if (*first == value) return first;
    }
    return last;
}

// Binary search on sorted range [first, last).
// Returns iterator to matching element, or last if not found.
template <typename It, typename T, typename Cmp = std::less<>>
It binary_search_range(It first, It last, const T& value, Cmp cmp = {}) {
    auto it = std::lower_bound(first, last, value, cmp);
    if (it != last && !cmp(value, *it)) return it;
    return last;
}

// lower_bound — first position where element >= value.
template <typename It, typename T, typename Cmp = std::less<>>
It lower_bound(It first, It last, const T& value, Cmp cmp = {}) {
    auto count = std::distance(first, last);
    while (count > 0) {
        auto step = count / 2;
        auto mid = std::next(first, step);
        if (cmp(*mid, value)) {
            first = std::next(mid);
            count -= step + 1;
        } else {
            count = step;
        }
    }
    return first;
}

// upper_bound — first position where element > value.
template <typename It, typename T, typename Cmp = std::less<>>
It upper_bound(It first, It last, const T& value, Cmp cmp = {}) {
    auto count = std::distance(first, last);
    while (count > 0) {
        auto step = count / 2;
        auto mid = std::next(first, step);
        if (cmp(value, *mid)) {
            count = step;
        } else {
            first = std::next(mid);
            count -= step + 1;
        }
    }
    return first;
}

}  // namespace algo
}  // namespace algorithm_x
