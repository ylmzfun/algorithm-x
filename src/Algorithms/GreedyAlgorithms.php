<?php

namespace DataStructures\Algorithms;

/**
 * 贪心算法集合
 * 包含经典的贪心算法问题解决方案
 */
class GreedyAlgorithms
{
    /**
     * 活动选择问题
     * 选择最多的不重叠活动
     * 时间复杂度: O(n log n), 空间复杂度: O(1)
     */
    public static function activitySelection(array $activities): array
    {
        if (empty($activities)) return [];
        
        // 按结束时间排序
        usort($activities, function($a, $b) {
            return $a['end'] <=> $b['end'];
        });
        
        $selected = [$activities[0]];
        $lastEndTime = $activities[0]['end'];
        
        for ($i = 1; $i < count($activities); $i++) {
            if ($activities[$i]['start'] >= $lastEndTime) {
                $selected[] = $activities[$i];
                $lastEndTime = $activities[$i]['end'];
            }
        }
        
        return $selected;
    }
    
    /**
     * 分数背包问题
     * 时间复杂度: O(n log n), 空间复杂度: O(1)
     */
    public static function fractionalKnapsack(array $items, float $capacity): float
    {
        if (empty($items) || $capacity <= 0) return 0;
        
        // 按价值密度排序（价值/重量）
        usort($items, function($a, $b) {
            $ratioA = $a['value'] / $a['weight'];
            $ratioB = $b['value'] / $b['weight'];
            return $ratioB <=> $ratioA; // 降序
        });
        
        $totalValue = 0;
        $remainingCapacity = $capacity;
        
        foreach ($items as $item) {
            if ($remainingCapacity >= $item['weight']) {
                // 完全装入
                $totalValue += $item['value'];
                $remainingCapacity -= $item['weight'];
            } else {
                // 部分装入
                $fraction = $remainingCapacity / $item['weight'];
                $totalValue += $item['value'] * $fraction;
                break;
            }
        }
        
        return $totalValue;
    }
    
    /**
     * 霍夫曼编码
     * 时间复杂度: O(n log n), 空间复杂度: O(n)
     */
    public static function huffmanCoding(array $frequencies): array
    {
        if (count($frequencies) < 2) {
            return array_keys($frequencies)[0] ?? '' ? [array_keys($frequencies)[0] => '0'] : [];
        }
        
        // 创建优先队列（最小堆）
        $heap = new \SplPriorityQueue();
        $heap->setExtractFlags(\SplPriorityQueue::EXTR_DATA);
        
        // 初始化叶子节点
        foreach ($frequencies as $char => $freq) {
            $heap->insert([
                'char' => $char,
                'freq' => $freq,
                'left' => null,
                'right' => null
            ], -$freq); // 负数实现最小堆
        }
        
        // 构建霍夫曼树
        while ($heap->count() > 1) {
            $left = $heap->extract();
            $right = $heap->extract();
            
            $merged = [
                'char' => null,
                'freq' => $left['freq'] + $right['freq'],
                'left' => $left,
                'right' => $right
            ];
            
            $heap->insert($merged, -$merged['freq']);
        }
        
        $root = $heap->extract();
        
        // 生成编码
        $codes = [];
        self::generateCodes($root, '', $codes);
        
        return $codes;
    }
    
    /**
     * 生成霍夫曼编码的辅助函数
     */
    private static function generateCodes($node, string $code, array &$codes): void
    {
        if ($node['char'] !== null) {
            // 叶子节点
            $codes[$node['char']] = $code === '' ? '0' : $code;
            return;
        }
        
        if ($node['left']) {
            self::generateCodes($node['left'], $code . '0', $codes);
        }
        if ($node['right']) {
            self::generateCodes($node['right'], $code . '1', $codes);
        }
    }
    
    /**
     * 区间调度最大化
     * 时间复杂度: O(n log n), 空间复杂度: O(1)
     */
    public static function intervalScheduling(array $intervals): array
    {
        if (empty($intervals)) return [];
        
        // 按结束时间排序
        usort($intervals, function($a, $b) {
            return $a[1] <=> $b[1];
        });
        
        $selected = [$intervals[0]];
        $lastEnd = $intervals[0][1];
        
        for ($i = 1; $i < count($intervals); $i++) {
            if ($intervals[$i][0] >= $lastEnd) {
                $selected[] = $intervals[$i];
                $lastEnd = $intervals[$i][1];
            }
        }
        
        return $selected;
    }
    
