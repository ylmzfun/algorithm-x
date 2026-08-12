#pragma once

#include <algorithm>
#include <cstddef>
#include <limits>
#include <utility>
#include <vector>

namespace algorithm_x {
namespace ds {

// ForwardStar — 链式前向星（静态数组式邻接表）。
// head_[u] 指向 u 的第一条出边（边编号），next_[i] 指向与边 i 同起点的下一条边，
// to_[i] 是边 i 的终点，weight_[i] 是边权。边从 0 开始编号。
// add_edge 采用头插法：新边插入到链表头部，O(1)；
// neighbors(u) 按插入顺序返回 u 的所有出边 {v, w}。
// 相比 vector 邻接表，前向星用紧凑数组存储，缓存局部性更好、常数更小。
class ForwardStar {
public:
    ForwardStar(std::size_t vertices, std::size_t max_edges)
        : head_(vertices, -1) {
        to_.reserve(max_edges);
        next_.reserve(max_edges);
        weight_.reserve(max_edges);
    }

    void add_edge(std::size_t u, std::size_t v, int w = 1) {
        to_.push_back(v);
        weight_.push_back(w);
        next_.push_back(static_cast<std::size_t>(head_[u]));  // head_ 为 -1 时转为 kNil 哨兵
        head_[u] = static_cast<int>(to_.size() - 1);
    }

    // 返回 u 的所有出边 {v, w}，按插入顺序。
    std::vector<std::pair<std::size_t, int>> neighbors(std::size_t u) const {
        if (head_[u] == -1) {
            return {};
        }
        std::vector<std::pair<std::size_t, int>> result;
        std::size_t e = static_cast<std::size_t>(head_[u]);
        while (e != kNil) {
            result.push_back({to_[e], weight_[e]});
            e = next_[e];
        }
        // 头插法使链表中边为逆序存储，反转后还原为插入顺序
        std::reverse(result.begin(), result.end());
        return result;
    }

    std::size_t edge_count() const { return to_.size(); }

private:
    static constexpr std::size_t kNil = std::numeric_limits<std::size_t>::max();

    std::vector<int> head_;          // head_[u]：u 的第一条出边编号，-1 表示无出边
    std::vector<std::size_t> to_;    // to_[i]：边 i 的终点
    std::vector<std::size_t> next_;  // next_[i]：下一条同起点边的编号，kNil 表示链表结束
    std::vector<int> weight_;        // weight_[i]：边 i 的权重
};

}  // namespace ds
}  // namespace algorithm_x
