<?php

use PHPUnit\Framework\TestCase;
use DataStructures\Algorithms\Sorting;
use DataStructures\Algorithms\SearchAlgorithms;
use DataStructures\Algorithms\DynamicProgramming;
use DataStructures\Algorithms\GreedyAlgorithms;
use DataStructures\Algorithms\BacktrackingAlgorithms;
use DataStructures\Algorithms\MathAlgorithms;

/**
 * 算法测试类
 * 测试各种算法的正确性和边界情况
 */
class AlgorithmsTest extends TestCase
{
    /**
     * 测试排序算法
     */
    public function testSortingAlgorithms(): void
    {
        $testData = [64, 34, 25, 12, 22, 11, 90, 5, 77, 30];
        $expected = [5, 11, 12, 22, 25, 30, 34, 64, 77, 90];
        
        // 测试快速排序
        $quickSortData = $testData;
        Sorting::quickSort($quickSortData);
        $this->assertEquals($expected, $quickSortData);
        
        // 测试归并排序
        $mergeSortData = $testData;
        Sorting::mergeSort($mergeSortData);
        $this->assertEquals($expected, $mergeSortData);
        
        // 测试堆排序
        $heapSortData = $testData;
        Sorting::heapSort($heapSortData);
        $this->assertEquals($expected, $heapSortData);
        
        // 测试插入排序
        $insertionSortData = $testData;
        Sorting::insertionSort($insertionSortData);
        $this->assertEquals($expected, $insertionSortData);
        
        // 测试选择排序
        $selectionSortData = $testData;
        Sorting::selectionSort($selectionSortData);
        $this->assertEquals($expected, $selectionSortData);
        
        // 测试冒泡排序
        $bubbleSortData = $testData;
        Sorting::bubbleSort($bubbleSortData);
        $this->assertEquals($expected, $bubbleSortData);
        
        // 测试排序验证
        $this->assertTrue(Sorting::isSorted($expected));
        $this->assertFalse(Sorting::isSorted($testData));
    }
    
    /**
     * 测试搜索算法
     */
    public function testSearchAlgorithms(): void
    {
        $sortedArray = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19];
        $target = 7;
        $expectedIndex = 3;
        
        // 测试线性搜索
        $this->assertEquals($expectedIndex, SearchAlgorithms::linearSearch($sortedArray, $target));
        
        // 测试二分搜索
        $this->assertEquals($expectedIndex, SearchAlgorithms::binarySearch($sortedArray, $target));
        
        // 测试递归二分搜索
        $this->assertEquals($expectedIndex, SearchAlgorithms::binarySearchRecursive($sortedArray, $target, 0, count($sortedArray) - 1));
        
        // 测试插值搜索
        $this->assertEquals($expectedIndex, SearchAlgorithms::interpolationSearch($sortedArray, $target));
        
