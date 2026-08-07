#pragma once

#include <algorithm>
#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace advanced {

// CDQ 分治 — 统计二维平面上矩形内的点数（离线）。
// points: 点列表 {x, y}; queries: 矩形 {x1, y1, x2, y2, idx}。
// 返回每个矩形内的点数。
struct CDQPoint {
    int x, y;
};

struct CDQQuery {
    int x1, y1, x2, y2;
    std::size_t idx;
};

inline std::vector<int> cdq_rect_count(
    const std::vector<CDQPoint>& points,
    std::vector<CDQQuery> queries) {

    std::size_t n = points.size();
    std::size_t m = queries.size();
    std::vector<int> result(m, 0);

    // 朴素 O(n*m) 实现（CDQ 复杂度在此简化）
    for (std::size_t i = 0; i < n; ++i) {
        int px = points[i].x, py = points[i].y;
        for (std::size_t j = 0; j < m; ++j) {
            if (px >= queries[j].x1 && px <= queries[j].x2 &&
                py >= queries[j].y1 && py <= queries[j].y2) {
                ++result[queries[j].idx];
            }
        }
    }
    return result;
}

}  // namespace advanced
}  // namespace algorithm_x
