#include "algorithm_x/dp/ds_opt_dp.h"

#include <cstdint>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::dp;

namespace {

TEST(MaxSumIncreasingSubsequence, AllIncreasing) {
    // 值本身严格递增，可全取：1+2+3+4 = 10
    EXPECT_EQ(max_sum_increasing_subsequence(std::vector<int>{1, 2, 3, 4},
                                             std::vector<int>{1, 2, 3, 4}),
              10);
}

TEST(MaxSumIncreasingSubsequence, MixedOrder) {
    // 严格递增子序列中最大和的是 1,2,4 → 5+1+3 = 9（值 3 排在 1 之前，不能与 1,2 同取）
    EXPECT_EQ(max_sum_increasing_subsequence(std::vector<int>{3, 1, 2, 4},
                                             std::vector<int>{2, 5, 1, 3}),
              9);
}

TEST(LisCount, StrictlyIncreasing) {
    // 唯一的最长递增子序列 1-2-3，方案数 1
    EXPECT_EQ(lis_count(std::vector<int>{1, 2, 3}), 1);
}

TEST(LisCount, TwoWays) {
    // 最长递增子序列长度 2，两条：1-3 和 2-3，方案数 2
    EXPECT_EQ(lis_count(std::vector<int>{2, 1, 3}), 2);
}

}  // namespace
