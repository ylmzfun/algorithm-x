#pragma once

#include <algorithm>
#include <cstddef>
#include <string>
#include <vector>

namespace algorithm_x {
namespace string {

// Levenshtein edit distance, O(n*m) DP.
// Supports insert, delete, replace (unit cost each).
inline int edit_distance(const std::string& a, const std::string& b) {
    std::size_t n = a.size(), m = b.size();
    // space-optimized: only keep previous row
    std::vector<int> prev(m + 1), cur(m + 1);
    for (std::size_t j = 0; j <= m; ++j) prev[j] = static_cast<int>(j);

    for (std::size_t i = 1; i <= n; ++i) {
        cur[0] = static_cast<int>(i);
        for (std::size_t j = 1; j <= m; ++j) {
            if (a[i - 1] == b[j - 1]) {
                cur[j] = prev[j - 1];
            } else {
                cur[j] =
                    1 + std::min({prev[j], cur[j - 1], prev[j - 1]});
            }
        }
        prev.swap(cur);
    }
    return prev[m];
}

// Longest Common Subsequence length, O(n*m).
inline int lcs_length(const std::string& a, const std::string& b) {
    std::size_t n = a.size(), m = b.size();
    std::vector<int> prev(m + 1, 0), cur(m + 1, 0);
    for (std::size_t i = 1; i <= n; ++i) {
        for (std::size_t j = 1; j <= m; ++j) {
            if (a[i - 1] == b[j - 1]) {
                cur[j] = prev[j - 1] + 1;
            } else {
                cur[j] = std::max(prev[j], cur[j - 1]);
            }
        }
        prev.swap(cur);
    }
    return prev[m];
}

// Longest Common Subsequence string recovery, O(n*m).
inline std::string lcs_string(const std::string& a, const std::string& b) {
    std::size_t n = a.size(), m = b.size();
    std::vector<std::vector<int>> dp(n + 1, std::vector<int>(m + 1, 0));
    for (std::size_t i = 1; i <= n; ++i) {
        for (std::size_t j = 1; j <= m; ++j) {
            if (a[i - 1] == b[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = std::max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    std::string result;
    std::size_t i = n, j = m;
    while (i > 0 && j > 0) {
        if (a[i - 1] == b[j - 1]) {
            result.push_back(a[i - 1]);
            --i;
            --j;
        } else if (dp[i - 1][j] > dp[i][j - 1]) {
            --i;
        } else {
            --j;
        }
    }
    std::reverse(result.begin(), result.end());
    return result;
}

}  // namespace string
}  // namespace algorithm_x
