#include "ds/red_black_tree.h"
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::ds;
namespace {
TEST(RBTree, InsertAndContains) {
    RedBlackTree<int> t; t.insert(5); t.insert(3); t.insert(7);
    EXPECT_TRUE(t.contains(3)); EXPECT_TRUE(t.contains(7)); EXPECT_FALSE(t.contains(9));
}
TEST(RBTree, Duplicate) { RedBlackTree<int> t; t.insert(1); EXPECT_FALSE(t.insert(1)); }
TEST(RBTree, Size) { RedBlackTree<int> t; t.insert(1); t.insert(2); EXPECT_EQ(t.size(), 2u); }
TEST(RBTree, Inorder) {
    RedBlackTree<int> t; for (int x : {5,2,8,1,3}) t.insert(x);
    std::vector<int> v; t.inorder([&](int x) { v.push_back(x); });
    EXPECT_TRUE(std::is_sorted(v.begin(), v.end()));
}
TEST(RBTree, Large) { RedBlackTree<int> t; for (int i=0;i<1000;++i) t.insert(i); EXPECT_EQ(t.size(),1000u); }
}  // namespace
