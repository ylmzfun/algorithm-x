<?php

namespace DataStructures\Advanced;

/**
 * SegmentTree - 线段树
 *
 * 思路：
 * 1. 基于完全二叉树，叶子节点存储原始数组元素
 * 2. 每个内部节点存储其子节点区间的聚合信息
 * 3. 支持区间查询和区间更新
 * 4. 延迟标记（lazy propagation）优化区间更新
 *
 * 作用：
 * - 高效处理区间查询（和、最小值、最大值等）
 * - 支持区间更新操作
 * - 比 Fenwick 树更通用，支持任意可结合的聚合操作
 *
 * 业务场景：
 * 1. 数据库：范围统计查询优化
 * 2. 游戏开发：区域伤害计算
 * 3. 金融系统：区间最大回撤
 * 4. 监控系统：时间段内最大值/最小值
 * 5. 地理信息：矩形区域查询
 * 6. 推荐系统：时间段内热门
 * 7. 日志分析：区间聚合统计
 * 8. 股票交易：区间最高价/最低价
 * 9. 传感器数据：滑动窗口聚合
 * 10. 算法竞赛：RMQ问题
 *
 * 时间复杂度：
 * - build: O(n)
 * - query: O(log n)
 * - update: O(log n)
 * - rangeUpdate: O(log n)（带延迟标记）
 */
class SegmentTree
{
    private array $tree;
    private array $lazy;
    private int $size;
    private string $operation; // 'sum', 'min', 'max'
    private $identity;         // 单位元

    /**
     * @param array $arr 初始数组
     * @param string $operation 聚合操作：'sum', 'min', 'max'
     */
    public function __construct(array $arr, string $operation = 'sum')
    {
        $this->size = count($arr);
        $this->operation = $operation;
        $this->identity = $this->getIdentity();

        // 线段树最多需要 4n 个节点
        $capacity = 4 * $this->size;
        $this->tree = array_fill(0, $capacity, $this->identity);
        $this->lazy = array_fill(0, $capacity, 0);

        if ($this->size > 0) {
            $this->build($arr, 0, 0, $this->size - 1);
        }
    }

    private function getIdentity()
    {
        switch ($this->operation) {
            case 'min':
                return PHP_INT_MAX;
            case 'max':
                return PHP_INT_MIN;
            default:
                return 0;
        }
    }

    private function merge($left, $right)
    {
        switch ($this->operation) {
            case 'min':
                return min($left, $right);
            case 'max':
                return max($left, $right);
            default:
                return $left + $right;
        }
    }

    /**
     * 构建线段树
     */
    private function build(array &$arr, int $node, int $start, int $end): void
    {
        if ($start === $end) {
            $this->tree[$node] = $arr[$start];
            return;
        }

        $mid = intdiv($start + $end, 2);
        $leftChild = 2 * $node + 1;
        $rightChild = 2 * $node + 2;

        $this->build($arr, $leftChild, $start, $mid);
        $this->build($arr, $rightChild, $mid + 1, $end);

        $this->tree[$node] = $this->merge($this->tree[$leftChild], $this->tree[$rightChild]);
    }

    /**
     * 延迟标记下推
     */
    private function pushDown(int $node, int $start, int $end): void
    {
        if ($this->lazy[$node] == 0) {
            return;
        }

        $lazyVal = $this->lazy[$node];

        if ($this->operation === 'sum') {
            $this->tree[$node] += $lazyVal * ($end - $start + 1);
        } else {
            $this->tree[$node] += $lazyVal;
        }

        if ($start !== $end) {
            $leftChild = 2 * $node + 1;
            $rightChild = 2 * $node + 2;
            $this->lazy[$leftChild] += $lazyVal;
            $this->lazy[$rightChild] += $lazyVal;
        }

        $this->lazy[$node] = 0;
    }

    /**
     * 区间更新：在 [ql, qr] 上每个元素增加 delta
     *
     * @param int $ql 查询左边界
     * @param int $qr 查询右边界
     * @param int|float $delta
     */
    public function rangeAdd(int $ql, int $qr, $delta): void
    {
        $this->rangeAddUtil(0, 0, $this->size - 1, $ql, $qr, $delta);
    }

    private function rangeAddUtil(int $node, int $start, int $end, int $ql, int $qr, $delta): void
    {
        $this->pushDown($node, $start, $end);

        if ($start > $qr || $end < $ql) {
            return;
        }

        if ($start >= $ql && $end <= $qr) {
            $this->lazy[$node] += $delta;
            $this->pushDown($node, $start, $end);
            return;
        }

        $mid = intdiv($start + $end, 2);
        $leftChild = 2 * $node + 1;
        $rightChild = 2 * $node + 2;

        $this->rangeAddUtil($leftChild, $start, $mid, $ql, $qr, $delta);
        $this->rangeAddUtil($rightChild, $mid + 1, $end, $ql, $qr, $delta);

        $this->tree[$node] = $this->merge($this->tree[$leftChild], $this->tree[$rightChild]);
    }

    /**
     * 单点更新
     *
     * @param int $idx
     * @param int|float $val
     */
    public function set(int $idx, $val): void
    {
        $current = $this->query($idx, $idx);
        $this->rangeAdd($idx, $idx, $val - $current);
    }

    /**
     * 区间查询 [ql, qr]
     *
     * @param int $ql
     * @param int $qr
     * @return int|float
     */
    public function query(int $ql, int $qr)
    {
        if ($ql > $qr || $ql < 0 || $qr >= $this->size) {
            return $this->identity;
        }
        return $this->queryUtil(0, 0, $this->size - 1, $ql, $qr);
    }

    private function queryUtil(int $node, int $start, int $end, int $ql, int $qr)
    {
        $this->pushDown($node, $start, $end);

        if ($start > $qr || $end < $ql) {
            return $this->identity;
        }

        if ($start >= $ql && $end <= $qr) {
            return $this->tree[$node];
        }

        $mid = intdiv($start + $end, 2);
        $leftChild = 2 * $node + 1;
        $rightChild = 2 * $node + 2;

        $leftResult = $this->queryUtil($leftChild, $start, $mid, $ql, $qr);
        $rightResult = $this->queryUtil($rightChild, $mid + 1, $end, $ql, $qr);

        return $this->merge($leftResult, $rightResult);
    }

    /**
     * 获取数组大小
     *
     * @return int
     */
    public function getSize(): int
    {
        return $this->size;
    }
}
