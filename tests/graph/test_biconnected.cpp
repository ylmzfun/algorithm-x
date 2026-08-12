#include "graph/biconnected.h"
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::graph;
namespace {
TEST(BCC, SimpleCycle) {
    std::vector<std::vector<std::size_t>> adj(3);
    adj[0] = {1,2}; adj[1] = {0,2}; adj[2] = {0,1};
    auto bcc = biconnected_components(adj);
    EXPECT_EQ(bcc.size(), 1u);
    EXPECT_EQ(bcc[0].size(), 3u);
}
TEST(BCC, Bridge) {
    std::vector<std::vector<std::size_t>> adj(4);
    adj[0] = {1}; adj[1] = {0,2}; adj[2] = {1,3}; adj[3] = {2};
    auto bcc = biconnected_components(adj);
    EXPECT_EQ(bcc.size(), 3u); // each edge is its own BCC (tree)
}
}  // namespace
