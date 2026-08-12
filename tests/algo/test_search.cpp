#include "algo/search.h"

#include <string>
#include <vector>

#include "gtest/gtest.h"

namespace {

TEST(LinearSearch, Found) {
    std::vector<int> v{3, 1, 4, 1, 5, 9};
    auto it = algorithm_x::algo::linear_search(v.begin(), v.end(), 4);
    EXPECT_NE(it, v.end());
    EXPECT_EQ(*it, 4);
    EXPECT_EQ(std::distance(v.begin(), it), 2);
}

TEST(LinearSearch, NotFound) {
    std::vector<int> v{1, 2, 3};
    auto it = algorithm_x::algo::linear_search(v.begin(), v.end(), 99);
    EXPECT_EQ(it, v.end());
}

TEST(LinearSearch, Empty) {
    std::vector<int> v;
    auto it = algorithm_x::algo::linear_search(v.begin(), v.end(), 1);
    EXPECT_EQ(it, v.end());
}

TEST(LinearSearch, FirstOccurrence) {
    std::vector<int> v{1, 2, 1, 3};
    auto it = algorithm_x::algo::linear_search(v.begin(), v.end(), 1);
    EXPECT_EQ(std::distance(v.begin(), it), 0);
}

// ============================================================
// binary_search_range
// ============================================================

TEST(BinarySearch, Found) {
    std::vector<int> v{1, 3, 5, 7, 9};
    auto it = algorithm_x::algo::binary_search_range(v.begin(), v.end(), 5);
    EXPECT_NE(it, v.end());
    EXPECT_EQ(*it, 5);
}

TEST(BinarySearch, NotFound) {
    std::vector<int> v{1, 3, 5, 7, 9};
    auto it = algorithm_x::algo::binary_search_range(v.begin(), v.end(), 4);
    EXPECT_EQ(it, v.end());
}

TEST(BinarySearch, Empty) {
    std::vector<int> v;
    auto it = algorithm_x::algo::binary_search_range(v.begin(), v.end(), 1);
    EXPECT_EQ(it, v.end());
}

TEST(BinarySearch, FirstAndLast) {
    std::vector<int> v{10, 20, 30, 40, 50};
    EXPECT_EQ(*algorithm_x::algo::binary_search_range(v.begin(), v.end(), 10), 10);
    EXPECT_EQ(*algorithm_x::algo::binary_search_range(v.begin(), v.end(), 50), 50);
}

TEST(BinarySearch, Duplicates) {
    std::vector<int> v{1, 2, 2, 2, 3};
    auto it = algorithm_x::algo::binary_search_range(v.begin(), v.end(), 2);
    EXPECT_NE(it, v.end());
    EXPECT_EQ(*it, 2);
}

TEST(BinarySearch, StringType) {
    std::vector<std::string> v{"apple", "banana", "cherry"};
    auto it = algorithm_x::algo::binary_search_range(v.begin(), v.end(), std::string("banana"));
    EXPECT_NE(it, v.end());
    EXPECT_EQ(*it, "banana");
}

// ============================================================
// lower_bound
// ============================================================

TEST(LowerBound, ExactMatch) {
    std::vector<int> v{1, 3, 5, 7, 9};
    auto it = algorithm_x::algo::lower_bound(v.begin(), v.end(), 5);
    EXPECT_EQ(*it, 5);
}

TEST(LowerBound, ValueBetween) {
    std::vector<int> v{1, 3, 5, 7, 9};
    auto it = algorithm_x::algo::lower_bound(v.begin(), v.end(), 4);
    EXPECT_EQ(*it, 5);  // first >= 4
}

TEST(LowerBound, BeforeAll) {
    std::vector<int> v{5, 6, 7};
    auto it = algorithm_x::algo::lower_bound(v.begin(), v.end(), 1);
    EXPECT_EQ(it, v.begin());
    EXPECT_EQ(*it, 5);
}

TEST(LowerBound, AfterAll) {
    std::vector<int> v{1, 2, 3};
    auto it = algorithm_x::algo::lower_bound(v.begin(), v.end(), 10);
    EXPECT_EQ(it, v.end());
}

TEST(LowerBound, Duplicates) {
    std::vector<int> v{2, 2, 2, 3, 3};
    auto it = algorithm_x::algo::lower_bound(v.begin(), v.end(), 2);
    EXPECT_EQ(it, v.begin());
    EXPECT_EQ(*it, 2);
}

// ============================================================
// upper_bound
// ============================================================

TEST(UpperBound, ExactMatch) {
    std::vector<int> v{1, 3, 5, 7, 9};
    auto it = algorithm_x::algo::upper_bound(v.begin(), v.end(), 5);
    EXPECT_EQ(*it, 7);  // first > 5
}

TEST(UpperBound, AfterAll) {
    std::vector<int> v{1, 2, 3};
    auto it = algorithm_x::algo::upper_bound(v.begin(), v.end(), 10);
    EXPECT_EQ(it, v.end());
}

TEST(UpperBound, BeforeAll) {
    std::vector<int> v{5, 6, 7};
    auto it = algorithm_x::algo::upper_bound(v.begin(), v.end(), 1);
    EXPECT_EQ(it, v.begin());
}

TEST(UpperBound, Duplicates) {
    std::vector<int> v{2, 2, 2, 3, 3};
    auto it = algorithm_x::algo::upper_bound(v.begin(), v.end(), 2);
    EXPECT_EQ(std::distance(v.begin(), it), 3);  // first > 2
    EXPECT_EQ(*it, 3);
}

}  // namespace
