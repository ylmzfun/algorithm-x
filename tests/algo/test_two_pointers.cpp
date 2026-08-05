#include "algorithm_x/algo/two_pointers.h"

#include <gtest/gtest.h>
#include <vector>

using namespace algorithm_x::algo;

// ============================================================
// two_sum_sorted
// ============================================================

TEST(TwoSumSorted, Found) {
    std::vector<int> arr = {1, 2, 3, 4, 6};
    auto [i, j] = two_sum_sorted(arr, 6);
    EXPECT_EQ(i, 1);
    EXPECT_EQ(j, 3);
}

TEST(TwoSumSorted, NotFound) {
    std::vector<int> arr = {1, 2, 3, 4};
    auto [i, j] = two_sum_sorted(arr, 10);
    EXPECT_EQ(i, -1);
    EXPECT_EQ(j, -1);
}

TEST(TwoSumSorted, MultipleSolutions) {
    std::vector<int> arr = {1, 1, 2, 3, 4, 4};
    auto [i, j] = two_sum_sorted(arr, 5);
    EXPECT_GE(i, 0);
    EXPECT_GE(j, 0);
    EXPECT_EQ(arr[static_cast<std::size_t>(i)] + arr[static_cast<std::size_t>(j)], 5);
}

TEST(TwoSumSorted, FirstTwo) {
    std::vector<int> arr = {1, 2, 5, 10};
    auto [i, j] = two_sum_sorted(arr, 3);
    EXPECT_EQ(i, 0);
    EXPECT_EQ(j, 1);
}

TEST(TwoSumSorted, LastTwo) {
    std::vector<int> arr = {1, 3, 5, 7};
    auto [i, j] = two_sum_sorted(arr, 12);
    EXPECT_EQ(i, 2);
    EXPECT_EQ(j, 3);
}

TEST(TwoSumSorted, SingleElement) {
    std::vector<int> arr = {5};
    auto [i, j] = two_sum_sorted(arr, 10);
    EXPECT_EQ(i, -1);
    EXPECT_EQ(j, -1);
}

TEST(TwoSumSorted, Empty) {
    std::vector<int> arr;
    auto [i, j] = two_sum_sorted(arr, 0);
    EXPECT_EQ(i, -1);
    EXPECT_EQ(j, -1);
}

// ============================================================
// remove_duplicates
// ============================================================

TEST(RemoveDuplicates, NoDuplicates) {
    std::vector<int> arr = {1, 2, 3, 4};
    auto len = remove_duplicates(arr);
    EXPECT_EQ(len, 4u);
    std::vector<int> expected = {1, 2, 3, 4};
    for (std::size_t i = 0; i < len; ++i) EXPECT_EQ(arr[i], expected[i]);
}

TEST(RemoveDuplicates, AllDuplicates) {
    std::vector<int> arr = {5, 5, 5, 5};
    auto len = remove_duplicates(arr);
    EXPECT_EQ(len, 1u);
    EXPECT_EQ(arr[0], 5);
}

TEST(RemoveDuplicates, SomeDuplicates) {
    std::vector<int> arr = {0, 0, 1, 1, 1, 2, 2, 3, 3, 4};
    auto len = remove_duplicates(arr);
    EXPECT_EQ(len, 5u);
    std::vector<int> expected = {0, 1, 2, 3, 4};
    for (std::size_t i = 0; i < len; ++i) EXPECT_EQ(arr[i], expected[i]);
}

TEST(RemoveDuplicates, SingleElement) {
    std::vector<int> arr = {7};
    auto len = remove_duplicates(arr);
    EXPECT_EQ(len, 1u);
    EXPECT_EQ(arr[0], 7);
}

TEST(RemoveDuplicates, Empty) {
    std::vector<int> arr;
    auto len = remove_duplicates(arr);
    EXPECT_EQ(len, 0u);
}

// ============================================================
// max_sum_fixed_window
// ============================================================

TEST(MaxSumFixedWindow, Normal) {
    std::vector<int> arr = {1, 4, 2, 10, 23, 3, 1, 0, 20};
    EXPECT_EQ(max_sum_fixed_window(arr, 4), 39);
}

TEST(MaxSumFixedWindow, KEqualsOne) {
    std::vector<int> arr = {1, 5, 3, 9};
    EXPECT_EQ(max_sum_fixed_window(arr, 1), 9);
}

TEST(MaxSumFixedWindow, KEqualsN) {
    std::vector<int> arr = {1, 2, 3};
    EXPECT_EQ(max_sum_fixed_window(arr, 3), 6);
}

TEST(MaxSumFixedWindow, KLargerThanN) {
    std::vector<int> arr = {1, 2, 3};
    EXPECT_EQ(max_sum_fixed_window(arr, 5), 0);
}

TEST(MaxSumFixedWindow, NegativeValues) {
    std::vector<int> arr = {-1, -4, -2, -10, -3};
    EXPECT_EQ(max_sum_fixed_window(arr, 3), -7);
    // windows: -1-4-2=-7, -4-2-10=-16, -2-10-3=-15. Max is -7.
}

TEST(MaxSumFixedWindow, AllSame) {
    std::vector<int> arr = {5, 5, 5, 5};
    EXPECT_EQ(max_sum_fixed_window(arr, 2), 10);
}

// ============================================================
// min_subarray_len
// ============================================================

TEST(MinSubarrayLen, Normal) {
    std::vector<int> arr = {2, 3, 1, 2, 4, 3};
    EXPECT_EQ(min_subarray_len(arr, 7), 2u);
}

