<?php

namespace DataStructures\Algorithms;

/**
 * 排序算法集合
 * 包含常见的排序算法实现
 */
class Sorting
{
    /**
     * 快速排序
     * 时间复杂度: 平均 O(n log n), 最坏 O(n²)
     * 空间复杂度: O(log n)
     */
    public static function quickSort(array &$arr, int $low = 0, int $high = null): void
    {
        if ($high === null) {
            $high = count($arr) - 1;
        }
        
        if ($low < $high) {
            $pi = self::partition($arr, $low, $high);
            self::quickSort($arr, $low, $pi - 1);
            self::quickSort($arr, $pi + 1, $high);
        }
    }
    
    private static function partition(array &$arr, int $low, int $high): int
    {
        $pivot = $arr[$high];
        $i = $low - 1;
        
        for ($j = $low; $j < $high; $j++) {
            if ($arr[$j] <= $pivot) {
                $i++;
                self::swap($arr, $i, $j);
            }
        }
        
        self::swap($arr, $i + 1, $high);
        return $i + 1;
    }
    
    /**
     * 归并排序
     * 时间复杂度: O(n log n)
     * 空间复杂度: O(n)
     */
    public static function mergeSort(array &$arr, int $left = 0, int $right = null): void
    {
        if ($right === null) {
            $right = count($arr) - 1;
        }
        
        if ($left < $right) {
            $mid = intval(($left + $right) / 2);
            self::mergeSort($arr, $left, $mid);
            self::mergeSort($arr, $mid + 1, $right);
            self::merge($arr, $left, $mid, $right);
        }
    }
    
    private static function merge(array &$arr, int $left, int $mid, int $right): void
    {
        $leftArr = array_slice($arr, $left, $mid - $left + 1);
        $rightArr = array_slice($arr, $mid + 1, $right - $mid);
        
        $i = 0; $j = 0; $k = $left;
        
        while ($i < count($leftArr) && $j < count($rightArr)) {
            if ($leftArr[$i] <= $rightArr[$j]) {
                $arr[$k] = $leftArr[$i];
                $i++;
            } else {
                $arr[$k] = $rightArr[$j];
                $j++;
            }
            $k++;
        }
        
        while ($i < count($leftArr)) {
            $arr[$k] = $leftArr[$i];
            $i++;
            $k++;
        }
        
        while ($j < count($rightArr)) {
            $arr[$k] = $rightArr[$j];
            $j++;
            $k++;
        }
    }
    
    /**
     * 堆排序
     * 时间复杂度: O(n log n)
     * 空间复杂度: O(1)
     */
    public static function heapSort(array &$arr): void
    {
        $n = count($arr);
        
        // 构建最大堆
        for ($i = intval($n / 2) - 1; $i >= 0; $i--) {
            self::heapify($arr, $n, $i);
        }
        
        // 逐个提取元素
        for ($i = $n - 1; $i > 0; $i--) {
            self::swap($arr, 0, $i);
            self::heapify($arr, $i, 0);
        }
    }
    
    private static function heapify(array &$arr, int $n, int $i): void
    {
        $largest = $i;
        $left = 2 * $i + 1;
        $right = 2 * $i + 2;
        
        if ($left < $n && $arr[$left] > $arr[$largest]) {
            $largest = $left;
        }
        
        if ($right < $n && $arr[$right] > $arr[$largest]) {
            $largest = $right;
        }
        
        if ($largest != $i) {
            self::swap($arr, $i, $largest);
            self::heapify($arr, $n, $largest);
        }
    }
    
    /**
     * 插入排序
     * 时间复杂度: O(n²)
     * 空间复杂度: O(1)
     */
    public static function insertionSort(array &$arr): void
    {
        $n = count($arr);
        for ($i = 1; $i < $n; $i++) {
            $key = $arr[$i];
            $j = $i - 1;
            
            while ($j >= 0 && $arr[$j] > $key) {
                $arr[$j + 1] = $arr[$j];
                $j--;
            }
            $arr[$j + 1] = $key;
        }
    }
    
    /**
     * 选择排序
     * 时间复杂度: O(n²)
     * 空间复杂度: O(1)
     */
    public static function selectionSort(array &$arr): void
    {
        $n = count($arr);
        for ($i = 0; $i < $n - 1; $i++) {
            $minIdx = $i;
            for ($j = $i + 1; $j < $n; $j++) {
                if ($arr[$j] < $arr[$minIdx]) {
                    $minIdx = $j;
                }
            }
            self::swap($arr, $minIdx, $i);
        }
    }
    
    /**
     * 冒泡排序
     * 时间复杂度: O(n²)
     * 空间复杂度: O(1)
     */
    public static function bubbleSort(array &$arr): void
    {
        $n = count($arr);
        for ($i = 0; $i < $n - 1; $i++) {
            $swapped = false;
            for ($j = 0; $j < $n - $i - 1; $j++) {
                if ($arr[$j] > $arr[$j + 1]) {
                    self::swap($arr, $j, $j + 1);
                    $swapped = true;
                }
            }
            if (!$swapped) break;
        }
    }
    
