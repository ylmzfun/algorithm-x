#include "algorithm_x/math/stirling.h"
#include "gtest/gtest.h"
using namespace algorithm_x::math;
namespace {
TEST(StirlingFirst, KnownValues) {
    EXPECT_EQ(stirling_first(0, 0), 1);
    EXPECT_EQ(stirling_first(3, 2), 3);
    EXPECT_EQ(stirling_first(4, 2), 11);
    EXPECT_EQ(stirling_first(5, 2), 50);
    EXPECT_EQ(stirling_first(4, 4), 1);
}
TEST(StirlingFirst, EdgeCases) {
    EXPECT_EQ(stirling_first(3, 0), 0);
    EXPECT_EQ(stirling_first(3, 4), 0);
    EXPECT_EQ(stirling_first(2, -1), 0);
}
TEST(StirlingSecond, KnownValues) {
    EXPECT_EQ(stirling_second(3, 2), 3);
    EXPECT_EQ(stirling_second(4, 2), 7);
    EXPECT_EQ(stirling_second(5, 3), 25);
    EXPECT_EQ(stirling_second(5, 5), 1);
    EXPECT_EQ(stirling_second(6, 2), 31);
}
TEST(StirlingSecond, EdgeCases) {
    EXPECT_EQ(stirling_second(3, 0), 0);
    EXPECT_EQ(stirling_second(0, 0), 1);
    EXPECT_EQ(stirling_second(3, 4), 0);
}
TEST(BellNumber, KnownValues) {
    EXPECT_EQ(bell_number(0), 1);
    EXPECT_EQ(bell_number(1), 1);
    EXPECT_EQ(bell_number(2), 2);
    EXPECT_EQ(bell_number(3), 5);
    EXPECT_EQ(bell_number(4), 15);
    EXPECT_EQ(bell_number(5), 52);
}
}  // namespace
