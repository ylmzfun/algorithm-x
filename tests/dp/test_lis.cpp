#include "algorithm_x/dp/lis.h"

#include <algorithm>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::dp;

namespace {

TEST(LisLength, Basic) {
    EXPECT_EQ(lis_length(std::vector<int>{10, 9, 2, 5, 3, 7, 101, 18}), 4u);
}

TEST(LisLength, Mixed) {
    EXPECT_EQ(lis_length(std::vector<int>{0, 1, 0, 3, 2, 3}), 4u);
}

TEST(LisLength, AllEqual) {
    EXPECT_EQ(lis_length(std::vector<int>{7, 7, 7, 7}), 1u);
}

TEST(LisLength, StrictlyIncreasing) {
    EXPECT_EQ(lis_length(std::vector<int>{1, 2, 3, 4, 5}), 5u);
}

TEST(LisLength, Empty) {
    EXPECT_EQ(lis_length(std::vector<int>{}), 0u);
}

TEST(LisSequence, Basic) {
    std::vector<int> nums = {10, 9, 2, 5, 3, 7, 101, 18};
    auto seq = lis_sequence(nums);
    EXPECT_EQ(seq.size(), lis_length(nums));
    EXPECT_TRUE(std::is_sorted(seq.begin(), seq.end()));
    for (int x : seq) {
        EXPECT_NE(std::find(nums.begin(), nums.end(), x), nums.end());
    }
}

TEST(LisSequence, Mixed) {
    std::vector<int> nums = {0, 1, 0, 3, 2, 3};
    auto seq = lis_sequence(nums);
    EXPECT_EQ(seq.size(), lis_length(nums));
    EXPECT_TRUE(std::is_sorted(seq.begin(), seq.end()));
    for (int x : seq) {
        EXPECT_NE(std::find(nums.begin(), nums.end(), x), nums.end());
    }
}

TEST(LisSequence, Empty) {
    auto seq = lis_sequence(std::vector<int>{});
    EXPECT_TRUE(seq.empty());
}

TEST(LisSequence, SingleElement) {
    auto seq = lis_sequence(std::vector<int>{42});
    EXPECT_EQ(seq.size(), 1u);
    EXPECT_EQ(seq[0], 42);
}

TEST(MaxSubarraySum, Classic) {
    EXPECT_EQ(max_subarray_sum(std::vector<int>{-2, 1, -3, 4, -1, 2, 1, -5, 4}),
              6);
}

TEST(MaxSubarraySum, SinglePositive) {
    EXPECT_EQ(max_subarray_sum(std::vector<int>{1}), 1);
}

TEST(MaxSubarraySum, SingleNegative) {
    EXPECT_EQ(max_subarray_sum(std::vector<int>{-1}), -1);
}

TEST(MaxSubarraySum, AllNegative) {
    EXPECT_EQ(max_subarray_sum(std::vector<int>{-3, -1, -2}), -1);
}

TEST(MaxSubarraySum, Empty) {
    EXPECT_EQ(max_subarray_sum(std::vector<int>{}), 0);
}

}  // namespace
