#pragma once

#include <algorithm>
#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace algo {

// ---- Two pointers ----

// Two-sum on sorted array.
// Returns indices {i, j} such that arr[i] + arr[j] == target, or {-1, -1}.
template <typename T>
std::pair<long, long> two_sum_sorted(const std::vector<T>& arr,
                                      const T& target) {
    long i = 0;
    long j = static_cast<long>(arr.size()) - 1;
    while (i < j) {
        T sum = arr[static_cast<std::size_t>(i)]
              + arr[static_cast<std::size_t>(j)];
        if (sum == target) return {i, j};
        if (sum < target) ++i;
        else              --j;
    }
    return {-1, -1};
}

// Remove duplicates in-place from a sorted array.
// Returns new length of deduplicated prefix.
template <typename T>
std::size_t remove_duplicates(std::vector<T>& arr) {
    if (arr.empty()) return 0;
    std::size_t k = 0;
    for (std::size_t i = 1; i < arr.size(); ++i) {
        if (arr[i] != arr[k]) arr[++k] = arr[i];
    }
    return k + 1;
}

// ---- Sliding window ----

// Maximum sum of any contiguous subarray of length k.
template <typename T>
T max_sum_fixed_window(const std::vector<T>& arr, std::size_t k) {
    if (arr.size() < k) return {};
    T sum = {};
    for (std::size_t i = 0; i < k; ++i) sum += arr[i];
    T best = sum;
    for (std::size_t i = k; i < arr.size(); ++i) {
        sum += arr[i] - arr[i - k];
        if (sum > best) best = sum;
    }
    return best;
}

// Minimum length of contiguous subarray with sum >= target.
// Returns 0 if no such subarray exists.
template <typename T>
std::size_t min_subarray_len(const std::vector<T>& arr, const T& target) {
    std::size_t n = arr.size();
    std::size_t best = n + 1;
    std::size_t left = 0;
    T sum = {};
    for (std::size_t right = 0; right < n; ++right) {
        sum += arr[right];
        while (sum >= target) {
            best = std::min(best, right - left + 1);
            sum -= arr[left++];
        }
    }
    return best > n ? 0 : best;
}

// ---- Prefix sum ----

// 1D prefix sum. query(l, r) returns sum(arr[l]..arr[r-1]), half-open.
template <typename T>
class PrefixSum {
public:
    explicit PrefixSum(const std::vector<T>& arr) : pre_(arr.size() + 1) {
        for (std::size_t i = 0; i < arr.size(); ++i) {
            pre_[i + 1] = pre_[i] + arr[i];
        }
    }

    T query(std::size_t l, std::size_t r) const {
        return pre_[r] - pre_[l];
    }

private:
    std::vector<T> pre_;
};

// 2D prefix sum. query returns sum of submatrix [r1..r2) x [c1..c2).
template <typename T>
class PrefixSum2D {
public:
    explicit PrefixSum2D(const std::vector<std::vector<T>>& mat) {
        std::size_t rows = mat.size();
        std::size_t cols = mat[0].size();
        pre_.assign(rows + 1, std::vector<T>(cols + 1, {}));
        for (std::size_t i = 0; i < rows; ++i) {
            for (std::size_t j = 0; j < cols; ++j) {
                pre_[i + 1][j + 1] = mat[i][j]
                                   + pre_[i][j + 1]
                                   + pre_[i + 1][j]
                                   - pre_[i][j];
            }
        }
    }

    T query(std::size_t r1, std::size_t c1,
            std::size_t r2, std::size_t c2) const {
        return pre_[r2][c2] - pre_[r1][c2]
             - pre_[r2][c1] + pre_[r1][c1];
    }

private:
    std::vector<std::vector<T>> pre_;
};

// Difference array — O(1) range add, O(n) restore.
template <typename T>
class DifferenceArray {
public:
    explicit DifferenceArray(const std::vector<T>& arr)
        : diff_(arr.size() + 1, {}) {
        diff_[0] = arr[0];
        for (std::size_t i = 1; i < arr.size(); ++i) {
            diff_[i] = arr[i] - arr[i - 1];
        }
    }

    // Add val to every element in [l, r].
    void add(std::size_t l, std::size_t r, const T& val) {
        diff_[l] += val;
        diff_[r + 1] -= val;
    }

    // Reconstruct the array from the difference array.
    std::vector<T> restore() const {
        std::vector<T> res(diff_.size() - 1);
        res[0] = diff_[0];
        for (std::size_t i = 1; i < res.size(); ++i) {
            res[i] = res[i - 1] + diff_[i];
        }
        return res;
    }

private:
    std::vector<T> diff_;
};

}  // namespace algo
}  // namespace algorithm_x
