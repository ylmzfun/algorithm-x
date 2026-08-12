#pragma once

#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <vector>

namespace algorithm_x {
namespace dp {

namespace {

// 坐标压缩：返回 values 去重、升序排序后的值域，原值按 1..m 排名映射。
inline std::vector<int> sorted_unique_values(const std::vector<int>& values) {
    std::vector<int> sorted = values;
    std::sort(sorted.begin(), sorted.end());
    sorted.erase(std::unique(sorted.begin(), sorted.end()), sorted.end());
    return sorted;
}

// 树状数组的聚合节点：记录"以某个值为结尾的最长 LIS 长度 + 该长度的方案数"。
struct LenCount {
    int64_t len;
    int64_t count;
};

// 合并两个节点：长度取较大者；长度相同时方案数相加。
inline LenCount len_count_merge(const LenCount& a, const LenCount& b) {
    if (a.len > b.len) {
        return a;
    }
    if (b.len > a.len) {
        return b;
    }
    return {a.len, a.count + b.count};
}

}  // namespace

// 线段树 / 树状数组优化 DP 的思想：
// 形如 dp[i] = f(weights[i], max{dp[j] | j < i 且 values[j] < values[i]}) 的转移，
// 朴素枚举所有 j 是 O(n^2)。把已算出的 dp 按下标值域组织进树状数组（Fenwick）：
//   - 前缀查询 [1, rank-1] 的最优值：O(log n) 汇总所有"已处理且值更小"的状态；
//   - 单点更新 rank 处的最优值：O(log n)；
//   - 按输入顺序逐个处理天然满足 j < i；
//   - 只查询严格更小的值域 [1, rank-1] 保证严格递增（< 而非 <=）。
// 值域需先做坐标压缩，把实际值映射到连续排名 1..m。
//
// 最大和递增子序列（严格递增）— O(n log n)。
// dp[i] = weights[i] + max{dp[j] | j < i 且 values[j] < values[i]}。
inline int64_t max_sum_increasing_subsequence(const std::vector<int>& values, const std::vector<int>& weights) {
    if (values.empty()) {
        return 0;
    }
    const std::vector<int> ranks = sorted_unique_values(values);
    const int m = static_cast<int>(ranks.size());

    // 树状数组：tree[i] 维护一段值域上的最大 dp 和
    std::vector<int64_t> tree(static_cast<std::size_t>(m) + 1, 0);

    auto query_max = [&tree](int idx) {
        int64_t res = 0;
        for (int i = idx; i > 0; i -= i & -i) {
            if (tree[static_cast<std::size_t>(i)] > res) {
                res = tree[static_cast<std::size_t>(i)];
            }
        }
        return res;
    };

    auto update_max = [&tree, m](int idx, int64_t val) {
        for (int i = idx; i <= m; i += i & -i) {
            if (val > tree[static_cast<std::size_t>(i)]) {
                tree[static_cast<std::size_t>(i)] = val;
            }
        }
    };

    int64_t answer = 0;
    for (std::size_t i = 0; i < values.size(); ++i) {
        // 当前值的排名（1 基）
        const int rank = static_cast<int>(
            std::lower_bound(ranks.begin(), ranks.end(), values[i]) - ranks.begin()) + 1;
        // 查询严格更小值域 [1, rank-1] 上的最大 dp
        const int64_t best = query_max(rank - 1);
        const int64_t cur = static_cast<int64_t>(weights[i]) + best;
        if (cur > answer) {
            answer = cur;
        }
        // 把当前 dp 值并入 rank 处
        update_max(rank, cur);
    }
    return answer;
}

// 最长递增子序列的方案数 — O(n log n)。
// 树状数组每个节点聚合一段值域上的 (最长长度, 方案数)：
// 处理每个元素 v 时，先查询前缀 [1, rank-1]（严格更小的值）得到最优 (len, count)，
// 则"以 v 结尾"的最长 LIS 信息为 (len+1, count)；若 len == 0 说明 v 只能作为
// 长度为 1 的新 LIS 起点，方案数为 1。再按 rank 单点并入树状数组（长度相同时累加计数）。
// 处理完所有元素后，整个值域的聚合即为全局最长 LIS 及其方案数。
inline int64_t lis_count(const std::vector<int>& values) {
    if (values.empty()) {
        return 0;
    }
    const std::vector<int> ranks = sorted_unique_values(values);
    const int m = static_cast<int>(ranks.size());

    // 树状数组：tree[i] 聚合一段值域上的 (最长长度, 方案数)
    const LenCount init{0, 0};
    std::vector<LenCount> tree(static_cast<std::size_t>(m) + 1, init);

    auto merge_into = [](LenCount& dst, const LenCount& src) {
        dst = len_count_merge(dst, src);
    };

    auto query = [&tree, &merge_into](int idx) {
        LenCount best{0, 0};
        for (int i = idx; i > 0; i -= i & -i) {
            merge_into(best, tree[static_cast<std::size_t>(i)]);
        }
        return best;
    };

    auto update = [&tree, m, &merge_into](int idx, const LenCount& val) {
        for (int i = idx; i <= m; i += i & -i) {
            merge_into(tree[static_cast<std::size_t>(i)], val);
        }
    };

    for (int v : values) {
        const int rank = static_cast<int>(
            std::lower_bound(ranks.begin(), ranks.end(), v) - ranks.begin()) + 1;
        const LenCount best = query(rank - 1);
        const LenCount cur{best.len + 1, best.len == 0 ? 1 : best.count};
        update(rank, cur);
    }

    // 整个值域上的聚合：全局最长 LIS 的长度与方案数
    return query(m).count;
}

}  // namespace dp
}  // namespace algorithm_x
