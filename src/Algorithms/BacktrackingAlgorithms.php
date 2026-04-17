<?php

namespace DataStructures\Algorithms;

/**
 * 回溯算法集合
 * 包含经典的回溯算法问题解决方案
 */
class BacktrackingAlgorithms
{
    /**
     * N皇后问题
     * 时间复杂度: O(N!), 空间复杂度: O(N)
     */
    public static function nQueens(int $n): array
    {
        $solutions = [];
        $board = array_fill(0, $n, array_fill(0, $n, '.'));
        
        self::solveNQueens($board, 0, $n, $solutions);
        
        return $solutions;
    }
    
    private static function solveNQueens(array &$board, int $row, int $n, array &$solutions): void
    {
        if ($row === $n) {
            $solution = [];
            for ($i = 0; $i < $n; $i++) {
                $solution[] = implode('', $board[$i]);
            }
            $solutions[] = $solution;
            return;
        }
        
        for ($col = 0; $col < $n; $col++) {
            if (self::isSafeQueen($board, $row, $col, $n)) {
                $board[$row][$col] = 'Q';
                self::solveNQueens($board, $row + 1, $n, $solutions);
                $board[$row][$col] = '.';
            }
        }
    }
    
    private static function isSafeQueen(array $board, int $row, int $col, int $n): bool
    {
        // 检查列
        for ($i = 0; $i < $row; $i++) {
            if ($board[$i][$col] === 'Q') {
                return false;
            }
        }
        
        // 检查左上对角线
        for ($i = $row - 1, $j = $col - 1; $i >= 0 && $j >= 0; $i--, $j--) {
            if ($board[$i][$j] === 'Q') {
                return false;
            }
        }
        
        // 检查右上对角线
        for ($i = $row - 1, $j = $col + 1; $i >= 0 && $j < $n; $i--, $j++) {
            if ($board[$i][$j] === 'Q') {
                return false;
            }
        }
        
        return true;
    }
    
    /**
     * 数独求解器
     * 时间复杂度: O(9^(n*n)), 空间复杂度: O(n*n)
     */
    public static function solveSudoku(array &$board): bool
    {
        for ($row = 0; $row < 9; $row++) {
            for ($col = 0; $col < 9; $col++) {
                if ($board[$row][$col] === '.') {
                    for ($num = 1; $num <= 9; $num++) {
                        if (self::isValidSudoku($board, $row, $col, (string)$num)) {
                            $board[$row][$col] = (string)$num;
                            
                            if (self::solveSudoku($board)) {
                                return true;
                            }
                            
                            $board[$row][$col] = '.';
                        }
                    }
                    return false;
                }
            }
        }
        return true;
    }
    
    private static function isValidSudoku(array $board, int $row, int $col, string $num): bool
    {
        // 检查行
        for ($j = 0; $j < 9; $j++) {
            if ($board[$row][$j] === $num) {
                return false;
            }
        }
        
        // 检查列
        for ($i = 0; $i < 9; $i++) {
            if ($board[$i][$col] === $num) {
                return false;
            }
        }
        
        // 检查3x3方格
        $startRow = intval($row / 3) * 3;
        $startCol = intval($col / 3) * 3;
        
        for ($i = $startRow; $i < $startRow + 3; $i++) {
            for ($j = $startCol; $j < $startCol + 3; $j++) {
                if ($board[$i][$j] === $num) {
                    return false;
                }
            }
        }
        
        return true;
    }
    
    /**
     * 全排列
     * 时间复杂度: O(n!), 空间复杂度: O(n)
     */
    public static function permutations(array $nums): array
    {
        $result = [];
        $current = [];
        $used = array_fill(0, count($nums), false);
        
        self::generatePermutations($nums, $current, $used, $result);
        
        return $result;
    }
    
    private static function generatePermutations(array $nums, array &$current, array &$used, array &$result): void
    {
        if (count($current) === count($nums)) {
            $result[] = $current;
            return;
        }
        
        for ($i = 0; $i < count($nums); $i++) {
            if (!$used[$i]) {
                $current[] = $nums[$i];
                $used[$i] = true;
                
                self::generatePermutations($nums, $current, $used, $result);
                
                array_pop($current);
                $used[$i] = false;
            }
        }
    }
    
    /**
     * 组合
     * 时间复杂度: O(C(n,k)), 空间复杂度: O(k)
     */
    public static function combinations(int $n, int $k): array
    {
        $result = [];
        $current = [];
        
        self::generateCombinations(1, $n, $k, $current, $result);
        
        return $result;
    }
    
    private static function generateCombinations(int $start, int $n, int $k, array &$current, array &$result): void
    {
        if (count($current) === $k) {
            $result[] = $current;
            return;
        }
        
        for ($i = $start; $i <= $n; $i++) {
            $current[] = $i;
            self::generateCombinations($i + 1, $n, $k, $current, $result);
            array_pop($current);
        }
    }
    
    /**
     * 子集
     * 时间复杂度: O(2^n), 空间复杂度: O(n)
     */
    public static function subsets(array $nums): array
    {
        $result = [];
        $current = [];
        
        self::generateSubsets($nums, 0, $current, $result);
        
        return $result;
    }
    
