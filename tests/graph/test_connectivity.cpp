#include "algorithm_x/graph/connectivity.h"

#include <algorithm>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::graph;

namespace {

// ============================================================
// tarjan_scc
// ============================================================

TEST(TarjanSCCTest, TwoSCCs) {
    // 0 → 1 → 2 → 0 (SCC 1), 3 alone (SCC 2)
    std::vector<std::vector<std::size_t>> adj = {
        {1},       // 0
        {2},       // 1
        {0},       // 2
        {}         // 3
    };
    auto [comp, cnt] = tarjan_scc(adj);
    EXPECT_EQ(cnt, 2u);
    EXPECT_EQ(comp[0], comp[1]);
    EXPECT_EQ(comp[1], comp[2]);
    EXPECT_NE(comp[0], comp[3]);
}

TEST(TarjanSCCTest, SingleSCC) {
    // 0 → 1 → 2 → 3 → 0 (all in one SCC)
    std::vector<std::vector<std::size_t>> adj = {
        {1}, {2}, {3}, {0}
    };
    auto [comp, cnt] = tarjan_scc(adj);
    EXPECT_EQ(cnt, 1u);
    EXPECT_EQ(comp[0], comp[1]);
    EXPECT_EQ(comp[1], comp[2]);
    EXPECT_EQ(comp[2], comp[3]);
}

TEST(TarjanSCCTest, EachNodeOwnSCC) {
    std::vector<std::vector<std::size_t>> adj = {{}, {}, {}};
    auto [comp, cnt] = tarjan_scc(adj);
    EXPECT_EQ(cnt, 3u);
    EXPECT_NE(comp[0], comp[1]);
    EXPECT_NE(comp[1], comp[2]);
    EXPECT_NE(comp[0], comp[2]);
}

TEST(TarjanSCCTest, SingleNode) {
    std::vector<std::vector<std::size_t>> adj = {{}};
    auto [comp, cnt] = tarjan_scc(adj);
    EXPECT_EQ(cnt, 1u);
    EXPECT_EQ(comp[0], 0u);
}

TEST(TarjanSCCTest, ChainWithBackEdge) {
    // 0→1→2→3, 3→1 (SCC: {1,2,3}, {0})
    std::vector<std::vector<std::size_t>> adj = {
        {1},       // 0
        {2},       // 1
        {3},       // 2
        {1}        // 3
    };
    auto [comp, cnt] = tarjan_scc(adj);
    EXPECT_EQ(cnt, 2u);
    EXPECT_NE(comp[0], comp[1]);
    EXPECT_EQ(comp[1], comp[2]);
    EXPECT_EQ(comp[2], comp[3]);
}

// ============================================================
// articulation_points
// ============================================================

TEST(ArticulationPointsTest, CutVertexInMiddle) {
    // 0 — 1 — 2 — 1 — 3  (1 is cut vertex between {0} and {2,3})
    //   0   1   2   3
    // 0: {1}
    // 1: {0,2,3}
    // 2: {1,3}
    // 3: {1,2}
    std::vector<std::vector<std::size_t>> adj = {
        {1},          // 0
        {0, 2, 3},    // 1
        {1, 3},       // 2
        {1, 2}        // 3
    };
    auto pts = articulation_points(adj);
    EXPECT_EQ(pts.size(), 1u);
    EXPECT_EQ(pts[0], 1u);
}

TEST(ArticulationPointsTest, NoCutVerticesCycle) {
    // 0 — 1 — 2 — 0 (triangle, no cut vertices)
    std::vector<std::vector<std::size_t>> adj = {
        {1, 2}, {0, 2}, {0, 1}
    };
    auto pts = articulation_points(adj);
    EXPECT_TRUE(pts.empty());
}

TEST(ArticulationPointsTest, SingleNode) {
    std::vector<std::vector<std::size_t>> adj = {{}};
    auto pts = articulation_points(adj);
    EXPECT_TRUE(pts.empty());
}

TEST(ArticulationPointsTest, StarGraph) {
    // Center 0 connected to leaves 1,2,3
    // 0 is a cut vertex
    std::vector<std::vector<std::size_t>> adj = {
        {1, 2, 3},  // 0
        {0},        // 1
        {0},        // 2
        {0}         // 3
    };
    auto pts = articulation_points(adj);
    EXPECT_EQ(pts.size(), 1u);
    EXPECT_EQ(pts[0], 0u);
}

// ============================================================
// bridges
// ============================================================

TEST(BridgesTest, SingleBridge) {
    // 0—1—2—3, only bridge is between 2 and 3? No, 0-1, 1-2, 2-3 are all bridges.
    // Let me use: triangle 0-1-2 with 2-3 pendant
    // 0: {1,2}, 1: {0,2}, 2: {0,1,3}, 3: {2}
    std::vector<std::vector<std::size_t>> adj = {
        {1, 2},      // 0
        {0, 2},      // 1
        {0, 1, 3},   // 2
        {2}          // 3
    };
    auto br = bridges(adj);
    EXPECT_EQ(br.size(), 1u);
    auto [u, v] = br[0];
    EXPECT_TRUE((u == 2 && v == 3) || (u == 3 && v == 2));
}

TEST(BridgesTest, NoBridgesInCycle) {
    // triangle
    std::vector<std::vector<std::size_t>> adj = {
        {1, 2}, {0, 2}, {0, 1}
    };
    auto br = bridges(adj);
    EXPECT_TRUE(br.empty());
}

TEST(BridgesTest, AllEdgesAreBridgesTree) {
    // 0—1—2 (line, both edges are bridges)
    std::vector<std::vector<std::size_t>> adj = {
        {1}, {0, 2}, {1}
    };
    auto br = bridges(adj);
    EXPECT_EQ(br.size(), 2u);
}

TEST(BridgesTest, SingleNode) {
    std::vector<std::vector<std::size_t>> adj = {{}};
    auto br = bridges(adj);
    EXPECT_TRUE(br.empty());
}

}  // namespace
