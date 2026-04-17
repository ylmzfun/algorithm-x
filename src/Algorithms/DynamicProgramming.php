<?php

namespace DataStructures\Algorithms;

/**
 * 动态规划算法集合
 * 包含经典的动态规划问题解决方案
 */
class DynamicProgramming
{
    /**
     * 斐波那契数列（动态规划版本）
     * 时间复杂度: O(n), 空间复杂度: O(n)
     */
    public static function fibonacci(int $n): int
    {
        if ($n <= 1) return $n;
        
        $dp = [0, 1];
        for ($i = 2; $i <= $n; $i++) {
            $dp[$i] = $dp[$i - 1] + $dp[$i - 2];
        }
        
        return $dp[$n];
    }
    
    /**
     * 斐波那契数列（空间优化版本）
     * 时间复杂度: O(n), 空间复杂度: O(1)
     */
    public static function fibonacciOptimized(int $n): int
    {
        if ($n <= 1) return $n;
        
        $prev2 = 0;
        $prev1 = 1;
        
        for ($i = 2; $i <= $n; $i++) {
            $current = $prev1 + $prev2;
            $prev2 = $prev1;
            $prev1 = $current;
        }
        
        return $prev1;
    }
    
    /**
     * 最长公共子序列（LCS）
     * 时间复杂度: O(m*n), 空间复杂度: O(m*n)
     */
    public static function longestCommonSubsequence(string $text1, string $text2): int
    {
        $m = strlen($text1);
        $n = strlen($text2);
        
        // 创建DP表
        $dp = array_fill(0, $m + 1, array_fill(0, $n + 1, 0));
        
        for ($i = 1; $i <= $m; $i++) {
            for ($j = 1; $j <= $n; $j++) {
                if ($text1[$i - 1] === $text2[$j - 1]) {
                    $dp[$i][$j] = $dp[$i - 1][$j - 1] + 1;
                } else {
                    $dp[$i][$j] = max($dp[$i - 1][$j], $dp[$i][$j - 1]);
                }
            }
        }
        
        return $dp[$m][$n];
    }
    
    /**
     * 编辑距离（Levenshtein距离）
     * 时间复杂度: O(m*n), 空间复杂度: O(m*n)
     */
    public static function editDistance(string $word1, string $word2): int
    {
        $m = strlen($word1);
        $n = strlen($word2);
        
        $dp = array_fill(0, $m + 1, array_fill(0, $n + 1, 0));
        
        // 初始化边界条件
        for ($i = 0; $i <= $m; $i++) {
            $dp[$i][0] = $i;
        }
        for ($j = 0; $j <= $n; $j++) {
            $dp[0][$j] = $j;
        }
        
        for ($i = 1; $i <= $m; $i++) {
            for ($j = 1; $j <= $n; $j++) {
                if ($word1[$i - 1] === $word2[$j - 1]) {
                    $dp[$i][$j] = $dp[$i - 1][$j - 1];
                } else {
                    $dp[$i][$j] = 1 + min(
                        $dp[$i - 1][$j],     // 删除
                        $dp[$i][$j - 1],     // 插入
                        $dp[$i - 1][$j - 1]  // 替换
                    );
                }
            }
        }
        
        return $dp[$m][$n];
    }
    
    /**
     * 0-1背包问题
     * 时间复杂度: O(n*W), 空间复杂度: O(n*W)
     */
    public static function knapsack01(array $weights, array $values, int $capacity): int
    {
        $n = count($weights);
        $dp = array_fill(0, $n + 1, array_fill(0, $capacity + 1, 0));
        
        for ($i = 1; $i <= $n; $i++) {
            for ($w = 1; $w <= $capacity; $w++) {
                if ($weights[$i - 1] <= $w) {
                    $dp[$i][$w] = max(
                        $values[$i - 1] + $dp[$i - 1][$w - $weights[$i - 1]],
                        $dp[$i - 1][$w]
                    );
                } else {
                    $dp[$i][$w] = $dp[$i - 1][$w];
                }
            }
        }
        
        return $dp[$n][$capacity];
    }
    
    /**
     * 最长递增子序列（LIS）
     * 时间复杂度: O(n²), 空间复杂度: O(n)
     */
    public static function longestIncreasingSubsequence(array $nums): int
    {
        if (empty($nums)) return 0;
        
        $n = count($nums);
        $dp = array_fill(0, $n, 1);
        
        for ($i = 1; $i < $n; $i++) {
            for ($j = 0; $j < $i; $j++) {
                if ($nums[$j] < $nums[$i]) {
                    $dp[$i] = max($dp[$i], $dp[$j] + 1);
                }
            }
        }
        
        return max($dp);
    }
    