    private static function generateSubsets(array $nums, int $index, array &$current, array &$result): void
    {
        $result[] = $current;
        
        for ($i = $index; $i < count($nums); $i++) {
            $current[] = $nums[$i];
            self::generateSubsets($nums, $i + 1, $current, $result);
            array_pop($current);
        }
    }
    
    /**
     * 单词搜索
     * 时间复杂度: O(N * 4^L), 空间复杂度: O(L)
     */
    public static function wordSearch(array $board, string $word): bool
    {
        $rows = count($board);
        $cols = count($board[0]);
        
        for ($i = 0; $i < $rows; $i++) {
            for ($j = 0; $j < $cols; $j++) {
                if (self::dfsWordSearch($board, $word, $i, $j, 0)) {
                    return true;
                }
            }
        }
        
        return false;
    }
    
    private static function dfsWordSearch(array &$board, string $word, int $row, int $col, int $index): bool
    {
        if ($index === strlen($word)) {
            return true;
        }
        
        if ($row < 0 || $row >= count($board) || $col < 0 || $col >= count($board[0]) ||
            $board[$row][$col] !== $word[$index]) {
            return false;
        }
        
        $temp = $board[$row][$col];
        $board[$row][$col] = '#'; // 标记为已访问
        
        $found = self::dfsWordSearch($board, $word, $row + 1, $col, $index + 1) ||
                 self::dfsWordSearch($board, $word, $row - 1, $col, $index + 1) ||
                 self::dfsWordSearch($board, $word, $row, $col + 1, $index + 1) ||
                 self::dfsWordSearch($board, $word, $row, $col - 1, $index + 1);
        
        $board[$row][$col] = $temp; // 恢复
        
        return $found;
    }
    
    /**
     * 括号生成
     * 时间复杂度: O(4^n / sqrt(n)), 空间复杂度: O(n)
     */
    public static function generateParentheses(int $n): array
    {
        $result = [];
        self::generateParenthesesHelper('', 0, 0, $n, $result);
        return $result;
    }
    
    private static function generateParenthesesHelper(string $current, int $open, int $close, int $max, array &$result): void
    {
        if (strlen($current) === $max * 2) {
            $result[] = $current;
            return;
        }
        
        if ($open < $max) {
            self::generateParenthesesHelper($current . '(', $open + 1, $close, $max, $result);
        }
        
        if ($close < $open) {
            self::generateParenthesesHelper($current . ')', $open, $close + 1, $max, $result);
        }
    }
    
    /**
     * 电话号码的字母组合
     * 时间复杂度: O(4^n), 空间复杂度: O(n)
     */
    public static function letterCombinations(string $digits): array
    {
        if (empty($digits)) return [];
        
        $mapping = [
            '2' => 'abc',
            '3' => 'def',
            '4' => 'ghi',
            '5' => 'jkl',
            '6' => 'mno',
            '7' => 'pqrs',
            '8' => 'tuv',
            '9' => 'wxyz'
        ];
        
        $result = [];
        self::generateLetterCombinations($digits, 0, '', $mapping, $result);
        
        return $result;
    }
    
    private static function generateLetterCombinations(string $digits, int $index, string $current, array $mapping, array &$result): void
    {
        if ($index === strlen($digits)) {
            $result[] = $current;
            return;
        }
        
        $digit = $digits[$index];
        $letters = $mapping[$digit];
        
        for ($i = 0; $i < strlen($letters); $i++) {
            self::generateLetterCombinations($digits, $index + 1, $current . $letters[$i], $mapping, $result);
        }
    }
    
    /**
     * 迷宫求解
     * 时间复杂度: O(4^(n*m)), 空间复杂度: O(n*m)
     */
    public static function solveMaze(array $maze, array $start, array $end): ?array
    {
        $rows = count($maze);
        $cols = count($maze[0]);
        $visited = array_fill(0, $rows, array_fill(0, $cols, false));
        $path = [];
        
        if (self::dfsMaze($maze, $start[0], $start[1], $end[0], $end[1], $visited, $path)) {
            return $path;
        }
        
        return null;
    }
    
    private static function dfsMaze(array $maze, int $row, int $col, int $endRow, int $endCol, array &$visited, array &$path): bool
    {
        if ($row === $endRow && $col === $endCol) {
            $path[] = [$row, $col];
            return true;
        }
        
        if ($row < 0 || $row >= count($maze) || $col < 0 || $col >= count($maze[0]) ||
            $maze[$row][$col] === 1 || $visited[$row][$col]) {
            return false;
        }
        
        $visited[$row][$col] = true;
        $path[] = [$row, $col];
        
        // 尝试四个方向
        $directions = [[0, 1], [1, 0], [0, -1], [-1, 0]];
        
        foreach ($directions as $dir) {
            $newRow = $row + $dir[0];
            $newCol = $col + $dir[1];
            
            if (self::dfsMaze($maze, $newRow, $newCol, $endRow, $endCol, $visited, $path)) {
                return true;
            }
        }
        
        // 回溯
        array_pop($path);
        $visited[$row][$col] = false;
        
        return false;
    }
}