#include "algorithm_x/ds/union_find.h"

#include <gtest/gtest.h>

using algorithm_x::ds::UnionFind;

TEST(UnionFindTest, InitialStateEachElementSeparate) {
    UnionFind uf(5);
    EXPECT_EQ(uf.count(), 5u);
    for (std::size_t i = 0; i < 4; ++i) {
        EXPECT_FALSE(uf.connected(i, i + 1));
    }
}

TEST(UnionFindTest, UniteTwoElements) {
    UnionFind uf(3);
    uf.unite(0, 1);
    EXPECT_TRUE(uf.connected(0, 1));
    EXPECT_FALSE(uf.connected(0, 2));
    EXPECT_FALSE(uf.connected(1, 2));
    EXPECT_EQ(uf.count(), 2u);
}

TEST(UnionFindTest, UniteMultipleTransitive) {
    UnionFind uf(5);
    uf.unite(0, 1);
    uf.unite(1, 2);
    EXPECT_TRUE(uf.connected(0, 2));
    EXPECT_TRUE(uf.connected(0, 1));
    EXPECT_TRUE(uf.connected(1, 2));
    EXPECT_EQ(uf.count(), 3u);
}

TEST(UnionFindTest, UnionAlreadyConnected) {
    UnionFind uf(4);
    uf.unite(0, 1);
    uf.unite(0, 1);  // no-op
    EXPECT_TRUE(uf.connected(0, 1));
    EXPECT_EQ(uf.count(), 3u);
}

TEST(UnionFindTest, CountAfterUnions) {
    UnionFind uf(6);
    EXPECT_EQ(uf.count(), 6u);
    uf.unite(0, 1);
    EXPECT_EQ(uf.count(), 5u);
    uf.unite(1, 2);
    EXPECT_EQ(uf.count(), 4u);
    uf.unite(3, 4);
    EXPECT_EQ(uf.count(), 3u);
    uf.unite(0, 3);
    EXPECT_EQ(uf.count(), 2u);
}

TEST(UnionFindTest, ChainPathCompression) {
    constexpr std::size_t N = 1000;
    UnionFind uf(N);
    for (std::size_t i = 0; i + 1 < N; ++i) {
        uf.unite(i, i + 1);
    }
    EXPECT_EQ(uf.count(), 1u);
    for (std::size_t i = 0; i < N; ++i) {
        EXPECT_TRUE(uf.connected(0, i));
    }
}

TEST(UnionFindTest, UnionByRankCorrectness) {
    UnionFind uf(10);
    // Merge all elements into one group
    for (std::size_t i = 0; i + 1 < 10; ++i) {
        uf.unite(i, i + 1);
    }
    EXPECT_EQ(uf.count(), 1u);
    for (std::size_t i = 0; i < 10; ++i) {
        EXPECT_TRUE(uf.connected(0, i));
    }
}

TEST(UnionFindTest, MultipleGroups) {
    UnionFind uf(8);
    uf.unite(0, 1);
    uf.unite(1, 2);
    uf.unite(4, 5);
    uf.unite(5, 6);
    EXPECT_EQ(uf.count(), 4u);  // {0,1,2}, {3}, {4,5,6}, {7}
    EXPECT_TRUE(uf.connected(0, 2));
    EXPECT_TRUE(uf.connected(4, 6));
    EXPECT_FALSE(uf.connected(0, 4));
    EXPECT_FALSE(uf.connected(2, 5));
    EXPECT_FALSE(uf.connected(3, 7));
}

TEST(UnionFindTest, SelfConnected) {
    UnionFind uf(3);
    EXPECT_TRUE(uf.connected(0, 0));
    EXPECT_TRUE(uf.connected(1, 1));
    EXPECT_TRUE(uf.connected(2, 2));
}
