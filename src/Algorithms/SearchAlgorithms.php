<?php

namespace DataStructures\Algorithms;

/**
 * 搜索算法集合
 * 包含常见的搜索算法实现
 */
class SearchAlgorithms
{
    /**
     * 线性搜索
     * 时间复杂度: O(n)
     * 空间复杂度: O(1)
     */
    public static function linearSearch(array $arr, $target): int
    {
        for ($i = 0; $i < count($arr); $i++) {
            if ($arr[$i] === $target) {
                return $i;
            }
        }
        return -1;
    }
    
    /**
     * 二分搜索 (数组必须已排序)
     * 时间复杂度: O(log n)
     * 空间复杂度: O(1)
     */
    public static function binarySearch(array $arr, $target): int
    {
        $left = 0;
        $right = count($arr) - 1;
        
        while ($left <= $right) {
            $mid = intval(($left + $right) / 2);
            
            if ($arr[$mid] === $target) {
                return $mid;
            } elseif ($arr[$mid] < $target) {
                $left = $mid + 1;
            } else {
                $right = $mid - 1;
            }
        }
        
        return -1;
    }
    
    /**
     * 递归二分搜索
     * 时间复杂度: O(log n)
     * 空间复杂度: O(log n)
     */
    public static function binarySearchRecursive(array $arr, $target, int $left = 0, int $right = null): int
    {
        if ($right === null) {
            $right = count($arr) - 1;
        }
        
        if ($left > $right) {
            return -1;
        }
        
        $mid = intval(($left + $right) / 2);
        
        if ($arr[$mid] === $target) {
            return $mid;
        } elseif ($arr[$mid] < $target) {
            return self::binarySearchRecursive($arr, $target, $mid + 1, $right);
        } else {
            return self::binarySearchRecursive($arr, $target, $left, $mid - 1);
        }
    }
    
    /**
     * 插值搜索 (适用于均匀分布的已排序数组)
     * 时间复杂度: 平均 O(log log n), 最坏 O(n)
     * 空间复杂度: O(1)
     */
    public static function interpolationSearch(array $arr, $target): int
    {
        $left = 0;
        $right = count($arr) - 1;
        
        while ($left <= $right && $target >= $arr[$left] && $target <= $arr[$right]) {
            if ($left === $right) {
                return $arr[$left] === $target ? $left : -1;
            }
            
            // 插值公式
            $pos = $left + intval((($target - $arr[$left]) / ($arr[$right] - $arr[$left])) * ($right - $left));
            
            if ($arr[$pos] === $target) {
                return $pos;
            } elseif ($arr[$pos] < $target) {
                $left = $pos + 1;
            } else {
                $right = $pos - 1;
            }
        }
        
        return -1;
    }
    
    /**
     * 指数搜索
     * 时间复杂度: O(log n)
     * 空间复杂度: O(1)
     */
    public static function exponentialSearch(array $arr, $target): int
    {
        $n = count($arr);
        
        if ($arr[0] === $target) {
            return 0;
        }
        
        // 找到范围
        $i = 1;
        while ($i < $n && $arr[$i] <= $target) {
            $i *= 2;
        }
        
        // 在找到的范围内进行二分搜索
        $left = intval($i / 2);
        $right = min($i, $n - 1);
        
        return self::binarySearchRange($arr, $target, $left, $right);
    }
    
    /**
     * 在指定范围内进行二分搜索
     */
    private static function binarySearchRange(array $arr, $target, int $left, int $right): int
    {
        while ($left <= $right) {
            $mid = intval(($left + $right) / 2);
            
            if ($arr[$mid] === $target) {
                return $mid;
            } elseif ($arr[$mid] < $target) {
                $left = $mid + 1;
            } else {
                $right = $mid - 1;
            }
        }
        
        return -1;
    }
    
    /**
     * 跳跃搜索
     * 时间复杂度: O(√n)
     * 空间复杂度: O(1)
     */
    public static function jumpSearch(array $arr, $target): int
    {
        $n = count($arr);
        $step = intval(sqrt($n));
        $prev = 0;
        
        // 跳跃查找
        while ($arr[min($step, $n) - 1] < $target) {
            $prev = $step;
            $step += intval(sqrt($n));
            if ($prev >= $n) {
                return -1;
            }
        }
        
        // 线性搜索
        while ($arr[$prev] < $target) {
            $prev++;
            if ($prev === min($step, $n)) {
                return -1;
            }
        }
        
        return $arr[$prev] === $target ? $prev : -1;
    }
    
