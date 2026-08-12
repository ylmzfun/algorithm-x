#pragma once

#include <algorithm>
#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace algo {

// ---- Activity selection ----
// Select maximum number of non-overlapping activities.
// Activities are sorted by finish time internally.
// Returns indices of selected activities.

inline std::vector<std::size_t> activity_selection(
    const std::vector<int>& start,
    const std::vector<int>& finish) {
    std::vector<std::size_t> selected;
    if (start.empty()) return selected;

    // Build index array and sort by finish time.
    std::vector<std::size_t> idx(start.size());
    for (std::size_t i = 0; i < idx.size(); ++i) idx[i] = i;
    std::sort(idx.begin(), idx.end(),
              [&](std::size_t a, std::size_t b) {
                  return finish[a] < finish[b];
              });

    selected.push_back(idx[0]);
    int last_finish = finish[idx[0]];
    for (std::size_t i = 1; i < idx.size(); ++i) {
        if (start[idx[i]] >= last_finish) {
            selected.push_back(idx[i]);
            last_finish = finish[idx[i]];
        }
    }
    return selected;
}

// ---- Fractional knapsack ----
// Items are divisible; maximize total value within capacity.

template <typename T>
T fractional_knapsack(const std::vector<T>& weights,
                      const std::vector<T>& values,
                      T capacity) {
    std::size_t n = weights.size();
    std::vector<std::size_t> idx(n);
    for (std::size_t i = 0; i < n; ++i) idx[i] = i;
    std::sort(idx.begin(), idx.end(), [&](std::size_t a, std::size_t b) {
        return values[a] * weights[b] > values[b] * weights[a];
    });

    T total = {};
    for (std::size_t i : idx) {
        if (capacity <= T{}) break;
        T take = std::min(weights[i], capacity);
        total += take * values[i] / weights[i];
        capacity -= take;
    }
    return total;
}

// ---- Greedy coin change ----
// Only works for canonical coin systems (e.g., US cents 25,10,5,1).
// Returns coin counts per denomination, or empty vector if impossible.

inline std::vector<int> coin_change_greedy(
    int amount, const std::vector<int>& coins) {
    std::vector<int> result(coins.size(), 0);
    for (std::size_t i = 0; i < coins.size(); ++i) {
        result[i] = amount / coins[i];
        amount %= coins[i];
    }
    if (amount != 0) return {};
    return result;
}

}  // namespace algo
}  // namespace algorithm_x