    /**
     * 计数排序
     * 时间复杂度: O(n + k)
     * 空间复杂度: O(k)
     */
    public static function countingSort(array &$arr, int $maxVal = null): void
    {
        if (empty($arr)) return;
        
        if ($maxVal === null) {
            $maxVal = max($arr);
        }
        
        $count = array_fill(0, $maxVal + 1, 0);
        
        // 计数
        foreach ($arr as $num) {
            $count[$num]++;
        }
        
        // 重构数组
        $index = 0;
        for ($i = 0; $i <= $maxVal; $i++) {
            while ($count[$i]-- > 0) {
                $arr[$index++] = $i;
            }
        }
    }
    
    /**
     * 基数排序
     * 时间复杂度: O(d * (n + k))
     * 空间复杂度: O(n + k)
     */
    public static function radixSort(array &$arr): void
    {
        if (empty($arr)) return;
        
        $max = max($arr);
        
        for ($exp = 1; intval($max / $exp) > 0; $exp *= 10) {
            self::countingSortByDigit($arr, $exp);
        }
    }
    
    private static function countingSortByDigit(array &$arr, int $exp): void
    {
        $n = count($arr);
        $output = array_fill(0, $n, 0);
        $count = array_fill(0, 10, 0);
        
        // 计数
        for ($i = 0; $i < $n; $i++) {
            $count[intval($arr[$i] / $exp) % 10]++;
        }
        
        // 累计计数
        for ($i = 1; $i < 10; $i++) {
            $count[$i] += $count[$i - 1];
        }
        
        // 构建输出数组
        for ($i = $n - 1; $i >= 0; $i--) {
            $digit = intval($arr[$i] / $exp) % 10;
            $output[$count[$digit] - 1] = $arr[$i];
            $count[$digit]--;
        }
        
        // 复制回原数组
        for ($i = 0; $i < $n; $i++) {
            $arr[$i] = $output[$i];
        }
    }
    
    /**
     * 桶排序
     * 时间复杂度: 平均 O(n + k), 最坏 O(n²)
     * 空间复杂度: O(n + k)
     */
    public static function bucketSort(array &$arr, int $bucketCount = 10): void
    {
        if (empty($arr)) return;
        
        $min = min($arr);
        $max = max($arr);
        $range = ($max - $min) / $bucketCount;
        
        $buckets = array_fill(0, $bucketCount, []);
        
        // 分配到桶中
        foreach ($arr as $num) {
            $bucketIndex = min(intval(($num - $min) / $range), $bucketCount - 1);
            $buckets[$bucketIndex][] = $num;
        }
        
        // 对每个桶排序并合并
        $arr = [];
        foreach ($buckets as $bucket) {
            if (!empty($bucket)) {
                sort($bucket);
                $arr = array_merge($arr, $bucket);
            }
        }
    }
    
    /**
     * 交换数组中两个元素
     */
    private static function swap(array &$arr, int $i, int $j): void
    {
        $temp = $arr[$i];
        $arr[$i] = $arr[$j];
        $arr[$j] = $temp;
    }
    
    /**
     * 检查数组是否已排序
     */
    public static function isSorted(array $arr, bool $ascending = true): bool
    {
        $n = count($arr);
        for ($i = 1; $i < $n; $i++) {
            if ($ascending && $arr[$i] < $arr[$i - 1]) {
                return false;
            }
            if (!$ascending && $arr[$i] > $arr[$i - 1]) {
                return false;
            }
        }
        return true;
    }
    
    /**
     * 获取排序算法的性能统计
     */
    public static function benchmarkSort(array $arr, string $algorithm = 'quickSort'): array
    {
        $testArr = $arr; // 复制数组
        $startTime = microtime(true);
        $startMemory = memory_get_usage();
        
        switch ($algorithm) {
            case 'quickSort':
                self::quickSort($testArr);
                break;
            case 'mergeSort':
                self::mergeSort($testArr);
                break;
            case 'heapSort':
                self::heapSort($testArr);
                break;
            case 'insertionSort':
                self::insertionSort($testArr);
                break;
            case 'selectionSort':
                self::selectionSort($testArr);
                break;
            case 'bubbleSort':
                self::bubbleSort($testArr);
                break;
            case 'countingSort':
                self::countingSort($testArr);
                break;
            case 'radixSort':
                self::radixSort($testArr);
                break;
            case 'bucketSort':
                self::bucketSort($testArr);
                break;
            default:
                throw new \InvalidArgumentException("Unknown sorting algorithm: $algorithm");
        }
        
        $endTime = microtime(true);
        $endMemory = memory_get_usage();
        
        return [
            'algorithm' => $algorithm,
            'time' => ($endTime - $startTime) * 1000, // 毫秒
            'memory' => $endMemory - $startMemory, // 字节
            'sorted' => self::isSorted($testArr)
        ];
    }
}