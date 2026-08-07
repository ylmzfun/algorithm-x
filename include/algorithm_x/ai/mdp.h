#pragma once

#include <algorithm>
#include <cmath>
#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace ai {

// MDP 值迭代 — 已知转移模型。
// transitions[u][a] = {next_state, prob, reward}
// gamma: 折扣因子; epsilon: 收敛阈值。
inline std::vector<double> value_iteration(
    const std::vector<std::vector<std::tuple<int, double, double>>>& transitions,
    std::size_t num_states, std::size_t num_actions,
    double gamma = 0.9, double epsilon = 1e-6) {

    std::vector<double> V(num_states, 0.0);
    while (true) {
        double delta = 0.0;
        for (std::size_t s = 0; s < num_states; ++s) {
            double best = -std::numeric_limits<double>::max();
            for (std::size_t a = 0; a < num_actions; ++a) {
                double val = 0.0;
                for (auto& [ns, prob, reward] : transitions[s * num_actions + a]) {
                    val += prob * (reward + gamma * V[static_cast<std::size_t>(ns)]);
                }
                if (val > best) best = val;
            }
            delta = std::max(delta, std::abs(best - V[s]));
            V[s] = best;
        }
        if (delta < epsilon) break;
    }
    return V;
}

// MDP 策略迭代。
inline std::pair<std::vector<double>, std::vector<int>> policy_iteration(
    const std::vector<std::vector<std::tuple<int, double, double>>>& transitions,
    std::size_t num_states, std::size_t num_actions,
    double gamma = 0.9) {

    std::vector<int> policy(num_states, 0);
    std::vector<double> V(num_states, 0.0);
    bool stable;

    do {
        // 策略评估（简化：迭代直到收敛）
        for (int iter = 0; iter < 1000; ++iter) {
            double delta = 0.0;
            for (std::size_t s = 0; s < num_states; ++s) {
                double val = 0.0;
                int a = policy[s];
                for (auto& [ns, prob, reward] :
                     transitions[s * num_actions + static_cast<std::size_t>(a)]) {
                    val += prob * (reward +
                                   gamma * V[static_cast<std::size_t>(ns)]);
                }
                delta = std::max(delta, std::abs(val - V[s]));
                V[s] = val;
            }
            if (delta < 1e-6) break;
        }

        // 策略改进
        stable = true;
        for (std::size_t s = 0; s < num_states; ++s) {
            int old_action = policy[s];
            double best = -std::numeric_limits<double>::max();
            for (std::size_t a = 0; a < num_actions; ++a) {
                double val = 0.0;
                for (auto& [ns, prob, reward] :
                     transitions[s * num_actions + a]) {
                    val += prob * (reward +
                                   gamma * V[static_cast<std::size_t>(ns)]);
                }
                if (val > best) { best = val; policy[s] = static_cast<int>(a); }
            }
            if (policy[s] != old_action) stable = false;
        }
    } while (!stable);

    return {V, policy};
}

}  // namespace ai
}  // namespace algorithm_x
