#include "algorithm_x/ds/fenwick_tree.h"
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::ds;
namespace {
TEST(FenwickTree, BuildAndSum) {
    FenwickTree<int> ft(5);
    ft.add(0, 1); ft.add(1, 2); ft.add(2, 3);
    EXPECT_EQ(ft.sum(2), 6);
}
TEST(FenwickTree, RangeSum) {
    FenwickTree<int> ft(5);
    for (int i = 0; i < 5; ++i) ft.add(i, i + 1);
    EXPECT_EQ(ft.range_sum(1, 3), 2 + 3 + 4);
}
TEST(FenwickTree, SingleElement) { FenwickTree<int> ft(1); ft.add(0, 42); EXPECT_EQ(ft.sum(0), 42); }
TEST(FenwickTree, Large) {
    FenwickTree<long long> ft(1000);
    for (int i = 0; i < 1000; ++i) ft.add(i, i);
    EXPECT_EQ(ft.range_sum(0, 999), 999LL * 1000 / 2);
}
}  // namespace
