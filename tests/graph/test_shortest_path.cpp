#include "graph/shortest_path.h"

#include <limits>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::graph;

// ============================================================
// Dijkstra
// ============================================================

TEST(DijkstraTest, SimpleGraph) {
    // 0 --1-- 1 --2-- 2
    // |        |        |
    // 4        3        1
    // |        |        |
    // 3 --5-- 4
    std::vector<std::vector<std::pair<std::size_t, int>>> adj(5);
    adj[0] = {{1, 1}, {3, 4}};
    adj[1] = {{0, 1}, {2, 2}, {4, 3}};
    adj[2] = {{1, 2}, {4, 1}};
    adj[3] = {{0, 4}, {4, 5}};
    adj[4] = {{1, 3}, {2, 1}, {3, 5}};

    auto dist = dijkstra(adj, 0);
    EXPECT_EQ(dist[0], 0);
    EXPECT_EQ(dist[1], 1);
    EXPECT_EQ(dist[2], 3);  // 0-1-2
    EXPECT_EQ(dist[3], 4);
    EXPECT_EQ(dist[4], 4);  // 0-1-4
}

TEST(DijkstraTest, UnreachableNode) {
    std::vector<std::vector<std::pair<std::size_t, int>>> adj(3);
    adj[0] = {{1, 5}};
    adj[1] = {{0, 5}};
    // node 2 is isolated

    auto dist = dijkstra(adj, 0);
    EXPECT_EQ(dist[0], 0);
    EXPECT_EQ(dist[1], 5);
    EXPECT_EQ(dist[2], std::numeric_limits<int>::max());
}

TEST(DijkstraTest, SingleNode) {
    std::vector<std::vector<std::pair<std::size_t, int>>> adj(1);
    auto dist = dijkstra(adj, 0);
    EXPECT_EQ(dist[0], 0);
}

TEST(DijkstraTest, MultipleEqualPaths) {
    // 0 --2-- 1 --3-- 3
    //  \              /
    //    ------5------
    std::vector<std::vector<std::pair<std::size_t, int>>> adj(4);
    adj[0] = {{1, 2}, {3, 5}};
    adj[1] = {{0, 2}, {3, 3}};
    adj[3] = {{0, 5}, {1, 3}};

    auto dist = dijkstra(adj, 0);
    EXPECT_EQ(dist[3], 5);  // 0-1-3 = 5, 0-3 = 5
}

// ============================================================
// Bellman-Ford
// ============================================================

TEST(BellmanFordTest, SimpleGraph) {
    std::vector<std::tuple<std::size_t, std::size_t, int>> edges = {
        {0, 1, 1}, {1, 2, 2}, {0, 3, 4}, {1, 4, 3}, {2, 4, 1}, {3, 4, 5}
    };
    auto [dist, neg] = bellman_ford(edges, 5, 0);
    EXPECT_FALSE(neg);
    EXPECT_EQ(dist[0], 0);
    EXPECT_EQ(dist[1], 1);
    EXPECT_EQ(dist[2], 3);  // 0-1-2
    EXPECT_EQ(dist[3], 4);
    EXPECT_EQ(dist[4], 4);  // 0-1-4  or 0-1-2-4
}

TEST(BellmanFordTest, NegativeEdgeNoCycle) {
    std::vector<std::tuple<std::size_t, std::size_t, int>> edges = {
        {0, 1, 4}, {0, 2, 5}, {1, 2, -3}
    };
    auto [dist, neg] = bellman_ford(edges, 3, 0);
    EXPECT_FALSE(neg);
    EXPECT_EQ(dist[0], 0);
    EXPECT_EQ(dist[1], 4);
    EXPECT_EQ(dist[2], 1);  // 0-1-2: 4 + (-3) = 1 < 5
}

TEST(BellmanFordTest, NegativeCycle) {
    // 0 -> 1 (1), 1 -> 2 (-1), 2 -> 1 (-1) = cycle 1-2-1 with total -2
    std::vector<std::tuple<std::size_t, std::size_t, int>> edges = {
        {0, 1, 1}, {1, 2, -1}, {2, 1, -1}
    };
    auto [dist, neg] = bellman_ford(edges, 3, 0);
    EXPECT_TRUE(neg);
}

TEST(BellmanFordTest, DisconnectedNegativeCycle) {
    // Graph: nodes 0,1 connected. nodes 2,3 have a negative cycle.
    // Source is 0, so negative cycle on 2-3 should be detected.
    std::vector<std::tuple<std::size_t, std::size_t, int>> edges = {
        {0, 1, 5}, {2, 3, 1}, {3, 2, -2}
    };
    auto [dist, neg] = bellman_ford(edges, 4, 0);
    // Bellman-Ford may or may not detect a negative cycle unreachable from src.
    // Standard implementation only detects cycles reachable from src.
    EXPECT_FALSE(neg);  // cycle 2-3 not reachable from 0
}

// ============================================================
// Floyd-Warshall
// ============================================================

TEST(FloydWarshallTest, SimpleGraph) {
    const int INF = std::numeric_limits<int>::max();
    std::vector<std::vector<int>> dist = {
        {0, 1, INF, 4},
        {1, 0, 2, INF},
        {INF, 2, 0, INF},
        {4, INF, INF, 0}
    };
    auto [res, neg] = floyd_warshall(dist);
    EXPECT_FALSE(neg);
    EXPECT_EQ(res[0][2], 3);  // 0-1-2
    EXPECT_EQ(res[0][3], 4);
    EXPECT_EQ(res[1][3], 5);  // 1-0-3
}

TEST(FloydWarshallTest, NegativeCycle) {
    const int INF = std::numeric_limits<int>::max();
    std::vector<std::vector<int>> dist = {
        {0, 1, INF},
        {INF, 0, -1},
        {-1, INF, 0}
    };
    auto [res, neg] = floyd_warshall(dist);
    EXPECT_TRUE(neg);
}

TEST(FloydWarshallTest, DisconnectedGraph) {
    const int INF = std::numeric_limits<int>::max();
    std::vector<std::vector<int>> dist = {
        {0, INF, INF},
        {INF, 0, INF},
        {INF, INF, 0}
    };
    auto [res, neg] = floyd_warshall(dist);
    EXPECT_FALSE(neg);
    EXPECT_EQ(res[0][1], INF);
    EXPECT_EQ(res[0][0], 0);
}
