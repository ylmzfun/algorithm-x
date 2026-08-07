#pragma once

#include <cstdint>
#include <vector>

namespace algorithm_x {
namespace math {

// Stirling numbers of the first kind (unsigned): s(n,k) = number of
// permutations of n elements with exactly k cycles.
// Recurrence: s(n,k) = s(n-1,k-1) + (n-1)*s(n-1,k)
inline int64_t stirling_first(int n, int k) {
    if (k > n || k < 0) return 0;
    if (n == 0) return k == 0 ? 1 : 0;
    if (k == 0) return 0;

    std::vector<std::vector<int64_t>> dp(
        static_cast<std::size_t>(n) + 1,
        std::vector<int64_t>(static_cast<std::size_t>(k) + 1, 0));
    dp[0][0] = 1;
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= k; ++j) {
            dp[static_cast<std::size_t>(i)][static_cast<std::size_t>(j)] =
                dp[static_cast<std::size_t>(i - 1)]
                  [static_cast<std::size_t>(j - 1)] +
                static_cast<int64_t>(i - 1) *
                    dp[static_cast<std::size_t>(i - 1)]
                      [static_cast<std::size_t>(j)];
        }
    }
    return dp[static_cast<std::size_t>(n)][static_cast<std::size_t>(k)];
}

// Stirling numbers of the second kind: S(n,k) = number of ways to partition
// a set of n elements into k non-empty subsets.
// Recurrence: S(n,k) = S(n-1,k-1) + k*S(n-1,k)
inline int64_t stirling_second(int n, int k) {
    if (k > n || k < 0) return 0;
    if (n == 0) return k == 0 ? 1 : 0;
    if (k == 0) return 0;

    std::vector<std::vector<int64_t>> dp(
        static_cast<std::size_t>(n) + 1,
        std::vector<int64_t>(static_cast<std::size_t>(k) + 1, 0));
    dp[0][0] = 1;
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= k; ++j) {
            dp[static_cast<std::size_t>(i)][static_cast<std::size_t>(j)] =
                dp[static_cast<std::size_t>(i - 1)]
                  [static_cast<std::size_t>(j - 1)] +
                static_cast<int64_t>(j) *
                    dp[static_cast<std::size_t>(i - 1)]
                      [static_cast<std::size_t>(j)];
        }
    }
    return dp[static_cast<std::size_t>(n)][static_cast<std::size_t>(k)];
}

// Bell number B(n): total number of ways to partition a set of n elements.
inline int64_t bell_number(int n) {
    if (n < 0) return 0;
    if (n <= 1) return 1;

    std::vector<int64_t> bell(static_cast<std::size_t>(n) + 1, 0);
    bell[0] = 1;
    for (int i = 1; i <= n; ++i) {
        int64_t sum = 0;
        for (int k = 0; k < i; ++k) {
            // Using Stirling numbers of the second kind
            sum += stirling_second(i, k + 1);
        }
        bell[static_cast<std::size_t>(i)] = sum;
    }
    return bell[static_cast<std::size_t>(n)];
}

}  // namespace math
}  // namespace algorithm_x
