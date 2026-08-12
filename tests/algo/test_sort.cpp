#include "algo/sort.h"

#include <algorithm>
#include <functional>
#include <numeric>
#include <random>
#include <vector>

#include "gtest/gtest.h"

namespace {

// ============================================================
// bubble_sort
// ============================================================

TEST(BubbleSort, Empty) {
    std::vector<int> v;
    algorithm_x::algo::bubble_sort(v.begin(), v.end());
    EXPECT_TRUE(v.empty());
}

TEST(BubbleSort, SingleElement) {
    std::vector<int> v{42};
    algorithm_x::algo::bubble_sort(v.begin(), v.end());
    EXPECT_EQ(v, std::vector<int>({42}));
}

TEST(BubbleSort, AlreadySorted) {
    std::vector<int> v{1, 2, 3, 4, 5};
    algorithm_x::algo::bubble_sort(v.begin(), v.end());
    EXPECT_EQ(v, std::vector<int>({1, 2, 3, 4, 5}));
}

TEST(BubbleSort, ReverseSorted) {
    std::vector<int> v{5, 4, 3, 2, 1};
    algorithm_x::algo::bubble_sort(v.begin(), v.end());
    EXPECT_EQ(v, std::vector<int>({1, 2, 3, 4, 5}));
}

TEST(BubbleSort, Random) {
    std::vector<int> v{3, 1, 4, 1, 5, 9, 2, 6};
    algorithm_x::algo::bubble_sort(v.begin(), v.end());
    EXPECT_TRUE(std::is_sorted(v.begin(), v.end()));
}

TEST(BubbleSort, CustomComparator) {
    std::vector<int> v{1, 2, 3, 4, 5};
    algorithm_x::algo::bubble_sort(v.begin(), v.end(), std::greater<>{});
    EXPECT_EQ(v, std::vector<int>({5, 4, 3, 2, 1}));
}

// ============================================================
// selection_sort
// ============================================================

TEST(SelectionSort, Empty) {
    std::vector<int> v;
    algorithm_x::algo::selection_sort(v.begin(), v.end());
    EXPECT_TRUE(v.empty());
}

TEST(SelectionSort, SingleElement) {
    std::vector<int> v{7};
    algorithm_x::algo::selection_sort(v.begin(), v.end());
    EXPECT_EQ(v, std::vector<int>({7}));
}

TEST(SelectionSort, AlreadySorted) {
    std::vector<int> v{1, 2, 3, 4, 5};
    algorithm_x::algo::selection_sort(v.begin(), v.end());
    EXPECT_EQ(v, std::vector<int>({1, 2, 3, 4, 5}));
}

TEST(SelectionSort, ReverseSorted) {
    std::vector<int> v{9, 7, 5, 3, 1};
    algorithm_x::algo::selection_sort(v.begin(), v.end());
    EXPECT_EQ(v, std::vector<int>({1, 3, 5, 7, 9}));
}

TEST(SelectionSort, Random) {
    std::vector<int> v{8, 3, 1, 7, 0, 10, 2};
    algorithm_x::algo::selection_sort(v.begin(), v.end());
    EXPECT_TRUE(std::is_sorted(v.begin(), v.end()));
}

// ============================================================
// insertion_sort
// ============================================================

TEST(InsertionSort, Empty) {
    std::vector<int> v;
    algorithm_x::algo::insertion_sort(v.begin(), v.end());
    EXPECT_TRUE(v.empty());
}

TEST(InsertionSort, SingleElement) {
    std::vector<int> v{99};
    algorithm_x::algo::insertion_sort(v.begin(), v.end());
    EXPECT_EQ(v, std::vector<int>({99}));
}

TEST(InsertionSort, AlreadySorted) {
    std::vector<int> v{1, 2, 3, 4, 5};
    algorithm_x::algo::insertion_sort(v.begin(), v.end());
    EXPECT_TRUE(std::is_sorted(v.begin(), v.end()));
}

TEST(InsertionSort, ReverseSorted) {
    std::vector<int> v{5, 4, 3, 2, 1};
    algorithm_x::algo::insertion_sort(v.begin(), v.end());
    EXPECT_TRUE(std::is_sorted(v.begin(), v.end()));
}

TEST(InsertionSort, MostlySorted) {
    std::vector<int> v{1, 2, 4, 3, 5, 7, 6, 8};
    algorithm_x::algo::insertion_sort(v.begin(), v.end());
    EXPECT_TRUE(std::is_sorted(v.begin(), v.end()));
}

TEST(InsertionSort, Random) {
    std::vector<int> v{5, 2, 8, 1, 9, 3};
    algorithm_x::algo::insertion_sort(v.begin(), v.end());
    EXPECT_TRUE(std::is_sorted(v.begin(), v.end()));
}

// ============================================================
// merge_sort
// ============================================================

TEST(MergeSort, Empty) {
    std::vector<int> v;
    algorithm_x::algo::merge_sort(v.begin(), v.end());
    EXPECT_TRUE(v.empty());
}

TEST(MergeSort, SingleElement) {
    std::vector<int> v{11};
    algorithm_x::algo::merge_sort(v.begin(), v.end());
    EXPECT_EQ(v, std::vector<int>({11}));
}

TEST(MergeSort, AlreadySorted) {
    std::vector<int> v{1, 2, 3, 4, 5};
    algorithm_x::algo::merge_sort(v.begin(), v.end());
    EXPECT_TRUE(std::is_sorted(v.begin(), v.end()));
}

TEST(MergeSort, ReverseSorted) {
    std::vector<int> v{5, 4, 3, 2, 1};
    algorithm_x::algo::merge_sort(v.begin(), v.end());
    EXPECT_TRUE(std::is_sorted(v.begin(), v.end()));
}

TEST(MergeSort, StabilityTest) {
    // Use pairs: (value, original_index). Sort by value and verify
    // equal values retain original index order.
    using Pair = std::pair<int, int>;
    std::vector<Pair> v{{3, 0}, {1, 1}, {2, 2}, {1, 3}, {3, 4}};
    algorithm_x::algo::merge_sort(v.begin(), v.end(),
        [](const Pair& a, const Pair& b) { return a.first < b.first; });
    EXPECT_EQ(v[0], Pair(1, 1));  // first occurrence of 1 has smaller index
    EXPECT_EQ(v[1], Pair(1, 3));
    EXPECT_EQ(v[2], Pair(2, 2));
    EXPECT_EQ(v[3], Pair(3, 0));  // first occurrence of 3
    EXPECT_EQ(v[4], Pair(3, 4));
}

TEST(MergeSort, Random) {
    std::vector<int> v{38, 27, 43, 3, 9, 82, 10};
    algorithm_x::algo::merge_sort(v.begin(), v.end());
    EXPECT_TRUE(std::is_sorted(v.begin(), v.end()));
}

// ============================================================
// quick_sort
// ============================================================

TEST(QuickSort, Empty) {
    std::vector<int> v;
    algorithm_x::algo::quick_sort(v.begin(), v.end());
    EXPECT_TRUE(v.empty());
}

TEST(QuickSort, SingleElement) {
    std::vector<int> v{55};
    algorithm_x::algo::quick_sort(v.begin(), v.end());
    EXPECT_EQ(v, std::vector<int>({55}));
}

TEST(QuickSort, AlreadySorted) {
    std::vector<int> v{1, 2, 3, 4, 5};
    algorithm_x::algo::quick_sort(v.begin(), v.end());
    EXPECT_TRUE(std::is_sorted(v.begin(), v.end()));
}

TEST(QuickSort, ReverseSorted) {
    std::vector<int> v{5, 4, 3, 2, 1};
    algorithm_x::algo::quick_sort(v.begin(), v.end());
    EXPECT_TRUE(std::is_sorted(v.begin(), v.end()));
}

TEST(QuickSort, ManyDuplicates) {
    std::vector<int> v{4, 2, 4, 2, 4, 2, 2, 4, 2, 4};
    algorithm_x::algo::quick_sort(v.begin(), v.end());
    EXPECT_TRUE(std::is_sorted(v.begin(), v.end()));
    EXPECT_EQ(v.front(), 2);
    EXPECT_EQ(v.back(), 4);
}

TEST(QuickSort, LargeRandom) {
    std::vector<int> v(1000);
    std::iota(v.begin(), v.end(), 0);
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(v.begin(), v.end(), g);
    algorithm_x::algo::quick_sort(v.begin(), v.end());
    EXPECT_TRUE(std::is_sorted(v.begin(), v.end()));
}

// ============================================================
// heap_sort
// ============================================================

TEST(HeapSort, Empty) {
    std::vector<int> v;
    algorithm_x::algo::heap_sort(v.begin(), v.end());
    EXPECT_TRUE(v.empty());
}

TEST(HeapSort, SingleElement) {
    std::vector<int> v{33};
    algorithm_x::algo::heap_sort(v.begin(), v.end());
    EXPECT_EQ(v, std::vector<int>({33}));
}

TEST(HeapSort, AlreadySorted) {
    std::vector<int> v{1, 2, 3, 4, 5};
    algorithm_x::algo::heap_sort(v.begin(), v.end());
    EXPECT_TRUE(std::is_sorted(v.begin(), v.end()));
}

TEST(HeapSort, ReverseSorted) {
    std::vector<int> v{9, 8, 7, 6, 5, 4, 3, 2, 1};
    algorithm_x::algo::heap_sort(v.begin(), v.end());
    EXPECT_TRUE(std::is_sorted(v.begin(), v.end()));
}

TEST(HeapSort, Random) {
    std::vector<int> v{12, 11, 13, 5, 6, 7};
    algorithm_x::algo::heap_sort(v.begin(), v.end());
    EXPECT_TRUE(std::is_sorted(v.begin(), v.end()));
}

// ============================================================
// counting_sort
// ============================================================

TEST(CountingSort, Empty) {
    std::vector<int> v;
    algorithm_x::algo::counting_sort(v.begin(), v.end());
    EXPECT_TRUE(v.empty());
}

TEST(CountingSort, SingleElement) {
    std::vector<int> v{0};
    algorithm_x::algo::counting_sort(v.begin(), v.end());
    EXPECT_EQ(v, std::vector<int>({0}));
}

TEST(CountingSort, SmallRange) {
    std::vector<int> v{3, 1, 4, 1, 5, 9, 2, 6};
    algorithm_x::algo::counting_sort(v.begin(), v.end());
    EXPECT_TRUE(std::is_sorted(v.begin(), v.end()));
}

TEST(CountingSort, NegativeValues) {
    std::vector<int> v{-3, 5, -1, 0, 2, -5, 7};
    algorithm_x::algo::counting_sort(v.begin(), v.end());
    EXPECT_TRUE(std::is_sorted(v.begin(), v.end()));
}

TEST(CountingSort, AlreadySorted) {
    std::vector<int> v{1, 2, 3, 4, 5};
    algorithm_x::algo::counting_sort(v.begin(), v.end());
    EXPECT_TRUE(std::is_sorted(v.begin(), v.end()));
}

// ============================================================
// radix_sort
// ============================================================

TEST(RadixSort, Empty) {
    std::vector<unsigned> v;
    algorithm_x::algo::radix_sort(v.begin(), v.end());
    EXPECT_TRUE(v.empty());
}

TEST(RadixSort, SingleElement) {
    std::vector<unsigned> v{42};
    algorithm_x::algo::radix_sort(v.begin(), v.end());
    EXPECT_EQ(v, std::vector<unsigned>({42}));
}

TEST(RadixSort, SmallRange) {
    std::vector<unsigned> v{3, 0, 2, 5, 4, 1};
    algorithm_x::algo::radix_sort(v.begin(), v.end());
    EXPECT_TRUE(std::is_sorted(v.begin(), v.end()));
}

TEST(RadixSort, LargeValues) {
    std::vector<unsigned> v{1000, 0, 54321, 99, 888, 1, 50000};
    algorithm_x::algo::radix_sort(v.begin(), v.end());
    EXPECT_TRUE(std::is_sorted(v.begin(), v.end()));
}

TEST(RadixSort, Duplicates) {
    std::vector<unsigned> v{5, 2, 5, 3, 2, 8, 5, 2};
    algorithm_x::algo::radix_sort(v.begin(), v.end());
    EXPECT_TRUE(std::is_sorted(v.begin(), v.end()));
}

// ============================================================
// Cross-validation: all sorts produce the same result
// ============================================================

TEST(AllSorts, ConsistentResult) {
    std::vector<int> original{49, 27, 38, 12, 5, 91, 64, 33, 17, 8};

    auto test = original; algorithm_x::algo::bubble_sort(test.begin(), test.end());
    auto expected = test;

    test = original; algorithm_x::algo::selection_sort(test.begin(), test.end());
    EXPECT_EQ(test, expected);

    test = original; algorithm_x::algo::insertion_sort(test.begin(), test.end());
    EXPECT_EQ(test, expected);

    test = original; algorithm_x::algo::merge_sort(test.begin(), test.end());
    EXPECT_EQ(test, expected);

    test = original; algorithm_x::algo::quick_sort(test.begin(), test.end());
    EXPECT_EQ(test, expected);

    test = original; algorithm_x::algo::heap_sort(test.begin(), test.end());
    EXPECT_EQ(test, expected);
}

}  // namespace
