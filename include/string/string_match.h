#pragma once

#include <cstddef>
#include <string>
#include <vector>

namespace algorithm_x {
namespace string {

// KMP (Knuth-Morris-Pratt) single-pattern matching, O(n + m).
// Returns all match start positions (0-indexed).
inline std::vector<std::size_t> kmp_search(const std::string& text,
                                            const std::string& pattern) {
    std::size_t n = text.size(), m = pattern.size();
    if (m == 0) return {};

    // build prefix function (pi array)
    std::vector<std::size_t> pi(m, 0);
    for (std::size_t i = 1, j = 0; i < m; ++i) {
        while (j > 0 && pattern[i] != pattern[j]) j = pi[j - 1];
        if (pattern[i] == pattern[j]) ++j;
        pi[i] = j;
    }

    // search
    std::vector<std::size_t> pos;
    for (std::size_t i = 0, j = 0; i < n; ++i) {
        while (j > 0 && text[i] != pattern[j]) j = pi[j - 1];
        if (text[i] == pattern[j]) ++j;
        if (j == m) {
            pos.push_back(i - m + 1);
            j = pi[j - 1];
        }
    }
    return pos;
}

// Rabin-Karp (rolling hash), O(n + m) expected.
// Returns all match start positions.
inline std::vector<std::size_t> rabin_karp(const std::string& text,
                                            const std::string& pattern) {
    const unsigned long long BASE = 131;
    const unsigned long long MOD = 1000000007ULL;

    std::size_t n = text.size(), m = pattern.size();
    if (m == 0 || m > n) return {};

    // compute BASE^(m-1) % MOD
    unsigned long long pow = 1;
    for (std::size_t i = 0; i < m - 1; ++i) pow = pow * BASE % MOD;

    // pattern hash
    unsigned long long pat_hash = 0;
    for (char c : pattern) pat_hash = (pat_hash * BASE + c) % MOD;

    // first window hash
    unsigned long long win_hash = 0;
    for (std::size_t i = 0; i < m; ++i) {
        win_hash = (win_hash * BASE + text[i]) % MOD;
    }

    std::vector<std::size_t> pos;
    if (win_hash == pat_hash && text.compare(0, m, pattern) == 0) {
        pos.push_back(0);
    }

    for (std::size_t i = m; i < n; ++i) {
        win_hash = (win_hash + MOD - (text[i - m] * pow % MOD)) % MOD;
        win_hash = (win_hash * BASE + text[i]) % MOD;
        if (win_hash == pat_hash &&
            text.compare(i - m + 1, m, pattern) == 0) {
            pos.push_back(i - m + 1);
        }
    }
    return pos;
}

// Z-function, O(n).
// Returns z[i] = length of longest common prefix of s[i:] and s.
inline std::vector<std::size_t> z_function(const std::string& s) {
    std::size_t n = s.size();
    std::vector<std::size_t> z(n, 0);
    std::size_t l = 0, r = 0;
    for (std::size_t i = 1; i < n; ++i) {
        if (i <= r) z[i] = std::min(r - i + 1, z[i - l]);
        while (i + z[i] < n && s[z[i]] == s[i + z[i]]) ++z[i];
        if (i + z[i] - 1 > r) {
            l = i;
            r = i + z[i] - 1;
        }
    }
    return z;
}

}  // namespace string
}  // namespace algorithm_x
