<?php

namespace DataStructures\Utils;

use DataStructures\Exceptions\DataStructureException;

/**
 * 数据结构工具类
 * 提供常用的辅助函数和实用工具
 */
class Utils
{
    /**
     * 交换数组中两个元素的位置
     */
    public static function swap(array &$array, int $i, int $j): void
    {
        if ($i === $j) {
            return;
        }
        
        $temp = $array[$i];
        $array[$i] = $array[$j];
        $array[$j] = $temp;
    }
    
    /**
     * 检查数组是否已排序
     */
    public static function isSorted(array $array, bool $ascending = true): bool
    {
        $count = count($array);
        if ($count <= 1) {
            return true;
        }
        
        for ($i = 1; $i < $count; $i++) {
            if ($ascending) {
                if ($array[$i] < $array[$i - 1]) {
                    return false;
                }
            } else {
                if ($array[$i] > $array[$i - 1]) {
                    return false;
                }
            }
        }
        
        return true;
    }
    
    /**
     * 生成随机数组
     */
    public static function generateRandomArray(int $size, int $min = 0, int $max = 100): array
    {
        $array = [];
        for ($i = 0; $i < $size; $i++) {
            $array[] = $min + ($i * 7 + 13) % ($max - $min + 1);
        }
        return $array;
    }
    
    /**
     * 生成有序数组
     */
    public static function generateSortedArray(int $size, int $start = 0, int $step = 1): array
    {
        $array = [];
        for ($i = 0; $i < $size; $i++) {
            $array[] = $start + ($i * $step);
        }
        return $array;
    }
    
    /**
     * 生成逆序数组
     */
    public static function generateReverseSortedArray(int $size, int $start = 100, int $step = 1): array
    {
        $array = [];
        for ($i = 0; $i < $size; $i++) {
            $array[] = $start - ($i * $step);
        }
        return $array;
    }
    
    /**
     * 深度克隆数组
     */
    public static function deepCloneArray(array $array): array
    {
        return unserialize(serialize($array));
    }
    
    /**
     * 比较两个值
     * 返回值: < 0 如果 $a < $b, 0 如果 $a == $b, > 0 如果 $a > $b
     */
    public static function compare($a, $b): int
    {
        if ($a < $b) {
            return -1;
        } elseif ($a > $b) {
            return 1;
        } else {
            return 0;
        }
    }
    
    /**
     * 字符串哈希函数 (djb2算法)
     */
    public static function hashString(string $str): int
    {
        $hash = 5381;
        $len = strlen($str);
        
        for ($i = 0; $i < $len; $i++) {
            $hash = (($hash << 5) + $hash) + ord($str[$i]);
        }
        
        return abs($hash);
    }
    
    /**
     * 简单哈希函数
     */
    public static function simpleHash($key, int $size): int
    {
        if (is_string($key)) {
            return self::hashString($key) % $size;
        } elseif (is_numeric($key)) {
            return abs((int)$key) % $size;
        } else {
            return abs(crc32(serialize($key))) % $size;
        }
    }
    
    /**
     * 验证索引是否有效
     */
    public static function validateIndex(int $index, int $size): void
    {
        if ($index < 0 || $index >= $size) {
            throw new DataStructureException("Index $index is out of bounds for size $size");
        }
    }
    
    /**
     * 验证范围是否有效
     */
    public static function validateRange(int $start, int $end, int $size): void
    {
        if ($start < 0 || $end >= $size || $start > $end) {
            throw new DataStructureException("Invalid range [$start, $end] for size $size");
        }
    }
    
    /**
     * 计算数组的统计信息
     */
    public static function getArrayStats(array $array): array
    {
        if (empty($array)) {
            return [
                'count' => 0,
                'min' => null,
                'max' => null,
                'sum' => 0,
                'average' => 0,
                'median' => null
            ];
        }
        
        $count = count($array);
        $min = min($array);
        $max = max($array);
        $sum = array_sum($array);
        $average = $sum / $count;
        
        // 计算中位数
        $sorted = $array;
        sort($sorted);
        $middle = intval($count / 2);
        
        if ($count % 2 === 0) {
            $median = ($sorted[$middle - 1] + $sorted[$middle]) / 2;
        } else {
            $median = $sorted[$middle];
        }
        
        return [
            'count' => $count,
            'min' => $min,
            'max' => $max,
            'sum' => $sum,
            'average' => $average,
            'median' => $median
        ];
    }
    
    /**
     * 格式化字节大小
     */
    public static function formatBytes(int $bytes, int $precision = 2): string
    {
        $units = ['B', 'KB', 'MB', 'GB', 'TB'];
        
        for ($i = 0; $bytes > 1024 && $i < count($units) - 1; $i++) {
            $bytes /= 1024;
        }
        
        return round($bytes, $precision) . ' ' . $units[$i];
    }
    
    /**
     * 格式化执行时间
     */
    public static function formatTime(float $seconds): string
    {
        if ($seconds < 0.001) {
            return round($seconds * 1000000, 2) . ' μs';
        } elseif ($seconds < 1) {
            return round($seconds * 1000, 2) . ' ms';
        } else {
            return round($seconds, 3) . ' s';
        }
    }
    
