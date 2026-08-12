#pragma once

#include <algorithm>
#include <cstddef>
#include <functional>
#include <random>
#include <vector>

namespace algorithm_x {
namespace ai {

// 遗传算法求 f(x) 最大值（x 为 double 向量）。
// pop_size: 种群大小; generations: 迭代代数;
// mutate_rate: 变异概率; crossover_rate: 交叉概率.
inline std::vector<double> genetic_algorithm(
    std::function<double(const std::vector<double>&)> fitness,
    std::size_t dim,
    const std::vector<double>& lower,
    const std::vector<double>& upper,
    std::size_t pop_size = 100, std::size_t generations = 200,
    double mutate_rate = 0.1, double crossover_rate = 0.8) {

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
        scores[i] = fitness(pop[i]);
    }

    for (std::size_t g = 0; g < generations; ++g) {
        std::vector<std::vector<double>> new_pop(pop_size);

        // 精英保留：保留最优个体
        std::size_t best_idx = static_cast<std::size_t>(
            std::max_element(scores.begin(), scores.end()) - scores.begin());
        new_pop[0] = pop[best_idx];

        for (std::size_t i = 1; i < pop_size; ++i) {
            // 锦标赛选择两个父代
            auto select = [&]() {
                std::uniform_int_distribution<int> idx(0, pop_size - 1);
                std::size_t a = idx(gen), b = idx(gen);
                return scores[a] > scores[b] ? pop[a] : pop[b];
            };
            auto p1 = select(), p2 = select();

            auto child = p1;
            if (prob(gen) < crossover_rate) {
                std::uniform_int_distribution<int> cross(0, dim - 1);
                std::size_t cp = cross(gen);
                for (std::size_t d = cp; d < dim; ++d) {
                    child[d] = p2[d];
                }
            }

            // 变异
            for (std::size_t d = 0; d < dim; ++d) {
                if (prob(gen) < mutate_rate) {
                    std::uniform_real_distribution<double> dis(lower[d],
                                                                upper[d]);
                    child[d] = dis(gen);
                }
            }
            new_pop[i] = child;
        }

        pop = std::move(new_pop);
        for (std::size_t i = 0; i < pop_size; ++i) {
            scores[i] = fitness(pop[i]);
        }
    }

    std::size_t best = static_cast<std::size_t>(
        std::max_element(scores.begin(), scores.end()) - scores.begin());
    return pop[best];
}

// 粒子群优化 (PSO) — 求 f(x) 最小值。
inline std::vector<double> particle_swarm(
    std::function<double(const std::vector<double>&)> f,
    std::size_t dim,
    const std::vector<double>& lower,
    const std::vector<double>& upper,
    std::size_t swarm_size = 50, std::size_t iterations = 200) {

    std::mt19937 gen(42);
    double w = 0.7, c1 = 1.5, c2 = 1.5;

    std::vector<std::vector<double>> pos(swarm_size, std::vector<double>(dim));
    std::vector<std::vector<double>> vel(swarm_size, std::vector<double>(dim, 0));
    std::vector<std::vector<double>> pbest_pos = pos;
    std::vector<double> pbest_val(swarm_size);
    std::vector<double> gbest_pos(dim);
    double gbest_val = std::numeric_limits<double>::max();

    for (std::size_t i = 0; i < swarm_size; ++i) {
        for (std::size_t d = 0; d < dim; ++d) {
            std::uniform_real_distribution<double> dis(lower[d], upper[d]);
            pos[i][d] = dis(gen);
        }
        pbest_pos[i] = pos[i];
        pbest_val[i] = f(pos[i]);
        if (pbest_val[i] < gbest_val) {
            gbest_val = pbest_val[i];
            gbest_pos = pos[i];
        }
    }

    std::uniform_real_distribution<double> r(0.0, 1.0);
    for (std::size_t iter = 0; iter < iterations; ++iter) {
        for (std::size_t i = 0; i < swarm_size; ++i) {
            for (std::size_t d = 0; d < dim; ++d) {
                double r1 = r(gen), r2 = r(gen);
                vel[i][d] = w * vel[i][d] +
                            c1 * r1 * (pbest_pos[i][d] - pos[i][d]) +
                            c2 * r2 * (gbest_pos[d] - pos[i][d]);
                pos[i][d] += vel[i][d];
                pos[i][d] = std::clamp(pos[i][d], lower[d], upper[d]);
            }
            double val = f(pos[i]);
            if (val < pbest_val[i]) {
                pbest_val[i] = val;
                pbest_pos[i] = pos[i];
                if (val < gbest_val) {
                    gbest_val = val;
                    gbest_pos = pos[i];
                }
            }
        }
    }
    return gbest_pos;
}

}  // namespace ai
}  // namespace algorithm_x
