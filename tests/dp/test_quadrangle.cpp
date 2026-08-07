#include "algorithm_x/dp/quadrangle.h"
#include "gtest/gtest.h"
using namespace algorithm_x::dp;
namespace {
TEST(Quadrangle, OptimalBST) {
    std::vector<int> freq={34,50};
    EXPECT_GE(optimal_bst(freq),84); // at least 34+2*50 or 50+2*34
}
}  // namespace
