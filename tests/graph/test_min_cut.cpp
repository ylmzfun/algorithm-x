#include "graph/min_cut.h"
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::graph;
namespace {
TEST(MinCut, Simple) {
    std::vector<std::vector<int>> cap = {{0,10,0},{0,0,5},{0,0,0}};
    auto [flow, side] = min_cut(cap, 0, 2);
    EXPECT_EQ(flow, 5);
    EXPECT_TRUE(side[0]); EXPECT_TRUE(side[1]); EXPECT_FALSE(side[2]);
}
}  // namespace