        // 测试不存在的元素
        $this->assertEquals(-1, SearchAlgorithms::binarySearch($sortedArray, 100));
    }
    
    /**
     * 测试动态规划算法
     */
    public function testDynamicProgramming(): void
    {
        // 测试斐波那契数列
        $this->assertEquals(0, DynamicProgramming::fibonacci(0));
        $this->assertEquals(1, DynamicProgramming::fibonacci(1));
        $this->assertEquals(55, DynamicProgramming::fibonacci(10));
        
        // 测试优化版斐波那契
        $this->assertEquals(55, DynamicProgramming::fibonacciOptimized(10));
        
        // 测试最长公共子序列
        $this->assertEquals(3, DynamicProgramming::longestCommonSubsequence("abcde", "ace"));
        $this->assertEquals(3, DynamicProgramming::longestCommonSubsequence("abc", "abc"));
        $this->assertEquals(0, DynamicProgramming::longestCommonSubsequence("abc", "def"));
        
        // 测试编辑距离
        $this->assertEquals(3, DynamicProgramming::editDistance("horse", "ros"));
        $this->assertEquals(5, DynamicProgramming::editDistance("intention", "execution"));
        
        // 测试0-1背包
        $weights = [10, 20, 30];
        $values = [60, 100, 120];
        $capacity = 50;
        $this->assertEquals(220, DynamicProgramming::knapsack01($weights, $values, $capacity));
        
        // 测试最长递增子序列
        $this->assertEquals(4, DynamicProgramming::longestIncreasingSubsequence([10, 9, 2, 5, 3, 7, 101, 18]));
        
        // 测试最大子数组和
        $this->assertEquals(6, DynamicProgramming::maxSubarraySum([-2, 1, -3, 4, -1, 2, 1, -5, 4]));
        
        // 测试硬币找零
        $this->assertEquals(3, DynamicProgramming::coinChange([1, 3, 4], 6));
        $this->assertEquals(-1, DynamicProgramming::coinChange([2], 3));
        
        // 测试爬楼梯
        $this->assertEquals(2, DynamicProgramming::climbStairs(2));
        $this->assertEquals(3, DynamicProgramming::climbStairs(3));
        
        // 测试房屋抢劫
        $this->assertEquals(4, DynamicProgramming::houseRobber([1, 2, 3, 1]));
        $this->assertEquals(12, DynamicProgramming::houseRobber([2, 7, 9, 3, 1]));
    }
    
    /**
     * 测试贪心算法
     */
    public function testGreedyAlgorithms(): void
    {
        // 测试活动选择
        $activities = [
            ['start' => 1, 'end' => 3],
            ['start' => 2, 'end' => 4],
            ['start' => 3, 'end' => 5],
            ['start' => 0, 'end' => 6],
            ['start' => 5, 'end' => 7],
            ['start' => 8, 'end' => 9],
            ['start' => 5, 'end' => 9]
        ];
        $selected = GreedyAlgorithms::activitySelection($activities);
        $this->assertGreaterThanOrEqual(3, count($selected));
        
        // 测试分数背包
        $items = [
            ['weight' => 10, 'value' => 60],
            ['weight' => 20, 'value' => 100],
            ['weight' => 30, 'value' => 120]
        ];
        $maxValue = GreedyAlgorithms::fractionalKnapsack($items, 50);
        $this->assertEquals(240, $maxValue);
        
        // 测试跳跃游戏
        $this->assertTrue(GreedyAlgorithms::canJump([2, 3, 1, 1, 4]));
        $this->assertFalse(GreedyAlgorithms::canJump([3, 2, 1, 0, 4]));
        
        // 测试最少跳跃次数
        $this->assertEquals(2, GreedyAlgorithms::minJumps([2, 3, 1, 1, 4]));
        
        // 测试股票最大利润
        $this->assertEquals(5, GreedyAlgorithms::maxProfit([7, 1, 5, 3, 6, 4]));
        $this->assertEquals(0, GreedyAlgorithms::maxProfit([7, 6, 4, 3, 1]));
        
        // 测试多次交易最大利润
        $this->assertEquals(7, GreedyAlgorithms::maxProfitMultiple([7, 1, 5, 3, 6, 4]));
    }
    
    /**
     * 测试回溯算法
     */
    public function testBacktrackingAlgorithms(): void
    {
        // 测试N皇后（4皇后）
        $solutions = BacktrackingAlgorithms::nQueens(4);
        $this->assertEquals(2, count($solutions));
        
        // 测试全排列
        $permutations = BacktrackingAlgorithms::permutations([1, 2, 3]);
        $this->assertEquals(6, count($permutations));
        
        // 测试组合
        $combinations = BacktrackingAlgorithms::combinations(4, 2);
        $this->assertEquals(6, count($combinations));
        
        // 测试子集
        $subsets = BacktrackingAlgorithms::subsets([1, 2, 3]);
        $this->assertEquals(8, count($subsets));
        
        // 测试单词搜索
        $board = [
            ['A', 'B', 'C', 'E'],
            ['S', 'F', 'C', 'S'],
            ['A', 'D', 'E', 'E']
        ];
        $this->assertTrue(BacktrackingAlgorithms::wordSearch($board, "ABCCED"));
        $this->assertTrue(BacktrackingAlgorithms::wordSearch($board, "SEE"));
        $this->assertFalse(BacktrackingAlgorithms::wordSearch($board, "ABCB"));
        
        // 测试括号生成
        $parentheses = BacktrackingAlgorithms::generateParentheses(3);
        $this->assertEquals(5, count($parentheses));
        $this->assertContains("((()))", $parentheses);
        $this->assertContains("(()())", $parentheses);
        
        // 测试电话号码字母组合
        $combinations = BacktrackingAlgorithms::letterCombinations("23");
        $this->assertEquals(9, count($combinations));
        $this->assertContains("ad", $combinations);
        $this->assertContains("cf", $combinations);
    }
    
    /**
     * 测试数学算法
     */
    public function testMathAlgorithms(): void
    {
        // 测试最大公约数
        $this->assertEquals(6, MathAlgorithms::gcd(48, 18));
        $this->assertEquals(1, MathAlgorithms::gcd(17, 13));
        
        // 测试最小公倍数
        $this->assertEquals(144, MathAlgorithms::lcm(48, 18));
        
        // 测试质数判断
        $this->assertTrue(MathAlgorithms::isPrime(17));
        $this->assertTrue(MathAlgorithms::isPrime(2));
        $this->assertFalse(MathAlgorithms::isPrime(4));
        $this->assertFalse(MathAlgorithms::isPrime(1));
        
        // 测试埃拉托斯特尼筛法
        $primes = MathAlgorithms::sieveOfEratosthenes(20);
        $expected = [2, 3, 5, 7, 11, 13, 17, 19];
        $this->assertEquals($expected, $primes);
        
        // 测试快速幂
        $this->assertEquals(1024, MathAlgorithms::fastPower(2, 10));
        $this->assertEquals(4, MathAlgorithms::fastPower(2, 10, 5));
        
        // 测试阶乘
        $this->assertEquals(1, MathAlgorithms::factorial(0));
        $this->assertEquals(1, MathAlgorithms::factorial(1));
        $this->assertEquals(120, MathAlgorithms::factorial(5));
        
        // 测试组合数
        $this->assertEquals(10, MathAlgorithms::combination(5, 2));
        $this->assertEquals(1, MathAlgorithms::combination(5, 0));
        $this->assertEquals(1, MathAlgorithms::combination(5, 5));
        
        // 测试排列数
        $this->assertEquals(20, MathAlgorithms::permutation(5, 2));
        $this->assertEquals(1, MathAlgorithms::permutation(5, 0));
        
        // 测试整数平方根
        $this->assertEquals(3, MathAlgorithms::intSqrt(9));
        $this->assertEquals(3, MathAlgorithms::intSqrt(10));
        $this->assertEquals(0, MathAlgorithms::intSqrt(0));
        
        // 测试完全平方数
        $this->assertTrue(MathAlgorithms::isPerfectSquare(16));
        $this->assertFalse(MathAlgorithms::isPerfectSquare(14));
        
        // 测试数字反转
        $this->assertEquals(321, MathAlgorithms::reverseInteger(123));
        $this->assertEquals(-321, MathAlgorithms::reverseInteger(-123));
        $this->assertEquals(21, MathAlgorithms::reverseInteger(120));
        
        // 测试回文数
        $this->assertTrue(MathAlgorithms::isPalindrome(121));
        $this->assertFalse(MathAlgorithms::isPalindrome(123));
        $this->assertFalse(MathAlgorithms::isPalindrome(-121));
        
        // 测试数字位数和
        $this->assertEquals(6, MathAlgorithms::digitSum(123));
        $this->assertEquals(1, MathAlgorithms::digitSum(10));
        
        // 测试数字位数
        $this->assertEquals(3, MathAlgorithms::countDigits(123));
        $this->assertEquals(1, MathAlgorithms::countDigits(0));
        
        // 测试约瑟夫问题
        $this->assertEquals(3, MathAlgorithms::josephus(5, 2));
        
        // 测试两点距离
        $distance = MathAlgorithms::distance([0, 0], [3, 4]);
        $this->assertEquals(5.0, $distance);
        
        // 测试三点共线
        $this->assertTrue(MathAlgorithms::areCollinear([0, 0], [1, 1], [2, 2]));
        $this->assertFalse(MathAlgorithms::areCollinear([0, 0], [1, 1], [2, 3]));
    }
    
    /**
     * 测试边界情况
     */
    public function testEdgeCases(): void
    {
        // 空数组排序
        $emptyArray = [];
        Sorting::quickSort($emptyArray);
        $this->assertEquals([], $emptyArray);
        
        // 单元素数组排序
        $singleElement = [42];
        Sorting::quickSort($singleElement);
        $this->assertEquals([42], $singleElement);
        
        // 空数组搜索
        $this->assertEquals(-1, SearchAlgorithms::linearSearch([], 5));
        
        // 动态规划边界情况
        $this->assertEquals(0, DynamicProgramming::fibonacci(0));
        $this->assertEquals(0, DynamicProgramming::longestCommonSubsequence("", "abc"));
        $this->assertEquals(0, DynamicProgramming::maxSubarraySum([]));
        
        // 数学算法边界情况
        $this->assertEquals(5, MathAlgorithms::gcd(5, 0));
        $this->assertEquals(0, MathAlgorithms::factorial(-1));
        $this->assertEquals(0, MathAlgorithms::combination(3, 5));
    }
}