<?php

namespace DataStructures\Advanced;

/**
 * FenwickTree - 二叉索引树（树状数组）
 *
 * 思路：
 * 1. 使用数组存储，索引 i 管理区间 [i - lowbit(i) + 1, i] 的信息
 * 2. lowbit(i) = i & (-i)，取最低位的1
 * 3. 单点更新：沿 lowbit 向上传播
 * 4. 前缀查询：沿 lowbit 向零聚合
 *
 * 作用：
 * - 高效处理前缀和查询和单点更新
 * - 支持区间查询（通过两次前缀查询做差）
 * - 比线段树更轻量，常数更小
 *
 * 业务场景：
 * 1. 排行榜：实时更新分数，查询排名
 * 2. 金融系统：动态计算移动平均
 * 3. 数据流：实时统计词频
 * 4. 游戏开发：战斗力排行
 * 5. 电商平台：商品评分统计
 * 6. 监控系统：滑动窗口计数
 * 7. 数据库：统计信息维护
 * 8. 搜索引擎：倒排索引长度
 * 9. 压缩算法：频率表维护
 * 10. 算法竞赛：逆序对计数
 *
 * 时间复杂度：
 * - update: O(log n)
 * - query: O(log n)
 * - rangeQuery: O(log n)
 */
class FenwickTree
{
    private array $tree;
    private int $size;

    /**
     * @param int $n 数组大小
     */
    public function __construct(int $n)
    {
        $this->size = $n;
        $this->tree = array_fill(0, $n + 1, 0);
    }

    /**
     * 用初始数组构建 Fenwick 树
     *
     * @param array $arr
     * @return self
     */
    public static function fromArray(array $arr): self
    {
        $n = count($arr);
        $ft = new self($n);
        for ($i = 0; $i < $n; $i++) {
            $ft->add($i, $arr[$i]);
        }
        return $ft;
    }

    /**
     * 单点更新：在索引 idx 处增加 delta
     *
     * @param int $idx 0-based 索引
     * @param int|float $delta
     */
    public function add(int $idx, $delta): void
    {
        $i = $idx + 1; // 转为 1-based
        while ($i <= $this->size) {
            $this->tree[$i] += $delta;
            $i += $i & (-$i);
        }
    }

    /**
     * 单点更新：将索引 idx 处的值设为 val
     *
     * @param int $idx
     * @param int|float $val
     */
    public function set(int $idx, $val): void
    {
        $current = $this->query($idx) - ($idx > 0 ? $this->query($idx - 1) : 0);
        $this->add($idx, $val - $current);
    }

    /**
     * 查询前缀和 [0, idx]
     *
     * @param int $idx 0-based 索引
     * @return int|float
     */
    public function query(int $idx)
    {
        if ($idx < 0) {
            return 0;
        }
        $idx = min($idx, $this->size - 1);
        $sum = 0;
        $i = $idx + 1;
        while ($i > 0) {
            $sum += $this->tree[$i];
            $i -= $i & (-$i);
        }
        return $sum;
    }

    /**
     * 区间查询 [left, right]
     *
     * @param int $left
     * @param int $right
     * @return int|float
     */
    public function rangeQuery(int $left, int $right)
    {
        return $this->query($right) - $this->query($left - 1);
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

    /**
     * 查找使得前缀和 >= target 的最小索引（需要树中所有值非负）
     *
     * @param int|float $target
     * @return int|null 找不到返回 null
     */
    public function lowerBound($target): ?int
    {
        if ($target <= 0) {
            return 0;
        }

        $idx = 0;
        $bitMask = 1;
        while ($bitMask <= $this->size) {
            $bitMask <<= 1;
        }
        $bitMask >>= 1;

        while ($bitMask > 0) {
            $nextIdx = $idx + $bitMask;
            if ($nextIdx <= $this->size && $this->tree[$nextIdx] < $target) {
                $target -= $this->tree[$nextIdx];
                $idx = $nextIdx;
            }
            $bitMask >>= 1;
        }

        return $idx < $this->size ? $idx : null;
    }
}

/**
 * FenwickTreeRange - 支持区间更新的二叉索引树
 *
 * 使用两个 Fenwick 树实现区间加法 + 区间查询
 * 时间复杂度：所有操作 O(log n)
 */
class FenwickTreeRange
{
    private FenwickTree $bit1;
    private FenwickTree $bit2;
    private int $size;

    public function __construct(int $n)
    {
        $this->size = $n;
        $this->bit1 = new FenwickTree($n);
        $this->bit2 = new FenwickTree($n);
    }

    /**
     * 用初始数组构建
     */
    public static function fromArray(array $arr): self
    {
        $n = count($arr);
        $ft = new self($n);
        for ($i = 0; $i < $n; $i++) {
            $ft->rangeAdd($i, $i, $arr[$i]);
        }
        return $ft;
    }

    /**
     * 区间更新：在 [l, r] 每个元素上增加 delta
     */
    public function rangeAdd(int $l, int $r, $delta): void
    {
        $this->bit1->add($l, $delta);
        $this->bit1->add($r + 1, -$delta);
        $this->bit2->add($l, $delta * ($l - 1));
        $this->bit2->add($r + 1, -$delta * $r);
    }

    /**
     * 单点查询
     */
    public function pointQuery(int $idx)
    {
        return $this->rangeQuery($idx, $idx);
    }

    /**
     * 区间查询 [l, r]
     */
    public function rangeQuery(int $l, int $r)
    {
        return $this->prefixSum($r) - $this->prefixSum($l - 1);
    }

    private function prefixSum(int $idx)
    {
        if ($idx < 0) {
            return 0;
        }
        $idx = min($idx, $this->size - 1);
        return $this->bit1->query($idx) * $idx - $this->bit2->query($idx);
    }

    public function getSize(): int
    {
        return $this->size;
    }
}
