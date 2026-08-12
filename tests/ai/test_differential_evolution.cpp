#include "ai/differential_evolution.h"
#include "gtest/gtest.h"
using namespace algorithm_x::ai;
namespace {
TEST(DE, Sphere) {
    auto f=[](const std::vector<double>&x){return x[0]*x[0];};
    auto r=differential_evolution(f,1,{-5.0},{5.0},50,100);
    EXPECT_NEAR(r[0],0.0,1.0);
}
}  // namespace
