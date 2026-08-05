#include <gtest/gtest.h>

#include <vector>

#include "algorithm_x/ds/graph.h"

using algorithm_x::ds::Graph;

TEST(GraphTest, UndirectedAddEdge) {
    Graph g(4);
    g.add_edge(0, 1);
    g.add_edge(0, 2);

    EXPECT_FALSE(g.is_directed());

    // Edge 0-1 exists both ways
    auto n0 = g.neighbors(0);
    EXPECT_EQ(n0.size(), 2);

    auto n1 = g.neighbors(1);
    EXPECT_EQ(n1.size(), 1);
    EXPECT_EQ(n1[0], 0);
}

TEST(GraphTest, DirectedAddEdge) {
    Graph g(4, true);
    g.add_edge(0, 1);

    EXPECT_TRUE(g.is_directed());

    auto n0 = g.neighbors(0);
    EXPECT_EQ(n0.size(), 1);
    EXPECT_EQ(n0[0], 1);

    // No back-edge in directed mode
    auto n1 = g.neighbors(1);
    EXPECT_TRUE(n1.empty());
}

TEST(GraphTest, DfsTraversal) {
    Graph g(5);
    g.add_edge(0, 1);
    g.add_edge(0, 2);
    g.add_edge(1, 3);
    g.add_edge(2, 4);

    std::vector<int> order;
    g.dfs(0, [&](std::size_t u) { order.push_back(static_cast<int>(u)); });

    EXPECT_EQ(order.size(), 5);
    // DFS should visit 0 first, then explore depth-first
    EXPECT_EQ(order[0], 0);
}

TEST(GraphTest, BfsTraversal) {
    Graph g(5);
    g.add_edge(0, 1);
    g.add_edge(0, 2);
    g.add_edge(1, 3);
    g.add_edge(2, 4);

    std::vector<int> order;
    g.bfs(0, [&](std::size_t u) { order.push_back(static_cast<int>(u)); });

    EXPECT_EQ(order.size(), 5);
    EXPECT_EQ(order[0], 0);
    // BFS: level 0 → levels 1 → level 3,4
    EXPECT_EQ(order[1], 1);
    EXPECT_EQ(order[2], 2);
    EXPECT_EQ(order[3], 3);
    EXPECT_EQ(order[4], 4);
}

TEST(GraphTest, TopologicalSortOnDag) {
    Graph g(4, true);
    g.add_edge(0, 1);
    g.add_edge(0, 2);
    g.add_edge(1, 3);
    g.add_edge(2, 3);

    auto order = g.topological_sort();

    EXPECT_EQ(order.size(), 4);
    EXPECT_EQ(order[0], 0);  // 0 has indegree 0

    // Verify topological ordering: for every edge u→v, u appears before v
    auto pos = [&](std::size_t v) {
        return static_cast<std::size_t>(
            std::find(order.begin(), order.end(), v) - order.begin());
    };
    EXPECT_LT(pos(0), pos(1));
    EXPECT_LT(pos(0), pos(2));
    EXPECT_LT(pos(1), pos(3));
    EXPECT_LT(pos(2), pos(3));
}

TEST(GraphTest, TopologicalSortWithCycleReturnsEmpty) {
    Graph g(3, true);
    g.add_edge(0, 1);
    g.add_edge(1, 2);
    g.add_edge(2, 0);  // cycle: 0→1→2→0

    auto order = g.topological_sort();

    EXPECT_TRUE(order.empty());
}

TEST(GraphTest, VerticesAndNeighbors) {
    Graph g(3);
    g.add_edge(0, 1);

    EXPECT_EQ(g.vertices(), 3);

    auto n0 = g.neighbors(0);
    EXPECT_EQ(n0.size(), 1);
    EXPECT_EQ(n0[0], 1);

    auto n2 = g.neighbors(2);
    EXPECT_TRUE(n2.empty());
}

TEST(GraphTest, DisconnectedGraphTraversal) {
    Graph g(4);
    g.add_edge(0, 1);

    // DFS from 0 should only visit 0 and 1
    std::vector<int> visited;
    g.dfs(0, [&](std::size_t u) { visited.push_back(static_cast<int>(u)); });

    EXPECT_EQ(visited.size(), 2);
}
