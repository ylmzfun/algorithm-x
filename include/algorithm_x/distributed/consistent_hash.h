#pragma once

#include <cstddef>
#include <functional>
#include <map>
#include <string>

namespace algorithm_x {
namespace distributed {

// 一致性哈希 — 使用虚拟节点打散负载。
class ConsistentHash {
public:
    // nodes: 物理节点名列表。virtual_nodes: 每个物理节点的虚拟节点数。
    ConsistentHash(const std::vector<std::string>& nodes,
                   int virtual_nodes = 150)
        : virtual_nodes_(virtual_nodes) {
        for (const auto& node : nodes) add_node(node);
    }

    // 添加物理节点。
    void add_node(const std::string& node) {
        for (int i = 0; i < virtual_nodes_; ++i) {
            std::string vnode = node + "#" + std::to_string(i);
            std::size_t hash = hasher_(vnode);
            ring_[hash] = node;
        }
    }

    // 移除物理节点。
    void remove_node(const std::string& node) {
        for (int i = 0; i < virtual_nodes_; ++i) {
            std::string vnode = node + "#" + std::to_string(i);
            std::size_t hash = hasher_(vnode);
            ring_.erase(hash);
        }
    }

    // 给定 key，返回负责该 key 的物理节点。
    std::string get_node(const std::string& key) const {
        if (ring_.empty()) return "";
        std::size_t hash = hasher_(key);
        auto it = ring_.lower_bound(hash);
        if (it == ring_.end()) it = ring_.begin();
        return it->second;
    }

    std::size_t node_count() const { return ring_.size(); }

private:
    int virtual_nodes_;
    std::map<std::size_t, std::string> ring_;
    std::hash<std::string> hasher_;
};

}  // namespace distributed
}  // namespace algorithm_x
