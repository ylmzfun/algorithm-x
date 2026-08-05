#pragma once

#include <algorithm>
#include <cmath>
#include <vector>

namespace algorithm_x {
namespace geom {

// 二维点 / 向量。
struct Point {
    double x, y;

    Point operator+(const Point& o) const { return {x + o.x, y + o.y}; }
    Point operator-(const Point& o) const { return {x - o.x, y - o.y}; }
    Point operator*(double k) const { return {x * k, y * k}; }
    double operator*(const Point& o) const { return x * o.x + y * o.y; }  // dot
    bool operator==(const Point& o) const { return x == o.x && y == o.y; }
};

// 叉积：a × b = |a||b| sin θ。正值表示 b 在 a 的逆时针方向。
inline double cross(const Point& a, const Point& b) {
    return a.x * b.y - a.y * b.x;
}

// 两点间欧氏距离。
inline double dist(const Point& a, const Point& b) {
    double dx = a.x - b.x, dy = a.y - b.y;
    return std::sqrt(dx * dx + dy * dy);
}

// 两点间距离的平方（避免开方）。
inline double dist2(const Point& a, const Point& b) {
    double dx = a.x - b.x, dy = a.y - b.y;
    return dx * dx + dy * dy;
}

// 多边形面积（顶点按逆时针或顺时针给出，返回有向面积）。
// 逆时针为正，绝对值 / 2 为实际面积。
inline double polygon_area(const std::vector<Point>& poly) {
    double area = 0;
    std::size_t n = poly.size();
    for (std::size_t i = 0; i < n; ++i) {
        std::size_t j = (i + 1) % n;
        area += cross(poly[i], poly[j]);
    }
    return area / 2.0;
}

// 判断点 c 是否在线段 ab 上（假设共线已判定）。
inline bool on_segment(const Point& a, const Point& b, const Point& c) {
    return std::min(a.x, b.x) <= c.x && c.x <= std::max(a.x, b.x) &&
           std::min(a.y, b.y) <= c.y && c.y <= std::max(a.y, b.y);
}

// 叉积方向：>0 逆时针，<0 顺时针，==0 共线。
inline double orient(const Point& a, const Point& b, const Point& c) {
    return cross(b - a, c - a);
}

}  // namespace geom
}  // namespace algorithm_x
