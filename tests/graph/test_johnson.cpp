#include "graph/johnson.h"
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::graph;
namespace {
TEST(Johnson, ThreeNode) {
    std::vector<std::vector<std::pair<std::size_t,int>>> adj(3);
    adj[0]={{1,2}}; adj[1]={{2,-1}}; adj[2]={{0,4}};
    auto dist=johnson(adj);
    ASSERT_EQ(dist.size(),3u);
    EXPECT_EQ(dist[0][1],2); EXPECT_EQ(dist[0][2],1);
}
}  // namespace
