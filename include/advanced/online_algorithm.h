#pragma once

#include <algorithm>
#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace advanced {

// 在线算法与竞争分析
// ==================
// 在线算法：输入是逐步到达的，算法必须在每一步做出不可撤销的决定，
// 无法预知未来。竞争分析把在线算法的代价与"离线最优"（能预知全部输入
// 的最优算法）的代价做比较：若对任意输入都有
//     cost_online ≤ c * cost_offline + d，
// 则称该在线算法是 c-竞争比的（c 越小越接近最优，d 为常数项）。

// 滑雪板租赁问题（ski rental）— 经典在线问题。
// 每天租滑雪板租金 1 元；也可以一次性花 buy_cost 元买下（买后不再付租金）。
// 在线策略（不知道实际一共会滑 days 天）：
//   前 min(days, buy_cost - 1) 天每天租 1 元；
//   若实际天数 days >= buy_cost，则在第 buy_cost 天直接买下。
// 总花费 = min(days, buy_cost - 1) + (days >= buy_cost ? buy_cost : 0)。
//
// 竞争比分析：离线最优（上帝视角）花费 OPT = min(days, buy_cost)
//   - 若 days < buy_cost：在线策略全程租，花费 days = OPT；
//   - 若 days >= buy_cost：在线策略花费 (buy_cost - 1) + buy_cost
//     = 2*buy_cost - 1，而 OPT = buy_cost，故在线花费 < 2 * OPT，
//     即竞争比严格小于 2。
// 事实上 ski rental 的最优确定型在线策略竞争比正是 2。
inline int ski_rental_cost(int buy_cost, int days) {
    if (buy_cost < 1) return std::max(days, 0);  // 买价非法时退化为全租
    if (days <= 0) return 0;
    int rent_days = std::min(days, buy_cost - 1);
    return rent_days + (days >= buy_cost ? buy_cost : 0);
}

// 在线列表查找（move-to-front, MTF 启发式）。
// 维护一个长度为 list_size 的列表（初始为 1..list_size，元素互不相同）。
// 依次处理每个请求元素（假定请求的元素都在列表中）：
//   查找代价 = 该元素在列表中的当前位置 + 1（从 1 开始计数）；
//   找到后把它移到队首（move-to-front）。
// 返回总查找代价。
//
// 竞争比：MTF 是"静态列表查找"问题的 2k-1 竞争比在线算法
// （k 为列表容量；k=2 时竞争比 3 是已知最优）。本实现只演示启发式的
// 行为，不实现竞争比证明。
inline int move_to_front_search(const std::vector<int>& requests, int list_size) {
    std::vector<int> list(
        static_cast<std::size_t>(std::max(list_size, 0)));
    for (int i = 0; i < list_size; ++i) {
        list[static_cast<std::size_t>(i)] = i + 1;
    }
    int total = 0;
    for (int r : requests) {
        std::size_t pos = 0;
        while (pos < list.size() && list[pos] != r) {
            ++pos;
        }
        total += static_cast<int>(pos) + 1;
        if (pos < list.size()) {
            // 把 [0, pos) 整体后移一位，把 r 放到队首。
            for (std::size_t i = pos; i > 0; --i) {
                list[i] = list[i - 1];
            }
            list[0] = r;
        }
    }
    return total;
}

}  // namespace advanced
}  // namespace algorithm_x
