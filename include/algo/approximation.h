#pragma once

#include <cstddef>
#include <utility>
#include <vector>

namespace algorithm_x {
namespace algo {

// greedy_set_cover — 集合覆盖问题的贪心近似算法。
// 每轮选择能覆盖最多"当前未覆盖元素"的集合加入答案，直到无法再覆盖新元素。
// 近似比：设全集大小为 n，贪心解至多是最优解的 ln(n) + 1 倍。
// 若某些元素不被任何集合覆盖，贪心照常进行，最终结果可能覆盖不了全集，
// 是否可接受由调用方自行判断。
inline std::vector<std::size_t> greedy_set_cover(
    const std::vector<std::vector<std::size_t>>& sets, std::size_t universe_size) {
    std::vector<bool> covered(universe_size, false);
    std::vector<bool> used(sets.size(), false);
    std::vector<std::size_t> chosen;
    std::size_t remaining = universe_size;  // 尚未覆盖的元素个数
    while (remaining > 0) {
        std::size_t best_set = 0;
        std::size_t best_gain = 0;
        bool found = false;
        for (std::size_t s = 0; s < sets.size(); ++s) {
            if (used[s]) {
                continue;
            }
            std::size_t gain = 0;
            for (const std::size_t e : sets[s]) {
                if (e < universe_size && !covered[e]) {
                    ++gain;
                }
            }
            if (gain > best_gain) {  // 严格大于：平局时保留下标更小的集合
                best_gain = gain;
                best_set = s;
                found = true;
            }
        }
        if (!found || best_gain == 0) {
            break;  // 没有集合能再覆盖新元素
        }
        used[best_set] = true;
        chosen.push_back(best_set);
        for (const std::size_t e : sets[best_set]) {
            if (e < universe_size && !covered[e]) {
                covered[e] = true;
                --remaining;
            }
        }
    }
    return chosen;
}

// vertex_cover_approx — 顶点覆盖问题的最大匹配贪心 2-近似。
// 每轮任取一条尚未被覆盖的边，把它的两个端点都加入覆盖，
// 并删除所有与这两个端点关联的边，重复直到所有边都被删除。
// 被选中的边两两不相邻，构成一个极大匹配 M，覆盖大小 = 2|M|；
// 而任何顶点覆盖都必须为 M 中每条边选至少一个端点，故 OPT >= |M|，
// 于是 2|M| <= 2 * OPT，即近似比为 2。返回覆盖大小。
inline int vertex_cover_approx(const std::vector<std::pair<int, int>>& edges,
                               int num_vertices) {
    std::vector<char> removed(edges.size(), 0);   // 边是否已被删除（被覆盖）
    std::vector<char> in_cover(num_vertices, 0);  // 顶点是否已在覆盖中
    int cover_size = 0;
    for (std::size_t i = 0; i < edges.size(); ++i) {
        if (removed[i]) {
            continue;
        }
        const int u = edges[i].first;
        const int v = edges[i].second;
        if (!in_cover[u]) {
            in_cover[u] = 1;
            ++cover_size;
        }
        if (!in_cover[v]) {
            in_cover[v] = 1;
            ++cover_size;
        }
        // 删除所有与 u 或 v 关联的边
        for (std::size_t j = 0; j < edges.size(); ++j) {
            if (removed[j]) {
                continue;
            }
            const int a = edges[j].first;
            const int b = edges[j].second;
            if (a == u || b == u || a == v || b == v) {
                removed[j] = 1;
            }
        }
    }
    return cover_size;
}

}  // namespace algo
}  // namespace algorithm_x
