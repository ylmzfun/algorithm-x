#include "algorithm_x/ds/b_tree.h"
#include "gtest/gtest.h"
using namespace algorithm_x::ds;
namespace {
TEST(BTree, InsertSearch) { BTree<3> bt; bt.insert(10); bt.insert(20); bt.insert(5); EXPECT_TRUE(bt.search(10)); EXPECT_FALSE(bt.search(99)); }
TEST(BTree, LargeInsert) { BTree<5> bt; for (int i=0;i<100;++i) bt.insert(i); for (int i=0;i<100;++i) EXPECT_TRUE(bt.search(i)); }
}  // namespace
