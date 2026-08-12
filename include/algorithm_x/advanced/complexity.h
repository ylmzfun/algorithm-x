#pragma once

#include <algorithm>
#include <cstddef>
#include <limits>
#include <vector>

namespace algorithm_x {
namespace advanced {

// ============================================================
// 计算理论：P / NP / NP 完全 / NP 困难（教学示例）
// ============================================================
//
// 以判定问题（答案为是/否的问题）为例给出严格定义：
//   - P：存在多项式时间（O(n^k)）判定算法的问题类。
//   - NP：存在多项式时间"验证器"的问题类。所谓验证器，是指给定问题实例
//     外加一个候选解（证书），能在多项式时间内判断该候选解是否合法。
//     显然 P ⊆ NP：P 里的问题直接跑判定算法即可当验证器用。
//   - 归约（reduction）：若存在多项式时间的变换 f，使得对任意实例 x 都有
//     "x 属于问题 A" 当且仅当 "f(x) 属于问题 B"，则称 A 多项式归约到 B
//     （A ≤p B）。它意味着 B 的求解器可以拿来求解 A，即 B 至少和 A 一样难。
//   - NP 完全（NP-complete）：属于 NP，并且所有 NP 问题都能多项式归约到它。
//     它们是 NP 中最难的一批问题；只要任何一个 NP 完全问题有多项式算法，
//     就得到 P = NP。
//   - NP 困难（NP-hard）：所有 NP 问题都能多项式归约到它，但它本身不要求
//     属于 NP（可以是优化问题、非判定问题等）。NP 完全 ⊆ NP 困难。
//
// 关系：P ⊆ NP，NP 完全 = NP 中最难者，NP 困难 ⊇ NP 完全。
// 目前 P 是否等于 NP 仍是计算机科学最重要的未解问题。
//
// 注意：本头文件只给出"教学示例"，用直观的小代码感受这几类问题的形状
// （NP 判定问题、NP 验证器、NP 困难优化问题），不提供严格的复杂度证明
// （严格证明需要构造多项式归约，超出本仓库范围）。
// ============================================================

// 子集和问题（NP 判定问题）— 2^n 指数级暴力枚举所有子集。
// 问能否从 nums 中选出若干个数，使它们的和恰好等于 target。
// 时间复杂度 O(2^n)，仅适合小数据（n ≤ 20 左右）。
inline bool subset_sum_brute(const std::vector<int>& nums, int target) {
    std::size_t n = nums.size();
    if (n >= 64) return false;  // 防御：超出可枚举范围（教学代码）
    for (std::size_t mask = 0; mask < (std::size_t{1} << n); ++mask) {
        long long sum = 0;
        for (std::size_t i = 0; i < n; ++i) {
            if ((mask & (std::size_t{1} << i)) != 0) {
                sum += nums[i];
            }
        }
        if (sum == target) return true;
    }
    return false;
}

// 子集和问题的多项式时间"验证器"（NP 定义的核心：给定候选解 indices，
// O(|indices|) 时间验证其合法性）：
//   1) 所有下标都合法（0 ≤ idx < nums.size()）；
//   2) 下标不重复；
//   3) 这些元素的和恰好等于 target。
inline bool subset_sum_verify(const std::vector<int>& nums, int target,
                              const std::vector<int>& indices) {
    std::vector<bool> used(nums.size(), false);
    long long sum = 0;
    for (int idx : indices) {
        if (idx < 0 || static_cast<std::size_t>(idx) >= nums.size()) {
            return false;  // 下标越界
        }
        std::size_t u = static_cast<std::size_t>(idx);
        if (used[u]) {
            return false;  // 下标重复
        }
        used[u] = true;
        sum += nums[u];
    }
    return sum == target;
}

// 旅行商问题（TSP）— NP 困难优化问题，O(n!) 暴力枚举。
// 固定从城市 0 出发，枚举其余 n-1 个城市的全排列并回到 0，
// 取总路程最小者。dist[i][j] 为城市 i 到城市 j 的距离。
// n 很小（≤ 8）时可用。
inline int tsp_brute_force(const std::vector<std::vector<int>>& dist) {
    std::size_t n = dist.size();
    if (n <= 1) return 0;
    std::vector<int> order;
    order.reserve(n - 1);
    for (std::size_t i = 1; i < n; ++i) {
        order.push_back(static_cast<int>(i));
    }
    int best = std::numeric_limits<int>::max();
    do {
        int cost = 0;
        int cur = 0;
        for (int next : order) {
            cost += dist[static_cast<std::size_t>(cur)]
                        [static_cast<std::size_t>(next)];
            cur = next;
        }
        cost += dist[static_cast<std::size_t>(cur)][0];  // 回到起点
        if (cost < best) best = cost;
    } while (std::next_permutation(order.begin(), order.end()));
    return best;
}

}  // namespace advanced
}  // namespace algorithm_x
