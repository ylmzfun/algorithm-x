#include "algorithm_x/perf/concepts.h"

#include <string>

#include "gtest/gtest.h"

using namespace algorithm_x::perf;

namespace {

// ---- Concepts ----

TEST(Concepts, Addable) {
    static_assert(Addable<int>);
    static_assert(Addable<std::string>);
    static_assert(!Addable<void>);
}

TEST(Concepts, Printable) {
    static_assert(Printable<int>);
    static_assert(!Printable<void>);
}

// ---- SFINAE ----

TEST(Sfinae, TwiceIntegral) {
    EXPECT_EQ(twice_sfinae(21), 42);
    EXPECT_EQ(twice_sfinae(-3), -6);
}

TEST(Sfinae, TwiceLongLong) {
    EXPECT_EQ(twice_sfinae(1LL << 40), 1LL << 41);
}

// ---- requires ----

TEST(Requires, TwiceIntegral) {
    EXPECT_EQ(twice_requires(10), 20);
}

TEST(Requires, SumAddable) {
    EXPECT_EQ(sum(2, 3), 5);
    EXPECT_EQ(sum(std::string("a"), std::string("b")), "ab");
}

// ---- Overload dispatch ----

TEST(Dispatch, Classify) {
    EXPECT_EQ(classify<int>(), "integral");
    EXPECT_EQ(classify<double>(), "floating_point");
    EXPECT_EQ(classify<std::string>(), "other");
}

// ---- if constexpr + concept ----

TEST(Transform, IntegralDoubles) {
    EXPECT_EQ(transform(5), 10);
}

TEST(Transform, FloatingSquares) {
    EXPECT_DOUBLE_EQ(transform(3.0), 9.0);
}

TEST(Transform, OtherReturnsDefault) {
    EXPECT_EQ(transform(std::string("abc")), std::string());
}

}  // namespace
