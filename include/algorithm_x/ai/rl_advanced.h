#pragma once

#include <algorithm>
#include <cstddef>
#include <cstdlib>
#include <map>
#include <random>
#include <utility>
#include <vector>

namespace algorithm_x {
namespace ai {

// SARSA — State-Action-Reward-State-Action (On-Policy TD Control)。
// grid: 0=通路, 1=障碍, 2=目标。
class SARSA {
public:
    SARSA(const std::vector<std::vector<int>>& grid,
          double alpha = 0.1, double gamma = 0.9, double epsilon = 0.1)
        : grid_(grid), rows_(static_cast<int>(grid.size())),
          cols_(static_cast<int>(grid[0].size())),
          alpha_(alpha), gamma_(gamma), epsilon_(epsilon) {
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

    void train(int episodes) {
        for (int ep = 0; ep < episodes; ++ep) {
            int r = std::uniform_int_distribution<int>(0, rows_ - 1)(gen_);
            int c = std::uniform_int_distribution<int>(0, cols_ - 1)(gen_);
            // 避开障碍和目标（随机起始）
            while (grid_[static_cast<std::size_t>(r)]
                        [static_cast<std::size_t>(c)] != 0) {
                r = std::uniform_int_distribution<int>(0, rows_ - 1)(gen_);
                c = std::uniform_int_distribution<int>(0, cols_ - 1)(gen_);
            }

            int a = epsilon_greedy(r, c);
            while (r != goal_r_ || c != goal_c_) {
                auto [nr, nc] = step(r, c, a);
                double reward = (nr == goal_r_ && nc == goal_c_) ? 100.0 : -1.0;
                int na = (nr == goal_r_ && nc == goal_c_) ? 0 : epsilon_greedy(nr, nc);

                double& q_cur = Q_[{r, c, a}];
                double q_next = (nr == goal_r_ && nc == goal_c_) ? 0.0 : Q_[{nr, nc, na}];
                q_cur += alpha_ * (reward + gamma_ * q_next - q_cur);

                r = nr; c = nc; a = na;
            }
        }
    }

    std::vector<std::pair<int, int>> get_path(int start_r, int start_c) const {
        std::vector<std::pair<int, int>> path;
        int r = start_r, c = start_c;
        for (int step = 0; step < rows_ * cols_ * 2; ++step) {
            path.emplace_back(r, c);
            if (r == goal_r_ && c == goal_c_) break;
            double best = -1e9;
            int best_a = 0;
            for (int a = 0; a < 4; ++a) {
                auto it = Q_.find({r, c, a});
                double q = (it != Q_.end()) ? it->second : 0.0;
                if (q > best) { best = q; best_a = a; }
            }
            auto [nr, nc] = step(r, c, best_a);
            r = nr; c = nc;
        }
        return path;
    }

private:
    int epsilon_greedy(int r, int c) {
        std::uniform_real_distribution<double> prob(0.0, 1.0);
        if (prob(gen_) < epsilon_) {
            return std::uniform_int_distribution<int>(0, 3)(gen_);
        }
        double best = -1e9;
        int best_a = 0;
        for (int a = 0; a < 4; ++a) {
            auto it = Q_.find({r, c, a});
            double q = (it != Q_.end()) ? it->second : 0.0;
            if (q > best) { best = q; best_a = a; }
        }
        return best_a;
    }

    std::pair<int, int> step(int r, int c, int a) const {
        static const int dr[] = {-1, 0, 1, 0};
        static const int dc[] = {0, 1, 0, -1};
        int nr = r + dr[a], nc = c + dc[a];
        if (nr < 0 || nr >= rows_ || nc < 0 || nc >= cols_ ||
            grid_[static_cast<std::size_t>(nr)]
                 [static_cast<std::size_t>(nc)] == 1) {
            return {r, c};  // 撞墙不动
        }
        return {nr, nc};
    }

    struct Key { int r, c, a; };
    struct KeyHash {
        std::size_t operator()(const Key& k) const {
            return (static_cast<std::size_t>(k.r) * 10000 +
                    static_cast<std::size_t>(k.c)) * 4 +
                   static_cast<std::size_t>(k.a);
        }
    };
    friend bool operator==(const Key& a, const Key& b) {
        return a.r == b.r && a.c == b.c && a.a == b.a;
    }

    const std::vector<std::vector<int>>& grid_;
    int rows_, cols_, goal_r_ = 0, goal_c_ = 0;
    double alpha_, gamma_, epsilon_;
    mutable std::mt19937 gen_{42};
    std::unordered_map<Key, double, KeyHash> Q_;
};

}  // namespace ai
}  // namespace algorithm_x
