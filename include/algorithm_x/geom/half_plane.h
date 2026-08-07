#pragma once

#include <algorithm>
#include <cmath>
#include <vector>

#include "point.h"

namespace algorithm_x {
namespace geom {

// 半平面交 — 每条半平面表示为 a·x + b·y + c ≤ 0。
// 返回交区域的多边形顶点（逆时针）。使用增量式 O(n²) 算法。
struct HalfPlane {
    double a, b, c;  // a*x + b*y + c <= 0
};

inline std::vector<Point> half_plane_intersection(
    const std::vector<HalfPlane>& planes) {
    if (planes.empty()) return {};

    const double INF = 1e9;
    const double EPS = 1e-9;

    // 初始为一个大矩形
    std::vector<Point> poly = {
        {-INF, -INF}, {INF, -INF}, {INF, INF}, {-INF, INF}};

    for (auto& hp : planes) {
        std::vector<Point> new_poly;

        auto inside = [&](const Point& p) {
            return hp.a * p.x + hp.b * p.y + hp.c <= EPS;
        };

        auto intersect = [&](const Point& p1, const Point& p2) -> Point {
            double d1 = hp.a * p1.x + hp.b * p1.y + hp.c;
            double d2 = hp.a * p2.x + hp.b * p2.y + hp.c;
            if (std::abs(d1 - d2) < EPS) return p1;
            double t = d1 / (d1 - d2);
            return {p1.x + t * (p2.x - p1.x), p1.y + t * (p2.y - p1.y)};
        };

        std::size_t m = poly.size();
        for (std::size_t i = 0; i < m; ++i) {
            std::size_t j = (i + 1) % m;
            bool in1 = inside(poly[i]);
            bool in2 = inside(poly[j]);

            if (in1) new_poly.push_back(poly[i]);
            if (in1 != in2) new_poly.push_back(intersect(poly[i], poly[j]));
        }
        poly = std::move(new_poly);
    }
    return poly;
}

}  // namespace geom
}  // namespace algorithm_x
