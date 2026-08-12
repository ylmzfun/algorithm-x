#pragma once

#include <cstdint>
#include <vector>

namespace algorithm_x {
namespace math {

// Nim 游戏：判断先手是否必胜。
// piles[i] 为第 i 堆石子数。异或和 != 0 则先手必胜。
inline bool nim_win(const std::vector<int>& piles) {
    int x = 0;
    for (int p : piles) x ^= p;
    return x != 0;
}

// Sprague-Grundy 函数：计算给定局面的 SG 值。
// 多个子游戏组合的 SG = sg(a) ^ sg(b) ^ ... ，SG != 0 则必胜。
// 这里给一个通用版：输入游戏图 adj[u] = {可到达的状态}。
inline int sg_function(const std::vector<std::vector<int>>& adj) {
    int n = static_cast<int>(adj.size());
    std::vector<int> sg(n, -1);

    auto dfs = [&](auto&& self, int u) -> int {
        if (sg[u] != -1) return sg[u];
        std::vector<bool> mex(n + 1, false);
        for (int v : adj[u]) {
            mex[self(self, v)] = true;
        }
        int g = 0;
        while (mex[g]) ++g;
        return sg[u] = g;
    };

    for (int i = 0; i < n; ++i) dfs(dfs, i);
    return sg[0];  // 返回起点的 SG 值
}

}  // namespace math
}  // namespace algorithm_x
