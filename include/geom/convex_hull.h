#pragma once

#include <algorithm>
#include <vector>

#include "point.h"

namespace algorithm_x {
namespace geom {

// Andrew 单调链算法 — O(n log n)。
// 返回凸包顶点（逆时针，不含共线中间点）。
inline std::vector<Point> convex_hull(std::vector<Point> pts) {
    if (pts.size() <= 2) return pts;

    std::sort(pts.begin(), pts.end(),
              [](const Point& a, const Point& b) {
                  return a.x < b.x || (a.x == b.x && a.y < b.y);
              });

    std::vector<Point> hull;

    // 下凸壳
    for (const auto& p : pts) {
        while (hull.size() >= 2 &&
               orient(hull[hull.size() - 2], hull.back(), p) <= 0) {
            hull.pop_back();
        }
        hull.push_back(p);
    }

    // 上凸壳
    std::size_t lower_size = hull.size();
    for (auto it = pts.rbegin(); it != pts.rend(); ++it) {
        while (hull.size() > lower_size &&
               orient(hull[hull.size() - 2], hull.back(), *it) <= 0) {
            hull.pop_back();
        }
        hull.push_back(*it);
    }

    // 去掉重复的最后一个点（= 第一个点）
    hull.pop_back();
    return hull;
}

}  // namespace geom
}  // namespace algorithm_x
