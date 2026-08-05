#include "algorithm_x/math/linear_algebra.h"
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::math;
namespace {
TEST(Determinant, TwoByTwo) {
    std::vector<std::vector<double>> m = {{3, 8}, {4, 6}};
    EXPECT_NEAR(determinant(m), -14.0, 1e-9);
}
TEST(Determinant, ThreeByThree) {
    std::vector<std::vector<double>> m = {{2, -3, 1}, {2, 0, -1}, {1, 4, 5}};
    EXPECT_NEAR(determinant(m), 49.0, 1e-9);
}
TEST(Determinant, Identity) {
    std::vector<std::vector<double>> m = {{1, 0}, {0, 1}};
    EXPECT_NEAR(determinant(m), 1.0, 1e-9);
}
}  // namespace