    /**
     * 三元搜索
     * 时间复杂度: O(log₃ n)
     * 空间复杂度: O(1)
     */
    public static function ternarySearch(array $arr, $target): int
    {
        $left = 0;
        $right = count($arr) - 1;
        
        while ($left <= $right) {
            $mid1 = $left + intval(($right - $left) / 3);
            $mid2 = $right - intval(($right - $left) / 3);
            
            if ($arr[$mid1] === $target) {
                return $mid1;
            }
            if ($arr[$mid2] === $target) {
                return $mid2;
            }
            
            if ($target < $arr[$mid1]) {
                $right = $mid1 - 1;
            } elseif ($target > $arr[$mid2]) {
                $left = $mid2 + 1;
            } else {
                $left = $mid1 + 1;
                $right = $mid2 - 1;
            }
        }
        
        return -1;
    }
    
    /**
     * 斐波那契搜索
     * 时间复杂度: O(log n)
     * 空间复杂度: O(1)
     */
    public static function fibonacciSearch(array $arr, $target): int
    {
        $n = count($arr);
        
        // 初始化斐波那契数
        $fibM2 = 0; // (m-2)th Fibonacci number
        $fibM1 = 1; // (m-1)th Fibonacci number
        $fibM = $fibM2 + $fibM1; // mth Fibonacci number
        
        // 找到最小的斐波那契数大于等于n
        while ($fibM < $n) {
            $fibM2 = $fibM1;
            $fibM1 = $fibM;
            $fibM = $fibM2 + $fibM1;
        }
        
        $offset = -1;
        
        while ($fibM > 1) {
            $i = min($offset + $fibM2, $n - 1);
            
            if ($arr[$i] < $target) {
                $fibM = $fibM1;
                $fibM1 = $fibM2;
                $fibM2 = $fibM - $fibM1;
                $offset = $i;
            } elseif ($arr[$i] > $target) {
                $fibM = $fibM2;
                $fibM1 = $fibM1 - $fibM2;
                $fibM2 = $fibM - $fibM1;
            } else {
                return $i;
            }
        }
        
        if ($fibM1 && $offset + 1 < $n && $arr[$offset + 1] === $target) {
            return $offset + 1;
        }
        
        return -1;
    }
    
    /**
     * 查找第一个出现的位置
     * 时间复杂度: O(log n)
     * 空间复杂度: O(1)
     */
    public static function findFirst(array $arr, $target): int
    {
        $left = 0;
        $right = count($arr) - 1;
        $result = -1;
        
        while ($left <= $right) {
            $mid = intval(($left + $right) / 2);
            
            if ($arr[$mid] === $target) {
                $result = $mid;
                $right = $mid - 1; // 继续在左半部分查找
            } elseif ($arr[$mid] < $target) {
                $left = $mid + 1;
            } else {
                $right = $mid - 1;
            }
        }
        
        return $result;
    }
    
    /**
     * 查找最后一个出现的位置
     * 时间复杂度: O(log n)
     * 空间复杂度: O(1)
     */
    public static function findLast(array $arr, $target): int
    {
        $left = 0;
        $right = count($arr) - 1;
        $result = -1;
        
        while ($left <= $right) {
            $mid = intval(($left + $right) / 2);
            
            if ($arr[$mid] === $target) {
                $result = $mid;
                $left = $mid + 1; // 继续在右半部分查找
            } elseif ($arr[$mid] < $target) {
                $left = $mid + 1;
            } else {
                $right = $mid - 1;
            }
        }
        
        return $result;
    }
    
    /**
     * 查找所有出现的位置
     * 时间复杂度: O(log n + k) k为出现次数
     * 空间复杂度: O(k)
     */
    public static function findAll(array $arr, $target): array
    {
        $first = self::findFirst($arr, $target);
        if ($first === -1) {
            return [];
        }
        
        $last = self::findLast($arr, $target);
        $result = [];
        
        for ($i = $first; $i <= $last; $i++) {
            $result[] = $i;
        }
        
        return $result;
    }
    
