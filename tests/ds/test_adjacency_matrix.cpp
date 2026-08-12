#include "algorithm_x/ds/adjacency_matrix.h"

#include <cstddef>

#include "gtest/gtest.h"

using namespace algorithm_x::ds;

namespace {

TEST(AdjacencyMatrixTest, UndirectedSymmetry) {
    AdjacencyMatrix g(4);
    g.add_edge(0, 1, 3);
    EXPECT_TRUE(g.has_edge(0, 1));
    EXPECT_TRUE(g.has_edge(1, 0));
    EXPECT_EQ(g.get_weight(0, 1), 3);
    EXPECT_EQ(g.get_weight(1, 0), 3);
    EXPECT_FALSE(g.has_edge(0, 2));
    EXPECT_EQ(g.get_weight(0, 2), 0);
}

TEST(AdjacencyMatrixTest, DirectedAsymmetric) {
    AdjacencyMatrix g(3, true);
    g.add_edge(0, 1, 5);
    EXPECT_TRUE(g.has_edge(0, 1));
    EXPECT_FALSE(g.has_edge(1, 0));
    EXPECT_EQ(g.get_weight(0, 1), 5);
    EXPECT_EQ(g.get_weight(1, 0), 0);
}

TEST(AdjacencyMatrixTest, WeightReadWriteAndOverwrite) {
    AdjacencyMatrix g(3);
    g.add_edge(0, 1, 7);
    g.add_edge(0, 1, 9);  // 覆盖旧权重
    EXPECT_EQ(g.get_weight(0, 1), 9);
    EXPECT_EQ(g.get_weight(1, 0), 9);  // 无向图同步更新两个方向
    EXPECT_TRUE(g.has_edge(1, 0));
}

TEST(AdjacencyMatrixTest, DefaultWeightIsOne) {
    AdjacencyMatrix g(2);
    g.add_edge(0, 1);
    EXPECT_EQ(g.get_weight(0, 1), 1);
    EXPECT_EQ(g.get_weight(1, 0), 1);
}

TEST(AdjacencyMatrixTest, NoEdgeReturnsZero) {
    AdjacencyMatrix g(3, true);
    g.add_edge(0, 2);
    EXPECT_EQ(g.get_weight(1, 0), 0);
    EXPECT_EQ(g.get_weight(1, 2), 0);
    EXPECT_FALSE(g.has_edge(1, 0));
}

TEST(AdjacencyMatrixTest, VertexCount) {
    AdjacencyMatrix g(5);
    EXPECT_EQ(g.vertices(), 5u);
    AdjacencyMatrix d(3, true);
    EXPECT_EQ(d.vertices(), 3u);
}

}  // namespace
