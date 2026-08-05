#include "algorithm_x/ds/skip_list.h"
#include "gtest/gtest.h"
using namespace algorithm_x::ds;
namespace {
TEST(SkipList, InsertAndSearch) {
    SkipList<int> sl; sl.insert(3); sl.insert(1); sl.insert(2);
    EXPECT_TRUE(sl.search(1)); EXPECT_TRUE(sl.search(3)); EXPECT_FALSE(sl.search(5));
}
TEST(SkipList, Erase) { SkipList<int> sl; sl.insert(5); sl.erase(5); EXPECT_FALSE(sl.search(5)); }
TEST(SkipList, Size) { SkipList<int> sl; sl.insert(1); sl.insert(2); EXPECT_EQ(sl.size(), 2u); }
TEST(SkipList, Empty) { SkipList<int> sl; EXPECT_TRUE(sl.empty()); sl.insert(1); EXPECT_FALSE(sl.empty()); }
TEST(SkipList, Large) { SkipList<int> sl; for (int i = 0; i < 500; ++i) sl.insert(i); EXPECT_TRUE(sl.search(250)); EXPECT_EQ(sl.size(), 500u); }
}  // namespace
