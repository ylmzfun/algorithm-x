#pragma once

#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <map>
#include <set>
#include <string>
#include <vector>

namespace algorithm_x {
namespace distributed {

// G-Counter（Grow-only Counter）：只增计数器 CRDT。
//
// 每个副本维护各副本的本地计数；value() 为所有副本计数之和。
// merge 逐副本取最大值——由于计数只增，合并结果单调不减，
// 合并运算满足交换律、结合律与幂等性，因此任意并发更新后，
// 各副本通过交换合并即可收敛到一致状态（最终一致性）。
class GCounter {
public:
    explicit GCounter(std::size_t replicas) : counts_(replicas, 0) {}

    // 副本 replica 的本地计数增加 delta（默认 1）。replica 须小于构造时的数量。
    void increment(std::size_t replica, int64_t delta = 1) {
        counts_[replica] += delta;
    }

    // 总计数：所有副本本地计数之和。
    int64_t value() const {
        int64_t total = 0;
        for (int64_t count : counts_) {
            total += count;
        }
        return total;
    }

    // 合并：逐副本取最大值（只增语义保证单调收敛）。
    void merge(const GCounter& other) {
        for (std::size_t i = 0; i < counts_.size(); ++i) {
            counts_[i] = std::max(counts_[i], other.counts_[i]);
        }
    }

    // 副本 replica 的本地计数。
    int64_t local(std::size_t replica) const { return counts_[replica]; }

private:
    std::vector<int64_t> counts_;
};

// ORSet（Observed-Remove Set）：观察移除集合 CRDT。
//
// 设计：
//   - 每个副本维护 adds_（元素 → 其 add 标签集合）与 rems_（元素 → 已删除标签集合）；
//   - 元素存在 ⇔ 存在未被删除的 add 标签：
//     contains(elem) = ∃ tag ∈ adds_[elem] 且 tag ∉ rems_[elem]；
//   - add：为元素生成一个全局唯一的标签并记入 adds_；
//   - remove：把本副本已知的 add 标签全部标记进 rems_（"只标记删除"）；
//     若本副本从未见过该元素的任何 add 标签，则无法指定具体标签，
//     此时记录元素级墓碑（哨兵标签 0）——合并后该元素不再存在；
//   - merge：adds_ 与 rems_ 均取并集，并保留各副本最大的标签计数。
//
// 标签唯一性：每个副本实例在构造时自动获得全局唯一的 replica_id，
// 标签编码为 (replica_id << 20) | seq，其中 seq 是本副本自己的计数（从 1 起），
// 合并时保留最大 seq（"合并时保留最大计数"），保证不同副本的标签永不冲突。
//
// 语义验证：
//   - A 添加 x，B 删除 x，merge 后 x 不存在：B 从未见过 x 的 add 标签，
//     只能记录元素级墓碑，墓碑使 x 的任何 add 都不再存活；
//   - A 添加 x、B 也添加 x，A 删除自己的 x 后 merge，x 仍存在：
//     A 只标记自己 add 的标签为已删除，B 的 add 标签仍然存活。
//
// 教学简化：元素级墓碑不会过期（墓碑存在时重新 add 也不会复活该元素，
// 经典 ORSet 中重新 add 使用新标签即可复活）；未模拟节点故障与网络乱序。
class ORSet {
public:
    ORSet() : replica_id_(next_replica_id()), seq_(0) {}

    // 显式指定副本编号（用于构造确定性的副本）；编号相同会导致标签冲突，勿重复使用。
    explicit ORSet(std::size_t replica_id) : replica_id_(replica_id), seq_(0) {}

    // 添加元素：生成一个全局唯一标签并记入 adds_。
    void add(const std::string& elem) {
        adds_[elem].insert(new_tag());
    }

    // 删除元素：
    //   - 本副本知道该元素的 add 标签：全部标记进 rems_（只标记删除）；
    //   - 本副本从未见过该元素：记录元素级墓碑（哨兵 0）。
    void remove(const std::string& elem) {
        auto it = adds_.find(elem);
        if (it == adds_.end() || it->second.empty()) {
            rems_[elem].insert(kTombstone);
            return;
        }
        for (int64_t tag : it->second) {
            rems_[elem].insert(tag);
        }
    }

    // 元素存在 ⇔ 存在未被删除的 add 标签。
    bool contains(const std::string& elem) const {
        auto add_it = adds_.find(elem);
        if (add_it == adds_.end() || add_it->second.empty()) return false;
        auto rem_it = rems_.find(elem);
        // 元素级墓碑：一旦被"元素级"删除，任何 add 都不再存活。
        if (rem_it != rems_.end() && rem_it->second.count(kTombstone) > 0) {
            return false;
        }
        for (int64_t tag : add_it->second) {
            if (rem_it == rems_.end() || rem_it->second.count(tag) == 0) {
                return true;  // 找到存活的 add 标签
            }
        }
        return false;
    }

    // 返回所有存在的元素（按字典序）。
    std::vector<std::string> elements() const {
        std::vector<std::string> result;
        for (const auto& kv : adds_) {
            if (contains(kv.first)) {
                result.push_back(kv.first);
            }
        }
        return result;
    }

    // 合并：adds_ 与 rems_ 取并集，并保留最大的标签计数（保证新标签不冲突）。
    void merge(const ORSet& other) {
        for (const auto& kv : other.adds_) {
            adds_[kv.first].insert(kv.second.begin(), kv.second.end());
        }
        for (const auto& kv : other.rems_) {
            rems_[kv.first].insert(kv.second.begin(), kv.second.end());
        }
        seq_ = std::max(seq_, other.seq_);
    }

private:
    // 元素级墓碑哨兵（正常标签从 1 起，永不等于 0）。
    static constexpr int64_t kTombstone = 0;
    // 每个副本标签计数占用的位数。
    static constexpr int kTagBits = 20;

    // 全局分配唯一的副本编号（单线程测试下按构造顺序确定）。
    static std::size_t next_replica_id() {
        static std::size_t id = 0;
        return id++;
    }

    // 生成全局唯一标签：(replica_id << 20) | 本副本自增计数。
    int64_t new_tag() {
        ++seq_;
        return (static_cast<int64_t>(replica_id_) << kTagBits) |
               static_cast<int64_t>(seq_);
    }

    std::size_t replica_id_;
    int64_t seq_ = 0;
    std::map<std::string, std::set<int64_t>> adds_;
    std::map<std::string, std::set<int64_t>> rems_;
};

}  // namespace distributed
}  // namespace algorithm_x
