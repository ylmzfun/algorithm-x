<?php

require_once __DIR__ . '/../vendor/autoload.php';

use DataStructures\Algorithms\Sorting;
use DataStructures\Algorithms\SearchAlgorithms;
use DataStructures\Graph\Graph;
use DataStructures\Graph\WeightedGraph;

/**
 * 算法演示程序
 * 展示各种算法的使用方法和性能
 */
class AlgorithmsDemo
{
    public function run(): void
    {
        echo "=== PHP 数据结构与算法库 - 算法演示 ===\n\n";
        
        $this->demonstrateSortingAlgorithms();
        $this->demonstrateSearchAlgorithms();
        $this->demonstrateBasicGraphOperations();
        
        echo "\n=== 算法演示完成 ===\n";
    }
    
    private function demonstrateSortingAlgorithms(): void
    {
        echo "\n--- 排序算法演示 ---\n";
        
        // 生成测试数据
        $data = [64, 34, 25, 12, 22, 11, 90, 5, 77, 30];
        echo "原始数据: [" . implode(", ", $data) . "]\n\n";
        
        // 快速排序
        $quickSortData = $data;
        Sorting::quickSort($quickSortData);
        echo "快速排序结果: [" . implode(", ", $quickSortData) . "]\n";
        
        // 归并排序
        $mergeSortData = $data;
        Sorting::mergeSort($mergeSortData);
        echo "归并排序结果: [" . implode(", ", $mergeSortData) . "]\n";
        
        // 堆排序
        $heapSortData = $data;
        Sorting::heapSort($heapSortData);
        echo "堆排序结果: [" . implode(", ", $heapSortData) . "]\n";
        
        // 插入排序
        $insertionSortData = $data;
        Sorting::insertionSort($insertionSortData);
        echo "插入排序结果: [" . implode(", ", $insertionSortData) . "]\n";
        
        // 选择排序
        $selectionSortData = $data;
        Sorting::selectionSort($selectionSortData);
        echo "选择排序结果: [" . implode(", ", $selectionSortData) . "]\n";
        
        // 冒泡排序
        $bubbleSortData = $data;
        Sorting::bubbleSort($bubbleSortData);
        echo "冒泡排序结果: [" . implode(", ", $bubbleSortData) . "]\n";
        
        // 验证排序结果
        echo "\n排序验证: " . (Sorting::isSorted($quickSortData) ? "✓ 正确" : "✗ 错误") . "\n";
        
        // 性能测试
        echo "\n--- 排序算法性能测试 ---\n";
        $largeData = [];
        for ($i = 0; $i < 1000; $i++) {
            $largeData[] = 1 + ($i * 7 + 13) % 1000;
        }
        
        $algorithms = [
            '快速排序' => 'quickSort',
            '归并排序' => 'mergeSort',
            '堆排序' => 'heapSort'
        ];
        
        foreach ($algorithms as $name => $method) {
            $testData = $largeData;
            $startTime = microtime(true);
            Sorting::$method($testData);
            $endTime = microtime(true);
            $duration = ($endTime - $startTime) * 1000;
            echo "$name (1000个元素): " . number_format($duration, 2) . " ms\n";
        }
    }
    
    private function demonstrateSearchAlgorithms(): void
    {
        echo "\n\n--- 搜索算法演示 ---\n";
        
        // 生成有序数组用于搜索
        $sortedArray = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25];
        echo "有序数组: [" . implode(", ", $sortedArray) . "]\n";
        echo "数组大小: " . count($sortedArray) . "\n";
        
        $target = 15;
        echo "搜索目标: $target\n\n";
        
        // 线性搜索
        $linearResult = SearchAlgorithms::linearSearch($sortedArray, $target);
        echo "线性搜索结果: " . ($linearResult !== -1 ? "找到，索引: $linearResult" : "未找到") . "\n";
        
