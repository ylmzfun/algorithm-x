<?php

require_once __DIR__ . '/../vendor/autoload.php';

use DataStructures\Algorithms\DynamicProgramming;
use DataStructures\Algorithms\GreedyAlgorithms;
use DataStructures\Algorithms\BacktrackingAlgorithms;
use DataStructures\Algorithms\MathAlgorithms;

/**
 * 综合算法演示程序
 * 展示动态规划、贪心、回溯和数学算法的使用
 */
class ComprehensiveAlgorithmsDemo
{
    public function run(): void
    {
        echo "=== PHP 数据结构与算法库 - 综合算法演示 ===\n\n";
        
        $this->demonstrateDynamicProgramming();
        $this->demonstrateGreedyAlgorithms();
        $this->demonstrateBacktrackingAlgorithms();
        $this->demonstrateMathAlgorithms();
        
        echo "\n=== 综合算法演示完成 ===\n";
    }
    
    private function demonstrateDynamicProgramming(): void
    {
        echo "\n--- 动态规划算法演示 ---\n";
        
        // 斐波那契数列
        echo "\n1. 斐波那契数列:\n";
        for ($i = 0; $i <= 10; $i++) {
            $fib = DynamicProgramming::fibonacci($i);
            echo "F($i) = $fib\n";
        }
        
        // 最长公共子序列
        echo "\n2. 最长公共子序列:\n";
        $text1 = "ABCDGH";
        $text2 = "AEDFHR";
        $lcs = DynamicProgramming::longestCommonSubsequence($text1, $text2);
        echo "字符串1: $text1\n";
        echo "字符串2: $text2\n";
        echo "最长公共子序列长度: $lcs\n";
        
        // 编辑距离
        echo "\n3. 编辑距离:\n";
        $word1 = "horse";
        $word2 = "ros";
        $distance = DynamicProgramming::editDistance($word1, $word2);
        echo "单词1: $word1\n";
        echo "单词2: $word2\n";
        echo "编辑距离: $distance\n";
        
        // 0-1背包问题
        echo "\n4. 0-1背包问题:\n";
        $weights = [10, 20, 30];
        $values = [60, 100, 120];
        $capacity = 50;
        $maxValue = DynamicProgramming::knapsack01($weights, $values, $capacity);
        echo "物品重量: [" . implode(", ", $weights) . "]\n";
        echo "物品价值: [" . implode(", ", $values) . "]\n";
        echo "背包容量: $capacity\n";
        echo "最大价值: $maxValue\n";
        
        // 最大子数组和
        echo "\n5. 最大子数组和:\n";
        $nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4];
        $maxSum = DynamicProgramming::maxSubarraySum($nums);
        echo "数组: [" . implode(", ", $nums) . "]\n";
        echo "最大子数组和: $maxSum\n";
        
