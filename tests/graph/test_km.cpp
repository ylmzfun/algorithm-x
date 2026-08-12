#include "graph/km.h"
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::graph;
namespace {
TEST(KM, Simple) {
    std::vector<std::vector<int>> cost = {{3, 2}, {4, 1}};
    auto [match, total] = km_algorithm(cost);
    EXPECT_EQ(total, 6); // match 0→1(2) + 1→0(4) = 6, or 0→0(3)+1→1(1)=4. Max is 6.
}
}  // namespace
