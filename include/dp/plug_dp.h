#pragma once

#include <cstddef>
#include <cstdint>
#include <vector>

namespace algorithm_x {
namespace dp {

// 插头 DP / 轮廓线 DP — 1×2 骨牌完全覆盖 rows×cols 棋盘的方案数。
//
// 状态设计（轮廓线）：
// 按行优先逐格扫描棋盘，已处理格子与未处理格子的分界线是一条"轮廓线"。
// 用一个 cols 位的二进制掩码 mask 记录轮廓线上各列的占用情况：
//   - 对已处理过的列 j（当前格左边）：bit j = 1 表示格子 (r+1, j) 已被本行
//     (r, j) 处竖放的骨牌占住（延伸到下一行）；
//   - 对尚未处理的列 j（当前格及其右边）：bit j = 1 表示格子 (r, j) 已被上方
//     竖放的骨牌或本行左侧横放的骨牌占住。
// 处理完当前格 (r, c) 后，bit c 的含义自动从"本行已占"切换为"下一行已占"，
// 因此同一个掩码位即可完成跨行传递，转移只与轮廓线有关。
//
// 转移（当前格 (r, c)，令 bit = 1 << c）：
//   1) mask 中 bit c 已置位：当前格已被覆盖，只需清掉该位（占位随轮廓线后移）；
//   2) 否则当前格空闲，可二选一：
//      - 竖放：覆盖 (r, c) 与 (r+1, c)，置位 bit c；
//      - 横放：覆盖 (r, c) 与 (r, c+1)，要求 c+1 < cols 且 bit (c+1) 空闲，置位 bit (c+1)。
// 全部格子处理完毕后，合法覆盖要求轮廓线为空（mask == 0）。
inline int64_t domino_tilings(int rows, int cols) {
    if (rows == 0 || cols == 0) {
        return 1;  // 空棋盘：恰好 1 种方案（什么都不放）
    }
    const int m = cols;
    const int state_count = 1 << m;
    std::vector<int64_t> dp(static_cast<std::size_t>(state_count), 0);
    dp[0] = 1;
    for (int r = 0; r < rows; ++r) {
        for (int c = 0; c < cols; ++c) {
            std::vector<int64_t> ndp(static_cast<std::size_t>(state_count), 0);
            const int bit = 1 << c;
            for (int mask = 0; mask < state_count; ++mask) {
                const int64_t ways = dp[static_cast<std::size_t>(mask)];
                if (ways == 0) {
                    continue;
                }
                if ((mask & bit) != 0) {
                    // 当前格已被覆盖：占位随轮廓线后移，清掉 bit c
                    ndp[static_cast<std::size_t>(mask & ~bit)] += ways;
                } else {
                    // 竖放：覆盖 (r, c) 与 (r+1, c)
                    ndp[static_cast<std::size_t>(mask | bit)] += ways;
                    // 横放：覆盖 (r, c) 与 (r, c+1)
                    if (c + 1 < cols && (mask & (bit << 1)) == 0) {
                        ndp[static_cast<std::size_t>(mask | (bit << 1))] += ways;
                    }
                }
            }
            dp.swap(ndp);
        }
    }
    // 所有格子处理完毕后，轮廓线必须为空
    return dp[0];
}

}  // namespace dp
}  // namespace algorithm_x
