#pragma once

#include <algorithm>
#include <cstddef>
#include <queue>
#include <utility>
#include <vector>

namespace algorithm_x {
namespace algo {

// branch_and_bound_knapsack — 0-1 背包问题的分支限界算法。
// 分支限界思想：把解空间组织成搜索树（每件物品做"取/不取"的二分分支），
// 用优先队列按上界 bound 降序扩展节点；节点的 bound 是"剩余物品按价值密度
// 排序后的分数背包"给出的上界（即松弛问题的最优值）。
// 当某节点的上界不超过当前已知最优解 best 时，该子树不可能更优，直接剪枝。
// 正确性：分数背包上界是合法上界，剪枝只丢弃不可能超过 best 的子树，
// 因此返回结果与朴素 DP 完全一致。
inline int branch_and_bound_knapsack(const std::vector<int>& weights,
                                     const std::vector<int>& values,
                                     int capacity) {
    const std::size_t n = weights.size();
    if (n == 0) {
        return 0;
    }

    // 物品按价值密度降序排列（权重为 0 的物品密度视为无穷大，排在最前）
    std::vector<std::pair<int, int>> items;  // {weight, value}
    items.reserve(n);
    for (std::size_t i = 0; i < n; ++i) {
        items.push_back({weights[i], values[i]});
    }
    std::sort(items.begin(), items.end(),
              [](const std::pair<int, int>& a, const std::pair<int, int>& b) {
                  if (a.first == 0) {
                      return b.first != 0;  // 零重物品密度无穷，排前
                  }
                  if (b.first == 0) {
                      return false;
                  }
                  return static_cast<double>(a.second) / a.first >
                         static_cast<double>(b.second) / b.first;
              });

    // 分数背包上界：从 level 号物品开始，用剩余容量 cap 尽量装满，最后一件可拆分
    const auto fractional_bound = [&items](int level, int profit, int cap) -> double {
        double ub = static_cast<double>(profit);
        for (std::size_t i = static_cast<std::size_t>(level); i < items.size(); ++i) {
            const int w = items[i].first;
            const int v = items[i].second;
            if (w == 0) {
                ub += static_cast<double>(v);  // 零重物品免费装入
            } else if (w <= cap) {
                ub += static_cast<double>(v);
                cap -= w;
            } else {
                ub += static_cast<double>(v) * static_cast<double>(cap) / static_cast<double>(w);
                break;
            }
        }
        return ub;
    };

    struct Node {
        int level;    // 下一个待决策的物品下标
        int profit;   // 已取物品的总价值
        int weight;   // 已取物品的总重量
        double bound; // 子树价值上界
        bool operator<(const Node& other) const {
            return bound < other.bound;  // priority_queue 是大顶堆，bound 最大者先出队
        }
    };

    std::priority_queue<Node> pq;
    pq.push({0, 0, 0, fractional_bound(0, 0, capacity)});

    int best = 0;
    while (!pq.empty()) {
        const Node cur = pq.top();
        pq.pop();
        if (cur.bound <= static_cast<double>(best)) {
            continue;  // 上界不超过已知最优，整棵子树剪枝
        }
        if (cur.level >= static_cast<int>(items.size())) {
            continue;
        }
        const int w = items[static_cast<std::size_t>(cur.level)].first;
        const int v = items[static_cast<std::size_t>(cur.level)].second;

        // 分支 1：取当前物品
        if (cur.weight + w <= capacity) {
            const int new_profit = cur.profit + v;
            if (new_profit > best) {
                best = new_profit;
            }
            if (cur.level + 1 < static_cast<int>(items.size())) {
                const double nb = fractional_bound(cur.level + 1, new_profit,
                                                   capacity - cur.weight - w);
                if (nb > static_cast<double>(best)) {
                    pq.push({cur.level + 1, new_profit, cur.weight + w, nb});
                }
            }
        }

        // 分支 2：不取当前物品
        if (cur.level + 1 < static_cast<int>(items.size())) {
            const double nb = fractional_bound(cur.level + 1, cur.profit,
                                               capacity - cur.weight);
            if (nb > static_cast<double>(best)) {
                pq.push({cur.level + 1, cur.profit, cur.weight, nb});
            }
        }
    }
    return best;
}

}  // namespace algo
}  // namespace algorithm_x