        // 二分搜索（迭代版本）
        $binaryResult = SearchAlgorithms::binarySearch($sortedArray, $target);
        echo "二分搜索结果: " . ($binaryResult !== -1 ? "找到，索引: $binaryResult" : "未找到") . "\n";
        
        // 二分搜索（递归版本）
        $binaryRecursiveResult = SearchAlgorithms::binarySearchRecursive($sortedArray, $target, 0, count($sortedArray) - 1);
        echo "递归二分搜索结果: " . ($binaryRecursiveResult !== -1 ? "找到，索引: $binaryRecursiveResult" : "未找到") . "\n";
        
        // 插值搜索
        $interpolationResult = SearchAlgorithms::interpolationSearch($sortedArray, $target);
        echo "插值搜索结果: " . ($interpolationResult !== -1 ? "找到，索引: $interpolationResult" : "未找到") . "\n";
        
        // 指数搜索
        $exponentialResult = SearchAlgorithms::exponentialSearch($sortedArray, $target);
        echo "指数搜索结果: " . ($exponentialResult !== -1 ? "找到，索引: $exponentialResult" : "未找到") . "\n";
        
        // 跳跃搜索
        $jumpResult = SearchAlgorithms::jumpSearch($sortedArray, $target);
        echo "跳跃搜索结果: " . ($jumpResult !== -1 ? "找到，索引: $jumpResult" : "未找到") . "\n";
        
        // 三分搜索
        $ternaryResult = SearchAlgorithms::ternarySearch($sortedArray, $target, 0, count($sortedArray) - 1);
        echo "三分搜索结果: " . ($ternaryResult !== -1 ? "找到，索引: $ternaryResult" : "未找到") . "\n";
        
        // 斐波那契搜索
        $fibonacciResult = SearchAlgorithms::fibonacciSearch($sortedArray, $target);
        echo "斐波那契搜索结果: " . ($fibonacciResult !== -1 ? "找到，索引: $fibonacciResult" : "未找到") . "\n";
        
        // 查找操作演示
        $duplicateArray = [1, 2, 2, 2, 3, 4, 5];
        echo "\n重复元素数组: [" . implode(", ", $duplicateArray) . "]\n";
        
        // 使用线性搜索查找元素
        $searchTarget = 2;
        $found = false;
        $positions = [];
        for ($i = 0; $i < count($duplicateArray); $i++) {
            if ($duplicateArray[$i] === $searchTarget) {
                $positions[] = $i;
                $found = true;
            }
        }
        
        if ($found) {
            echo "元素{$searchTarget}的出现位置: [" . implode(", ", $positions) . "]\n";
            echo "第一次出现位置: {$positions[0]}\n";
            echo "最后一次出现位置: " . end($positions) . "\n";
        } else {
            echo "元素{$searchTarget}未找到\n";
        }
        
        // 在旋转数组中搜索
        $rotatedArray = [4, 5, 6, 7, 0, 1, 2];
        echo "\n旋转数组: [" . implode(", ", $rotatedArray) . "]\n";
        $rotatedTarget = 0;
        $rotatedResult = SearchAlgorithms::searchInRotatedArray($rotatedArray, $rotatedTarget);
        echo "在旋转数组中搜索 $rotatedTarget: " . ($rotatedResult !== -1 ? "找到，索引: $rotatedResult" : "未找到") . "\n";
        
        // 查找旋转点
        $rotationPoint = SearchAlgorithms::findRotationPoint($rotatedArray);
        echo "旋转点索引: $rotationPoint (值: {$rotatedArray[$rotationPoint]})\n";
        
