#pragma once

#include <cstddef>
#include <cstdint>
#include <vector>

namespace algorithm_x {
namespace math {

// 母函数（生成函数）原理：
// 对"无限供应、单件重量为 w"的一类物品，其数量序列 {a_n}（a_n = 组成总重量 n 的方案数）
// 对应的母函数是几何级数 1 + x^w + x^{2w} + ...，其中第 k 项 x^{kw} 表示取 k 件该物品。
// 多类物品组合时，最终方案数序列 = 各物品母函数逐项相乘（多项式卷积，对应方案数求和）。
// 本函数从常数多项式 1 出发，对每种重量 w 做一次"完全背包式"卷积：
//   ways[s] += ways[s - w]  （s 从小到大递增遍历）
// 等价于把当前多项式乘上 (1 + x^w + x^{2w} + ...) 并截断到 max_sum 次。
// 返回 ways[s] = 用给定物品种类组成总重量 s 的方案数（顺序无关，整数拆分的组合版本）。
inline std::vector<int64_t> generating_function_ways(const std::vector<int>& weights, int max_sum) {
    if (max_sum < 0) {
        return {};
    }
    std::vector<int64_t> ways(static_cast<std::size_t>(max_sum) + 1, 0);
    ways[0] = 1;  // 总重量为 0：空组合，恰好 1 种方案
    for (int w : weights) {
        if (w <= 0) {
            continue;  // 忽略非正重量
        }
        // 乘上 (1 + x^w + x^{2w} + ...)：s 从小到大保证同一种类可重复取（无限供应）
        for (int s = w; s <= max_sum; ++s) {
            ways[static_cast<std::size_t>(s)] += ways[static_cast<std::size_t>(s - w)];
        }
    }
    return ways;
}

}  // namespace math
}  // namespace algorithm_x
