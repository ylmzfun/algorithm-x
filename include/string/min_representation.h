#pragma once

#include <algorithm>
#include <cstddef>
#include <string>

namespace algorithm_x {
namespace string {

// Booth's algorithm — find lexicographically smallest rotation O(n).
inline std::string min_representation(const std::string& s) {
    if (s.empty()) return "";
    std::size_t n = s.size();
    std::size_t i = 0, j = 1, k = 0;
    while (i < n && j < n && k < n) {
        char a = s[(i + k) % n];
        char b = s[(j + k) % n];
        if (a == b) {
            ++k;
        } else {
            if (a > b) i += k + 1;
            else       j += k + 1;
            if (i == j) ++j;
            k = 0;
        }
    }
    std::size_t start = std::min(i, j);
    return s.substr(start) + s.substr(0, start);
}

}  // namespace string
}  // namespace algorithm_x
