#pragma once

#include <algorithm>
#include <cstddef>
#include <functional>
#include <random>
#include <vector>

namespace algorithm_x {
namespace ai {

// 差分进化 (DE) — 最小化 f(x)。
inline std::vector<double> differential_evolution(
    std::function<double(const std::vector<double>&)> f,
    std::size_t dim,
    const std::vector<double>& lower,
    const std::vector<double>& upper,
    std::size_t pop_size = 50, std::size_t generations = 200,
    double F = 0.8, double CR = 0.9) {

    std::mt19937 gen(42);
    std::uniform_real_distribution<double> prob(0.0, 1.0);

    // 初始化种群
    std::vector<std::vector<double>> pop(pop_size);
    std::vector<double> scores(pop_size);
    for (std::size_t i = 0; i < pop_size; ++i) {
        pop[i].resize(dim);
        for (std::size_t d = 0; d < dim; ++d) {
            std::uniform_real_distribution<double> dis(lower[d], upper[d]);
            pop[i][d] = dis(gen);
        }
        scores[i] = f(pop[i]);
    }

    for (std::size_t g = 0; g < generations; ++g) {
        for (std::size_t i = 0; i < pop_size; ++i) {
            // 选三个不同的随机个体
            std::uniform_int_distribution<std::size_t> idx(0, pop_size - 1);
            std::size_t a, b, c;
            do { a = idx(gen); } while (a == i);
            do { b = idx(gen); } while (b == i || b == a);
            do { c = idx(gen); } while (c == i || c == a || c == b);

            std::uniform_int_distribution<std::size_t> dim_idx(0, dim - 1);
            std::size_t R = dim_idx(gen);

            std::vector<double> trial = pop[i];
            for (std::size_t d = 0; d < dim; ++d) {
                if (prob(gen) < CR || d == R) {
                    trial[d] = std::clamp(
                        pop[a][d] + F * (pop[b][d] - pop[c][d]),
                        lower[d], upper[d]);
                }
            }

            double trial_score = f(trial);
            if (trial_score < scores[i]) {
                pop[i] = trial;
                scores[i] = trial_score;
            }
        }
    }

    std::size_t best = static_cast<std::size_t>(
        std::min_element(scores.begin(), scores.end()) - scores.begin());
    return pop[best];
}

}  // namespace ai
}  // namespace algorithm_x
