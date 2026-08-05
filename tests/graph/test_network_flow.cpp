#include "algorithm_x/graph/network_flow.h"

#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::graph;

// ============================================================
// Dinic max flow
// ============================================================

TEST(DinicTest, SimplePath) {
    DinicGraph g(3);  // s=0, a=1, t=2
    g.add_edge(0, 1, 10);
    g.add_edge(1, 2, 10);
    EXPECT_EQ(g.max_flow(0, 2), 10);
}

TEST(DinicTest, ParallelEdges) {
    DinicGraph g(2);
    g.add_edge(0, 1, 3);
    g.add_edge(0, 1, 4);
    EXPECT_EQ(g.max_flow(0, 1), 7);
}

TEST(DinicTest, DiamondGraph) {
    // s→a→t  and  s→b→t  with a→b bottleneck
    DinicGraph g(4);  // 0=s, 1=a, 2=b, 3=t
    g.add_edge(0, 1, 10);
    g.add_edge(0, 2, 10);
    g.add_edge(1, 2, 5);
    g.add_edge(1, 3, 10);
    g.add_edge(2, 3, 10);
    EXPECT_EQ(g.max_flow(0, 3), 20);
}

TEST(DinicTest, ZeroCapacity) {
    DinicGraph g(2);
    g.add_edge(0, 1, 0);
    EXPECT_EQ(g.max_flow(0, 1), 0);
}

TEST(DinicTest, NoPath) {
    DinicGraph g(3);
    g.add_edge(0, 1, 10);
    // no edge to 2
    EXPECT_EQ(g.max_flow(0, 2), 0);
}

TEST(DinicTest, SingleEdge) {
    DinicGraph g(2);
    g.add_edge(0, 1, 42);
    EXPECT_EQ(g.max_flow(0, 1), 42);
}

// ============================================================
// Bipartite matching
// ============================================================

TEST(BipartiteMatching, Complete2x2) {
    std::vector<std::vector<std::size_t>> adj = {{0, 1}, {0, 1}};
    auto match = bipartite_matching(2, 2, adj);
    int cnt = 0;
    for (auto m : match) if (m != -1) ++cnt;
    EXPECT_EQ(cnt, 2);
}

TEST(BipartiteMatching, SpecificEdges) {
    // L={0,1,2}, R={0,1,2}
    // 0→{0,1}, 1→{1}, 2→{2}
    std::vector<std::vector<std::size_t>> adj = {{0, 1}, {1}, {2}};
    auto match = bipartite_matching(3, 3, adj);
    int cnt = 0;
    for (auto m : match) if (m != -1) ++cnt;
    EXPECT_EQ(cnt, 3);
}

TEST(BipartiteMatching, NoEdges) {
    std::vector<std::vector<std::size_t>> adj = {{}, {}};
    auto match = bipartite_matching(2, 2, adj);
    for (auto m : match) EXPECT_EQ(m, -1);
}

TEST(BipartiteMatching, Chain) {
    // 3 L-nodes, each connected to the same single R-node
    std::vector<std::vector<std::size_t>> adj = {{0}, {0}, {0}};
    auto match = bipartite_matching(3, 1, adj);
    int cnt = 0;
    for (auto m : match) if (m != -1) ++cnt;
    EXPECT_EQ(cnt, 1);
}