        // 硬币找零
        echo "\n6. 硬币找零:\n";
        $coins = [1, 3, 4];
        $amount = 6;
        $minCoins = DynamicProgramming::coinChange($coins, $amount);
        echo "硬币面额: [" . implode(", ", $coins) . "]\n";
        echo "目标金额: $amount\n";
        echo "最少硬币数: $minCoins\n";
    }
    
    private function demonstrateGreedyAlgorithms(): void
    {
        echo "\n\n--- 贪心算法演示 ---\n";
        
        // 活动选择问题
        echo "\n1. 活动选择问题:\n";
        $activities = [
            ['start' => 1, 'end' => 3, 'name' => 'A'],
            ['start' => 2, 'end' => 4, 'name' => 'B'],
            ['start' => 3, 'end' => 5, 'name' => 'C'],
            ['start' => 0, 'end' => 6, 'name' => 'D'],
            ['start' => 5, 'end' => 7, 'name' => 'E'],
            ['start' => 8, 'end' => 9, 'name' => 'F'],
            ['start' => 5, 'end' => 9, 'name' => 'G']
        ];
        
        echo "所有活动:\n";
        foreach ($activities as $activity) {
            echo "  {$activity['name']}: [{$activity['start']}, {$activity['end']}]\n";
        }
        
        $selected = GreedyAlgorithms::activitySelection($activities);
        echo "\n选中的活动:\n";
        foreach ($selected as $activity) {
            echo "  {$activity['name']}: [{$activity['start']}, {$activity['end']}]\n";
        }
        echo "总共选择了 " . count($selected) . " 个活动\n";
        
        // 分数背包问题
        echo "\n2. 分数背包问题:\n";
        $items = [
            ['weight' => 10, 'value' => 60, 'name' => '物品1'],
            ['weight' => 20, 'value' => 100, 'name' => '物品2'],
            ['weight' => 30, 'value' => 120, 'name' => '物品3']
        ];
        $capacity = 50;
        
        echo "物品信息:\n";
        foreach ($items as $item) {
            $ratio = $item['value'] / $item['weight'];
            echo "  {$item['name']}: 重量={$item['weight']}, 价值={$item['value']}, 价值密度=" . number_format($ratio, 2) . "\n";
        }
        
        $maxValue = GreedyAlgorithms::fractionalKnapsack($items, $capacity);
        echo "背包容量: $capacity\n";
        echo "最大价值: $maxValue\n";
        
        // 跳跃游戏
        echo "\n3. 跳跃游戏:\n";
        $testCases = [
            [2, 3, 1, 1, 4],
            [3, 2, 1, 0, 4],
            [1, 2, 3]
        ];
        
        foreach ($testCases as $i => $nums) {
            $canJump = GreedyAlgorithms::canJump($nums);
            echo "数组" . ($i + 1) . ": [" . implode(", ", $nums) . "] - " . ($canJump ? "可以到达" : "无法到达") . "\n";
            
            if ($canJump) {
                $minJumps = GreedyAlgorithms::minJumps($nums);
                echo "  最少跳跃次数: $minJumps\n";
            }
        }
        
        // 股票买卖
        echo "\n4. 股票买卖:\n";
        $prices = [7, 1, 5, 3, 6, 4];
        echo "股票价格: [" . implode(", ", $prices) . "]\n";
        
        $maxProfit1 = GreedyAlgorithms::maxProfit($prices);
        echo "单次交易最大利润: $maxProfit1\n";
        
        $maxProfit2 = GreedyAlgorithms::maxProfitMultiple($prices);
        echo "多次交易最大利润: $maxProfit2\n";
    }
    
    private function demonstrateBacktrackingAlgorithms(): void
    {
        echo "\n\n--- 回溯算法演示 ---\n";
        
        // N皇后问题
        echo "\n1. 4皇后问题:\n";
        $solutions = BacktrackingAlgorithms::nQueens(4);
        echo "找到 " . count($solutions) . " 个解:\n";
        foreach ($solutions as $i => $solution) {
            echo "\n解" . ($i + 1) . ":\n";
            foreach ($solution as $row) {
                echo "  $row\n";
            }
        }
        
        // 全排列
        echo "\n2. 全排列:\n";
        $nums = [1, 2, 3];
        $permutations = BacktrackingAlgorithms::permutations($nums);
        echo "数组 [" . implode(", ", $nums) . "] 的全排列:\n";
        foreach ($permutations as $perm) {
            echo "  [" . implode(", ", $perm) . "]\n";
        }
        
        // 组合
        echo "\n3. 组合:\n";
        $n = 4;
        $k = 2;
        $combinations = BacktrackingAlgorithms::combinations($n, $k);
        echo "C($n, $k) 的所有组合:\n";
        foreach ($combinations as $comb) {
            echo "  [" . implode(", ", $comb) . "]\n";
        }
        
        // 子集
        echo "\n4. 子集:\n";
        $nums = [1, 2, 3];
        $subsets = BacktrackingAlgorithms::subsets($nums);
        echo "数组 [" . implode(", ", $nums) . "] 的所有子集:\n";
        foreach ($subsets as $subset) {
            echo "  [" . implode(", ", $subset) . "]\n";
        }
        
        // 括号生成
        echo "\n5. 括号生成:\n";
        $n = 3;
        $parentheses = BacktrackingAlgorithms::generateParentheses($n);
        echo "$n 对括号的所有有效组合:\n";
        foreach ($parentheses as $p) {
            echo "  $p\n";
        }
        
        // 电话号码字母组合
        echo "\n6. 电话号码字母组合:\n";
        $digits = "23";
        $combinations = BacktrackingAlgorithms::letterCombinations($digits);
        echo "数字 '$digits' 对应的字母组合:\n";
        foreach ($combinations as $comb) {
            echo "  $comb\n";
        }
    }
    
    private function demonstrateMathAlgorithms(): void
    {
        echo "\n\n--- 数学算法演示 ---\n";
        
        // 最大公约数和最小公倍数
        echo "\n1. 最大公约数和最小公倍数:\n";
        $testPairs = [[48, 18], [17, 13], [100, 25]];
        foreach ($testPairs as $pair) {
            $gcd = MathAlgorithms::gcd($pair[0], $pair[1]);
            $lcm = MathAlgorithms::lcm($pair[0], $pair[1]);
            echo "  gcd({$pair[0]}, {$pair[1]}) = $gcd\n";
            echo "  lcm({$pair[0]}, {$pair[1]}) = $lcm\n";
        }
        
        // 质数相关
        echo "\n2. 质数算法:\n";
        $numbers = [2, 3, 4, 17, 25, 29];
        foreach ($numbers as $num) {
            $isPrime = MathAlgorithms::isPrime($num);
            echo "  $num " . ($isPrime ? "是" : "不是") . "质数\n";
        }
        
        echo "\n  20以内的质数:\n";
        $primes = MathAlgorithms::sieveOfEratosthenes(20);
        echo "  [" . implode(", ", $primes) . "]\n";
        
        // 快速幂
        echo "\n3. 快速幂算法:\n";
        $testCases = [[2, 10], [3, 4], [5, 3]];
        foreach ($testCases as $case) {
            $result = MathAlgorithms::fastPower($case[0], $case[1]);
            $resultMod = MathAlgorithms::fastPower($case[0], $case[1], 1000);
            echo "  {$case[0]}^{$case[1]} = $result\n";
            echo "  {$case[0]}^{$case[1]} mod 1000 = $resultMod\n";
        }
        
        // 组合数和排列数
        echo "\n4. 组合数和排列数:\n";
        $n = 5;
        for ($k = 0; $k <= $n; $k++) {
            $comb = MathAlgorithms::combination($n, $k);
            $perm = MathAlgorithms::permutation($n, $k);
            echo "  C($n, $k) = $comb, P($n, $k) = $perm\n";
        }
        
        // 数字操作
        echo "\n5. 数字操作:\n";
        $numbers = [123, -456, 1001, 12321];
        foreach ($numbers as $num) {
            $reversed = MathAlgorithms::reverseInteger($num);
            $isPalindrome = MathAlgorithms::isPalindrome(abs($num));
            $digitSum = MathAlgorithms::digitSum($num);
            $digitCount = MathAlgorithms::countDigits($num);
            
            echo "  数字: $num\n";
            echo "    反转: $reversed\n";
            echo "    是否回文: " . ($isPalindrome ? "是" : "否") . "\n";
            echo "    数字和: $digitSum\n";
            echo "    位数: $digitCount\n";
        }
        
        // 平方根
        echo "\n6. 平方根算法:\n";
        $numbers = [9, 16, 10, 25, 30];
        foreach ($numbers as $num) {
            $intSqrt = MathAlgorithms::intSqrt($num);
            $isPerfect = MathAlgorithms::isPerfectSquare($num);
            echo "  $num 的整数平方根: $intSqrt, 是否完全平方数: " . ($isPerfect ? "是" : "否") . "\n";
        }
        
        // 约瑟夫问题
        echo "\n7. 约瑟夫问题:\n";
        $testCases = [[5, 2], [7, 3], [10, 3]];
        foreach ($testCases as $case) {
            $survivor = MathAlgorithms::josephus($case[0], $case[1]);
            echo "  n={$case[0]}, k={$case[1]} 时，幸存者位置: $survivor\n";
        }
        
        // 几何计算
        echo "\n8. 几何计算:\n";
        $point1 = [0, 0];
        $point2 = [3, 4];
        $point3 = [6, 8];
        
        $distance = MathAlgorithms::distance($point1, $point2);
        $collinear = MathAlgorithms::areCollinear($point1, $point2, $point3);
        
        echo "  点1: (" . implode(", ", $point1) . ")\n";
        echo "  点2: (" . implode(", ", $point2) . ")\n";
        echo "  点3: (" . implode(", ", $point3) . ")\n";
        echo "  点1到点2的距离: $distance\n";
        echo "  三点是否共线: " . ($collinear ? "是" : "否") . "\n";
    }
}

// 运行演示
try {
    $demo = new ComprehensiveAlgorithmsDemo();
    $demo->run();
} catch (Exception $e) {
    echo "错误: " . $e->getMessage() . "\n";
    echo "堆栈跟踪:\n" . $e->getTraceAsString() . "\n";
}