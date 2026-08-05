#include "algorithm_x/math/game_theory.h"
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::math;
namespace {
TEST(Nim, Win) { EXPECT_TRUE(nim_win({1, 3, 5})); }
TEST(Nim, Lose) { EXPECT_FALSE(nim_win({1, 1})); }
TEST(Nim, Single) { EXPECT_TRUE(nim_win({1})); EXPECT_FALSE(nim_win({0})); }
}  // namespace
