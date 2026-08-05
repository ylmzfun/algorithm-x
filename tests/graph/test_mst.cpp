#include "algorithm_x/graph/mst.h"

#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::graph;

namespace {

// Standard test graph:
//    (0)--2--(1)--3--(2)
//     |     / |     /
//    6|   1   5|   4
//     | /     | /
//    (3)     (4)
// MST total weight = 1+2+3+4 = 10
const std::vector<Edge> kStandardEdges = {
    {0, 1, 2}, {0, 3, 6}, {1, 2, 3},
    {1, 3, 1}, {1, 4, 5}, {2, 4, 4},
};

std::vector<std::vector<std::pair<std::size_t, int>>>
build_adj(std::size_t n, const std::vector<Edge>& edges) {
    std::vector<std::vector<std::pair<std::size_t, int>>> adj(n);
    for (auto& e : edges) {
        adj[e.u].emplace_back(e.v, e.w);
        adj[e.v].emplace_back(e.u, e.w);
    }
    return adj;
}

// ============================================================
// Kruskal
// ============================================================

TEST(KruskalTest, StandardGraph) {
    std::size_t n = 5;
    auto [mst, total] = kruskal(kStandardEdges, n);
    EXPECT_EQ(total, 10);
    EXPECT_EQ(mst.size(), n - 1);
}

TEST(KruskalTest, EmptyGraph) {
    auto [mst, total] = kruskal({}, 0);
    EXPECT_EQ(total, 0);
    EXPECT_TRUE(mst.empty());
}

TEST(KruskalTest, SingleNode) {
    auto [mst, total] = kruskal({}, 1);
    EXPECT_EQ(total, 0);
    EXPECT_TRUE(mst.empty());
}

TEST(KruskalTest, DisconnectedGraph) {
    // Two components: (0-1 weight=1), (2-3 weight=2), no edge between them.
    std::vector<Edge> edges = {{0, 1, 1}, {2, 3, 2}};
    auto [mst, total] = kruskal(edges, 4);
    // Only 2 edges found (n-1 = 3 needed for a tree, but we get 2)
    EXPECT_EQ(mst.size(), 2u);
    EXPECT_EQ(total, 3);
}

// ============================================================
// Prim
// ============================================================

TEST(PrimTest, StandardGraph) {
    auto adj = build_adj(5, kStandardEdges);
    EXPECT_EQ(prim(adj), 10);
}

TEST(PrimTest, EmptyGraph) {
    std::vector<std::vector<std::pair<std::size_t, int>>> adj;
    EXPECT_EQ(prim(adj), 0);
}

TEST(PrimTest, SingleNode) {
    std::vector<std::vector<std::pair<std::size_t, int>>> adj(1);
    EXPECT_EQ(prim(adj), 0);
}

TEST(PrimTest, DisconnectedGraph) {
    // Components: 0-1, 2-3
    std::vector<std::vector<std::pair<std::size_t, int>>> adj(4);
    adj[0].emplace_back(1, 1);
    adj[1].emplace_back(0, 1);
    adj[2].emplace_back(3, 2);
    adj[3].emplace_back(2, 2);
    EXPECT_EQ(prim(adj), -1);
}

TEST(PrimTest, ConsistenceWithKruskal) {
    std::size_t n = 6;
    std::vector<Edge> edges = {
        {0, 1, 4}, {0, 2, 3}, {1, 2, 1},
        {1, 3, 2}, {2, 3, 4}, {3, 4, 2},
        {4, 5, 6}, {2, 5, 5},
    };
    auto [mst, kruskal_total] = kruskal(edges, n);
    auto adj = build_adj(n, edges);
    auto prim_total = prim(adj);
    EXPECT_EQ(kruskal_total, prim_total);
}

}  // namespace
