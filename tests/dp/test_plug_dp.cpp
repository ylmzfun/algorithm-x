#include "algorithm_x/dp/plug_dp.h"

#include <cstdint>

#include "gtest/gtest.h"

using namespace algorithm_x::dp;

namespace {

TEST(DominoTilings, SmallBoards) {
    EXPECT_EQ(domino_tilings(2, 2), 2);
    EXPECT_EQ(domino_tilings(2, 3), 3);
    EXPECT_EQ(domino_tilings(2, 4), 5);
}

TEST(DominoTilings, OddArea) {
    // 3×3 共 9 个格子，面积为奇数，无法用 1×2 骨牌完全覆盖
    EXPECT_EQ(domino_tilings(3, 3), 0);
}

TEST(DominoTilings, MediumBoards) {
    EXPECT_EQ(domino_tilings(4, 4), 36);
    EXPECT_EQ(domino_tilings(3, 4), 11);
}

TEST(DominoTilings, EmptyBoard) {
    EXPECT_EQ(domino_tilings(0, 5), 1);
    EXPECT_EQ(domino_tilings(5, 0), 1);
}

}  // namespace
