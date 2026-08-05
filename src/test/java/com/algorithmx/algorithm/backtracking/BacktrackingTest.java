package com.algorithmx.algorithm.backtracking;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class BacktrackingTest {

    @Test void solveSudoku() {
        char[][] board = {
            {'5','3','.','.','7','.','.','.','.'},
            {'6','.','.','1','9','5','.','.','.'},
            {'.','9','8','.','.','.','.','6','.'},
            {'8','.','.','.','6','.','.','.','3'},
            {'4','.','.','8','.','3','.','.','1'},
            {'7','.','.','.','2','.','.','.','6'},
            {'.','6','.','.','.','.','2','8','.'},
            {'.','.','.','4','1','9','.','.','5'},
            {'.','.','.','.','8','.','.','7','9'}
        };
        Backtracking.solveSudoku(board);
        // 验证每行每列每宫无不重复数字
        for (int i = 0; i < 9; i++) {
            Set<Character> row = new HashSet<>();
            Set<Character> col = new HashSet<>();
            for (int j = 0; j < 9; j++) {
                assertTrue(row.add(board[i][j]), "row " + i + " dup " + board[i][j]);
                assertTrue(col.add(board[j][i]), "col " + i + " dup " + board[j][i]);
            }
        }
        for (int r = 0; r < 9; r += 3) {
            for (int c = 0; c < 9; c += 3) {
                Set<Character> box = new HashSet<>();
                for (int i = 0; i < 9; i++) {
                    char ch = board[r + i / 3][c + i % 3];
                    assertTrue(box.add(ch) || ch == '.', "box dup");
                }
            }
        }
    }
}