    /**
     * 最小生成树 - Prim算法
     * 时间复杂度: O(V²), 空间复杂度: O(V)
     */
    public static function primMST(array $graph): array
    {
        $vertices = count($graph);
        if ($vertices === 0) return [];
        
        $selected = array_fill(0, $vertices, false);
        $key = array_fill(0, $vertices, PHP_INT_MAX);
        $parent = array_fill(0, $vertices, -1);
        $mst = [];
        
        $key[0] = 0;
        
        for ($count = 0; $count < $vertices - 1; $count++) {
            $u = self::minKey($key, $selected);
            $selected[$u] = true;
            
            if ($parent[$u] !== -1) {
                $mst[] = [$parent[$u], $u, $graph[$parent[$u]][$u]];
            }
            
            for ($v = 0; $v < $vertices; $v++) {
                if ($graph[$u][$v] !== 0 && !$selected[$v] && $graph[$u][$v] < $key[$v]) {
                    $parent[$v] = $u;
                    $key[$v] = $graph[$u][$v];
                }
            }
        }
        
        return $mst;
    }
    
    /**
     * 找到最小键值的顶点
     */
    private static function minKey(array $key, array $selected): int
    {
        $min = PHP_INT_MAX;
        $minIndex = -1;
        
        for ($v = 0; $v < count($key); $v++) {
            if (!$selected[$v] && $key[$v] < $min) {
                $min = $key[$v];
                $minIndex = $v;
            }
        }
        
        return $minIndex;
    }
    
    /**
     * 加油站问题
     * 时间复杂度: O(n), 空间复杂度: O(1)
     */
    public static function gasStation(array $gas, array $cost): int
    {
        $totalGas = array_sum($gas);
        $totalCost = array_sum($cost);
        
        if ($totalGas < $totalCost) {
            return -1; // 无解
        }
        
        $currentGas = 0;
        $start = 0;
        
        for ($i = 0; $i < count($gas); $i++) {
            $currentGas += $gas[$i] - $cost[$i];
            
            if ($currentGas < 0) {
                $currentGas = 0;
                $start = $i + 1;
            }
        }
        
        return $start;
    }
    
    /**
     * 跳跃游戏
     * 时间复杂度: O(n), 空间复杂度: O(1)
     */
    public static function canJump(array $nums): bool
    {
        $maxReach = 0;
        
        for ($i = 0; $i < count($nums); $i++) {
            if ($i > $maxReach) {
                return false;
            }
            $maxReach = max($maxReach, $i + $nums[$i]);
        }
        
        return true;
    }
    
    /**
     * 跳跃游戏II - 最少跳跃次数
     * 时间复杂度: O(n), 空间复杂度: O(1)
     */
    public static function minJumps(array $nums): int
    {
        if (count($nums) <= 1) return 0;
        
        $jumps = 0;
        $currentEnd = 0;
        $farthest = 0;
        
        for ($i = 0; $i < count($nums) - 1; $i++) {
            $farthest = max($farthest, $i + $nums[$i]);
            
            if ($i === $currentEnd) {
                $jumps++;
                $currentEnd = $farthest;
            }
        }
        
        return $jumps;
    }
    
    /**
     * 买卖股票的最佳时机
     * 时间复杂度: O(n), 空间复杂度: O(1)
     */
    public static function maxProfit(array $prices): int
    {
        if (count($prices) < 2) return 0;
        
        $minPrice = $prices[0];
        $maxProfit = 0;
        
        for ($i = 1; $i < count($prices); $i++) {
            if ($prices[$i] < $minPrice) {
                $minPrice = $prices[$i];
            } else {
                $maxProfit = max($maxProfit, $prices[$i] - $minPrice);
            }
        }
        
        return $maxProfit;
    }
    
    /**
     * 买卖股票的最佳时机II（可多次交易）
     * 时间复杂度: O(n), 空间复杂度: O(1)
     */
    public static function maxProfitMultiple(array $prices): int
    {
        $profit = 0;
        
        for ($i = 1; $i < count($prices); $i++) {
            if ($prices[$i] > $prices[$i - 1]) {
                $profit += $prices[$i] - $prices[$i - 1];
            }
        }
        
        return $profit;
    }
    
    /**
     * 分发糖果
     * 时间复杂度: O(n), 空间复杂度: O(n)
     */
    public static function candy(array $ratings): int
    {
        $n = count($ratings);
        if ($n === 0) return 0;
        
        $candies = array_fill(0, $n, 1);
        
        // 从左到右
        for ($i = 1; $i < $n; $i++) {
            if ($ratings[$i] > $ratings[$i - 1]) {
                $candies[$i] = $candies[$i - 1] + 1;
            }
        }
        
        // 从右到左
        for ($i = $n - 2; $i >= 0; $i--) {
            if ($ratings[$i] > $ratings[$i + 1]) {
                $candies[$i] = max($candies[$i], $candies[$i + 1] + 1);
            }
        }
        
        return array_sum($candies);
    }
}