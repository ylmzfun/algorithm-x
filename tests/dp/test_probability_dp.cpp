#include "algorithm_x/dp/probability_dp.h"
#include "gtest/gtest.h"
using namespace algorithm_x::dp;
namespace {
TEST(ProbDP, CoinToss) { EXPECT_NEAR(coin_toss_probability(2,1),0.5,1e-9); EXPECT_NEAR(coin_toss_probability(2,2),0.25,1e-9); }
}  // namespace
