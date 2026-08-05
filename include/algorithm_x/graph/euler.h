#pragma once

#include <cstddef>
#include <stack>
#include <vector>

namespace algorithm_x {
namespace graph {

// 无向图欧拉路径/回路（Hierholzer 算法）。
// 返回路径上的顶点序列，不存在返回空。
inline std::vector<std::size_t> euler_path(
    std::vector<std::vector<std::size_t>> adj) {
    std::size_t n = adj.size();

    // 检查度数：奇数度顶点必须为 0 或 2
    std::size_t odd = 0, start = 0;
    for (std::size_t u = 0; u < n; ++u) {
        if (adj[u].size() % 2 == 1) {
            ++odd;
            start = u;
        }
    }
    if (odd != 0 && odd != 2) return {};

    // Hierholzer
    std::vector<std::size_t> result;
    std::stack<std::size_t> stk;
    stk.push(start);

    while (!stk.empty()) {
        std::size_t u = stk.top();
        if (adj[u].empty()) {
            result.push_back(u);
            stk.pop();
        } else {
            std::size_t v = adj[u].back();
            adj[u].pop_back();
            // 删除反向边
            auto& vec = adj[v];
            for (auto it = vec.begin(); it != vec.end(); ++it) {
                if (*it == u) {
                    vec.erase(it);
                    break;
                }
            }
            stk.push(v);
        }
    }

    // 验证是否用了所有边
    for (std::size_t u = 0; u < n; ++u) {
        if (!adj[u].empty()) return {};  // 图不连通
    }
    return result;
}

}  // namespace graph
}  // namespace algorithm_x
