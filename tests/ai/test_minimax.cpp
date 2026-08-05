#include "algorithm_x/ai/minimax.h"
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::ai;
namespace {
TEST(Minimax, TicTacToe) {
    std::vector<int> board(9, 0);
    int score = alphabeta(board, 0, -1000, 1000, true);
    EXPECT_GE(score, 0);
}
}  // namespace
