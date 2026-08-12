#include "ai/csp.h"

#include <utility>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::ai;

namespace {

// 校验 n 皇后放置是否合法：行（隐含）/ 列 / 主副对角线均不冲突。
bool is_valid_placement(const std::vector<int>& ans) {
    int n = static_cast<int>(ans.size());
    if (n <= 0) {
        return false;
    }
    std::vector<bool> col(static_cast<std::size_t>(n), false);
    std::vector<bool> diag1(static_cast<std::size_t>(2 * n - 1), false);
    std::vector<bool> diag2(static_cast<std::size_t>(2 * n - 1), false);
    for (int r = 0; r < n; ++r) {
        int c = ans[static_cast<std::size_t>(r)];
        if (c < 0 || c >= n) {
            return false;
        }
        int d1 = r - c + (n - 1);
        int d2 = r + c;
        if (col[static_cast<std::size_t>(c)] ||
            diag1[static_cast<std::size_t>(d1)] ||
            diag2[static_cast<std::size_t>(d2)]) {
            return false;
        }
        col[static_cast<std::size_t>(c)] = true;
        diag1[static_cast<std::size_t>(d1)] = true;
        diag2[static_cast<std::size_t>(d2)] = true;
    }
    return true;
}

TEST(NQueensForwardChecking, KnownCounts) {
    EXPECT_EQ(count_n_queens_forward_checking(1), 1U);
    EXPECT_EQ(count_n_queens_forward_checking(4), 2U);
    EXPECT_EQ(count_n_queens_forward_checking(5), 10U);
    EXPECT_EQ(count_n_queens_forward_checking(8), 92U);
}

TEST(NQueensForwardChecking, InvalidInput) {
    EXPECT_EQ(count_n_queens_forward_checking(0), 0U);
    EXPECT_EQ(count_n_queens_forward_checking(-4), 0U);
}

TEST(Ac3MapColoring, AustraliaMap) {
    // 澳大利亚风格 7 区域（0=WA 1=NT 2=SA 3=Q 4=NSW 5=V 6=T），7 条邻接边。
    // 含三角 WA-NT-SA ⇒ 不可 2 着色；手算 3 着色：WA=0 NT=1 SA=2 Q=0 NSW=1 V=0 T=0。
    const std::vector<std::pair<int, int>> edges = {
        {0, 1},  // WA-NT
        {0, 2},  // WA-SA
        {1, 2},  // NT-SA
        {1, 3},  // NT-Q
        {2, 4},  // SA-NSW
        {3, 4},  // Q-NSW
        {4, 5},  // NSW-V
    };
    EXPECT_TRUE(ac3_map_coloring(edges, 7, 3));
    EXPECT_FALSE(ac3_map_coloring(edges, 7, 2));
}

TEST(Ac3MapColoring, QuadrilateralTwoColors) {
    // 4 区域环（0-1-2-3-0）：偶数环 ⇒ 二分图 ⇒ 2 色可着色。
    const std::vector<std::pair<int, int>> edges = {{0, 1}, {1, 2}, {2, 3}, {3, 0}};
    EXPECT_TRUE(ac3_map_coloring(edges, 4, 2));
    EXPECT_TRUE(ac3_map_coloring(edges, 4, 3));
}

TEST(Ac3MapColoring, TriangleNotTwoColorable) {
    // 三角形（3 区域环）：奇环 ⇒ 不可 2 着色；3 色可着色。
    const std::vector<std::pair<int, int>> edges = {{0, 1}, {1, 2}, {2, 0}};
    EXPECT_FALSE(ac3_map_coloring(edges, 3, 2));
    EXPECT_TRUE(ac3_map_coloring(edges, 3, 3));
}

TEST(Ac3MapColoring, PruningAndInvalidInput) {
    // 1 色 + 任意一条边 ⇒ AC-3 清空域 ⇒ false；无边孤立点 1 色可着色 ⇒ true。
    EXPECT_FALSE(ac3_map_coloring({{0, 1}}, 2, 1));
    EXPECT_TRUE(ac3_map_coloring({}, 2, 1));
    // 非法输入 / 非法边 / 自环。
    EXPECT_FALSE(ac3_map_coloring({}, 0, 3));
    EXPECT_FALSE(ac3_map_coloring({{0, 1}}, 1, 3));
    EXPECT_FALSE(ac3_map_coloring({{0, 0}}, 1, 3));
}

TEST(MinConflictsNQueens, FindsValidSolutions) {
    for (int n : {4, 8, 20}) {
        std::vector<int> sol = min_conflicts_n_queens(n);
        ASSERT_FALSE(sol.empty()) << "n=" << n;
        ASSERT_EQ(sol.size(), static_cast<std::size_t>(n)) << "n=" << n;
        EXPECT_TRUE(is_valid_placement(sol)) << "n=" << n;
    }
}

TEST(MinConflictsNQueens, DeterministicAndDegenerate) {
    // 固定种子 42 ⇒ 结果确定可复现。
    EXPECT_EQ(min_conflicts_n_queens(8), min_conflicts_n_queens(8));
    EXPECT_TRUE(min_conflicts_n_queens(0).empty());
    EXPECT_TRUE(min_conflicts_n_queens(-2).empty());
}

}  // namespace
