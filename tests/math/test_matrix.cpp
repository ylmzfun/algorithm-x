#include "algorithm_x/math/matrix.h"

#include <cstdint>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::math;

namespace {

TEST(MatrixMul, TwoByTwo) {
    std::vector<std::vector<int>> A = {{1, 2}, {3, 4}};
    std::vector<std::vector<int>> B = {{5, 6}, {7, 8}};
    auto C = matrix_mul(A, B);
    // {{1*5+2*7, 1*6+2*8}, {3*5+4*7, 3*6+4*8}} = {{19,22},{43,50}}
    EXPECT_EQ(C[0][0], 19); EXPECT_EQ(C[0][1], 22);
    EXPECT_EQ(C[1][0], 43); EXPECT_EQ(C[1][1], 50);
}

TEST(MatrixMul, Identity) {
    std::vector<std::vector<int>> I = {{1, 0}, {0, 1}};
    std::vector<std::vector<int>> A = {{3, 1}, {4, 2}};
    auto C = matrix_mul(A, I);
    EXPECT_EQ(C, A);
}

TEST(MatrixPow, ZeroPower) {
    std::vector<std::vector<int>> A = {{1, 1}, {1, 0}};
    auto R = matrix_pow(A, 0);
    EXPECT_EQ(R[0][0], 1); EXPECT_EQ(R[0][1], 0);
    EXPECT_EQ(R[1][0], 0); EXPECT_EQ(R[1][1], 1);
}

TEST(MatrixPow, FifthPower) {
    std::vector<std::vector<int>> F = {{1, 1}, {1, 0}};
    auto R = matrix_pow(F, 5);
    EXPECT_EQ(R[0][0], 8); EXPECT_EQ(R[0][1], 5);
    EXPECT_EQ(R[1][0], 5); EXPECT_EQ(R[1][1], 3);
}

TEST(Fibonacci, BasicSequence) {
    EXPECT_EQ(fibonacci<int64_t>(0), 0);
    EXPECT_EQ(fibonacci<int64_t>(1), 1);
    EXPECT_EQ(fibonacci<int64_t>(5), 5);
    EXPECT_EQ(fibonacci<int64_t>(10), 55);
    EXPECT_EQ(fibonacci<int64_t>(20), 6765);
}

TEST(Fibonacci, LargeN) {
    EXPECT_EQ(fibonacci<int64_t>(50), 12586269025LL);
}

TEST(GaussianElimination, Solve3x3) {
    // 2x + y - z = 8
    // -3x - y + 2z = -11
    // -2x + y + 2z = -3
    std::vector<std::vector<double>> A = {
        {2, 1, -1},
        {-3, -1, 2},
        {-2, 1, 2}
    };
    std::vector<double> b = {8, -11, -3};
    auto x = gaussian_elimination(A, b);
    ASSERT_EQ(x.size(), 3u);
    EXPECT_NEAR(x[0], 2.0, 1e-9);
    EXPECT_NEAR(x[1], 3.0, 1e-9);
    EXPECT_NEAR(x[2], -1.0, 1e-9);
}

TEST(GaussianElimination, SingularMatrix) {
    std::vector<std::vector<double>> A = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };
    std::vector<double> b = {1, 2, 3};
    auto x = gaussian_elimination(A, b);
    EXPECT_TRUE(x.empty());
}

TEST(GaussianElimination, Identity) {
    std::vector<std::vector<double>> A = {
        {1, 0, 0},
        {0, 1, 0},
        {0, 0, 1}
    };
    std::vector<double> b = {4, 5, 6};
    auto x = gaussian_elimination(A, b);
    ASSERT_EQ(x.size(), 3u);
    EXPECT_DOUBLE_EQ(x[0], 4.0);
    EXPECT_DOUBLE_EQ(x[1], 5.0);
    EXPECT_DOUBLE_EQ(x[2], 6.0);
}

}  // namespace
