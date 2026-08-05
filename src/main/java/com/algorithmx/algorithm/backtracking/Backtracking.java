package com.algorithmx.algorithm.backtracking;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * 回溯算法 — 排列、组合、子集
 */
public class Backtracking {

    // ==================== 全排列 ====================

    public static List<List<Integer>> permute(int[] nums) {
        List<List<Integer>> res = new ArrayList<>();
        boolean[] used = new boolean[nums.length];
        backtrackPermute(nums, used, new ArrayList<>(), res);
        return res;
    }

    private static void backtrackPermute(int[] nums, boolean[] used,
                                          List<Integer> path, List<List<Integer>> res) {
        if (path.size() == nums.length) { res.add(new ArrayList<>(path)); return; }
        for (int i = 0; i < nums.length; i++) {
            if (used[i]) continue;
            used[i] = true;
            path.add(nums[i]);
            backtrackPermute(nums, used, path, res);
            path.remove(path.size() - 1);
            used[i] = false;
        }
    }

    // ==================== 子集 ====================

    public static List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> res = new ArrayList<>();
        backtrackSubsets(nums, 0, new ArrayList<>(), res);
        return res;
    }

    private static void backtrackSubsets(int[] nums, int start,
                                          List<Integer> path, List<List<Integer>> res) {
        res.add(new ArrayList<>(path));
        for (int i = start; i < nums.length; i++) {
            path.add(nums[i]);
            backtrackSubsets(nums, i + 1, path, res);
            path.remove(path.size() - 1);
        }
    }

    // ==================== 组合 — 从 1..n 中选 k 个 ====================

    public static List<List<Integer>> combine(int n, int k) {
        List<List<Integer>> res = new ArrayList<>();
        backtrackCombine(n, k, 1, new ArrayList<>(), res);
        return res;
    }

    private static void backtrackCombine(int n, int k, int start,
                                          List<Integer> path, List<List<Integer>> res) {
        if (path.size() == k) { res.add(new ArrayList<>(path)); return; }
        for (int i = start; i <= n; i++) {
            // 剪枝：剩余元素不够
            if (n - i + 1 < k - path.size()) break;
            path.add(i);
            backtrackCombine(n, k, i + 1, path, res);
            path.remove(path.size() - 1);
        }
    }

    // ==================== N 皇后 ====================

    public static List<List<String>> solveNQueens(int n) {
        List<List<String>> res = new ArrayList<>();
        char[][] board = new char[n][n];
        for (char[] row : board) Arrays.fill(row, '.');
        backtrackQueens(board, 0, res);
        return res;
    }

    private static void backtrackQueens(char[][] board, int row, List<List<String>> res) {
        int n = board.length;
        if (row == n) {
            List<String> solution = new ArrayList<>();
            for (char[] r : board) solution.add(new String(r));
            res.add(solution);
            return;
        }
        for (int col = 0; col < n; col++) {
            if (!isValid(board, row, col)) continue;
            board[row][col] = 'Q';
            backtrackQueens(board, row + 1, res);
            board[row][col] = '.';
        }
    }

    private static boolean isValid(char[][] board, int row, int col) {
        int n = board.length;
        for (int i = 0; i < row; i++) if (board[i][col] == 'Q') return false;            // 正上
        for (int i = row - 1, j = col - 1; i >= 0 && j >= 0; i--, j--)                  // 左上
            if (board[i][j] == 'Q') return false;
        for (int i = row - 1, j = col + 1; i >= 0 && j < n; i--, j++)                   // 右上
            if (board[i][j] == 'Q') return false;
        return true;
    }

    // ==================== 数独 ====================

    /** 解数独 — 原地修改，假设唯一解 */
    public static void solveSudoku(char[][] board) {
        backtrackSudoku(board);
    }

    private static boolean backtrackSudoku(char[][] board) {
        for (int i = 0; i < 9; i++) {
            for (int j = 0; j < 9; j++) {
                if (board[i][j] != '.') continue;
                for (char c = '1'; c <= '9'; c++) {
                    if (!validSudoku(board, i, j, c)) continue;
                    board[i][j] = c;
                    if (backtrackSudoku(board)) return true;
                    board[i][j] = '.';
                }
                return false; // 1-9 都不行，回溯
            }
        }
        return true; // 全部填完
    }

    private static boolean validSudoku(char[][] board, int row, int col, char c) {
        for (int i = 0; i < 9; i++) {
            if (board[row][i] == c) return false;                     // 同行
            if (board[i][col] == c) return false;                     // 同列
            if (board[row / 3 * 3 + i / 3][col / 3 * 3 + i % 3] == c) // 同宫
                return false;
        }
        return true;
    }
}
