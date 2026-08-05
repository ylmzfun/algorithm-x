#include "algorithm_x/ai/search.h"

#include <algorithm>
#include <cmath>
#include <functional>
#include <utility>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::ai;

namespace {

TEST(AStar, SimplePath) {
    std::vector<std::vector<int>> grid = {
        {0, 0, 0},
        {0, 0, 0},
        {0, 0, 0},
    };
    auto path = astar(grid, {0, 0}, {2, 2});
    ASSERT_FALSE(path.empty());
    EXPECT_EQ(path.front(), (GridPos{0, 0}));
    EXPECT_EQ(path.back(), (GridPos{2, 2}));
}

TEST(AStar, ObstacleDetour) {
    std::vector<std::vector<int>> grid = {
        {0, 0, 0},
        {0, 1, 0},
        {0, 0, 0},
    };
    auto path = astar(grid, {0, 0}, {2, 2});
    ASSERT_FALSE(path.empty());
    EXPECT_EQ(path.front(), (GridPos{0, 0}));
    EXPECT_EQ(path.back(), (GridPos{2, 2}));

    // Verify no position in path is an obstacle.
    for (const auto& p : path) {
        EXPECT_EQ(grid[static_cast<std::size_t>(p.r)]
                      [static_cast<std::size_t>(p.c)],
                  0);
    }

    // Verify adjacent steps differ by exactly one Manhattan unit.
    for (std::size_t i = 1; i < path.size(); ++i) {
        int dr = std::abs(path[i].r - path[i - 1].r);
        int dc = std::abs(path[i].c - path[i - 1].c);
        EXPECT_EQ(dr + dc, 1);
    }
}

TEST(AStar, GoalBlocked) {
    std::vector<std::vector<int>> grid = {
        {0, 0},
        {0, 1},
    };
    auto path = astar(grid, {0, 0}, {1, 1});
    EXPECT_TRUE(path.empty());
}

TEST(AStar, StartEqualsGoal) {
    std::vector<std::vector<int>> grid = {{0, 0}, {0, 0}};
    auto path = astar(grid, {0, 0}, {0, 0});
    ASSERT_FALSE(path.empty());
    EXPECT_EQ(path.front(), (GridPos{0, 0}));
}

TEST(SimulatedAnnealing, QuadraticOrigin) {
    auto f = [](double x) { return x * x; };
    double result = simulated_annealing(f, -5.0, 5.0, 20000);
    EXPECT_NEAR(result, 0.0, 0.5);
}

TEST(SimulatedAnnealing, ShiftedQuadratic) {
    auto f = [](double x) { return (x - 3.0) * (x - 3.0); };
    double result = simulated_annealing(f, -10.0, 10.0, 20000);
    EXPECT_NEAR(result, 3.0, 0.5);
}

}  // namespace
