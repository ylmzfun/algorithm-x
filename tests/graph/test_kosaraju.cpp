#include "graph/kosaraju.h"
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::graph;
namespace {
TEST(Kosaraju, TwoSCCs) {
    std::vector<std::vector<std::size_t>> adj(4);
    adj[0] = {1}; adj[1] = {2}; adj[2] = {0}; adj[3] = {};
    auto [comp, cnt] = kosaraju_scc(adj);
    EXPECT_EQ(cnt, 2u);
}
TEST(Kosaraju, SingleSCC) {
    std::vector<std::vector<std::size_t>> adj(3);
    adj[0] = {1}; adj[1] = {2}; adj[2] = {0};
    EXPECT_EQ(kosaraju_scc(adj).second, 1u);
}
TEST(Kosaraju, EachNodeSeparate) {
    std::vector<std::vector<std::size_t>> adj(3);
    EXPECT_EQ(kosaraju_scc(adj).second, 3u);
}
}  // namespace