    /**
     * 查找峰值元素
     * 时间复杂度: O(log n)
     * 空间复杂度: O(1)
     */
    public static function findPeak(array $arr): int
    {
        $n = count($arr);
        
        if ($n === 1) return 0;
        if ($arr[0] >= $arr[1]) return 0;
        if ($arr[$n - 1] >= $arr[$n - 2]) return $n - 1;
        
        $left = 1;
        $right = $n - 2;
        
        while ($left <= $right) {
            $mid = intval(($left + $right) / 2);
            
            if ($arr[$mid] >= $arr[$mid - 1] && $arr[$mid] >= $arr[$mid + 1]) {
                return $mid;
            } elseif ($arr[$mid] < $arr[$mid + 1]) {
                $left = $mid + 1;
            } else {
                $right = $mid - 1;
            }
        }
        
        return -1;
    }
    
    /**
     * 在旋转排序数组中搜索
     * 时间复杂度: O(log n)
     * 空间复杂度: O(1)
     */
    public static function searchInRotatedArray(array $arr, $target): int
    {
        $left = 0;
        $right = count($arr) - 1;
        
        while ($left <= $right) {
            $mid = intval(($left + $right) / 2);
            
            if ($arr[$mid] === $target) {
                return $mid;
            }
            
            // 判断哪一半是有序的
            if ($arr[$left] <= $arr[$mid]) {
                // 左半部分有序
                if ($target >= $arr[$left] && $target < $arr[$mid]) {
                    $right = $mid - 1;
                } else {
                    $left = $mid + 1;
                }
            } else {
                // 右半部分有序
                if ($target > $arr[$mid] && $target <= $arr[$right]) {
                    $left = $mid + 1;
                } else {
                    $right = $mid - 1;
                }
            }
        }
        
        return -1;
    }
    
    /**
     * 查找旋转点
     * 时间复杂度: O(log n)
     * 空间复杂度: O(1)
     */
    public static function findRotationPoint(array $arr): int
    {
        $left = 0;
        $right = count($arr) - 1;
        
        while ($left < $right) {
            $mid = intval(($left + $right) / 2);
            
            if ($arr[$mid] > $arr[$right]) {
                $left = $mid + 1;
            } else {
                $right = $mid;
            }
        }
        
        return $left;
    }
    
    /**
     * 查找缺失的数字
     * 时间复杂度: O(log n)
     * 空间复杂度: O(1)
     */
    public static function findMissingNumber(array $arr): int
    {
        $left = 0;
        $right = count($arr) - 1;
        
        while ($left <= $right) {
            $mid = intval(($left + $right) / 2);
            
            // 如果arr[mid] = mid，则缺失的数字在右半部分
            if ($arr[$mid] === $mid) {
                $left = $mid + 1;
            } else {
                $right = $mid - 1;
            }
        }
        
        return $left;
    }
    
    /**
     * 搜索性能基准测试
     */
    public static function benchmarkSearch(array $arr, $target, string $algorithm = 'binarySearch'): array
    {
        $startTime = microtime(true);
        $startMemory = memory_get_usage();
        
        switch ($algorithm) {
            case 'linearSearch':
                $result = self::linearSearch($arr, $target);
                break;
            case 'binarySearch':
                $result = self::binarySearch($arr, $target);
                break;
            case 'interpolationSearch':
                $result = self::interpolationSearch($arr, $target);
                break;
            case 'exponentialSearch':
                $result = self::exponentialSearch($arr, $target);
                break;
            case 'jumpSearch':
                $result = self::jumpSearch($arr, $target);
                break;
            case 'ternarySearch':
                $result = self::ternarySearch($arr, $target);
                break;
            case 'fibonacciSearch':
                $result = self::fibonacciSearch($arr, $target);
                break;
            default:
                throw new \InvalidArgumentException("Unknown search algorithm: $algorithm");
        }
        
        $endTime = microtime(true);
        $endMemory = memory_get_usage();
        
        return [
            'algorithm' => $algorithm,
            'result' => $result,
            'found' => $result !== -1,
            'time' => ($endTime - $startTime) * 1000, // 毫秒
            'memory' => $endMemory - $startMemory // 字节
        ];
    }
}