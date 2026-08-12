#include "dp/advanced_dp.h"
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::dp;
namespace {
TEST(DigitDP, SumDigits) {
    EXPECT_EQ(digit_dp_sum(9), 45);
    EXPECT_EQ(digit_dp_sum(0), 0);
}
TEST(TreeDP, MaxIndependentSet) {
    std::vector<std::vector<std::size_t>> adj(4);
    adj[0] = {1}; adj[1] = {0, 2}; adj[2] = {1, 3}; adj[3] = {2};
    EXPECT_EQ(tree_dp_max_independent_set(adj), 2);
}
TEST(TreeDP, SingleNode) {
    std::vector<std::vector<std::size_t>> adj(1);
    EXPECT_EQ(tree_dp_max_independent_set(adj), 1);
}
}  // namespace
