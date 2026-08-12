#pragma once

#include <algorithm>
#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace geom {

// 矩形 {x1, y1, x2, y2} 其中 x1 < x2, y1 < y2。
struct Rect {
    double x1, y1, x2, y2;
};

// 矩形面积并（扫描线算法）。
// 离散化 y 坐标，扫描线从左到右。
inline double rectangle_union_area(const std::vector<Rect>& rects) {
    if (rects.empty()) return 0.0;

    // 收集离散化 y 坐标
    std::vector<double> ys;
    for (auto& r : rects) {
        ys.push_back(r.y1);
        ys.push_back(r.y2);
    }
    std::sort(ys.begin(), ys.end());
    ys.erase(std::unique(ys.begin(), ys.end()), ys.end());

    // 事件：x 坐标处矩形进入 (+1) / 离开 (-1)
    struct Event {
        double x;
        int y1_idx, y2_idx, type;  // +1 enter, -1 exit
        bool operator<(const Event& o) const { return x < o.x; }
    };
    std::vector<Event> events;
    for (auto& r : rects) {
        int y1 = static_cast<int>(
            std::lower_bound(ys.begin(), ys.end(), r.y1) - ys.begin());
        int y2 = static_cast<int>(
            std::lower_bound(ys.begin(), ys.end(), r.y2) - ys.begin());
        events.push_back({r.x1, y1, y2, 1});
        events.push_back({r.x2, y1, y2, -1});
    }
    std::sort(events.begin(), events.end());

    // 线段树维护覆盖长度
    int m = static_cast<int>(ys.size()) - 1;
    std::vector<int> cnt(4 * static_cast<std::size_t>(m), 0);
    std::vector<double> len(4 * static_cast<std::size_t>(m), 0.0);

    auto update = [&](auto&& self, int node, int l, int r) -> void {
        if (cnt[node] > 0) {
            len[static_cast<std::size_t>(node)] = ys[static_cast<std::size_t>(r)] -
                                                   ys[static_cast<std::size_t>(l)];
        } else if (r - l == 1) {
            len[static_cast<std::size_t>(node)] = 0.0;
        } else {
            len[static_cast<std::size_t>(node)] =
                len[static_cast<std::size_t>(node * 2)] +
                len[static_cast<std::size_t>(node * 2 + 1)];
        }
    };

    auto add = [&](auto&& self, int node, int l, int r, int ql, int qr, int val) -> void {
        if (ql >= r || qr <= l) return;
        if (ql <= l && r <= qr) {
            cnt[node] += val;
            update(update, node, l, r);
            return;
        }
        int mid = (l + r) / 2;
        self(self, node * 2, l, mid, ql, qr, val);
        self(self, node * 2 + 1, mid, r, ql, qr, val);
        update(update, node, l, r);
    };

    double area = 0.0;
    double prev_x = events[0].x;
    for (auto& e : events) {
        area += len[1] * (e.x - prev_x);
        prev_x = e.x;
        add(add, 1, 0, m, e.y1_idx, e.y2_idx, e.type);
    }
    return area;
}

}  // namespace geom
}  // namespace algorithm_x
