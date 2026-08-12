#include "algo/backtracking.h"

#include <algorithm>
#include <numeric>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::algo;

namespace {

// ============================================================
// solve_n_queens
// ============================================================

bool queens_no_attack(const std::vector<std::string>& board) {
    int n = static_cast<int>(board.size());
    // Check row count: each row must have exactly 1 Q
    for (int i = 0; i < n; ++i) {
        int cnt = 0;
        for (int j = 0; j < n; ++j)
            if (board[static_cast<size_t>(i)][static_cast<size_t>(j)] == 'Q') ++cnt;
        if (cnt != 1) return false;
    }
    // Check columns
    for (int j = 0; j < n; ++j) {
        int cnt = 0;
        for (int i = 0; i < n; ++i)
            if (board[static_cast<size_t>(i)][static_cast<size_t>(j)] == 'Q') ++cnt;
        if (cnt > 1) return false;
    }
    // Check diagonals
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (board[static_cast<size_t>(i)][static_cast<size_t>(j)] == 'Q') {
                for (int d = 1; i + d < n && j + d < n; ++d)
                    if (board[static_cast<size_t>(i + d)][static_cast<size_t>(j + d)] == 'Q')
                        return false;
                for (int d = 1; i + d < n && j - d >= 0; ++d)
                    if (board[static_cast<size_t>(i + d)][static_cast<size_t>(j - d)] == 'Q')
                        return false;
            }
        }
    }
    return true;
}

TEST(NQueens, N4HasSolution) {
    auto res = solve_n_queens(4);
    EXPECT_EQ(res.size(), 4u);
    EXPECT_TRUE(queens_no_attack(res));
}

TEST(NQueens, N1HasSolution) {
    auto res = solve_n_queens(1);
    EXPECT_EQ(res.size(), 1u);
    EXPECT_EQ(res[0], "Q");
}

TEST(NQueens, N0ReturnsEmpty) {
    auto res = solve_n_queens(0);
    EXPECT_TRUE(res.empty());
}

TEST(NQueens, N8HasSolution) {
    auto res = solve_n_queens(8);
    EXPECT_EQ(res.size(), 8u);
    EXPECT_TRUE(queens_no_attack(res));
    int q_count = 0;
    for (const auto& row : res)
        for (char c : row)
            if (c == 'Q') ++q_count;
    EXPECT_EQ(q_count, 8);
}

TEST(NQueens, N2NoSolution) {
    auto res = solve_n_queens(2);
    EXPECT_TRUE(res.empty());
}

TEST(NQueens, N3NoSolution) {
    auto res = solve_n_queens(3);
    EXPECT_TRUE(res.empty());
}

// ============================================================
// subset_sum_exists
// ============================================================

TEST(SubsetSumExists, TargetExists) {
    EXPECT_TRUE(subset_sum_exists({3, 34, 4, 12, 5, 2}, 9));  // 4+5
    EXPECT_TRUE(subset_sum_exists({2, 3, 7, 8, 10}, 11));      // 3+8
    EXPECT_TRUE(subset_sum_exists({1, 2, 3}, 6));              // 1+2+3
    EXPECT_TRUE(subset_sum_exists({5}, 5));
}

TEST(SubsetSumExists, TargetDoesNotExist) {
    EXPECT_FALSE(subset_sum_exists({3, 34, 4, 12, 5, 2}, 30));
    EXPECT_FALSE(subset_sum_exists({1, 2, 3}, 7));
}

TEST(SubsetSumExists, EmptySet) {
    EXPECT_FALSE(subset_sum_exists({}, 5));
}

TEST(SubsetSumExists, NegativeTarget) {
    EXPECT_FALSE(subset_sum_exists({1, 2, 3}, -1));
}

TEST(SubsetSumExists, TargetZero) {
    EXPECT_TRUE(subset_sum_exists({1, 2, 3}, 0));
    EXPECT_TRUE(subset_sum_exists({}, 0));
}

// ============================================================
// subset_sum_find
// ============================================================

TEST(SubsetSumFind, ValidSubset) {
    auto res = subset_sum_find({3, 34, 4, 12, 5, 2}, 9);
    EXPECT_FALSE(res.empty());
    EXPECT_EQ(std::accumulate(res.begin(), res.end(), 0), 9);
}

TEST(SubsetSumFind, NoSolution) {
    auto res = subset_sum_find({3, 34, 4, 12, 5, 2}, 30);
    EXPECT_TRUE(res.empty());
}

TEST(SubsetSumFind, SingleElement) {
    auto res = subset_sum_find({7}, 7);
    EXPECT_EQ(res.size(), 1u);
    EXPECT_EQ(res[0], 7);
}

// ============================================================
// permutations
// ============================================================

TEST(Permutations, N3) {
    auto perms = permutations(std::vector<int>{1, 2, 3});
    EXPECT_EQ(perms.size(), 6u);
    // all must be distinct
    std::sort(perms.begin(), perms.end());
    EXPECT_EQ(std::adjacent_find(perms.begin(), perms.end()) == perms.end(), true);
}

TEST(Permutations, N1) {
    auto perms = permutations(std::vector<int>{42});
    EXPECT_EQ(perms.size(), 1u);
    EXPECT_EQ(perms[0].size(), 1u);
    EXPECT_EQ(perms[0][0], 42);
}

TEST(Permutations, Empty) {
    auto perms = permutations(std::vector<int>{});
    EXPECT_EQ(perms.size(), 1u);
}

// ============================================================
// subsets
// ============================================================

TEST(Subsets, N3) {
    auto subs = subsets(std::vector<int>{1, 2, 3});
    EXPECT_EQ(subs.size(), 8u);
    std::vector<size_t> sizes;
    for (auto& s : subs) sizes.push_back(s.size());
    std::sort(sizes.begin(), sizes.end());
    EXPECT_EQ(sizes, (std::vector<size_t>{0, 1, 1, 1, 2, 2, 2, 3}));
}

TEST(Subsets, N0) {
    auto subs = subsets(std::vector<int>{});
    EXPECT_EQ(subs.size(), 1u);
    EXPECT_TRUE(subs[0].empty());
}

// ============================================================
// combinations
// ============================================================

TEST(Combinations, C4K2) {
    auto combs = combinations(std::vector<int>{1, 2, 3, 4}, 2);
    EXPECT_EQ(combs.size(), 6u);
    for (auto& c : combs) EXPECT_EQ(c.size(), 2u);
}

TEST(Combinations, C3K0) {
    auto combs = combinations(std::vector<int>{1, 2, 3}, 0);
    EXPECT_EQ(combs.size(), 1u);
    EXPECT_TRUE(combs[0].empty());
}

TEST(Combinations, C3K3) {
    auto combs = combinations(std::vector<int>{1, 2, 3}, 3);
    EXPECT_EQ(combs.size(), 1u);
    EXPECT_EQ(combs[0].size(), 3u);
}

TEST(Combinations, C5K2) {
    auto combs = combinations(std::vector<int>{1, 2, 3, 4, 5}, 2);
    EXPECT_EQ(combs.size(), 10u);
}

}  // namespace
