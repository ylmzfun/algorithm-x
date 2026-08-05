#include "algorithm_x/math/fft.h"
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::math;
namespace {
TEST(FFT, Multiply) {
    std::vector<int> a = {1, 2, 1}; // 1+2x+x^2
    std::vector<int> b = {1, 1};     // 1+x
    auto c = fft_multiply(a, b);
    ASSERT_GE(c.size(), 4u);
    EXPECT_EQ(c[0], 1); EXPECT_EQ(c[1], 3); EXPECT_EQ(c[2], 3); EXPECT_EQ(c[3], 1);
}
}  // namespace
