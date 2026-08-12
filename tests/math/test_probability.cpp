#include "algorithm_x/math/probability.h"
#include "gtest/gtest.h"
using namespace algorithm_x::math;
namespace {
TEST(ExpectedValue, Basic) {
    EXPECT_NEAR(expected_value({0.5, 0.5}, {2.0, 4.0}), 3.0, 1e-12);
    EXPECT_NEAR(expected_value({0.25, 0.75}, {0.0, 100.0}), 75.0, 1e-12);
    EXPECT_NEAR(expected_value({1.0}, {7.0}), 7.0, 1e-12);
}
TEST(BinomialCoeff, KnownValues) {
    EXPECT_DOUBLE_EQ(binomial_coeff_double(5, 2), 10.0);
    EXPECT_DOUBLE_EQ(binomial_coeff_double(6, 3), 20.0);
    EXPECT_DOUBLE_EQ(binomial_coeff_double(10, 0), 1.0);
    EXPECT_DOUBLE_EQ(binomial_coeff_double(10, 10), 1.0);
    EXPECT_DOUBLE_EQ(binomial_coeff_double(5, 6), 0.0);
}
TEST(BinomialProbability, FairCoin) {
    // 抛 10 次公平硬币，恰好 5 次正面 = C(10,5) / 2^10
    EXPECT_NEAR(binomial_probability(10, 5, 0.5), 252.0 / 1024.0, 1e-12);
    EXPECT_NEAR(binomial_probability(1, 1, 0.3), 0.3, 1e-12);
    EXPECT_NEAR(binomial_probability(1, 0, 0.3), 0.7, 1e-12);
    EXPECT_NEAR(binomial_probability(2, 1, 0.5), 0.5, 1e-12);
}
}  // namespace
