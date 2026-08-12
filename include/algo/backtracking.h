#pragma once

#include <algorithm>
#include <cstddef>
#include <cstdlib>
#include <numeric>
#include <string>
#include <vector>

namespace algorithm_x {
namespace algo {

// ---- N-Queens ----
// Returns one valid board with 'Q' for queens and '.' for empty cells.
// Returns empty vector if no solution exists (e.g., n=2, n=3).

inline std::vector<std::string> solve_n_queens(int n) {
    if (n <= 0) return {};

    auto sz = static_cast<std::size_t>(n);
    std::vector<std::string> board(sz, std::string(sz, '.'));
    std::vector<int> cols(sz, -1);

    auto is_safe = [&](int row, int col) {
        for (int r = 0; r < row; ++r) {
            if (cols[static_cast<std::size_t>(r)] == col ||
                std::abs(cols[static_cast<std::size_t>(r)] - col) == row - r) {
                return false;
            }
        }
        return true;
    };

    auto backtrack = [&](auto&& self, int row) -> bool {
        if (row == n) return true;
        for (int col = 0; col < n; ++col) {
            if (is_safe(row, col)) {
                cols[static_cast<std::size_t>(row)] = col;
                board[static_cast<std::size_t>(row)]
                     [static_cast<std::size_t>(col)] = 'Q';
                if (self(self, row + 1)) return true;
                board[static_cast<std::size_t>(row)]
                     [static_cast<std::size_t>(col)] = '.';
            }
        }
        return false;
    };

    return backtrack(backtrack, 0) ? board : std::vector<std::string>{};
}

// ---- Subset sum ----

// Check if any subset sums to target.
inline bool subset_sum_exists(const std::vector<int>& nums, int target) {
    int total = std::accumulate(nums.begin(), nums.end(), 0);
    if (target < 0 || target > total) return false;

    auto dfs = [&](auto&& self, std::size_t i, int rem) -> bool {
        if (rem == 0) return true;
        if (i == nums.size() || rem < 0) return false;
        if (self(self, i + 1, rem - nums[i])) return true;
        return self(self, i + 1, rem);
    };
    return dfs(dfs, 0, target);
}

// Find one subset that sums to target.
inline std::vector<int> subset_sum_find(const std::vector<int>& nums,
                                         int target) {
    int total = std::accumulate(nums.begin(), nums.end(), 0);
    if (target < 0 || target > total) return {};

    std::vector<int> result;
    auto dfs = [&](auto&& self, std::size_t i, int rem) -> bool {
        if (rem == 0) return true;
        if (i == nums.size() || rem < 0) return false;
        result.push_back(nums[i]);
        if (self(self, i + 1, rem - nums[i])) return true;
        result.pop_back();
        return self(self, i + 1, rem);
    };

    return dfs(dfs, 0, target) ? result : std::vector<int>{};
}

// ---- Permutations ----
// Returns all permutations of the input (lexicographic order).

template <typename T>
std::vector<std::vector<T>> permutations(std::vector<T> nums) {
    std::vector<std::vector<T>> result;
    std::sort(nums.begin(), nums.end());
    do {
        result.push_back(nums);
    } while (std::next_permutation(nums.begin(), nums.end()));
    return result;
}

// ---- Power set ----
// Returns all subsets (2^n), n should be <= 20.

template <typename T>
std::vector<std::vector<T>> subsets(const std::vector<T>& nums) {
    std::size_t n = nums.size();
    std::vector<std::vector<T>> result;
    for (std::size_t mask = 0; mask < (std::size_t{1} << n); ++mask) {
        std::vector<T> subset;
        for (std::size_t i = 0; i < n; ++i) {
            if (mask & (std::size_t{1} << i)) subset.push_back(nums[i]);
        }
        result.push_back(std::move(subset));
    }
    return result;
}

// ---- Combinations C(n, k) ----
// Generate all k-combinations via backtracking.

template <typename T>
void combinations_backtrack(std::size_t start, std::size_t k,
                            std::vector<T>& current,
                            const std::vector<T>& nums,
                            std::vector<std::vector<T>>& result) {
    if (current.size() == k) {
        result.push_back(current);
        return;
    }
    for (std::size_t i = start; i < nums.size(); ++i) {
        current.push_back(nums[i]);
        combinations_backtrack(i + 1, k, current, nums, result);
        current.pop_back();
    }
}

template <typename T>
std::vector<std::vector<T>> combinations(const std::vector<T>& nums,
                                         std::size_t k) {
    std::vector<std::vector<T>> result;
    std::vector<T> current;
    combinations_backtrack(0, k, current, nums, result);
    return result;
}

}  // namespace algo
}  // namespace algorithm_x