        // 查找缺失数字
        $missingArray = [0, 1, 3, 4, 5];
        echo "\n缺失数字数组: [" . implode(", ", $missingArray) . "]\n";
        $missingNumber = SearchAlgorithms::findMissingNumber($missingArray);
        echo "缺失的数字: $missingNumber\n";
    }
    
    private function demonstrateBasicGraphOperations(): void
    {
        echo "\n\n--- 图基本操作演示 ---\n";
        
        // 创建无向图
        $graph = new Graph();
        $vertices = ['A', 'B', 'C', 'D', 'E'];
        
        foreach ($vertices as $vertex) {
            $graph->addVertex($vertex);
        }
        
        $graph->addEdge('A', 'B');
        $graph->addEdge('A', 'C');
        $graph->addEdge('B', 'D');
        $graph->addEdge('C', 'D');
        $graph->addEdge('D', 'E');
        
        echo "图的顶点: [" . implode(", ", $graph->getVertices()) . "]\n";
        echo "图的大小: " . count($graph->getVertices()) . " 个顶点\n";
        echo "图是否为空: " . ($graph->isEmpty() ? "是" : "否") . "\n";
        
        // 检查边的存在
        echo "\n边的存在性检查:\n";
        $edgesToCheck = [['A', 'B'], ['A', 'E'], ['B', 'C'], ['C', 'D']];
        foreach ($edgesToCheck as $edge) {
            $exists = $graph->hasEdge($edge[0], $edge[1]);
            echo "  {$edge[0]} - {$edge[1]}: " . ($exists ? "存在" : "不存在") . "\n";
        }
        
        // 获取邻居
        echo "\n各顶点的邻居:\n";
        foreach ($vertices as $vertex) {
            $neighbors = $graph->getNeighbors($vertex);
            echo "  $vertex: [" . implode(", ", $neighbors) . "]\n";
        }
        
        // 获取度数
        echo "\n各顶点的度数:\n";
        foreach ($vertices as $vertex) {
            $degree = $graph->getDegree($vertex);
            echo "  $vertex: $degree\n";
        }
        
        // 创建加权图
        echo "\n--- 加权图演示 ---\n";
        $weightedGraph = new WeightedGraph();
        $cities = ['北京', '上海', '广州', '深圳'];
        
        foreach ($cities as $city) {
            $weightedGraph->addVertex($city);
        }
        
        // 添加带权重的边（距离）
        $weightedGraph->addEdge('北京', '上海', 1200);
        $weightedGraph->addEdge('北京', '广州', 2100);
        $weightedGraph->addEdge('上海', '广州', 1400);
        $weightedGraph->addEdge('广州', '深圳', 140);
        
        echo "加权图的顶点: [" . implode(", ", $weightedGraph->getVertices()) . "]\n";
        
        // 显示权重
        echo "\n边的权重:\n";
        $edges = [['北京', '上海'], ['北京', '广州'], ['上海', '广州'], ['广州', '深圳']];
        foreach ($edges as $edge) {
            $weight = $weightedGraph->getWeight($edge[0], $edge[1]);
            if ($weight !== null) {
                echo "  {$edge[0]} - {$edge[1]}: {$weight}km\n";
            }
        }
        
        // 修改权重
        echo "\n修改权重演示:\n";
        $oldWeight = $weightedGraph->getWeight('北京', '上海');
        echo "北京-上海原权重: {$oldWeight}km\n";
        
        $weightedGraph->setWeight('北京', '上海', 1150);
        $newWeight = $weightedGraph->getWeight('北京', '上海');
        echo "北京-上海新权重: {$newWeight}km\n";
        
        // 移除边和顶点
        echo "\n移除操作演示:\n";
        echo "移除边 广州-深圳: " . ($weightedGraph->removeEdge('广州', '深圳') ? "成功" : "失败") . "\n";
        echo "移除顶点 深圳: " . ($weightedGraph->removeVertex('深圳') ? "成功" : "失败") . "\n";
        echo "移除后的顶点: [" . implode(", ", $weightedGraph->getVertices()) . "]\n";
    }
}

// 运行演示
try {
    $demo = new AlgorithmsDemo();
    $demo->run();
} catch (Exception $e) {
    echo "错误: " . $e->getMessage() . "\n";
    echo "堆栈跟踪:\n" . $e->getTraceAsString() . "\n";
}