    /**
     * 测量函数执行时间
     */
    public static function measureTime(callable $function, ...$args): array
    {
        $startTime = microtime(true);
        $startMemory = memory_get_usage();
        
        $result = call_user_func_array($function, $args);
        
        $endTime = microtime(true);
        $endMemory = memory_get_usage();
        
        return [
            'result' => $result,
            'time' => $endTime - $startTime,
            'memory' => $endMemory - $startMemory,
            'formatted_time' => self::formatTime($endTime - $startTime),
            'formatted_memory' => self::formatBytes($endMemory - $startMemory)
        ];
    }
    
    /**
     * 生成唯一ID
     */
    public static function generateId(): string
    {
        return uniqid('ds_', true);
    }
    
    /**
     * 检查是否为质数
     */
    public static function isPrime(int $n): bool
    {
        if ($n < 2) {
            return false;
        }
        
        if ($n === 2) {
            return true;
        }
        
        if ($n % 2 === 0) {
            return false;
        }
        
        $sqrt = (int)sqrt($n);
        for ($i = 3; $i <= $sqrt; $i += 2) {
            if ($n % $i === 0) {
                return false;
            }
        }
        
        return true;
    }
    
    /**
     * 获取下一个质数
     */
    public static function getNextPrime(int $n): int
    {
        $candidate = $n + 1;
        while (!self::isPrime($candidate)) {
            $candidate++;
        }
        return $candidate;
    }
    
    /**
     * 计算最大公约数
     */
    public static function gcd(int $a, int $b): int
    {
        while ($b !== 0) {
            $temp = $b;
            $b = $a % $b;
            $a = $temp;
        }
        return abs($a);
    }
    
    /**
     * 计算最小公倍数
     */
    public static function lcm(int $a, int $b): int
    {
        return abs($a * $b) / self::gcd($a, $b);
    }
    
    /**
     * 二进制搜索插入位置
     */
    public static function binarySearchInsertPosition(array $array, $target): int
    {
        $left = 0;
        $right = count($array);
        
        while ($left < $right) {
            $mid = intval(($left + $right) / 2);
            
            if ($array[$mid] < $target) {
                $left = $mid + 1;
            } else {
                $right = $mid;
            }
        }
        
        return $left;
    }
    
    /**
     * 打印数组（用于调试）
     */
    public static function printArray(array $array, string $title = "Array"): void
    {
        echo "$title: [" . implode(", ", $array) . "]\n";
    }
    
    /**
     * 打印矩阵（用于调试）
     */
    public static function printMatrix(array $matrix, string $title = "Matrix"): void
    {
        echo "$title:\n";
        foreach ($matrix as $row) {
            echo "[" . implode(", ", $row) . "]\n";
        }
    }
    
    /**
     * 验证回调函数
     */
    public static function validateCallback($callback): void
    {
        if (!is_callable($callback)) {
            throw new DataStructureException("Invalid callback function");
        }
    }
    
    /**
     * 安全的数组访问
     */
    public static function safeArrayGet(array $array, $key, $default = null)
    {
        return array_key_exists($key, $array) ? $array[$key] : $default;
    }
    
    /**
     * 数组去重（保持顺序）
     */
    public static function arrayUniqueOrdered(array $array): array
    {
        $seen = [];
        $result = [];
        
        foreach ($array as $item) {
            $key = serialize($item);
            if (!isset($seen[$key])) {
                $seen[$key] = true;
                $result[] = $item;
            }
        }
        
        return $result;
    }
    
    /**
     * 检查数组是否包含重复元素
     */
    public static function hasDuplicates(array $array): bool
    {
        return count($array) !== count(array_unique($array));
    }
    
    /**
     * 获取数组中的重复元素
     */
    public static function getDuplicates(array $array): array
    {
        $counts = array_count_values($array);
        $duplicates = [];
        
        foreach ($counts as $value => $count) {
            if ($count > 1) {
                $duplicates[] = $value;
            }
        }
        
        return $duplicates;
    }
    
    /**
     * 数组分块
     */
    public static function arrayChunk(array $array, int $size): array
    {
        if ($size <= 0) {
            throw new DataStructureException("Chunk size must be positive");
        }
        
        return array_chunk($array, $size);
    }
    
    /**
     * 数组扁平化
     */
    public static function arrayFlatten(array $array): array
    {
        $result = [];
        
        foreach ($array as $item) {
            if (is_array($item)) {
                $result = array_merge($result, self::arrayFlatten($item));
            } else {
                $result[] = $item;
            }
        }
        
        return $result;
    }
    
    /**
     * 计算数组的笛卡尔积
     */
    public static function cartesianProduct(array ...$arrays): array
    {
        if (empty($arrays)) {
            return [[]];
        }
        
        $result = [[]];
        
        foreach ($arrays as $array) {
            $temp = [];
            foreach ($result as $resultItem) {
                foreach ($array as $item) {
                    $temp[] = array_merge($resultItem, [$item]);
                }
            }
            $result = $temp;
        }
        
        return $result;
    }
}