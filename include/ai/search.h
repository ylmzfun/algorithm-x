#pragma once

#include <algorithm>
#include <cmath>
#include <cstddef>
#include <functional>
#include <queue>
#include <random>
#include <unordered_map>
#include <unordered_set>
#include <vector>

namespace algorithm_x {
namespace ai {

// A* 搜索（网格路径规划）。
// grid: 0=通路, 1=障碍。返回从 start 到 goal 的路径点序列，无解返回空。
struct GridPos {
    int r, c;
    bool operator==(const GridPos& o) const { return r == o.r && c == o.c; }
};

}  // namespace ai
}  // namespace algorithm_x

// Hash for GridPos (must be in global namespace for unordered_map).
template <>
struct std::hash<algorithm_x::ai::GridPos> {
    std::size_t operator()(const algorithm_x::ai::GridPos& p) const {
        return static_cast<std::size_t>(p.r) * 10000 +
               static_cast<std::size_t>(p.c);
    }
};

namespace algorithm_x {
namespace ai {

inline std::vector<GridPos> astar(const std::vector<std::vector<int>>& grid,
                                   GridPos start, GridPos goal) {
    int rows = static_cast<int>(grid.size());
    int cols = static_cast<int>(grid[0].size());
    const int dr[] = {-1, 0, 1, 0};
    const int dc[] = {0, 1, 0, -1};

    auto heuristic = [&](const GridPos& a) {
        return std::abs(a.r - goal.r) + std::abs(a.c - goal.c);
    };

    auto encode = [&](const GridPos& p) { return p.r * cols + p.c; };

    struct Node {
        int f, g, h, key;  // key = encoded position
        bool operator>(const Node& o) const { return f > o.f; }
    };

    std::priority_queue<Node, std::vector<Node>, std::greater<>> open;
    std::unordered_map<int, int> g_score;
    std::unordered_map<int, int> came_from;

    int s_key = encode(start);
    g_score[s_key] = 0;
    open.push({heuristic(start), 0, heuristic(start), s_key});

    while (!open.empty()) {
        Node cur = open.top();
        open.pop();
        int u_key = cur.key;
        int u_r = u_key / cols, u_c = u_key % cols;

        if (u_r == goal.r && u_c == goal.c) {
            // 重建路径
            std::vector<GridPos> path;
            int k = u_key;
            while (k != s_key) {
                path.push_back({k / cols, k % cols});
                k = came_from[k];
            }
            path.push_back(start);
            std::reverse(path.begin(), path.end());
            return path;
        }

        if (cur.g > g_score[u_key]) continue;

        for (int d = 0; d < 4; ++d) {
            int nr = u_r + dr[d], nc = u_c + dc[d];
            if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
            if (grid[static_cast<std::size_t>(nr)]
                    [static_cast<std::size_t>(nc)] == 1) continue;

            int v_key = nr * cols + nc;
            int new_g = cur.g + 1;
            auto it = g_score.find(v_key);
            if (it == g_score.end() || new_g < it->second) {
                g_score[v_key] = new_g;
                came_from[v_key] = u_key;
                int h = std::abs(nr - goal.r) + std::abs(nc - goal.c);
                open.push({new_g + h, new_g, h, v_key});
            }
        }
    }
    return {};  // 无解
}

// 模拟退火 — 求函数 f(x) 在 [lo, hi] 上的最小值（连续）。
// f: double → double 的代价函数。
inline double simulated_annealing(std::function<double(double)> f,
                                   double lo, double hi,
                                   int iterations = 10000) {
    std::mt19937 gen(42);
    std::uniform_real_distribution<double> dis(lo, hi);
    std::uniform_real_distribution<double> prob(0.0, 1.0);

    double x = dis(gen);
    double best_x = x;
    double best_val = f(x);
    double temp = 1.0;

    for (int i = 0; i < iterations; ++i) {
        std::normal_distribution<double> neigh(x, (hi - lo) * temp * 0.1);
        double nx = neigh(gen);
        nx = std::clamp(nx, lo, hi);

        double delta = f(nx) - f(x);
        if (delta < 0 || prob(gen) < std::exp(-delta / temp)) {
            x = nx;
            if (f(x) < best_val) {
                best_val = f(x);
                best_x = x;
            }
        }
        temp *= 0.999;
    }
    return best_x;
}

}  // namespace ai
}  // namespace algorithm_x
