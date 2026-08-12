#include "algo/divide_conquer.h"

#include <functional>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::algo;

namespace {

TEST(MaxSubarraySum, AllPositive) {
    EXPECT_EQ(max_subarray_sum(std::vector<int>{1, 2, 3, 4}), 10);
}

TEST(MaxSubarraySum, AllNegative) {
    EXPECT_EQ(max_subarray_sum(std::vector<int>{-5, -2, -9, -1}), -1);
}

TEST(MaxSubarraySum, Mixed) {
    EXPECT_EQ(max_subarray_sum(std::vector<int>{3, -2, 5, -1}), 6);
}

TEST(MaxSubarraySum, SingleElement) {
    EXPECT_EQ(max_subarray_sum(std::vector<int>{5}), 5);
    EXPECT_EQ(max_subarray_sum(std::vector<int>{-3}), -3);
}

TEST(MaxSubarraySum, Empty) {
    EXPECT_EQ(max_subarray_sum(std::vector<int>{}), 0);
}

TEST(MaxSubarraySum, Classic) {
    EXPECT_EQ(max_subarray_sum(std::vector<int>{-2, 1, -3, 4, -1, 2, 1, -5, 4}), 6);
}

TEST(MaxSubarrayDC, MatchesKadane) {
    std::vector<std::vector<int>> cases = {
        {1, 2, 3, 4},
        {-5, -2, -9, -1},
        {3, -2, 5, -1},
        {-2, 1, -3, 4, -1, 2, 1, -5, 4},
        {5},
        {-3},
        {}
    };
    for (const auto& arr : cases)
        EXPECT_EQ(max_subarray_dc(arr), max_subarray_sum(arr));
}

TEST(Quickselect, MinElement) {
    std::vector<int> arr = {5, 2, 8, 1, 9};
    auto it = quickselect(arr.begin(), arr.end(), 0);
    EXPECT_EQ(*it, 1);
}

TEST(Quickselect, MaxElement) {
    std::vector<int> arr = {5, 2, 8, 1, 9};
    auto it = quickselect(arr.begin(), arr.end(), arr.size() - 1);
    EXPECT_EQ(*it, 9);
}

TEST(Quickselect, MiddleElement) {
    std::vector<int> arr = {5, 2, 8, 1, 9, 3, 7};
    auto it = quickselect(arr.begin(), arr.end(), 3);
    EXPECT_EQ(*it, 5);
}

TEST(Quickselect, Duplicates) {
    std::vector<int> arr = {3, 1, 3, 2, 3};
    auto it = quickselect(arr.begin(), arr.end(), 2);
    EXPECT_EQ(*it, 3);
}

TEST(Quickselect, SingleElement) {
    std::vector<int> arr = {42};
    auto it = quickselect(arr.begin(), arr.end(), 0);
    EXPECT_EQ(*it, 42);
}

TEST(Quickselect, EmptyRange) {
    std::vector<int> arr;
    auto it = quickselect(arr.begin(), arr.end(), 0);
    EXPECT_EQ(it, arr.end());
}

TEST(Quickselect, DescendingComparator) {
    std::vector<int> arr = {5, 2, 8, 1, 9};
    auto it = quickselect(arr.begin(), arr.end(), 0, std::greater<>{});
    EXPECT_EQ(*it, 9);
}

}  // namespace
