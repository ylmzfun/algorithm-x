#pragma once

#include <algorithm>
#include <cstddef>
#include <deque>
#include <limits>
#include <random>
#include <utility>
#include <vector>

namespace algorithm_x {
namespace ai {

// N 皇后解计数：回溯 + 前向检查式剪枝。
// 依次为每一行选择列，用列 / 主对角线 / 副对角线三个 bool 数组做 O(1) 冲突
// 检测，发生冲突即剪枝（等价于每放一个皇后就把其影响位置从后续行可用位置中
// 剔除）。已知值：n=1→1, n=4→2, n=5→10, n=8→92。
inline std::size_t count_n_queens_forward_checking(int n) {
    if (n <= 0) {
        return 0;
    }
    std::vector<bool> col(static_cast<std::size_t>(n), false);
    std::vector<bool> diag1(static_cast<std::size_t>(2 * n - 1), false);
    std::vector<bool> diag2(static_cast<std::size_t>(2 * n - 1), false);
    std::size_t count = 0;
    auto dfs = [&](auto&& self, int row) -> void {
        if (row == n) {
            ++count;
            return;
        }
        for (int c = 0; c < n; ++c) {
            int d1 = row - c + (n - 1);
            int d2 = row + c;
            if (col[static_cast<std::size_t>(c)] ||
                diag1[static_cast<std::size_t>(d1)] ||
                diag2[static_cast<std::size_t>(d2)]) {
                continue;
            }
            col[static_cast<std::size_t>(c)] = true;
            diag1[static_cast<std::size_t>(d1)] = true;
            diag2[static_cast<std::size_t>(d2)] = true;
            self(self, row + 1);
            col[static_cast<std::size_t>(c)] = false;
            diag1[static_cast<std::size_t>(d1)] = false;
            diag2[static_cast<std::size_t>(d2)] = false;
        }
    };
    dfs(dfs, 0);
    return count;
}

// AC-3 弧一致性检查 k-着色。
// edges 为无向邻接边（区域编号 0..num_regions-1），num_colors 为可用颜色数；
// 每个区域 X_i 的域为 {0..num_colors-1}，约束为相邻区域颜色不同。
// 算法为标准 AC-3：队列存放弧 (X_i, X_j)，revise 时从 X_i 的域中删除在 X_j 的
// 域中无任何可取值的颜色；任一域变空 ⇒ 不可满足，返回 false。
//
// 约定与限制（重要）：
//  - AC-3 只保证弧一致性，是 k-着色可满足性的必要不充分条件；
//  - 对无环（树形 / 森林）约束图，弧一致性是完全判定：AC-3 结束后所有域
//    非空即返回 true（即"所有域非空 ⇒ true"的约定行为）；
//  - 对含环图，弧一致性不足（例如奇环 2-着色满足弧一致却不可满足，AC-3
//    不会清空任何域），"所有域非空即 true"会误判；因此本函数在 AC-3 剪枝
//    结束后，对含环图用确定性回溯（区域 / 颜色固定顺序 DFS）在剪枝后的域上
//    搜索完整着色，返回真实的 k-着色可满足性。
// 测试中的小图（澳大利亚 7 区域、四边形、三角形）均由此给出正确判定。
inline bool ac3_map_coloring(const std::vector<std::pair<int, int>>& edges,
                             int num_regions, int num_colors) {
    if (num_regions <= 0 || num_colors <= 0) {
        return false;
    }

    // 邻接表（去重）
    std::vector<std::vector<int>> adj(static_cast<std::size_t>(num_regions));
    for (const auto& e : edges) {
        if (e.first < 0 || e.second < 0 || e.first >= num_regions ||
            e.second >= num_regions) {
            return false;  // 非法边
        }
        if (e.first == e.second) {
            return false;  // 自环：区域不能与自身颜色不同
        }
        adj[static_cast<std::size_t>(e.first)].push_back(e.second);
        adj[static_cast<std::size_t>(e.second)].push_back(e.first);
    }
    for (auto& nbrs : adj) {
        std::sort(nbrs.begin(), nbrs.end());
        nbrs.erase(std::unique(nbrs.begin(), nbrs.end()), nbrs.end());
    }

    // 每个区域的域初始为全部颜色
    std::vector<std::vector<bool>> domain(
        static_cast<std::size_t>(num_regions),
        std::vector<bool>(static_cast<std::size_t>(num_colors), true));

    // AC-3 主循环
    std::deque<std::pair<int, int>> queue;
    for (int i = 0; i < num_regions; ++i) {
        for (int j : adj[static_cast<std::size_t>(i)]) {
            queue.emplace_back(i, j);
        }
    }
    auto revise = [&](int xi, int xj) -> bool {
        bool changed = false;
        for (int c = 0; c < num_colors; ++c) {
            if (!domain[static_cast<std::size_t>(xi)][static_cast<std::size_t>(c)]) {
                continue;
            }
            bool supported = false;
            for (int d = 0; d < num_colors; ++d) {
                if (d != c &&
                    domain[static_cast<std::size_t>(xj)][static_cast<std::size_t>(d)]) {
                    supported = true;
                    break;
                }
            }
            if (!supported) {
                domain[static_cast<std::size_t>(xi)][static_cast<std::size_t>(c)] = false;
                changed = true;
            }
        }
        return changed;
    };
    while (!queue.empty()) {
        std::pair<int, int> arc = queue.front();
        queue.pop_front();
        int xi = arc.first;
        int xj = arc.second;
        if (revise(xi, xj)) {
            bool empty = true;
            for (int c = 0; c < num_colors; ++c) {
                if (domain[static_cast<std::size_t>(xi)][static_cast<std::size_t>(c)]) {
                    empty = false;
                    break;
                }
            }
            if (empty) {
                return false;  // 某域变空 ⇒ 不可满足
            }
            for (int xk : adj[static_cast<std::size_t>(xi)]) {
                if (xk != xj) {
                    queue.emplace_back(xk, xi);
                }
            }
        }
    }

    // AC-3 结束且所有域非空：无环约束图可由此直接判定（约定行为）。
    std::vector<bool> visited(static_cast<std::size_t>(num_regions), false);
    bool has_cycle = false;
    auto detect_cycle = [&](auto&& self, int u, int parent) -> void {
        visited[static_cast<std::size_t>(u)] = true;
        for (int v : adj[static_cast<std::size_t>(u)]) {
            if (v == parent) {
                continue;
            }
            if (visited[static_cast<std::size_t>(v)]) {
                has_cycle = true;
                return;
            }
            self(self, v, u);
            if (has_cycle) {
                return;
            }
        }
    };
    for (int i = 0; i < num_regions && !has_cycle; ++i) {
        if (!visited[static_cast<std::size_t>(i)]) {
            detect_cycle(detect_cycle, i, -1);
        }
    }
    if (!has_cycle) {
        return true;
    }

    // 含环图：在剪枝后的域上确定性回溯补全判定。
    std::vector<int> color(static_cast<std::size_t>(num_regions), -1);
    auto backtrack = [&](auto&& self, int region) -> bool {
        if (region == num_regions) {
            return true;
        }
        for (int c = 0; c < num_colors; ++c) {
            if (!domain[static_cast<std::size_t>(region)][static_cast<std::size_t>(c)]) {
                continue;
            }
            bool ok = true;
            for (int v : adj[static_cast<std::size_t>(region)]) {
                if (color[static_cast<std::size_t>(v)] == c) {
                    ok = false;
                    break;
                }
            }
            if (!ok) {
                continue;
            }
            color[static_cast<std::size_t>(region)] = c;
            if (self(self, region + 1)) {
                return true;
            }
            color[static_cast<std::size_t>(region)] = -1;
        }
        return false;
    };
    return backtrack(backtrack, 0);
}

// 最小冲突启发式求解 N 皇后。
// 随机初始放置（确定性种子 42），每步从当前冲突的皇后中随机选一个，移到冲突
// 最少的列（平局随机），直至无冲突或达到 max_steps。返回 ans[r] = 第 r 行
// 皇后的列号；max_steps 内未找到解返回空 vector。
inline std::vector<int> min_conflicts_n_queens(int n, int max_steps = 1000) {
    if (n <= 0) {
        return {};
    }

    std::mt19937 gen(42);
    std::uniform_int_distribution<int> col_dist(0, n - 1);

    std::vector<int> ans(static_cast<std::size_t>(n));
    for (int r = 0; r < n; ++r) {
        ans[static_cast<std::size_t>(r)] = col_dist(gen);
    }

    std::vector<int> col_count(static_cast<std::size_t>(n), 0);
    std::vector<int> diag1_count(static_cast<std::size_t>(2 * n - 1), 0);
    std::vector<int> diag2_count(static_cast<std::size_t>(2 * n - 1), 0);
    for (int r = 0; r < n; ++r) {
        int c = ans[static_cast<std::size_t>(r)];
        ++col_count[static_cast<std::size_t>(c)];
        ++diag1_count[static_cast<std::size_t>(r - c + n - 1)];
        ++diag2_count[static_cast<std::size_t>(r + c)];
    }

    // 皇后 r 与其它皇后的冲突数
    auto queen_conflicts = [&](int r) -> int {
        int c = ans[static_cast<std::size_t>(r)];
        return (col_count[static_cast<std::size_t>(c)] - 1) +
               (diag1_count[static_cast<std::size_t>(r - c + n - 1)] - 1) +
               (diag2_count[static_cast<std::size_t>(r + c)] - 1);
    };
    auto total_conflicts = [&]() -> int {
        int total = 0;
        for (int r = 0; r < n; ++r) {
            total += queen_conflicts(r);
        }
        return total;
    };
    // 皇后放到 (r, c) 后的冲突数（当前列不计自身）
    auto evaluate = [&](int r, int c) -> int {
        if (c == ans[static_cast<std::size_t>(r)]) {
            return (col_count[static_cast<std::size_t>(c)] - 1) +
                   (diag1_count[static_cast<std::size_t>(r - c + n - 1)] - 1) +
                   (diag2_count[static_cast<std::size_t>(r + c)] - 1);
        }
        return col_count[static_cast<std::size_t>(c)] +
               diag1_count[static_cast<std::size_t>(r - c + n - 1)] +
               diag2_count[static_cast<std::size_t>(r + c)];
    };

    for (int step = 0; step < max_steps; ++step) {
        if (total_conflicts() == 0) {
            return ans;
        }
        // 收集当前有冲突的皇后所在行
        std::vector<int> conflicted_rows;
        for (int r = 0; r < n; ++r) {
            if (queen_conflicts(r) > 0) {
                conflicted_rows.push_back(r);
            }
        }
        std::uniform_int_distribution<int> row_dist(
            0, static_cast<int>(conflicted_rows.size()) - 1);
        int r = conflicted_rows[static_cast<std::size_t>(row_dist(gen))];

        // 选冲突最少的列，平局随机
        std::vector<int> best_cols;
        int best_conflicts = std::numeric_limits<int>::max();
        for (int c = 0; c < n; ++c) {
            int conflicts = evaluate(r, c);
            if (conflicts < best_conflicts) {
                best_conflicts = conflicts;
                best_cols.clear();
                best_cols.push_back(c);
            } else if (conflicts == best_conflicts) {
                best_cols.push_back(c);
            }
        }
        std::uniform_int_distribution<int> best_dist(
            0, static_cast<int>(best_cols.size()) - 1);
        int c_new = best_cols[static_cast<std::size_t>(best_dist(gen))];

        // 移动皇后并更新冲突计数
        int c_old = ans[static_cast<std::size_t>(r)];
        if (c_new != c_old) {
            --col_count[static_cast<std::size_t>(c_old)];
            --diag1_count[static_cast<std::size_t>(r - c_old + n - 1)];
            --diag2_count[static_cast<std::size_t>(r + c_old)];
            ans[static_cast<std::size_t>(r)] = c_new;
            ++col_count[static_cast<std::size_t>(c_new)];
            ++diag1_count[static_cast<std::size_t>(r - c_new + n - 1)];
            ++diag2_count[static_cast<std::size_t>(r + c_new)];
        }
    }
    if (total_conflicts() == 0) {
        return ans;
    }
    return {};
}

}  // namespace ai
}  // namespace algorithm_x
