#pragma once

#include <algorithm>
#include <cstddef>
#include <string>
#include <vector>

namespace algorithm_x {
namespace string {

// Manacher's algorithm for longest palindromic substring, O(n).
// Handles both odd and even length palindromes via '#' padding.
inline std::string longest_palindrome(const std::string& s) {
    if (s.empty()) return {};

    // transform: "abc" → "^#a#b#c#$"
    std::string t = "^#";
    for (char c : s) {
        t += c;
        t += '#';
    }
    t += '$';

    std::size_t n = t.size();
    std::vector<std::size_t> p(n, 0);
    std::size_t center = 0, right = 0;
    std::size_t max_len = 0, max_center = 0;

    for (std::size_t i = 1; i < n - 1; ++i) {
        if (i < right) p[i] = std::min(right - i, p[2 * center - i]);
        while (t[i + p[i] + 1] == t[i - p[i] - 1]) ++p[i];
        if (i + p[i] > right) {
            center = i;
            right = i + p[i];
        }
        if (p[i] > max_len) {
            max_len = p[i];
            max_center = i;
        }
    }

    std::size_t start = (max_center - max_len) / 2;
    return s.substr(start, max_len);
}

}  // namespace string
}  // namespace algorithm_x
