#include "algorithm_x/algo/branch_and_bound.h"

#include <algorithm>
#include <cstddef>
#include <random>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::algo;

namespace {

// 朴素 O(n * cap) 的 0-1 背包 DP，作为分支限界结果的基准。
int naive_knapsack_dp(const std::vector<int>& weights,
                      const std::vector<int>& values, int capacity) {
    std::vector<int> dp(static_cast<std::size_t>(capacity) + 1, 0);
    for (std::size_t i = 0; i < weights.size(); ++i) {
        for (int c = capacity; c >= weights[i]; --c) {
            dp[static_cast<std::size_t>(c)] =
                std::max(dp[static_cast<std::size_t>(c)],
                         dp[static_cast<std::size_t>(c - weights[i])] + values[i]);
        }
    }
    return dp[static_cast<std::size_t>(capacity)];
}

TEST(BranchAndBoundKnapsack, KnownExample) {
    // weights = {2,3,4,5}, values = {3,4,5,6}, capacity = 5 -> 7
    EXPECT_EQ(branch_and_bound_knapsack({2, 3, 4, 5}, {3, 4, 5, 6}, 5), 7);
}

TEST(BranchAndBoundKnapsack, EdgeCases) {
    EXPECT_EQ(branch_and_bound_knapsack({}, {}, 5), 0);
    EXPECT_EQ(branch_and_bound_knapsack({2, 3}, {4, 5}, 0), 0);
    EXPECT_EQ(branch_and_bound_knapsack({2, 3}, {4, 5}, -1), 0);
}

TEST(BranchAndBoundKnapsack, ZeroWeightItem) {
    // 零重物品免费取走，价值 7；剩余容量 5 内取 {2,3} -> 3 + 4 = 7，合计 14
    EXPECT_EQ(branch_and_bound_knapsack({0, 2, 3}, {7, 3, 4}, 5), 14);
}

TEST(BranchAndBoundKnapsack, MatchesNaiveDPOnRandomCases) {
    std::mt19937 rng(20240812);
    std::uniform_int_distribution<int> n_dist(1, 10);
    std::uniform_int_distribution<int> w_dist(1, 10);
    std::uniform_int_distribution<int> v_dist(0, 12);
    std::uniform_int_distribution<int> cap_dist(0, 20);
    for (int t = 0; t < 200; ++t) {
        const int n = n_dist(rng);
        std::vector<int> weights(static_cast<std::size_t>(n));
        std::vector<int> values(static_cast<std::size_t>(n));
        for (int i = 0; i < n; ++i) {
            weights[static_cast<std::size_t>(i)] = w_dist(rng);
            values[static_cast<std::size_t>(i)] = v_dist(rng);
        }
        const int cap = cap_dist(rng);
        EXPECT_EQ(branch_and_bound_knapsack(weights, values, cap),
                  naive_knapsack_dp(weights, values, cap))
            << "case " << t << ": cap = " << cap;
    }
}

}  // namespace
