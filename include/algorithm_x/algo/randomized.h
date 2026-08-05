#pragma once

#include <algorithm>
#include <cstddef>
#include <iterator>
#include <random>
#include <vector>

namespace algorithm_x {
namespace algo {

// Fisher-Yates shuffle — produces every permutation with equal probability.
template <typename It>
void shuffle(It first, It last) {
    static std::random_device rd;
    static std::mt19937 gen(rd());
    auto n = static_cast<long>(std::distance(first, last));
    for (long i = n - 1; i > 0; --i) {
        std::uniform_int_distribution<long> dist(0, i);
        long j = dist(gen);
        std::iter_swap(std::next(first, i), std::next(first, j));
    }
}

// Randomized quickselect — O(n) expected, no median-of-three needed.
template <typename It, typename Cmp = std::less<>>
It randomized_quickselect(It first, It last, std::size_t k,
                          Cmp cmp = {}) {
    auto n = static_cast<std::size_t>(std::distance(first, last));
    if (n == 0) return last;
    if (n == 1) return first;

    // Random pivot.
    static std::random_device rd;
    static std::mt19937 gen(rd());
    std::uniform_int_distribution<std::size_t> dist(0, n - 1);
    auto pivot_it = std::next(first, static_cast<long>(dist(gen)));
    std::iter_swap(pivot_it, std::prev(last));

    auto& pivot = *std::prev(last);
    auto i = first;
    for (auto j = first; j != std::prev(last); ++j) {
        if (cmp(*j, pivot)) std::iter_swap(i++, j);
    }
    std::iter_swap(i, std::prev(last));

    auto p = static_cast<std::size_t>(std::distance(first, i));
    if (p == k) return i;
    if (p > k) return randomized_quickselect(first, i, k, cmp);
    return randomized_quickselect(std::next(i), last, k - p - 1, cmp);
}

// Monte Carlo estimation of pi.
// More samples give higher precision.
inline double monte_carlo_pi(long long samples) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<double> dist(-1.0, 1.0);
    long long inside = 0;
    for (long long i = 0; i < samples; ++i) {
        double x = dist(gen);
        double y = dist(gen);
        if (x * x + y * y <= 1.0) ++inside;
    }
    return 4.0 * inside / samples;
}

// Reservoir sampling — randomly select k items from a stream.
template <typename It>
std::vector<typename std::iterator_traits<It>::value_type>
reservoir_sample(It first, It last, std::size_t k) {
    using T = typename std::iterator_traits<It>::value_type;
    if (k == 0) return {};

    std::vector<T> reservoir;
    reservoir.reserve(k);

    auto it = first;
    for (std::size_t i = 0; i < k && it != last; ++i, ++it) {
        reservoir.push_back(*it);
    }

    // If fewer than k elements exist, return what we have.
    if (reservoir.size() < k) return reservoir;

    static std::random_device rd;
    static std::mt19937 gen(rd());
    std::size_t i = k;
    for (; it != last; ++it, ++i) {
        std::uniform_int_distribution<std::size_t> dist(0, i);
        std::size_t j = dist(gen);
        if (j < k) reservoir[j] = *it;
    }
    return reservoir;
}

}  // namespace algo
}  // namespace algorithm_x
