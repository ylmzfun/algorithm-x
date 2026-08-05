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

    // ==================== 背包问题变体 ====================

    /**
     * 完全背包问题（每种物品无限件）
     * 时间复杂度: O(n * capacity)
     * 空间复杂度: O(capacity)
     *
     * @param array $weights 物品重量列表
     * @param array $values 物品价值列表
     * @param int $capacity 背包容量
     * @return int 最大价值
     */
    public static function unboundedKnapsack(array $weights, array $values, int $capacity): int
    {
        $dp = array_fill(0, $capacity + 1, 0);

        for ($i = 0; $i < count($weights); $i++) {
            // 正序遍历（与0-1背包的区别）
            for ($w = $weights[$i]; $w <= $capacity; $w++) {
                $dp[$w] = max($dp[$w], $dp[$w - $weights[$i]] + $values[$i]);
            }
        }

        return $dp[$capacity];
    }

    /**
     * 多重背包问题（每种物品有限件数）
     * 使用二进制优化将每种物品拆分为多个0-1背包物品
     * 时间复杂度: O(n * capacity * log(count))
     * 空间复杂度: O(capacity)
     *
     * @param array $weights 物品重量列表
     * @param array $values 物品价值列表
     * @param array $counts 每种物品的数量限制
     * @param int $capacity 背包容量
     * @return int 最大价值
     */
    public static function boundedKnapsack(array $weights, array $values, array $counts, int $capacity): int
    {
        $dp = array_fill(0, $capacity + 1, 0);

        for ($i = 0; $i < count($weights); $i++) {
            $remaining = $counts[$i];
            $k = 1;

            // 二进制拆分
            while ($remaining > 0) {
                $take = min($k, $remaining);
                $w = $weights[$i] * $take;
                $v = $values[$i] * $take;

                // 0-1 背包（逆序遍历）
                for ($c = $capacity; $c >= $w; $c--) {
                    $dp[$c] = max($dp[$c], $dp[$c - $w] + $v);
                }

                $remaining -= $take;
                $k <<= 1;
            }
        }

        return $dp[$capacity];
    }

    /**
     * 分组背包问题（每组物品最多选一件）
     * 时间复杂度: O(n * capacity)
     * 空间复杂度: O(capacity)
     *
     * @param array $groups 分组物品: [[[weight, value], [weight, value], ...], ...]
     * @param int $capacity 背包容量
     * @return int 最大价值
     */
    public static function groupedKnapsack(array $groups, int $capacity): int
    {
        $dp = array_fill(0, $capacity + 1, 0);

        foreach ($groups as $group) {
            // 对每个容量，尝试该组中的每个物品
            for ($c = $capacity; $c >= 0; $c--) {
                foreach ($group as $item) {
                    $w = $item[0];
                    $v = $item[1];
                    if ($c >= $w) {
                        $dp[$c] = max($dp[$c], $dp[$c - $w] + $v);
                    }
                }
            }
        }

        return $dp[$capacity];
    }

    // ==================== 高级 DP 变体 ====================

    /**
     * 状态压缩 DP — 旅行商问题 (TSP)
     *
     * 给定 n 个城市及两两距离，求从0出发，访问所有城市恰好一次的最短路径长度。
     * 时间复杂度: O(n² × 2^n)
     *
     * @param array $dist 距离矩阵 dist[i][j]
     * @return int 最短路径长度
     */
    public static function tsp(array $dist): int
    {
        $n = count($dist);
        if ($n <= 1) {
            return 0;
        }

        $INF = PHP_INT_MAX;
        $fullMask = (1 << $n) - 1;

        // dp[mask][i] = 从0出发，访问 mask 集合的城市，最后停在 i 的最短距离
        $dp = [];
        for ($mask = 0; $mask <= $fullMask; $mask++) {
            $dp[$mask] = array_fill(0, $n, $INF);
        }

        $dp[1][0] = 0;  // 从城市0出发

        for ($mask = 1; $mask <= $fullMask; $mask++) {
            for ($u = 0; $u < $n; $u++) {
                if (!($mask & (1 << $u)) || $dp[$mask][$u] === $INF) {
                    continue;
                }
                for ($v = 0; $v < $n; $v++) {
                    if ($mask & (1 << $v)) {
                        continue;
                    }
                    $newMask = $mask | (1 << $v);
                    $dp[$newMask][$v] = min($dp[$newMask][$v], $dp[$mask][$u] + $dist[$u][$v]);
                }
            }
        }

        // 回到起点（可选）— 这里求Hamilton路径，不回起点
        $answer = $INF;
        for ($i = 0; $i < $n; $i++) {
            $answer = min($answer, $dp[$fullMask][$i]);
        }

        return $answer === $INF ? -1 : $answer;
    }

    /**
     * 树形 DP — 树的最大独立集
     *
     * 给定树（邻接表），求最大的独立集（选取的节点互不相邻）。
     *
     * @param array $tree 邻接表 ['node' => [child1, child2, ...]]
     * @param mixed $root 根节点
     * @return int 最大独立集大小
     */
    public static function treeMaxIndependentSet(array $tree, $root): int
    {
        $dp = [];

        $dfs = function($node, $parent) use (&$dfs, $tree, &$dp): void {
            $dp[$node] = [0, 1]; // [不选, 选]

            if (isset($tree[$node])) {
                foreach ($tree[$node] as $child) {
                    if ($child === $parent) {
                        continue;
                    }
                    $dfs($child, $node);
                    // 不选当前节点：子节点可选可不选
                    $dp[$node][0] += max($dp[$child][0], $dp[$child][1]);
                    // 选当前节点：子节点都不能选
                    $dp[$node][1] += $dp[$child][0];
                }
            }
        };

        $dfs($root, null);
        return max($dp[$root][0], $dp[$root][1]);
    }

    /**
     * 数位 DP — 统计 [0, n] 中不包含数字 4 的个数
     *
     * @param int $n 上界
     * @return int
     */
    public static function digitDPCountNoFour(int $n): int
    {
        $digits = array_map('intval', str_split((string)$n));
        $len = count($digits);

        $memo = [];

        $dfs = function($pos, $tight, $started) use (&$dfs, $digits, $len, &$memo): int {
            if ($pos === $len) {
                return $started ? 1 : 0;
            }

            $key = $pos . '_' . ($tight ? '1' : '0') . '_' . ($started ? '1' : '0');
            if (isset($memo[$key])) {
                return $memo[$key];
            }

            $limit = $tight ? $digits[$pos] : 9;
            $total = 0;

            for ($d = 0; $d <= $limit; $d++) {
                if ($d === 4) {
                    continue;
                }
                $newTight = $tight && ($d === $limit);
                $newStarted = $started || ($d > 0);
                $total += $dfs($pos + 1, $newTight, $newStarted);
            }

            $memo[$key] = $total;
            return $total;
        };

        return $dfs(0, true, false);
    }

    /**
     * 区间 DP — 矩阵链乘法最小代价
     *
     * 给定矩阵维度 dims[0..n]，矩阵 i 的维度是 dims[i-1] × dims[i]
     * 求最优乘法顺序的最小标量乘法次数。
     *
     * @param array $dims
     * @return int
     */
    public static function matrixChainOrder(array $dims): int
    {
        $n = count($dims) - 1;
        if ($n <= 1) {
            return 0;
        }

        $dp = [];
        for ($i = 0; $i < $n; $i++) {
            $dp[$i] = array_fill(0, $n, PHP_INT_MAX);
            $dp[$i][$i] = 0;
        }

        for ($len = 2; $len <= $n; $len++) {
            for ($i = 0; $i <= $n - $len; $i++) {
                $j = $i + $len - 1;
                for ($k = $i; $k < $j; $k++) {
                    $cost = $dp[$i][$k] + $dp[$k + 1][$j]
                            + $dims[$i] * $dims[$k + 1] * $dims[$j + 1];
                    $dp[$i][$j] = min($dp[$i][$j], $cost);
                }
            }
        }

        return $dp[0][$n - 1];
    }
}