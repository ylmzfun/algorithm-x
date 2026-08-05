#include "algorithm_x/graph/spfa.h"
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::graph;
namespace {
TEST(SPFA, ShortestPath) {
    std::vector<std::vector<std::pair<std::size_t,int>>> adj(4);
    adj[0] = {{1,1},{2,4}}; adj[1] = {{2,2},{3,5}}; adj[2] = {{3,1}};
    auto [d, neg] = spfa(adj, 0);
    EXPECT_EQ(d[3], 4); EXPECT_FALSE(neg);
}
TEST(SPFA, NegativeCycle) {
    std::vector<std::vector<std::pair<std::size_t,int>>> adj(3);
    adj[0] = {{1,1}}; adj[1] = {{2,-1}}; adj[2] = {{0,-1}};
    EXPECT_TRUE(spfa(adj, 0).second);
}
}  // namespace
