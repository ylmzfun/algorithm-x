#pragma once

#include <algorithm>
#include <cstddef>
#include <iterator>
#include <vector>

namespace algorithm_x {
namespace algo {

// 桶排序 — 整数专用，O(n + k)，k = max_val - min_val + 1。
template <typename It>
void bucket_sort(It first, It last) {
    if (first == last) return;
    using T = typename std::iterator_traits<It>::value_type;
    auto [min_it, max_it] = std::minmax_element(first, last);
    T min_val = *min_it, max_val = *max_it;
    std::size_t range = static_cast<std::size_t>(max_val - min_val + 1);

    std::vector<std::vector<T>> buckets(range);
    for (auto it = first; it != last; ++it) {
        buckets[static_cast<std::size_t>(*it - min_val)].push_back(*it);
    }

    auto out = first;
    for (auto& bucket : buckets) {
        for (const auto& v : bucket) {
            *out++ = v;
        }
    }
}

// 三分查找 — 在单峰函数 f 的 [l, r] 上找最小值点。
// f 必须是凸函数（U 形）。
template <typename T, typename F>
T ternary_search(T l, T r, F f, const T eps = T{0}) {
    while (r - l > eps) {
        T m1 = l + (r - l) / 3;
        T m2 = r - (r - l) / 3;
        if (f(m1) < f(m2)) {
            r = m2;
        } else {
            l = m1;
        }
    }
    return l;
}

}  // namespace algo
}  // namespace algorithm_x
