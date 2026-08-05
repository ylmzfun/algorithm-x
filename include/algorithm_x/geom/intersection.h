#pragma once

#include <algorithm>
#include <limits>
#include <vector>

#include "point.h"

namespace algorithm_x {
namespace geom {

// 判断线段 ab 和 cd 是否相交（包括端点接触）。
inline bool segment_intersect(const Point& a, const Point& b,
                               const Point& c, const Point& d) {
    double o1 = orient(a, b, c);
    double o2 = orient(a, b, d);
    double o3 = orient(c, d, a);
    double o4 = orient(c, d, b);

    if (o1 * o2 < 0 && o3 * o4 < 0) return true;  // 严格相交

    // 共线且端点在线段上
    const double eps = 1e-9;
    if (std::abs(o1) < eps && on_segment(a, b, c)) return true;
    if (std::abs(o2) < eps && on_segment(a, b, d)) return true;
    if (std::abs(o3) < eps && on_segment(c, d, a)) return true;
    if (std::abs(o4) < eps && on_segment(c, d, b)) return true;

    return false;
}

// 最近点对（分治法）— O(n log n)。
// 返回 {点1索引, 点2索引, 距离}。
// 调用者传入点数组（会被排序），返回原始点的距离。
inline double closest_pair(std::vector<Point>& pts) {
    std::sort(pts.begin(), pts.end(),
              [](const Point& a, const Point& b) { return a.x < b.x; });

    const double INF = std::numeric_limits<double>::max();

    auto solve = [&](auto&& self, std::size_t l, std::size_t r) -> double {
        if (r - l <= 1) return INF;
        if (r - l == 2) return dist(pts[l], pts[l + 1]);

        std::size_t mid = l + (r - l) / 2;
        double d = std::min(self(self, l, mid), self(self, mid, r));

        // 带状区域内的点按 y 排序
        std::vector<Point> strip;
        double mid_x = pts[mid].x;
        for (std::size_t i = l; i < r; ++i) {
            if (std::abs(pts[i].x - mid_x) < d) {
                strip.push_back(pts[i]);
            }
        }
        std::sort(strip.begin(), strip.end(),
                  [](const Point& a, const Point& b) { return a.y < b.y; });

        for (std::size_t i = 0; i < strip.size(); ++i) {
            for (std::size_t j = i + 1;
                 j < strip.size() && strip[j].y - strip[i].y < d; ++j) {
                d = std::min(d, dist(strip[i], strip[j]));
            }
        }
        return d;
    };

    return solve(solve, 0, pts.size());
}

}  // namespace geom
}  // namespace algorithm_x
