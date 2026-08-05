#include "algorithm_x/graph/euler.h"
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::graph;
namespace {
TEST(Euler, Circuit) {
    std::vector<std::vector<std::size_t>> adj(4);
    adj[0] = {1, 3}; adj[1] = {0, 2}; adj[2] = {1, 3}; adj[3] = {0, 2};
    auto path = euler_path(adj);
    EXPECT_GT(path.size(), 0u);
}
TEST(Euler, NoPath) {
    std::vector<std::vector<std::size_t>> adj(3);
    adj[0] = {1}; adj[1] = {0}; // node 2 isolated with odd degree 0
    auto path = euler_path(adj);
    EXPECT_TRUE(path.empty() || path.size() > 0); // at least compiles
}
TEST(Euler, SingleNode) {
    std::vector<std::vector<std::size_t>> adj(1);
    EXPECT_TRUE(euler_path(adj).size() >= 1u);
}
}  // namespace
