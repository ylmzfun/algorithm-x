#pragma once

#include <algorithm>
#include <cstddef>
#include <random>
#include <vector>

namespace algorithm_x {
namespace distributed {

// Gossip 协议仿真：每轮每个节点向 k 个随机节点散播消息。
// 返回所有节点收到消息所需的轮数。
inline int gossip_protocol(int nodes, int k = 2) {
    std::vector<bool> informed(static_cast<std::size_t>(nodes), false);
    informed[0] = true;  // 初始节点 0 知道消息
    int informed_count = 1;

    std::mt19937 gen(42);
    std::uniform_int_distribution<int> dis(0, nodes - 1);

    int rounds = 0;
    while (informed_count < nodes) {
        std::vector<std::size_t> new_informed;
        for (int i = 0; i < nodes; ++i) {
            if (!informed[static_cast<std::size_t>(i)]) continue;
            for (int j = 0; j < k; ++j) {
                int target = dis(gen);
                if (!informed[static_cast<std::size_t>(target)]) {
                    new_informed.push_back(static_cast<std::size_t>(target));
                    informed[static_cast<std::size_t>(target)] = true;
                }
            }
        }
        informed_count += static_cast<int>(new_informed.size());
        ++rounds;
    }
    return rounds;
}

}  // namespace distributed
}  // namespace algorithm_x
