#include "ds/avl_tree.h"

#include <gtest/gtest.h>
#include <vector>

using algorithm_x::ds::AVLTree;

TEST(AVLTree, DefaultEmpty) {
    AVLTree<int> t;
    EXPECT_TRUE(t.empty());
    EXPECT_EQ(t.size(), 0);
}

TEST(AVLTree, InsertAndContains) {
    AVLTree<int> t;
    t.insert(10);
    t.insert(5);
    t.insert(15);

    EXPECT_TRUE(t.contains(10));
    EXPECT_TRUE(t.contains(5));
    EXPECT_TRUE(t.contains(15));
    EXPECT_FALSE(t.contains(999));
    EXPECT_EQ(t.size(), 3);
}

TEST(AVLTree, DuplicateIgnored) {
    AVLTree<int> t;
    t.insert(10);
    t.insert(10);
    EXPECT_EQ(t.size(), 1);
}

TEST(AVLTree, InsertBalanced) {
    AVLTree<int> t;
    // Insert sorted — AVL should self-balance
    std::vector<int> input = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    for (int v : input) {
        t.insert(v);
    }
    // Verify all present via inorder
    std::vector<int> result;
    t.inorder([&](int v) { result.push_back(v); });
    EXPECT_EQ(result, input);
}

TEST(AVLTree, EraseAndContains) {
    AVLTree<int> t;
    t.insert(10);
    t.insert(5);
    t.insert(15);
    t.insert(3);

    t.erase(5);
    EXPECT_FALSE(t.contains(5));
    EXPECT_TRUE(t.contains(10));
    EXPECT_TRUE(t.contains(15));
    EXPECT_TRUE(t.contains(3));
    EXPECT_EQ(t.size(), 3);
}

TEST(AVLTree, EraseStillBalanced) {
    AVLTree<int> t;
    for (int i = 1; i <= 50; ++i) {
        t.insert(i);
    }
    // Erase half and verify inorder still sorted
    for (int i = 1; i <= 50; i += 2) {
        t.erase(i);
    }
    std::vector<int> result;
    t.inorder([&](int v) { result.push_back(v); });

    std::vector<int> expected;
    for (int i = 2; i <= 50; i += 2) {
        expected.push_back(i);
    }
    EXPECT_EQ(result, expected);
}

TEST(AVLTree, LargeInsertStress) {
    AVLTree<int> t;
    const int n = 1000;
    for (int i = n; i >= 1; --i) {
        t.insert(i);
    }
    EXPECT_EQ(t.size(), n);

    std::vector<int> result;
    t.inorder([&](int v) { result.push_back(v); });
    ASSERT_EQ(result.size(), n);
    for (int i = 0; i < n; ++i) {
        EXPECT_EQ(result[i], i + 1);
    }
}
