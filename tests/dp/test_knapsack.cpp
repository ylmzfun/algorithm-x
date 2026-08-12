#include "dp/knapsack.h"

#include <numeric>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::dp;

namespace {

// ---- 0-1 Knapsack ----------------------------------------------------------

TEST(Knapsack01, Classic) {
    std::vector<int> w = {10, 20, 30};
    std::vector<int> v = {60, 100, 120};
    EXPECT_EQ(knapsack_01(w, v, 50), 220);  // items 1 + 2
}

TEST(Knapsack01, ZeroCapacity) {
    std::vector<int> w = {10, 20};
    std::vector<int> v = {60, 100};
    EXPECT_EQ(knapsack_01(w, v, 0), 0);
}

TEST(Knapsack01, EmptyItems) {
    EXPECT_EQ(knapsack_01({}, {}, 50), 0);
}

TEST(Knapsack01, SingleItemFits) {
    EXPECT_EQ(knapsack_01({5}, {10}, 10), 10);
}

TEST(Knapsack01, SingleItemTooHeavy) {
    EXPECT_EQ(knapsack_01({15}, {10}, 10), 0);
}

// ---- 0-1 Knapsack with item recovery ----------------------------------------

TEST(Knapsack01WithItems, MatchesBasic) {
    std::vector<int> w = {10, 20, 30};
    std::vector<int> v = {60, 100, 120};
    auto [val, items] = knapsack_01_with_items(w, v, 50);
    EXPECT_EQ(val, knapsack_01(w, v, 50));
    int total_w = 0, total_v = 0;
    for (auto i : items) {
        total_w += w[i];
        total_v += v[i];
    }
    EXPECT_LE(total_w, 50);
    EXPECT_EQ(total_v, val);
}

TEST(Knapsack01WithItems, NoItems) {
    auto [val, items] = knapsack_01_with_items({5}, {10}, 1);
    EXPECT_EQ(val, 0);
    EXPECT_TRUE(items.empty());
}

// ---- Complete Knapsack ------------------------------------------------------

TEST(KnapsackComplete, Classic) {
    // capacity=4, weight={1,2}, value={1,3}
    // Best: 2 × item1 = value 6
    EXPECT_EQ(knapsack_complete({1, 2}, {1, 3}, 4), 6);
}

TEST(KnapsackComplete, ZeroCapacity) {
    EXPECT_EQ(knapsack_complete({1, 2}, {1, 3}, 0), 0);
}

TEST(KnapsackComplete, TakeAllSame) {
    EXPECT_EQ(knapsack_complete({2}, {5}, 6), 15);  // 3 × 5
}

// ---- Multiple Knapsack (binary splitting) -----------------------------------

TEST(KnapsackMultiple, LimitedByCount) {
    // capacity=4, weight={1}, value={1}, count={3}
    // Can take at most 3 items → value 3
    EXPECT_EQ(knapsack_multiple({1}, {1}, {3}, 4), 3);
}

TEST(KnapsackMultiple, Comprehensive) {
    // capacity=8, weights={2,3,4}, values={3,4,5}, counts={3,2,1}
    std::vector<int> w = {2, 3, 4};
    std::vector<int> v = {3, 4, 5};
    std::vector<int> c = {3, 2, 1};
    int result = knapsack_multiple(w, v, c, 8);
    // Brute-force verify
    int best = 0;
    for (int c0 = 0; c0 <= c[0]; ++c0)
        for (int c1 = 0; c1 <= c[1]; ++c1)
            for (int c2 = 0; c2 <= c[2]; ++c2) {
                int tw = c0 * w[0] + c1 * w[1] + c2 * w[2];
                int tv = c0 * v[0] + c1 * v[1] + c2 * v[2];
                if (tw <= 8) best = std::max(best, tv);
            }
    EXPECT_EQ(result, best);
}

TEST(KnapsackMultiple, ZeroCapacity) {
    EXPECT_EQ(knapsack_multiple({1}, {1}, {1}, 0), 0);
}

}  // namespace
