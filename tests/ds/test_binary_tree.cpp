#include "ds/binary_tree.h"

#include <gtest/gtest.h>
#include <string>
#include <vector>

using algorithm_x::ds::BinarySearchTree;

TEST(BinarySearchTree, DefaultEmpty) {
    BinarySearchTree<int> t;
    EXPECT_TRUE(t.empty());
    EXPECT_EQ(t.size(), 0);
    EXPECT_EQ(t.root(), nullptr);
}

TEST(BinarySearchTree, InsertAndContains) {
    BinarySearchTree<int> t;
    EXPECT_TRUE(t.insert(10));
    EXPECT_TRUE(t.insert(5));
    EXPECT_TRUE(t.insert(15));
    EXPECT_TRUE(t.insert(3));
    EXPECT_TRUE(t.insert(7));

    EXPECT_EQ(t.size(), 5);
    EXPECT_FALSE(t.empty());

    EXPECT_TRUE(t.contains(10));
    EXPECT_TRUE(t.contains(5));
    EXPECT_TRUE(t.contains(15));
    EXPECT_TRUE(t.contains(3));
    EXPECT_TRUE(t.contains(7));
    EXPECT_FALSE(t.contains(999));
}

TEST(BinarySearchTree, DuplicateInsert) {
    BinarySearchTree<int> t;
    EXPECT_TRUE(t.insert(10));
    EXPECT_FALSE(t.insert(10));
    EXPECT_EQ(t.size(), 1);
}

TEST(BinarySearchTree, FindMinMax) {
    BinarySearchTree<int> t;
    t.insert(50);
    t.insert(30);
    t.insert(70);
    t.insert(20);
    t.insert(40);
    t.insert(60);
    t.insert(80);

    EXPECT_EQ(t.find_min()->data, 20);
    EXPECT_EQ(t.find_max()->data, 80);
}

TEST(BinarySearchTree, EraseLeaf) {
    BinarySearchTree<int> t;
    t.insert(10);
    t.insert(5);
    t.insert(15);

    EXPECT_TRUE(t.erase(5));
    EXPECT_FALSE(t.contains(5));
    EXPECT_EQ(t.size(), 2);
}

TEST(BinarySearchTree, EraseOneChild) {
    BinarySearchTree<int> t;
    t.insert(10);
    t.insert(5);
    t.insert(3);  // left child of 5

    EXPECT_TRUE(t.erase(5));
    EXPECT_FALSE(t.contains(5));
    EXPECT_TRUE(t.contains(3));
    EXPECT_TRUE(t.contains(10));
}

TEST(BinarySearchTree, EraseTwoChildren) {
    BinarySearchTree<int> t;
    t.insert(50);
    t.insert(30);
    t.insert(70);
    t.insert(20);
    t.insert(40);
    t.insert(60);
    t.insert(80);

    EXPECT_TRUE(t.erase(50));
    EXPECT_FALSE(t.contains(50));
    EXPECT_EQ(t.size(), 6);
}

TEST(BinarySearchTree, InorderTraversal) {
    BinarySearchTree<int> t;
    t.insert(50);
    t.insert(30);
    t.insert(70);
    t.insert(20);
    t.insert(40);

    std::vector<int> values;
    t.inorder([&](int v) { values.push_back(v); });

    ASSERT_EQ(values.size(), 5);
    EXPECT_EQ(values[0], 20);
    EXPECT_EQ(values[1], 30);
    EXPECT_EQ(values[2], 40);
    EXPECT_EQ(values[3], 50);
    EXPECT_EQ(values[4], 70);
}

TEST(BinarySearchTree, PreorderTraversal) {
    BinarySearchTree<int> t;
    t.insert(50);
    t.insert(30);
    t.insert(70);
    t.insert(20);
    t.insert(40);

    std::vector<int> values;
    t.preorder([&](int v) { values.push_back(v); });

    ASSERT_EQ(values.size(), 5);
    EXPECT_EQ(values[0], 50);
    EXPECT_EQ(values[1], 30);
    EXPECT_EQ(values[2], 20);
    EXPECT_EQ(values[3], 40);
    EXPECT_EQ(values[4], 70);
}

TEST(BinarySearchTree, PostorderTraversal) {
    BinarySearchTree<int> t;
    t.insert(50);
    t.insert(30);
    t.insert(70);
    t.insert(20);
    t.insert(40);

    std::vector<int> values;
    t.postorder([&](int v) { values.push_back(v); });

    ASSERT_EQ(values.size(), 5);
    EXPECT_EQ(values[0], 20);
    EXPECT_EQ(values[1], 40);
    EXPECT_EQ(values[2], 30);
    EXPECT_EQ(values[3], 70);
    EXPECT_EQ(values[4], 50);
}

TEST(BinarySearchTree, LevelOrderTraversal) {
    BinarySearchTree<int> t;
    t.insert(50);
    t.insert(30);
    t.insert(70);
    t.insert(20);
    t.insert(40);

    std::vector<int> values;
    t.level_order([&](int v) { values.push_back(v); });

    ASSERT_EQ(values.size(), 5);
    EXPECT_EQ(values[0], 50);
    EXPECT_EQ(values[1], 30);
    EXPECT_EQ(values[2], 70);
    EXPECT_EQ(values[3], 20);
    EXPECT_EQ(values[4], 40);
}

TEST(BinarySearchTree, StringType) {
    BinarySearchTree<std::string> t;
    t.insert("banana");
    t.insert("apple");
    t.insert("cherry");

    EXPECT_TRUE(t.contains("apple"));
    EXPECT_TRUE(t.contains("banana"));
    EXPECT_TRUE(t.contains("cherry"));
    EXPECT_FALSE(t.contains("durian"));
}
