#pragma once

#include <algorithm>
#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace distributed {

// 向量时钟 — 用于分布式系统中事件的因果排序。
class VectorClock {
public:
    explicit VectorClock(std::size_t num_nodes) : clock_(num_nodes, 0) {}

    // 本节点发生事件，递增自己的时钟。
    void increment(std::size_t node_id) { ++clock_[node_id]; }

    // 合并另一个向量时钟（取每维最大值）。
    void merge(const VectorClock& other) {
        for (std::size_t i = 0; i < clock_.size(); ++i) {
            clock_[i] = std::max(clock_[i], other.clock_[i]);
        }
    }

    // 检查与 other 是否并发（既不在对方之前也不在之后）。
    bool is_concurrent(const VectorClock& other) const {
        bool less = false, greater = false;
        for (std::size_t i = 0; i < clock_.size(); ++i) {
            if (clock_[i] < other.clock_[i]) less = true;
            if (clock_[i] > other.clock_[i]) greater = true;
        }
        return less && greater;
    }

    // 检查当前时钟是否发生在 other 之前。
    bool happens_before(const VectorClock& other) const {
        bool strict = false;
        for (std::size_t i = 0; i < clock_.size(); ++i) {
            if (clock_[i] > other.clock_[i]) return false;
            if (clock_[i] < other.clock_[i]) strict = true;
        }
        return strict;
    }

    const std::vector<int>& clock() const { return clock_; }
    std::size_t size() const { return clock_.size(); }

private:
    std::vector<int> clock_;
};

}  // namespace distributed
}  // namespace algorithm_x
