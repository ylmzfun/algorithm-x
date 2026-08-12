#include "algo/greedy.h"

#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::algo;

namespace {

// ============================================================
// activity_selection
// ============================================================

TEST(ActivitySelection, StandardExample) {
    std::vector<int> start = {1, 3, 0, 5, 8, 5};
    std::vector<int> finish = {2, 4, 6, 7, 9, 9};
    auto selected = activity_selection(start, finish);
    EXPECT_FALSE(selected.empty());
    // Verify no overlap among selected activities
    for (std::size_t i = 1; i < selected.size(); ++i) {
        std::size_t prev = selected[i - 1];
        std::size_t cur = selected[i];
        EXPECT_GE(start[cur], finish[prev]);
    }
}

TEST(ActivitySelection, Empty) {
    std::vector<int> start, finish;
    auto selected = activity_selection(start, finish);
    EXPECT_TRUE(selected.empty());
}

TEST(ActivitySelection, SingleActivity) {
    std::vector<int> start = {2};
    std::vector<int> finish = {5};
    auto selected = activity_selection(start, finish);
    EXPECT_EQ(selected.size(), 1u);
    EXPECT_EQ(selected[0], 0u);
}

TEST(ActivitySelection, AllNonOverlapping) {
    std::vector<int> start  = {1, 3, 6};
    std::vector<int> finish = {2, 5, 8};
    auto selected = activity_selection(start, finish);
    EXPECT_EQ(selected.size(), 3u);
}

TEST(ActivitySelection, AllOverlapping) {
    std::vector<int> start  = {1, 1, 1};
    std::vector<int> finish = {5, 5, 5};
    auto selected = activity_selection(start, finish);
    EXPECT_EQ(selected.size(), 1u);
}

// ============================================================
// fractional_knapsack
// ============================================================

TEST(FractionalKnapsack, StandardCase) {
    std::vector<double> weights = {10, 20, 30};
    std::vector<double> values  = {60, 100, 120};
    double max_val = fractional_knapsack(weights, values, 50.0);
    EXPECT_NEAR(max_val, 240.0, 1e-9);
}

TEST(FractionalKnapsack, PartialItem) {
    std::vector<double> weights = {30, 40};
    std::vector<double> values  = {90, 100};
    double max_val = fractional_knapsack(weights, values, 20.0);
    EXPECT_NEAR(max_val, 60.0, 1e-9);  // take 20/30 of first item
}

TEST(FractionalKnapsack, ZeroCapacity) {
    std::vector<double> weights = {10, 20};
    std::vector<double> values  = {60, 100};
    double max_val = fractional_knapsack(weights, values, 0.0);
    EXPECT_NEAR(max_val, 0.0, 1e-9);
}

TEST(FractionalKnapsack, SingleItemFits) {
    std::vector<double> weights = {5};
    std::vector<double> values  = {50};
    double max_val = fractional_knapsack(weights, values, 10.0);
    EXPECT_NEAR(max_val, 50.0, 1e-9);
}

// ============================================================
// coin_change_greedy
// ============================================================

TEST(CoinChangeGreedy, CanonicalSystem) {
    std::vector<int> coins = {25, 10, 5, 1};
    auto result = coin_change_greedy(63, coins);
    ASSERT_EQ(result.size(), 4u);
    EXPECT_EQ(result[0], 2);  // 2 × 25
    EXPECT_EQ(result[1], 1);  // 1 × 10
    EXPECT_EQ(result[2], 0);  // 0 × 5
    EXPECT_EQ(result[3], 3);  // 3 × 1
}

TEST(CoinChangeGreedy, ZeroAmount) {
    std::vector<int> coins = {25, 10, 5, 1};
    auto result = coin_change_greedy(0, coins);
    ASSERT_EQ(result.size(), 4u);
    for (int c : result) EXPECT_EQ(c, 0);
}

TEST(CoinChangeGreedy, NonCanonicalSystem) {
    // Greedy may be suboptimal but should not crash
    std::vector<int> coins = {4, 3, 1};
    auto result = coin_change_greedy(6, coins);
    ASSERT_EQ(result.size(), 3u);
    // Greedy: 4+1+1 = 6 → {1, 0, 2}; verify sum matches
    int sum = result[0] * 4 + result[1] * 3 + result[2] * 1;
    EXPECT_EQ(sum, 6);
}

TEST(CoinChangeGreedy, ImpossibleCoinsAreZero) {
    // Greedy cannot make 7 with coins {5, 3} (no 1-cent)
    std::vector<int> coins = {5, 3};
    auto result = coin_change_greedy(7, coins);
    // Function returns empty when impossible to make
    EXPECT_TRUE(result.empty());
}

}  // namespace
