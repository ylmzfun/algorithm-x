#include "algo/randomized.h"

#include <algorithm>
#include <cmath>
#include <set>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::algo;

namespace {

// ------------------------------------------------------------
// shuffle
// ------------------------------------------------------------

TEST(ShuffleTest, PreservesElements) {
    std::vector<int> v(100);
    for (int i = 0; i < 100; ++i) v[i] = i;
    std::vector<int> orig = v;
    shuffle(v.begin(), v.end());
    std::sort(v.begin(), v.end());
    EXPECT_EQ(v, orig);
}

TEST(ShuffleTest, ChangesOrder) {
    std::vector<int> v(100);
    for (int i = 0; i < 100; ++i) v[i] = i;
    std::vector<int> orig = v;
    shuffle(v.begin(), v.end());
    // With 100 elements, probability of identical order is ~1/100!  ≈ 0
    EXPECT_NE(v, orig);
}

TEST(ShuffleTest, Empty) {
    std::vector<int> v;
    shuffle(v.begin(), v.end());
    EXPECT_TRUE(v.empty());
}

TEST(ShuffleTest, SingleElement) {
    std::vector<int> v = {42};
    shuffle(v.begin(), v.end());
    EXPECT_EQ(v[0], 42);
}

// ------------------------------------------------------------
// randomized_quickselect
// ------------------------------------------------------------

TEST(RandomizedQuickselectTest, MinElement) {
    std::vector<int> v = {5, 3, 8, 1, 9, 2};
    auto it = randomized_quickselect(v.begin(), v.end(), 0);
    EXPECT_EQ(*it, 1);
}

TEST(RandomizedQuickselectTest, MaxElement) {
    std::vector<int> v = {5, 3, 8, 1, 9, 2};
    auto it = randomized_quickselect(v.begin(), v.end(), v.size() - 1);
    EXPECT_EQ(*it, 9);
}

TEST(RandomizedQuickselectTest, MiddleElement) {
    std::vector<int> v = {5, 3, 8, 1, 9, 2};
    std::vector<int> sorted = v;
    std::sort(sorted.begin(), sorted.end());
    for (std::size_t k = 0; k < v.size(); ++k) {
        auto it = randomized_quickselect(v.begin(), v.end(), k);
        EXPECT_EQ(*it, sorted[k]) << "k=" << k;
    }
}

TEST(RandomizedQuickselectTest, SingleElement) {
    std::vector<int> v = {7};
    auto it = randomized_quickselect(v.begin(), v.end(), 0);
    EXPECT_EQ(*it, 7);
}

TEST(RandomizedQuickselectTest, Empty) {
    std::vector<int> v;
    auto it = randomized_quickselect(v.begin(), v.end(), 0);
    EXPECT_EQ(it, v.end());
}

// ------------------------------------------------------------
// monte_carlo_pi
// ------------------------------------------------------------

TEST(MonteCarloPiTest, ApproximatesPi) {
    double pi = monte_carlo_pi(100000);
    EXPECT_NEAR(pi, 3.14159, 0.1);
}

TEST(MonteCarloPiTest, MoreSamplesMoreAccurate) {
    double pi = monte_carlo_pi(500000);
    EXPECT_NEAR(pi, 3.14159, 0.05);
}

TEST(MonteCarloPiTest, ZeroSamples) {
    // 0/0 is NaN; implementation divides 4.0 * 0 / 0 → NaN.
    // We just verify it doesn't crash.
    double pi = monte_carlo_pi(0);
    EXPECT_TRUE(std::isnan(pi) || pi >= 0.0);
}

// ------------------------------------------------------------
// reservoir_sample
// ------------------------------------------------------------

TEST(ReservoirSampleTest, SampleK) {
    std::vector<int> v(100);
    for (int i = 0; i < 100; ++i) v[i] = i;
    auto sample = reservoir_sample(v.begin(), v.end(), 5);
    EXPECT_EQ(sample.size(), 5u);
    std::set<int> sample_set(sample.begin(), sample.end());
    for (int x : sample) {
        EXPECT_GE(x, 0);
        EXPECT_LT(x, 100);
    }
}

TEST(ReservoirSampleTest, KGreaterThanN) {
    std::vector<int> v = {1, 2, 3};
    auto sample = reservoir_sample(v.begin(), v.end(), 10);
    EXPECT_EQ(sample.size(), 3u);
}

TEST(ReservoirSampleTest, KZero) {
    std::vector<int> v = {1, 2, 3, 4, 5};
    auto sample = reservoir_sample(v.begin(), v.end(), 0);
    EXPECT_TRUE(sample.empty());
}

TEST(ReservoirSampleTest, EmptyInput) {
    std::vector<int> v;
    auto sample = reservoir_sample(v.begin(), v.end(), 3);
    EXPECT_TRUE(sample.empty());
}

}  // namespace
