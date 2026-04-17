<?php

/**
 * 算法基准测试工具
 * 用于比较不同算法的性能表现
 */

require_once __DIR__ . '/../vendor/autoload.php';

use DataStructures\Algorithms\Sorting;
use DataStructures\Algorithms\SearchAlgorithms;
use DataStructures\Algorithms\DynamicProgramming;
use DataStructures\Algorithms\MathAlgorithms;
use DataStructures\Utils\Utils;
use DataStructures\Config\Config;

class Benchmark
{
    private $results = [];
    private $outputFormat = 'text';
    
    public function __construct(string $outputFormat = 'text')
    {
        $this->outputFormat = $outputFormat;
        Config::setupRuntime();
    }
    
    /**
     * 运行所有基准测试
     */
    public function runAll(): void
    {
        $this->printHeader();
        
        $this->benchmarkSortingAlgorithms();
        $this->benchmarkSearchAlgorithms();
        $this->benchmarkDynamicProgramming();
        $this->benchmarkMathAlgorithms();
        
        $this->printResults();
        $this->generateReport();
    }
    
    /**
     * 基准测试排序算法
     */
    public function benchmarkSortingAlgorithms(): void
    {
        $this->printSection('排序算法基准测试');
        
        $algorithms = [
            'QuickSort' => function(&$arr) { Sorting::quickSort($arr); },
            'MergeSort' => function(&$arr) { Sorting::mergeSort($arr); },
            'HeapSort' => function(&$arr) { Sorting::heapSort($arr); },
            'InsertionSort' => function(&$arr) { Sorting::insertionSort($arr); },
            'SelectionSort' => function(&$arr) { Sorting::selectionSort($arr); },
            'BubbleSort' => function(&$arr) { Sorting::bubbleSort($arr); }
        ];
        
        $sizes = [100, 500, 1000, 2000];
        
        foreach ($sizes as $size) {
            $this->printSubSection("数组大小: {$size}");
            
            // 生成测试数据
            $originalArray = Utils::generateRandomArray($size, 1, 1000);
            
            foreach ($algorithms as $name => $algorithm) {
                // 跳过大数据集上的慢算法
                if ($size > 1000 && in_array($name, ['BubbleSort', 'SelectionSort', 'InsertionSort'])) {
                    continue;
                }
                
                $testArray = $originalArray;
                $result = $this->measurePerformance($algorithm, $testArray, 3);
                
                $this->results['sorting'][$size][$name] = $result;
                $this->printResult($name, $result);
            }
        }
    }
    
    /**
     * 基准测试搜索算法
     */
    public function benchmarkSearchAlgorithms(): void
    {
        $this->printSection('搜索算法基准测试');
        
        $sizes = [1000, 5000, 10000, 20000];
        
        foreach ($sizes as $size) {
            $this->printSubSection("数组大小: {$size}");
            
            // 生成有序数组
            $array = range(1, $size);
            $target = $size / 2;
            
            $algorithms = [
                'LinearSearch' => function() use ($array, $target) {
                    return SearchAlgorithms::linearSearch($array, $target);
                },
                'BinarySearch' => function() use ($array, $target) {
                    return SearchAlgorithms::binarySearch($array, $target);
                },
                'InterpolationSearch' => function() use ($array, $target) {
                    return SearchAlgorithms::interpolationSearch($array, $target);
                },
                'ExponentialSearch' => function() use ($array, $target) {
                    return SearchAlgorithms::exponentialSearch($array, $target);
                },
                'JumpSearch' => function() use ($array, $target) {
                    return SearchAlgorithms::jumpSearch($array, $target);
                }
            ];
            
            foreach ($algorithms as $name => $algorithm) {
                // 线性搜索在大数据集上太慢
                if ($size > 5000 && $name === 'LinearSearch') {
                    continue;
                }
                
                $result = $this->measurePerformance($algorithm, null, 100);
                $this->results['search'][$size][$name] = $result;
                $this->printResult($name, $result);
            }
        }
    }
    
