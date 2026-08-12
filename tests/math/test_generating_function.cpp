#include "math/generating_function.h"

#include <cstdint>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::math;

namespace {

TEST(GeneratingFunctionWays, KnownCombinations) {
    // weights = {1, 2, 3}，总重量 4 的拆法：1+1+1+1、1+1+2、1+3、2+2，共 4 种
    std::vector<int64_t> ways = generating_function_ways(std::vector<int>{1, 2, 3}, 4);
    EXPECT_EQ(ways[0], 1);
    EXPECT_EQ(ways[3], 3);
    EXPECT_EQ(ways[4], 4);
}

TEST(GeneratingFunctionWays, SingleWeightOne) {
    // weights = {1}：任何总重量都只有 1 种方案（全部用重量 1）
    std::vector<int64_t> ways = generating_function_ways(std::vector<int>{1}, 5);
    for (int s = 0; s <= 5; ++s) {
        EXPECT_EQ(ways[static_cast<std::size_t>(s)], 1);
    }
}

TEST(GeneratingFunctionWays, SingleWeightTwo) {
    // weights = {2}：只能组成偶数总重量
    std::vector<int64_t> ways = generating_function_ways(std::vector<int>{2}, 5);
    EXPECT_EQ(ways[0], 1);
    EXPECT_EQ(ways[4], 1);
    EXPECT_EQ(ways[5], 0);
}

TEST(GeneratingFunctionWays, NegativeMaxSum) {
    EXPECT_TRUE(generating_function_ways(std::vector<int>{1, 2}, -1).empty());
}

}  // namespace
