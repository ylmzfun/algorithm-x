<?php

namespace DataStructures\Tests;

require_once __DIR__ . '/../vendor/autoload.php';

use DataStructures\Algorithms\Sorting;
use DataStructures\Algorithms\SearchAlgorithms;
use DataStructures\Algorithms\DynamicProgramming;
use DataStructures\Algorithms\GreedyAlgorithms;
use DataStructures\Algorithms\MathAlgorithms;
use DataStructures\Utils\Utils;

/**
 * 性能测试类
 * 用于测试各种算法的性能表现
 */
class PerformanceTest
{
    private $results = [];
    
    /**
     * 运行所有性能测试
     */
    public function runAllTests(): void
    {
        echo "\n=== 算法性能测试 ===\n";
        
        $this->testSortingAlgorithms();
        $this->testSearchAlgorithms();
        $this->testDynamicProgramming();
        $this->testMathAlgorithms();
        
        $this->printSummary();
    }
    
    /**
     * 测试排序算法性能
     */
    private function testSortingAlgorithms(): void
    {
        echo "\n--- 排序算法性能测试 ---\n";
        
        $sizes = [1000, 5000, 10000];
        
        foreach ($sizes as $size) {
            echo "\n数组大小: {$size}\n";
            
            // 生成随机数组
            $array = Utils::generateRandomArray($size, 1, 1000);
            
            // 测试快速排序
            $testArray = $array;
            $time = $this->measureTime(function() use (&$testArray) {
                Sorting::quickSort($testArray);
            });
            echo "快速排序: {$time}ms\n";
            $this->results['QuickSort'][$size] = $time;
            
            // 测试归并排序
            $testArray = $array;
            $time = $this->measureTime(function() use (&$testArray) {
                Sorting::mergeSort($testArray);
            });
            echo "归并排序: {$time}ms\n";
            $this->results['MergeSort'][$size] = $time;
            
            // 测试堆排序
            $testArray = $array;
            $time = $this->measureTime(function() use (&$testArray) {
                Sorting::heapSort($testArray);
            });
            echo "堆排序: {$time}ms\n";
            $this->results['HeapSort'][$size] = $time;
        }
    }
    
    /**
     * 测试搜索算法性能
     */
    private function testSearchAlgorithms(): void
    {
        echo "\n--- 搜索算法性能测试 ---\n";
        
        $sizes = [10000, 50000, 100000];
        
        foreach ($sizes as $size) {
            echo "\n数组大小: {$size}\n";
            
            // 生成有序数组
            $array = range(1, $size);
            $target = $size / 2;
            
            // 测试二分搜索
            $time = $this->measureTime(function() use ($array, $target) {
                SearchAlgorithms::binarySearch($array, $target);
            });
            echo "二分搜索: {$time}ms\n";
            $this->results['BinarySearch'][$size] = $time;
        }
    }
    
    /**
     * 测试动态规划算法性能
     */
    private function testDynamicProgramming(): void
    {
        echo "\n--- 动态规划算法性能测试 ---\n";
        
        $dp = new DynamicProgramming();
        
        // 测试斐波那契数列
        $numbers = [30, 35, 40];
        foreach ($numbers as $n) {
            $time = $this->measureTime(function() use ($dp, $n) {
                $dp->fibonacciOptimized($n);
            });
            echo "斐波那契({$n}): {$time}ms\n";
        }
        
        // 测试最长公共子序列
        $strings = [
            ['ABCDGH', 'AEDFHR'],
            ['AGGTAB', 'GXTXAYB'],
            ['ABCDEFGHIJKLMNOP', 'ACEGIKMOQSUWY']
        ];
        
        foreach ($strings as $i => $pair) {
            $time = $this->measureTime(function() use ($dp, $pair) {
                $dp->longestCommonSubsequence($pair[0], $pair[1]);
            });
            echo "LCS测试" . ($i + 1) . ": {$time}ms\n";
        }
    }
    
    /**
     * 测试数学算法性能
     */
    private function testMathAlgorithms(): void
    {
        echo "\n--- 数学算法性能测试 ---\n";
        
        $math = new MathAlgorithms();
        
        // 测试质数筛法
        $limits = [1000, 10000, 100000];
        foreach ($limits as $limit) {
            $time = $this->measureTime(function() use ($math, $limit) {
                $math->sieveOfEratosthenes($limit);
            });
            echo "质数筛法({$limit}): {$time}ms\n";
        }
        
        // 测试快速幂
        $cases = [
            [2, 10, 1000],
            [3, 20, 1000],
            [5, 30, 1000]
        ];
        
        foreach ($cases as $i => $case) {
            $time = $this->measureTime(function() use ($math, $case) {
                $math->fastPower($case[0], $case[1], $case[2]);
            });
            echo "快速幂测试" . ($i + 1) . ": {$time}ms\n";
        }
        
        // 测试GCD
        $pairs = [
            [1071, 462],
            [12345, 6789],
            [987654321, 123456789]
        ];
        
        foreach ($pairs as $i => $pair) {
            $time = $this->measureTime(function() use ($math, $pair) {
                $math->gcd($pair[0], $pair[1]);
            });
            echo "GCD测试" . ($i + 1) . ": {$time}ms\n";
        }
    }
    
    /**
     * 测量函数执行时间
     */
    private function measureTime(callable $function): float
    {
        $start = microtime(true);
        $function();
        $end = microtime(true);
        
        return round(($end - $start) * 1000, 3); // 转换为毫秒
    }
    
    /**
     * 打印测试总结
     */
    private function printSummary(): void
    {
        echo "\n=== 性能测试总结 ===\n";
        echo "测试完成时间: " . date('Y-m-d H:i:s') . "\n";
        echo "PHP版本: " . PHP_VERSION . "\n";
        echo "内存使用: " . round(memory_get_peak_usage() / 1024 / 1024, 2) . "MB\n";
        
        if (!empty($this->results)) {
            echo "\n排序算法性能对比 (1000元素):\n";
            foreach (['QuickSort', 'MergeSort', 'HeapSort'] as $algorithm) {
                if (isset($this->results[$algorithm][1000])) {
                    echo "{$algorithm}: {$this->results[$algorithm][1000]}ms\n";
                }
            }
        }
    }
}

// 如果直接运行此文件，执行性能测试
if (basename(__FILE__) === basename($_SERVER['SCRIPT_NAME'])) {
    $test = new PerformanceTest();
    $test->runAllTests();
}