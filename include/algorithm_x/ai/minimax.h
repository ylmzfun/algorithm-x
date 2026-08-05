#pragma once

#include <algorithm>
#include <climits>
#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace ai {

// Tic-Tac-Toe board: 3x3, 0=empty, 1=X(max), 2=O(min).
// 评估函数：X 胜 +10，O 胜 -10，平局 0。
inline int evaluate_ttt(const std::vector<int>& board) {
    const int wins[8][3] = {{0,1,2},{3,4,5},{6,7,8},{0,3,6},
                             {1,4,7},{2,5,8},{0,4,8},{2,4,6}};
    for (int i = 0; i < 8; ++i) {
        int a = board[wins[i][0]], b = board[wins[i][1]],
            c = board[wins[i][2]];
        if (a != 0 && a == b && b == c) return (a == 1) ? 10 : -10;
    }
    return 0;
}

inline bool is_ttt_full(const std::vector<int>& board) {
    for (int cell : board)
        if (cell == 0) return false;
    return true;
}

// Minimax — 返回当前局面下的最优得分。
inline int minimax(std::vector<int>& board, int depth, bool is_max) {
    int score = evaluate_ttt(board);
    if (score == 10) return score - depth;
    if (score == -10) return score + depth;
    if (is_ttt_full(board)) return 0;

    if (is_max) {
        int best = INT_MIN;
        for (int i = 0; i < 9; ++i) {
            if (board[i] == 0) {
                board[i] = 1;
                best = std::max(best, minimax(board, depth + 1, false));
                board[i] = 0;
            }
        }
        return best;
    } else {
        int best = INT_MAX;
        for (int i = 0; i < 9; ++i) {
            if (board[i] == 0) {
                board[i] = 2;
                best = std::min(best, minimax(board, depth + 1, true));
                board[i] = 0;
            }
        }
        return best;
    }
}

// Alpha-Beta 剪枝。
inline int alphabeta(std::vector<int>& board, int depth, int alpha, int beta,
                      bool is_max) {
    int score = evaluate_ttt(board);
    if (score == 10) return score - depth;
    if (score == -10) return score + depth;
    if (is_ttt_full(board)) return 0;

    if (is_max) {
        int best = INT_MIN;
        for (int i = 0; i < 9; ++i) {
            if (board[i] == 0) {
                board[i] = 1;
                best = std::max(best,
                                 alphabeta(board, depth + 1, alpha, beta, false));
                board[i] = 0;
                alpha = std::max(alpha, best);
                if (beta <= alpha) break;
            }
        }
        return best;
    } else {
        int best = INT_MAX;
        for (int i = 0; i < 9; ++i) {
            if (board[i] == 0) {
                board[i] = 2;
                best = std::min(best,
                                 alphabeta(board, depth + 1, alpha, beta, true));
                board[i] = 0;
                beta = std::min(beta, best);
                if (beta <= alpha) break;
            }
        }
        return best;
    }
}

}  // namespace ai
}  // namespace algorithm_x
