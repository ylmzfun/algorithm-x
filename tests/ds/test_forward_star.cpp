#include "ds/forward_star.h"

#include <cstddef>
#include <utility>

#include "gtest/gtest.h"

using namespace algorithm_x::ds;

namespace {

TEST(ForwardStarTest, NeighborsInInsertionOrder) {
    ForwardStar fs(4, 10);
    fs.add_edge(0, 1, 5);
    fs.add_edge(0, 2, 3);
    fs.add_edge(0, 3, 7);
    const auto nbrs = fs.neighbors(0);
    ASSERT_EQ(nbrs.size(), 3u);
    EXPECT_EQ(nbrs[0].first, 1u);
    EXPECT_EQ(nbrs[0].second, 5);
    EXPECT_EQ(nbrs[1].first, 2u);
    EXPECT_EQ(nbrs[1].second, 3);
    EXPECT_EQ(nbrs[2].first, 3u);
    EXPECT_EQ(nbrs[2].second, 7);
    EXPECT_EQ(fs.edge_count(), 3u);
}

TEST(ForwardStarTest, WeightedEdge) {
    ForwardStar fs(3, 4);
    fs.add_edge(1, 2, 10);
    const auto nbrs = fs.neighbors(1);
    ASSERT_EQ(nbrs.size(), 1u);
    EXPECT_EQ(nbrs[0].first, 2u);
    EXPECT_EQ(nbrs[0].second, 10);
}

TEST(ForwardStarTest, UndirectedPairs) {
    ForwardStar fs(3, 6);
    fs.add_edge(0, 1, 4);
    fs.add_edge(1, 0, 4);
    fs.add_edge(1, 2, 2);
    fs.add_edge(2, 1, 2);
    const auto n1 = fs.neighbors(1);
    ASSERT_EQ(n1.size(), 2u);
    EXPECT_EQ(n1[0].first, 0u);
    EXPECT_EQ(n1[0].second, 4);
    EXPECT_EQ(n1[1].first, 2u);
    EXPECT_EQ(n1[1].second, 2);
    const auto n0 = fs.neighbors(0);
    ASSERT_EQ(n0.size(), 1u);
    EXPECT_EQ(n0[0].first, 1u);
    EXPECT_EQ(n0[0].second, 4);
    const auto n2 = fs.neighbors(2);
    ASSERT_EQ(n2.size(), 1u);
    EXPECT_EQ(n2[0].first, 1u);
    EXPECT_EQ(n2[0].second, 2);
    EXPECT_EQ(fs.edge_count(), 4u);
}

TEST(ForwardStarTest, EdgeCount) {
    ForwardStar fs(2, 5);
    EXPECT_EQ(fs.edge_count(), 0u);
    fs.add_edge(0, 1);
    fs.add_edge(1, 0);
    fs.add_edge(0, 1);
    EXPECT_EQ(fs.edge_count(), 3u);
}

TEST(ForwardStarTest, VertexWithoutEdgesIsEmpty) {
    ForwardStar fs(5, 8);
    fs.add_edge(0, 1);
    fs.add_edge(2, 3);
    EXPECT_TRUE(fs.neighbors(4).empty());
    EXPECT_FALSE(fs.neighbors(0).empty());
    ASSERT_EQ(fs.neighbors(0).size(), 1u);
    EXPECT_EQ(fs.neighbors(0)[0].first, 1u);
}

}  // namespace
