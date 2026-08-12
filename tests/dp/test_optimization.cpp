#include "dp/optimization.h"
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::dp;
namespace {
TEST(MonotonicQueue, SlidingMax) {
    std::vector<int> arr = {1, 3, -1, -3, 5, 3, 6, 7};
    auto res = sliding_window_max(arr, 3);
    ASSERT_EQ(res.size(), 6u);
    EXPECT_EQ(res[0], 3); EXPECT_EQ(res[1], 3); EXPECT_EQ(res[2], 5);
    EXPECT_EQ(res[3], 5); EXPECT_EQ(res[4], 6); EXPECT_EQ(res[5], 7);
}
}  // namespace
