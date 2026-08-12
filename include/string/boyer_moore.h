#pragma once

#include <algorithm>
#include <cstddef>
#include <string>
#include <vector>

namespace algorithm_x {
namespace string {

// Boyer-Moore 字符串匹配（坏字符规则）— 平均 O(n/m)，最坏 O(nm)。
inline std::vector<std::size_t> boyer_moore_search(
    const std::string& text, const std::string& pattern) {
    std::size_t n = text.size(), m = pattern.size();
    if (m == 0 || m > n) return {};

    // 坏字符跳转表（仅 ASCII）
    const int ALPHABET = 256;
    std::vector<int> bad_char(ALPHABET, -1);
    for (int i = 0; i < static_cast<int>(m); ++i) {
        bad_char[static_cast<unsigned char>(pattern[static_cast<std::size_t>(i)])] = i;
    }

    std::vector<std::size_t> result;
    std::size_t shift = 0;
    while (shift <= n - m) {
        int j = static_cast<int>(m) - 1;
        while (j >= 0 && pattern[static_cast<std::size_t>(j)] ==
                              text[shift + static_cast<std::size_t>(j)]) {
            --j;
        }
        if (j < 0) {
            result.push_back(shift);
            shift += (shift + m < n) ? static_cast<std::size_t>(
                         m - bad_char[static_cast<unsigned char>(text[shift + m])]) : 1;
        } else {
            int bc = bad_char[static_cast<unsigned char>(
                text[shift + static_cast<std::size_t>(j)])];
            shift += static_cast<std::size_t>(std::max(1, j - bc));
        }
    }
    return result;
}

}  // namespace string
}  // namespace algorithm_x