    /**
     * 基准测试动态规划算法
     */
    public function benchmarkDynamicProgramming(): void
    {
        $this->printSection('动态规划算法基准测试');
        
        $dp = new DynamicProgramming();
        
        // 斐波那契数列测试
        $this->printSubSection('斐波那契数列');
        $fibNumbers = [20, 25, 30, 35, 40];
        
        foreach ($fibNumbers as $n) {
            $algorithms = [
                'Fibonacci' => function() use ($dp, $n) {
                    return $dp->fibonacci($n);
                },
                'FibonacciOptimized' => function() use ($dp, $n) {
                    return $dp->fibonacciOptimized($n);
                }
            ];
            
            foreach ($algorithms as $name => $algorithm) {
                // 普通递归在大数字上太慢
                if ($n > 30 && $name === 'Fibonacci') {
                    continue;
                }
                
                $result = $this->measurePerformance($algorithm, null, 10);
                $this->results['dp']['fibonacci'][$n][$name] = $result;
                $this->printResult("{$name}({$n})", $result);
            }
        }
        
        // LCS测试
        $this->printSubSection('最长公共子序列');
        $testCases = [
            ['ABCDGH', 'AEDFHR'],
            ['AGGTAB', 'GXTXAYB'],
            ['PROGRAMMING', 'ALGORITHM'],
            ['ABCDEFGHIJKLMNOP', 'ACEGIKMOQSUWY']
        ];
        
        foreach ($testCases as $i => $case) {
            $algorithm = function() use ($dp, $case) {
                return $dp->longestCommonSubsequence($case[0], $case[1]);
            };
            
            $result = $this->measurePerformance($algorithm, null, 10);
            $this->results['dp']['lcs'][$i] = $result;
            $this->printResult("LCS({$case[0]}, {$case[1]})", $result);
        }
    }
    
    /**
     * 基准测试数学算法
     */
    public function benchmarkMathAlgorithms(): void
    {
        $this->printSection('数学算法基准测试');
        
        $math = new MathAlgorithms();
        
        // 质数筛法测试
        $this->printSubSection('质数筛法');
        $limits = [1000, 5000, 10000, 50000];
        
        foreach ($limits as $limit) {
            $algorithm = function() use ($math, $limit) {
                return $math->sieveOfEratosthenes($limit);
            };
            
            $result = $this->measurePerformance($algorithm, null, 5);
            $this->results['math']['sieve'][$limit] = $result;
            $this->printResult("Sieve({$limit})", $result);
        }
        
        // GCD测试
        $this->printSubSection('最大公约数');
        $testCases = [
            [48, 18],
            [1071, 462],
            [12345, 6789],
            [987654321, 123456789]
        ];
        
        foreach ($testCases as $i => $case) {
            $algorithm = function() use ($math, $case) {
                return $math->gcd($case[0], $case[1]);
            };
            
            $result = $this->measurePerformance($algorithm, null, 1000);
            $this->results['math']['gcd'][$i] = $result;
            $this->printResult("GCD({$case[0]}, {$case[1]})", $result);
        }
        
        // 快速幂测试
        $this->printSubSection('快速幂');
        $testCases = [
            [2, 10, 1000],
            [3, 20, 1000],
            [5, 100, 1000000],
            [7, 1000, 1000000007]
        ];
        
        foreach ($testCases as $i => $case) {
            $algorithm = function() use ($math, $case) {
                return $math->fastPower($case[0], $case[1], $case[2]);
            };
            
            $result = $this->measurePerformance($algorithm, null, 100);
            $this->results['math']['power'][$i] = $result;
            $this->printResult("Power({$case[0]}^{$case[1]} mod {$case[2]})", $result);
        }
    }
    
