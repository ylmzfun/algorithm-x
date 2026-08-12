#include "ai/evolution.h"

#include <cmath>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::ai;

namespace {

TEST(GeneticAlgorithm, MaxQuadratic1D) {
    auto fitness = [](const std::vector<double>& x) {
        return -std::pow(x[0] - 5.0, 2) + 10.0;
    };
    auto result = genetic_algorithm(fitness, 1, {-10.0}, {10.0},
                                    200, 300, 0.05, 0.8);
    EXPECT_NEAR(result[0], 5.0, 0.5);
    EXPECT_NEAR(fitness(result), 10.0, 0.5);
}

TEST(GeneticAlgorithm, MaxQuadratic2D) {
    auto fitness = [](const std::vector<double>& x) {
        return -std::pow(x[0] - 2.0, 2) - std::pow(x[1] - 3.0, 2) + 20.0;
    };
    auto result = genetic_algorithm(fitness, 2, {-10.0, -10.0},
                                    {10.0, 10.0}, 200, 300, 0.05, 0.8);
    EXPECT_NEAR(result[0], 2.0, 0.5);
    EXPECT_NEAR(result[1], 3.0, 0.5);
}

TEST(ParticleSwarm, MinXSquared) {
    auto f = [](const std::vector<double>& x) { return x[0] * x[0]; };
    auto result = particle_swarm(f, 1, {-10.0}, {10.0}, 100, 300);
    EXPECT_NEAR(result[0], 0.0, 0.1);
}

TEST(ParticleSwarm, MinShiftedQuadratic) {
    auto f = [](const std::vector<double>& x) {
        return std::pow(x[0] - 7.0, 2);
    };
    auto result = particle_swarm(f, 1, {-10.0}, {10.0}, 100, 300);
    EXPECT_NEAR(result[0], 7.0, 0.1);
}

TEST(ParticleSwarm, MinSumOfSquares2D) {
    auto f = [](const std::vector<double>& x) {
        return x[0] * x[0] + x[1] * x[1];
    };
    auto result = particle_swarm(f, 2, {-10.0, -10.0},
                                  {10.0, 10.0}, 100, 300);
    EXPECT_NEAR(result[0], 0.0, 0.1);
    EXPECT_NEAR(result[1], 0.0, 0.1);
}

}  // namespace
