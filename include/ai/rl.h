#pragma once

#include <algorithm>
#include <cstddef>
#include <cstdlib>
#include <map>
#include <random>
#include <vector>

namespace algorithm_x {
namespace ai {

// Q-Learning — 网格世界。
// grid: 0=通路, 1=障碍, 2=目标。返回 Q 表和最优策略。
class QLearning {
public:
    QLearning(const std::vector<std::vector<int>>& grid,
              double alpha = 0.1, double gamma = 0.9, double epsilon = 0.1)
        : grid_(grid), rows_(static_cast<int>(grid.size())),
          cols_(static_cast<int>(grid[0].size())),
          alpha_(alpha), gamma_(gamma), epsilon_(epsilon) {
        // 查找目标位置
        for (int r = 0; r < rows_; ++r) {
            for (int c = 0; c < cols_; ++c) {
                if (grid_[static_cast<std::size_t>(r)]
                        [static_cast<std::size_t>(c)] == 2) {
                    goal_r_ = r;
                    goal_c_ = c;
                }
            }
        }
    }

    // 训练 episodes 轮。
    void train(int episodes = 1000) {
        std::mt19937 gen(42);
        const int dr[] = {-1, 0, 1, 0};
        const int dc[] = {0, 1, 0, -1};

        for (int ep = 0; ep < episodes; ++ep) {
            // 随机起始位置（非障碍非目标）
            int r, c;
            do {
                r = std::uniform_int_distribution<int>(0, rows_ - 1)(gen);
                c = std::uniform_int_distribution<int>(0, cols_ - 1)(gen);
            } while (grid_[static_cast<std::size_t>(r)]
                         [static_cast<std::size_t>(c)] != 0);

            for (int step = 0; step < rows_ * cols_ * 2; ++step) {
                if (r == goal_r_ && c == goal_c_) break;

                int state = encode(r, c);
                int action;
                if (std::uniform_real_distribution<double>(0, 1)(gen) <
                    epsilon_) {
                    action = std::uniform_int_distribution<int>(0, 3)(gen);
                } else {
                    action = best_action(state);
                }

                int nr = std::clamp(r + dr[action], 0, rows_ - 1);
                int nc = std::clamp(c + dc[action], 0, cols_ - 1);
                if (grid_[static_cast<std::size_t>(nr)]
                        [static_cast<std::size_t>(nc)] == 1) {
                    nr = r;
                    nc = c;  // 撞墙不动
                }

                double reward = -0.1;  // 每步小惩罚
                if (nr == goal_r_ && nc == goal_c_) reward = 10.0;

                int next_state = encode(nr, nc);
                double& cur_q = q_[{state, action}];
                double max_next = 0.0;
                for (int a = 0; a < 4; ++a) {
                    auto it = q_.find({next_state, a});
                    if (it != q_.end()) max_next = std::max(max_next, it->second);
                }
                cur_q += alpha_ * (reward + gamma_ * max_next - cur_q);

                r = nr;
                c = nc;
            }
        }
    }

    // 获取状态的最优动作（0=上, 1=右, 2=下, 3=左）。
    int best_action(int state) const {
        int best = 0;
        double best_val = -1e9;
        for (int a = 0; a < 4; ++a) {
            auto it = q_.find({state, a});
            double val = (it != q_.end()) ? it->second : 0.0;
            if (val > best_val) {
                best_val = val;
                best = a;
            }
        }
        return best;
    }

    // 获取从 (r,c) 到目标的路径。
    std::vector<std::pair<int, int>> get_path(int start_r, int start_c) const {
        std::vector<std::pair<int, int>> path;
        int r = start_r, c = start_c;
        const int dr[] = {-1, 0, 1, 0};
        const int dc[] = {0, 1, 0, -1};

        for (int step = 0; step < rows_ * cols_; ++step) {
            path.emplace_back(r, c);
            if (r == goal_r_ && c == goal_c_) break;
            int a = best_action(encode(r, c));
            r = std::clamp(r + dr[a], 0, rows_ - 1);
            c = std::clamp(c + dc[a], 0, cols_ - 1);
        }
        return path;
    }

    int rows() const { return rows_; }
    int cols() const { return cols_; }

private:
    int encode(int r, int c) const { return r * cols_ + c; }

    std::vector<std::vector<int>> grid_;
    int rows_, cols_;
    int goal_r_ = 0, goal_c_ = 0;
    double alpha_, gamma_, epsilon_;
    std::map<std::pair<int, int>, double> q_;
};

}  // namespace ai
}  // namespace algorithm_x
