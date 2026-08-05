#include "algorithm_x/math/prime.h"

#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::math;

namespace {

TEST(IsPrimeTrial, SmallNumbers) {
    EXPECT_FALSE(is_prime_trial(0));
    EXPECT_FALSE(is_prime_trial(1));
    EXPECT_TRUE(is_prime_trial(2));
    EXPECT_TRUE(is_prime_trial(3));
    EXPECT_FALSE(is_prime_trial(4));
    EXPECT_TRUE(is_prime_trial(5));
}

TEST(IsPrimeTrial, MediumNumbers) {
    EXPECT_TRUE(is_prime_trial(97));
    EXPECT_FALSE(is_prime_trial(100));
    EXPECT_FALSE(is_prime_trial(1));
}

TEST(IsPrimeTrial, Negative) {
    EXPECT_FALSE(is_prime_trial(-1));
    EXPECT_FALSE(is_prime_trial(-10));
}

TEST(IsPrimeTrial, LargePrime) {
    EXPECT_TRUE(is_prime_trial(999983));
}

TEST(MillerRabin, AgreesWithTrial) {
    for (int64_t n = 2; n <= 10000; ++n) {
        EXPECT_EQ(is_prime_miller_rabin(n), is_prime_trial(n)) << "failed for n=" << n;
    }
}

TEST(MillerRabin, SmallNumbers) {
    EXPECT_FALSE(is_prime_miller_rabin(0));
    EXPECT_FALSE(is_prime_miller_rabin(1));
    EXPECT_TRUE(is_prime_miller_rabin(2));
    EXPECT_TRUE(is_prime_miller_rabin(3));
    EXPECT_FALSE(is_prime_miller_rabin(4));
}

TEST(MillerRabin, LargeValues) {
    EXPECT_TRUE(is_prime_miller_rabin(999983));
    EXPECT_FALSE(is_prime_miller_rabin(999984));
}

TEST(SieveBool, Basic) {
    auto is_prime = sieve_bool(10);
    for (std::size_t i = 0; i <= 1; ++i) EXPECT_FALSE(is_prime[i]);
    EXPECT_TRUE(is_prime[2]);
    EXPECT_TRUE(is_prime[3]);
    EXPECT_FALSE(is_prime[4]);
    EXPECT_TRUE(is_prime[5]);
    EXPECT_FALSE(is_prime[6]);
    EXPECT_TRUE(is_prime[7]);
    EXPECT_FALSE(is_prime[8]);
    EXPECT_FALSE(is_prime[9]);
    EXPECT_FALSE(is_prime[10]);
}

TEST(SieveBool, ZeroAndOne) {
    auto p0 = sieve_bool(0);
    EXPECT_EQ(p0.size(), 1u);
    EXPECT_FALSE(p0[0]);

    auto p1 = sieve_bool(1);
    EXPECT_EQ(p1.size(), 2u);
    EXPECT_FALSE(p1[0]);
    EXPECT_FALSE(p1[1]);
}

TEST(LinearSieve, AgreesWithSieveBool) {
    auto [is_prime, min_p] = linear_sieve(30);
    auto ref = sieve_bool(30);
    for (std::size_t i = 0; i <= 30; ++i) {
        EXPECT_EQ(is_prime[i], ref[i]) << "differs at " << i;
    }
}

TEST(LinearSieve, MinPrimeFactor) {
    auto [is_prime, min_p] = linear_sieve(12);
    EXPECT_EQ(min_p[2], 2u);
    EXPECT_EQ(min_p[3], 3u);
    EXPECT_EQ(min_p[4], 2u);
    EXPECT_EQ(min_p[5], 5u);
    EXPECT_EQ(min_p[6], 2u);
    EXPECT_EQ(min_p[7], 7u);
    EXPECT_EQ(min_p[8], 2u);
    EXPECT_EQ(min_p[9], 3u);
    EXPECT_EQ(min_p[10], 2u);
    EXPECT_EQ(min_p[11], 11u);
    EXPECT_EQ(min_p[12], 2u);
}

TEST(PrimeFactors, SmallNumbers) {
    auto f12 = prime_factors(12);
    std::sort(f12.begin(), f12.end());
    EXPECT_EQ(f12, (std::vector<int64_t>{2, 2, 3}));

    auto f84 = prime_factors(84);
    std::sort(f84.begin(), f84.end());
    EXPECT_EQ(f84, (std::vector<int64_t>{2, 2, 3, 7}));

    auto f13 = prime_factors(13);
    std::sort(f13.begin(), f13.end());
    EXPECT_EQ(f13, (std::vector<int64_t>{13}));
}

TEST(PrimeFactors, EdgeCases) {
    EXPECT_TRUE(prime_factors(1).empty());
    EXPECT_TRUE(prime_factors(0).empty());
    EXPECT_TRUE(prime_factors(-1).empty());
}

TEST(PrimeFactors, LargeNumber) {
    auto f100 = prime_factors(100);
    std::sort(f100.begin(), f100.end());
    EXPECT_EQ(f100, (std::vector<int64_t>{2, 2, 5, 5}));
}

}  // namespace