TEST(MinSubarrayLen, ExactMatch) {
    std::vector<int> arr = {1, 2, 3, 4};
    EXPECT_EQ(min_subarray_len(arr, 10), 4u);
}

TEST(MinSubarrayLen, NoSolution) {
    std::vector<int> arr = {1, 2, 3};
    EXPECT_EQ(min_subarray_len(arr, 100), 0u);
}

TEST(MinSubarrayLen, TargetGreaterThanSum) {
    std::vector<int> arr = {1, 1, 1, 1};
    EXPECT_EQ(min_subarray_len(arr, 10), 0u);
}

TEST(MinSubarrayLen, SingleElementEqTarget) {
    std::vector<int> arr = {5, 1, 2, 3};
    EXPECT_EQ(min_subarray_len(arr, 5), 1u);
}

// ============================================================
// PrefixSum
// ============================================================

TEST(PrefixSum, FullRange) {
    PrefixSum<int> ps({1, 2, 3, 4, 5});
    EXPECT_EQ(ps.query(0, 5), 15);
}

TEST(PrefixSum, SingleElement) {
    PrefixSum<int> ps({10, 20, 30});
    EXPECT_EQ(ps.query(1, 2), 20);
}

TEST(PrefixSum, EmptyRange) {
    PrefixSum<int> ps({1, 2, 3});
    EXPECT_EQ(ps.query(1, 1), 0);
    EXPECT_EQ(ps.query(0, 0), 0);
}

TEST(PrefixSum, Suffix) {
    PrefixSum<int> ps({1, 2, 3, 4, 5});
    EXPECT_EQ(ps.query(3, 5), 9);  // 4 + 5
}

// ============================================================
// PrefixSum2D
// ============================================================

TEST(PrefixSum2D, TwoByTwo) {
    std::vector<std::vector<int>> mat = {
        {1, 2},
        {3, 4},
    };
    PrefixSum2D<int> ps(mat);
    EXPECT_EQ(ps.query(0, 0, 2, 2), 10);
    EXPECT_EQ(ps.query(0, 1, 2, 2), 6);   // col 1: 2 + 4
    EXPECT_EQ(ps.query(1, 0, 2, 2), 7);   // row 1: 3 + 4
    EXPECT_EQ(ps.query(0, 0, 1, 1), 1);   // top-left
}

TEST(PrefixSum2D, ThreeByThree) {
    std::vector<std::vector<int>> mat = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9},
    };
    PrefixSum2D<int> ps(mat);
    EXPECT_EQ(ps.query(0, 0, 3, 3), 45);
    EXPECT_EQ(ps.query(0, 0, 2, 2), 12);    // [1,2;4,5]
    EXPECT_EQ(ps.query(1, 1, 3, 3), 28);    // [5,6;8,9]
    EXPECT_EQ(ps.query(1, 1, 2, 3), 11);    // [5,6]
}

TEST(PrefixSum2D, SingleCell) {
    std::vector<std::vector<int>> mat = {{5}};
    PrefixSum2D<int> ps(mat);
    EXPECT_EQ(ps.query(0, 0, 1, 1), 5);
}

TEST(PrefixSum2D, EmptySubmatrix) {
    std::vector<std::vector<int>> mat = {
        {1, 2},
        {3, 4},
    };
    PrefixSum2D<int> ps(mat);
    EXPECT_EQ(ps.query(1, 1, 1, 1), 0);  // r1 == r2
    EXPECT_EQ(ps.query(0, 0, 0, 1), 0);  // r1 == r2
    EXPECT_EQ(ps.query(0, 0, 1, 0), 0);  // c1 == c2
}

// ============================================================
// DifferenceArray
// ============================================================

TEST(DifferenceArray, AddMiddle) {
    std::vector<int> arr = {1, 2, 3, 4, 5};
    DifferenceArray<int> da(arr);
    da.add(1, 3, 10);
    auto res = da.restore();
    std::vector<int> expected = {1, 12, 13, 14, 5};
    EXPECT_EQ(res, expected);
}

TEST(DifferenceArray, AddPrefix) {
    std::vector<int> arr = {1, 2, 3, 4};
    DifferenceArray<int> da(arr);
    da.add(0, 1, 5);
    auto res = da.restore();
    std::vector<int> expected = {6, 7, 3, 4};
    EXPECT_EQ(res, expected);
}

TEST(DifferenceArray, AddSuffix) {
    std::vector<int> arr = {1, 2, 3, 4};
    DifferenceArray<int> da(arr);
    da.add(2, 3, 10);
    auto res = da.restore();
    std::vector<int> expected = {1, 2, 13, 14};
    EXPECT_EQ(res, expected);
}

TEST(DifferenceArray, MultipleOverlappingAdds) {
    std::vector<int> arr = {0, 0, 0, 0, 0};
    DifferenceArray<int> da(arr);
    da.add(0, 2, 3);   // [3, 3, 3, 0, 0]
    da.add(1, 4, 1);   // [3, 4, 4, 1, 1]
    auto res = da.restore();
    std::vector<int> expected = {3, 4, 4, 1, 1};
    EXPECT_EQ(res, expected);
}

TEST(DifferenceArray, RestoreVerifies) {
    std::vector<int> arr = {10, 20, 30, 40};
    DifferenceArray<int> da(arr);
    auto res = da.restore();
    EXPECT_EQ(res, arr);  // no modifications
}
