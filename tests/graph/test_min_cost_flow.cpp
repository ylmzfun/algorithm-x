#include "algorithm_x/graph/min_cost_flow.h"
#include "gtest/gtest.h"
using namespace algorithm_x::graph;
namespace {
TEST(MinCostFlow, SingleEdge) {
    MinCostMaxFlow mcmf(2);
    mcmf.add_edge(0, 1, 5, 2);
    auto [flow, cost] = mcmf.solve(0, 1);
    EXPECT_EQ(flow, 5);
    EXPECT_EQ(cost, 10);
}
}  // namespace
