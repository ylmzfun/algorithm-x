#include "algorithm_x/advanced/complexity.h"

#include <vector>

#include "gtest/gtest.h"
using namespace algorithm_x::advanced;
namespace {
TEST(SubsetSum, BruteForce) {
    std::vector<int> nums = {3, 34, 4, 12, 5, 2};
    EXPECT_TRUE(subset_sum_brute(nums, 9));    // 4 + 5 = 9
    EXPECT_TRUE(subset_sum_brute(nums, 36));   // 34 + 2 = 36
    EXPECT_TRUE(subset_sum_brute(nums, 0));    // 空子集
    EXPECT_FALSE(subset_sum_brute(nums, 30));  // 无 34 时最大和为 26
    EXPECT_FALSE(subset_sum_brute(nums, 1));   // 集合中没有 1
}

TEST(SubsetSum, Verify) {
    std::vector<int> nums = {3, 34, 4, 12, 5, 2};
    // 合法解：nums[2] + nums[4] = 4 + 5 = 9
    EXPECT_TRUE(subset_sum_verify(nums, 9, {2, 4}));
    // 和不对：3 + 4 + 5 = 12 != 9
    EXPECT_FALSE(subset_sum_verify(nums, 9, {0, 2, 4}));
    // 下标越界
    EXPECT_FALSE(subset_sum_verify(nums, 9, {2, 6}));
    // 负数下标
    EXPECT_FALSE(subset_sum_verify(nums, 9, {-1, 2}));
    // 下标重复
    EXPECT_FALSE(subset_sum_verify(nums, 4, {2, 2}));
    // 空候选解：和为 0
    EXPECT_TRUE(subset_sum_verify(nums, 0, {}));
    // 空候选解配非 0 目标
    EXPECT_FALSE(subset_sum_verify(nums, 5, {}));
}

TEST(Tsp, BruteForce) {
    // 4 城距离矩阵，最优回路 0->1->3->2->0 = 10+25+30+15 = 80。
    std::vector<std::vector<int>> dist = {
        {0, 10, 15, 20},
        {10, 0, 35, 25},
        {15, 35, 0, 30},
        {20, 25, 30, 0},
    };
    EXPECT_EQ(tsp_brute_force(dist), 80);
    // 单城 / 两城边界。
    EXPECT_EQ(tsp_brute_force({{0}}), 0);
    EXPECT_EQ(tsp_brute_force({{0, 5}, {5, 0}}), 10);
}
}  // namespace
