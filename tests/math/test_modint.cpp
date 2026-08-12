#include "math/modint.h"

#include <cstdint>
#include <tuple>

#include "gtest/gtest.h"

using namespace algorithm_x::math;

namespace {

TEST(ExtendedGCD, Basic) {
    auto [g, x, y] = extended_gcd(30, 12);
    EXPECT_EQ(g, 6);
    EXPECT_EQ(30 * x + 12 * y, 6);
}

TEST(ExtendedGCD, CoPrime) {
    auto [g, x, y] = extended_gcd(17, 5);
    EXPECT_EQ(g, 1);
    EXPECT_EQ(17 * x + 5 * y, 1);
}

TEST(ExtendedGCD, OneZero) {
    auto [g, x, y] = extended_gcd(17, 0);
    EXPECT_EQ(g, 17);
    EXPECT_EQ(x, 1);
    EXPECT_EQ(y, 0);
}

TEST(ExtendedGCD, ZeroOne) {
    auto [g, x, y] = extended_gcd(0, 5);
    EXPECT_EQ(g, 5);
}

TEST(GcdExt, Various) {
    EXPECT_EQ(gcd_ext(48, 18), 6);
    EXPECT_EQ(gcd_ext(7, 13), 1);
    EXPECT_EQ(gcd_ext(100, 0), 100);
    EXPECT_EQ(gcd_ext(0, 5), 5);
    EXPECT_EQ(gcd_ext(17, 17), 17);
}

TEST(ModInverse, Basic) {
    EXPECT_EQ(mod_inverse(3, 7), 5);
    EXPECT_EQ(mod_inverse(10, 17), 12);
}

TEST(ModInverse, Verify) {
    int64_t m = 1000000007;
    for (int64_t a = 1; a <= 10; ++a) {
        int64_t inv = mod_inverse(a, m);
        EXPECT_EQ((a * inv) % m, 1 % m);
    }
}

TEST(FastPow, Basic) {
    EXPECT_EQ(fast_pow(2, 10, 1000), 24);
    EXPECT_EQ(fast_pow(3, 5, 7), 5);
    EXPECT_EQ(fast_pow(5, 0, 100), 1);
    EXPECT_EQ(fast_pow(1, 1000000, 100), 1);
}

TEST(FastPow, Large) {
    EXPECT_EQ(fast_pow(2, 60, 1000000007), (1LL << 60) % 1000000007);
}

TEST(CRT, Classic) {
    std::vector<int64_t> r = {2, 3, 2};
    std::vector<int64_t> m = {3, 5, 7};
    EXPECT_EQ(crt(r, m), 23);
}

TEST(CRT, Single) {
    EXPECT_EQ(crt({5}, {7}), 5);
}

TEST(CRT, TwoEquations) {
    EXPECT_EQ(crt({1, 0}, {2, 3}), 3);  // x ≡ 1 (mod 2), x ≡ 0 (mod 3) → x = 3
}

TEST(EulerPhi, Basic) {
    EXPECT_EQ(euler_phi(1), 1);
    EXPECT_EQ(euler_phi(6), 2);
    EXPECT_EQ(euler_phi(12), 4);
    EXPECT_EQ(euler_phi(13), 12);
    EXPECT_EQ(euler_phi(100), 40);
}

TEST(EulerPhi, Prime) {
    // φ(p) = p-1 for prime p
    EXPECT_EQ(euler_phi(17), 16);
    EXPECT_EQ(euler_phi(97), 96);
}

}  // namespace
