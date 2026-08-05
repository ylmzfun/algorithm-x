#pragma once

#include <algorithm>
#include <cstddef>
#include <iterator>
#include <vector>

namespace algorithm_x {
namespace algo {

// ---- O(n^2) sorting ----

template <typename It, typename Cmp = std::less<>>
void bubble_sort(It first, It last, Cmp cmp = {}) {
    if (first == last) return;
    for (auto end = last; end != first;) {
        auto new_end = first;
        auto prev = first;
        for (auto cur = std::next(first); cur != end; ++cur) {
            if (cmp(*cur, *prev)) {
                std::iter_swap(cur, prev);
                new_end = cur;
            }
            prev = cur;
        }
        end = new_end;
    }
}

template <typename It, typename Cmp = std::less<>>
void selection_sort(It first, It last, Cmp cmp = {}) {
    for (; first != last; ++first) {
        auto min_it = first;
        for (auto it = std::next(first); it != last; ++it) {
            if (cmp(*it, *min_it)) min_it = it;
        }
        if (min_it != first) std::iter_swap(first, min_it);
    }
}

template <typename It, typename Cmp = std::less<>>
void insertion_sort(It first, It last, Cmp cmp = {}) {
    for (auto it = first; it != last; ++it) {
        auto key = std::move(*it);
        auto j = it;
        while (j != first && cmp(key, *std::prev(j))) {
            *j = std::move(*std::prev(j));
            --j;
        }
        *j = std::move(key);
    }
}

// ---- O(n log n) sorting ----

template <typename It, typename Cmp = std::less<>>
void merge_sort(It first, It last, Cmp cmp = {}) {
    auto n = static_cast<std::size_t>(std::distance(first, last));
    if (n <= 1) return;

    auto mid = std::next(first, static_cast<long>(n / 2));
    merge_sort(first, mid, cmp);
    merge_sort(mid, last, cmp);

    using T = typename std::iterator_traits<It>::value_type;
    std::vector<T> left(first, mid);
    std::vector<T> right(mid, last);

    auto l = left.begin();
    auto r = right.begin();
    auto out = first;
    while (l != left.end() && r != right.end()) {
        if (!cmp(*r, *l)) {
            *out++ = std::move(*l++);
        } else {
            *out++ = std::move(*r++);
        }
    }
    while (l != left.end()) *out++ = std::move(*l++);
    while (r != right.end()) *out++ = std::move(*r++);
}

template <typename It, typename Cmp = std::less<>>
void quick_sort(It first, It last, Cmp cmp = {}) {
    auto n = std::distance(first, last);
    if (n <= 1) return;

    // Median-of-three pivot selection.
    auto mid = std::next(first, n / 2);
    auto last_elem = std::prev(last);
    if (cmp(*mid, *first)) std::iter_swap(first, mid);
    if (cmp(*last_elem, *first)) std::iter_swap(first, last_elem);
    if (cmp(*last_elem, *mid)) std::iter_swap(mid, last_elem);
    std::iter_swap(mid, std::prev(last));

    auto& pivot = *std::prev(last);
    auto i = first;
    for (auto j = first; j != std::prev(last); ++j) {
        if (cmp(*j, pivot)) {
            if (i != j) std::iter_swap(i, j);
            ++i;
        }
    }
    std::iter_swap(i, std::prev(last));

    quick_sort(first, i, cmp);
    quick_sort(std::next(i), last, cmp);
}

template <typename It, typename Cmp = std::less<>>
void heap_sort(It first, It last, Cmp cmp = {}) {
    auto n = static_cast<std::size_t>(std::distance(first, last));
    if (n <= 1) return;

    auto sift_down = [&](std::size_t i, std::size_t size) {
        while (true) {
            std::size_t best = i;
            std::size_t l = 2 * i + 1;
            std::size_t r = 2 * i + 2;
            if (l < size && cmp(*(first + best), *(first + l))) best = l;
            if (r < size && cmp(*(first + best), *(first + r))) best = r;
            if (best == i) break;
            std::iter_swap(first + i, first + best);
            i = best;
        }
    };

    for (std::size_t i = n / 2; i-- > 0;) sift_down(i, n);
    for (std::size_t i = n - 1; i > 0; --i) {
        std::iter_swap(first, first + i);
        sift_down(0, i);
    }
}

// ---- Non-comparison sorting (integer only) ----

template <typename It>
void counting_sort(It first, It last) {
    if (first == last) return;

    using T = typename std::iterator_traits<It>::value_type;
    auto [min_it, max_it] = std::minmax_element(first, last);
    T min_val = *min_it;
    T max_val = *max_it;
    std::size_t range = static_cast<std::size_t>(max_val - min_val + 1);

    std::vector<std::size_t> count(range, 0);
    for (auto it = first; it != last; ++it) {
        ++count[static_cast<std::size_t>(*it - min_val)];
    }

    auto out = first;
    for (std::size_t i = 0; i < range; ++i) {
        for (std::size_t j = 0; j < count[i]; ++j) {
            *out++ = static_cast<T>(i) + min_val;
        }
    }
}

// LSD radix sort for non-negative integers.
template <typename It>
void radix_sort(It first, It last) {
    if (first == last) return;

    using T = typename std::iterator_traits<It>::value_type;
    auto max_val = *std::max_element(first, last);
    std::vector<T> buf(static_cast<std::size_t>(std::distance(first, last)));

    for (T exp = 1; max_val / exp > 0; exp *= 10) {
        std::size_t count[10] = {};
        for (auto it = first; it != last; ++it) {
            ++count[static_cast<std::size_t>((*it / exp) % 10)];
        }
        for (int i = 1; i < 10; ++i) {
            count[i] += count[i - 1];
        }
        for (auto it = last; it != first;) {
            --it;
            T digit = (*it / exp) % 10;
            buf[--count[static_cast<std::size_t>(digit)]] = *it;
        }
        std::copy(buf.begin(), buf.end(), first);
    }
}

}  // namespace algo
}  // namespace algorithm_x
