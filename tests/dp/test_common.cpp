#include "dp/common.h"

#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::dp;

namespace {

TEST(MatrixChainOrder, Standard) {
    std::vector<int> dims = {10, 20, 30, 40, 30};
    EXPECT_EQ(matrix_chain_order(dims), 30000);
}

TEST(MatrixChainOrder, ThreeMatrices) {
    std::vector<int> dims = {10, 20, 30};
    EXPECT_EQ(matrix_chain_order(dims), 6000);
}

TEST(MatrixChainOrder, SingleMatrix) {
    std::vector<int> dims = {5, 10};
    EXPECT_EQ(matrix_chain_order(dims), 0);
}

TEST(MatrixChainOrder, Empty) {
    std::vector<int> dims = {5};
    EXPECT_EQ(matrix_chain_order(dims), 0);
}

TEST(CoinChangeDP, Amount11) {
    std::vector<int> coins = {1, 2, 5};
    EXPECT_EQ(coin_change_dp(coins, 11), 3);
}

TEST(CoinChangeDP, AmountZero) {
    std::vector<int> coins = {1, 2, 5};
    EXPECT_EQ(coin_change_dp(coins, 0), 0);
}

TEST(CoinChangeDP, Impossible) {
    std::vector<int> coins = {2};
    EXPECT_EQ(coin_change_dp(coins, 3), -1);
}

TEST(CoinChangeDP, LargeAmount) {
    std::vector<int> coins = {1};
    EXPECT_EQ(coin_change_dp(coins, 100), 100);
}

TEST(BurstBalloons, Standard) {
    std::vector<int> nums = {3, 1, 5, 8};
    EXPECT_EQ(burst_balloons(nums), 167);
}

TEST(BurstBalloons, Single) {
    std::vector<int> nums = {5};
    EXPECT_EQ(burst_balloons(nums), 5);
}

TEST(BurstBalloons, Two) {
    std::vector<int> nums = {3, 8};
    EXPECT_EQ(burst_balloons(nums), 3 * 8 + std::max(3, 8));
}

}  // namespace
