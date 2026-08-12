#pragma once

#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace advanced {

// 摊还分析 — 动态数组扩容的每步开销。
// n 次 push_back 的总开销为 O(n)，均摊 O(1)。
inline std::vector<double> amortized_push_cost(std::size_t n) {
    std::vector<double> cost(n, 0.0);
    std::size_t capacity = 1;
    std::size_t size = 0;

    for (std::size_t i = 0; i < n; ++i) {
        if (size == capacity) {
            // 扩容：复制所有已有元素
            cost[i] = static_cast<double>(size) + 1.0;  // 复制 + 插入
            capacity *= 2;
        } else {
            cost[i] = 1.0;  // 仅插入
        }
        ++size;
    }
    return cost;
}

// 计算均摊代价：总代价 / n。
inline double amortized_average(std::size_t n) {
    auto costs = amortized_push_cost(n);
    double total = 0;
    for (double c : costs) total += c;
    return n > 0 ? total / static_cast<double>(n) : 0.0;
}

}  // namespace advanced
}  // namespace algorithm_x
