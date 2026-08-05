#include "algorithm_x/math/combinatorics.h"
#include <cstdint>
#include "gtest/gtest.h"
using namespace algorithm_x::math;
namespace {
TEST(Catalan, Known) { EXPECT_EQ(catalan_number(0), 1); EXPECT_EQ(catalan_number(3), 5); EXPECT_EQ(catalan_number(5), 42); }
TEST(Binomial, Known) { EXPECT_EQ(binomial(5, 2), 10); EXPECT_EQ(binomial(10, 0), 1); EXPECT_EQ(binomial(10, 10), 1); }
}  // namespace