    /**
     * 最大子数组和（Kadane算法）
     * 时间复杂度: O(n), 空间复杂度: O(1)
     */
    public static function maxSubarraySum(array $nums): int
    {
        if (empty($nums)) return 0;
        
        $maxSoFar = $nums[0];
        $maxEndingHere = $nums[0];
        
        for ($i = 1; $i < count($nums); $i++) {
            $maxEndingHere = max($nums[$i], $maxEndingHere + $nums[$i]);
            $maxSoFar = max($maxSoFar, $maxEndingHere);
        }
        
        return $maxSoFar;
    }
    
    /**
     * 硬币找零问题
     * 时间复杂度: O(amount * n), 空间复杂度: O(amount)
     */
    public static function coinChange(array $coins, int $amount): int
    {
        $dp = array_fill(0, $amount + 1, $amount + 1);
        $dp[0] = 0;
        
        for ($i = 1; $i <= $amount; $i++) {
            foreach ($coins as $coin) {
                if ($coin <= $i) {
                    $dp[$i] = min($dp[$i], $dp[$i - $coin] + 1);
                }
            }
        }
        
        return $dp[$amount] > $amount ? -1 : $dp[$amount];
    }
    
    /**
     * 爬楼梯问题
     * 时间复杂度: O(n), 空间复杂度: O(1)
     */
    public static function climbStairs(int $n): int
    {
        if ($n <= 2) return $n;
        
        $prev2 = 1;
        $prev1 = 2;
        
        for ($i = 3; $i <= $n; $i++) {
            $current = $prev1 + $prev2;
            $prev2 = $prev1;
            $prev1 = $current;
        }
        
        return $prev1;
    }
    
    /**
     * 房屋抢劫问题
     * 时间复杂度: O(n), 空间复杂度: O(1)
     */
    public static function houseRobber(array $nums): int
    {
        if (empty($nums)) return 0;
        if (count($nums) === 1) return $nums[0];
        
        $prev2 = 0;
        $prev1 = $nums[0];
        
        for ($i = 1; $i < count($nums); $i++) {
            $current = max($prev1, $prev2 + $nums[$i]);
            $prev2 = $prev1;
            $prev1 = $current;
        }
        
        return $prev1;
    }
    
    /**
     * 最小路径和
     * 时间复杂度: O(m*n), 空间复杂度: O(m*n)
     */
    public static function minPathSum(array $grid): int
    {
        if (empty($grid) || empty($grid[0])) return 0;
        
        $m = count($grid);
        $n = count($grid[0]);
        
        $dp = array_fill(0, $m, array_fill(0, $n, 0));
        $dp[0][0] = $grid[0][0];
        
        // 初始化第一行
        for ($j = 1; $j < $n; $j++) {
            $dp[0][$j] = $dp[0][$j - 1] + $grid[0][$j];
        }
        
        // 初始化第一列
        for ($i = 1; $i < $m; $i++) {
            $dp[$i][0] = $dp[$i - 1][0] + $grid[$i][0];
        }
        
        // 填充DP表
        for ($i = 1; $i < $m; $i++) {
            for ($j = 1; $j < $n; $j++) {
                $dp[$i][$j] = min($dp[$i - 1][$j], $dp[$i][$j - 1]) + $grid[$i][$j];
            }
        }
        
        return $dp[$m - 1][$n - 1];
    }
    
    /**
     * 不同路径数
     * 时间复杂度: O(m*n), 空间复杂度: O(m*n)
     */
    public static function uniquePaths(int $m, int $n): int
    {
        $dp = array_fill(0, $m, array_fill(0, $n, 1));
        
        for ($i = 1; $i < $m; $i++) {
            for ($j = 1; $j < $n; $j++) {
                $dp[$i][$j] = $dp[$i - 1][$j] + $dp[$i][$j - 1];
            }
        }
        
        return $dp[$m - 1][$n - 1];
    }
    
    /**
     * 回文子串计数
     * 时间复杂度: O(n²), 空间复杂度: O(n²)
     */
    public static function countPalindromicSubstrings(string $s): int
    {
        $n = strlen($s);
        $dp = array_fill(0, $n, array_fill(0, $n, false));
        $count = 0;
        
        // 单个字符都是回文
        for ($i = 0; $i < $n; $i++) {
            $dp[$i][$i] = true;
            $count++;
        }
        
        // 长度为2的回文
        for ($i = 0; $i < $n - 1; $i++) {
            if ($s[$i] === $s[$i + 1]) {
                $dp[$i][$i + 1] = true;
                $count++;
            }
        }
        
        // 长度大于2的回文
        for ($len = 3; $len <= $n; $len++) {
            for ($i = 0; $i <= $n - $len; $i++) {
                $j = $i + $len - 1;
                if ($s[$i] === $s[$j] && $dp[$i + 1][$j - 1]) {
                    $dp[$i][$j] = true;
                    $count++;
                }
            }
        }
        
        return $count;
    }
}