    /**
     * 测量算法性能
     */
    private function measurePerformance(callable $algorithm, &$data = null, int $iterations = 1): array
    {
        $times = [];
        $memoryUsages = [];
        
        for ($i = 0; $i < $iterations; $i++) {
            // 重置数据
            if ($data !== null) {
                $testData = $data;
            }
            
            // 记录开始状态
            $startTime = microtime(true);
            $startMemory = memory_get_usage();
            
            // 执行算法
            if ($data !== null) {
                $algorithm($testData);
            } else {
                $algorithm();
            }
            
            // 记录结束状态
            $endTime = microtime(true);
            $endMemory = memory_get_usage();
            
            $times[] = ($endTime - $startTime) * 1000; // 转换为毫秒
            $memoryUsages[] = $endMemory - $startMemory;
        }
        
        return [
            'avg_time' => array_sum($times) / count($times),
            'min_time' => min($times),
            'max_time' => max($times),
            'avg_memory' => array_sum($memoryUsages) / count($memoryUsages),
            'iterations' => $iterations
        ];
    }
    
    /**
     * 打印标题
     */
    private function printHeader(): void
    {
        if ($this->outputFormat === 'text') {
            echo "\n" . str_repeat('=', 60) . "\n";
            echo "         算法性能基准测试工具\n";
            echo "         PHP版本: " . PHP_VERSION . "\n";
            echo "         测试时间: " . date('Y-m-d H:i:s') . "\n";
            echo str_repeat('=', 60) . "\n";
        }
    }
    
    /**
     * 打印章节标题
     */
    private function printSection(string $title): void
    {
        if ($this->outputFormat === 'text') {
            echo "\n" . str_repeat('-', 40) . "\n";
            echo "  {$title}\n";
            echo str_repeat('-', 40) . "\n";
        }
    }
    
    /**
     * 打印子章节标题
     */
    private function printSubSection(string $title): void
    {
        if ($this->outputFormat === 'text') {
            echo "\n{$title}:\n";
        }
    }
    
    /**
     * 打印结果
     */
    private function printResult(string $name, array $result): void
    {
        if ($this->outputFormat === 'text') {
            printf("  %-20s: %8.3fms (内存: %8s)\n", 
                $name, 
                $result['avg_time'], 
                $this->formatBytes($result['avg_memory'])
            );
        }
    }
    
    /**
     * 打印所有结果
     */
    private function printResults(): void
    {
        if ($this->outputFormat === 'json') {
            echo json_encode($this->results, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
        }
    }
    
    /**
     * 生成报告
     */
    private function generateReport(): void
    {
        $reportFile = __DIR__ . '/../tests/output/benchmark_report_' . date('Y-m-d_H-i-s') . '.json';
        
        // 确保输出目录存在
        $outputDir = dirname($reportFile);
        if (!is_dir($outputDir)) {
            mkdir($outputDir, 0755, true);
        }
        
        $report = [
            'timestamp' => date('c'),
            'php_version' => PHP_VERSION,
            'memory_limit' => ini_get('memory_limit'),
            'max_execution_time' => ini_get('max_execution_time'),
            'results' => $this->results
        ];
        
        file_put_contents($reportFile, json_encode($report, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
        
        if ($this->outputFormat === 'text') {
            echo "\n报告已保存到: {$reportFile}\n";
        }
    }
    
    /**
     * 格式化字节数
     */
    private function formatBytes(int $bytes): string
    {
        if ($bytes >= 1024 * 1024) {
            return round($bytes / 1024 / 1024, 2) . 'MB';
        } elseif ($bytes >= 1024) {
            return round($bytes / 1024, 2) . 'KB';
        } else {
            return $bytes . 'B';
        }
    }
}

// 命令行参数处理
$outputFormat = 'text';
if (isset($argv[1]) && in_array($argv[1], ['text', 'json'])) {
    $outputFormat = $argv[1];
}

// 运行基准测试
if (basename(__FILE__) === basename($_SERVER['SCRIPT_NAME'])) {
    $benchmark = new Benchmark($outputFormat);
    $benchmark->runAll();
}