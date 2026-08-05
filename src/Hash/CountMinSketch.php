<?php

namespace DataStructures\Hash;

/**
 * CountMinSketch - 计数最小草图
 *
 * 思路：
 * 1. 使用 d 行 w 列的二维计数器数组
 * 2. 每行有独立的哈希函数，将元素映射到 [0, w-1]
 * 3. 插入时对所有行对应的计数器+1
 * 4. 查询频率时取所有行对应的计数器最小值
 * 5. 只会高估不会低估，误差可控
 *
 * 作用：
 * - 用亚线性空间统计海量数据流中的元素频率
 * - 空间效率极高，适合流式处理
 *
 * 业务场景：
 * 1. 搜索引擎：热门查询词统计
 * 2. 推荐系统：物品点击频率
 * 3. 网络监控：流量统计、DDoS检测
 * 4. 日志分析：错误频率
 * 5. 广告系统：展示/点击计数
 * 6. 社交网络：热门话题追踪
 * 7. IoT：传感器数据频率
 * 8. CDN：热门资源统计
 * 9. 数据库：查询优化器统计信息
 * 10. 流式计算：近似Top-K
 *
 * 时间复杂度：O(d) 每次操作
 * 空间复杂度：O(d × w)
 * 误差范围：频率 ≤ 估计值 ≤ 频率 + ε × N（N为总计数，ε = e/w）
 * 置信度：1 - δ（δ = 1/2^d）
 */
class CountMinSketch
{
    private array $table;
    private int $depth;     // d: 行数
    private int $width;     // w: 列数
    private int $totalCount;
    private array $seeds;

    /**
     * @param float $epsilon 误差率 (如 0.01 表示 1% 误差)
     * @param float $delta 失败概率 (如 0.01 表示 99% 置信度)
     */
    public function __construct(float $epsilon = 0.01, float $delta = 0.01)
    {
        $this->width = (int)ceil(M_E / $epsilon);
        $this->depth = (int)ceil(log(1 / $delta));
        $this->width = max(16, $this->width);
        $this->depth = max(2, $this->depth);
        $this->totalCount = 0;

        // 初始化计数器数组
        $this->table = [];
        for ($i = 0; $i < $this->depth; $i++) {
            $this->table[$i] = array_fill(0, $this->width, 0);
        }

        // 生成随机种子
        $this->seeds = [];
        for ($i = 0; $i < $this->depth; $i++) {
            $this->seeds[$i] = random_int(1, PHP_INT_MAX);
        }
    }

    /**
     * 增加计数
     *
     * @param string|int $item
     * @param int $count 增量
     */
    public function add($item, int $count = 1): void
    {
        $this->totalCount += $count;
        $hash = $this->hashItem($item);

        for ($i = 0; $i < $this->depth; $i++) {
            $col = $this->hashToColumn($hash, $this->seeds[$i]);
            $this->table[$i][$col] += $count;
        }
    }

    /**
     * 查询估计频率
     *
     * @param string|int $item
     * @return int
     */
    public function estimate($item): int
    {
        $hash = $this->hashItem($item);
        $min = PHP_INT_MAX;

        for ($i = 0; $i < $this->depth; $i++) {
            $col = $this->hashToColumn($hash, $this->seeds[$i]);
            $min = min($min, $this->table[$i][$col]);
        }

        return $min;
    }

    /**
     * 获取总计数
     */
    public function getTotalCount(): int
    {
        return $this->totalCount;
    }

    /**
     * 重置所有计数器
     */
    public function reset(): void
    {
        for ($i = 0; $i < $this->depth; $i++) {
            $this->table[$i] = array_fill(0, $this->width, 0);
        }
        $this->totalCount = 0;
    }

    /**
     * 合并另一个 CountMinSketch
     */
    public function merge(CountMinSketch $other): void
    {
        if ($this->depth !== $other->depth || $this->width !== $other->width) {
            throw new \InvalidArgumentException('Cannot merge sketches with different dimensions');
        }

        for ($i = 0; $i < $this->depth; $i++) {
            for ($j = 0; $j < $this->width; $j++) {
                $this->table[$i][$j] += $other->table[$i][$j];
            }
        }

        $this->totalCount += $other->totalCount;
    }

    /**
     * 获取内部状态（用于序列化）
     */
    public function getState(): array
    {
        return [
            'depth' => $this->depth,
            'width' => $this->width,
            'totalCount' => $this->totalCount,
            'table' => $this->table,
            'seeds' => $this->seeds,
        ];
    }

    /**
     * 从状态恢复
     */
    public static function fromState(array $state): self
    {
        $sketch = new self();
        $sketch->depth = $state['depth'];
        $sketch->width = $state['width'];
        $sketch->totalCount = $state['totalCount'];
        $sketch->table = $state['table'];
        $sketch->seeds = $state['seeds'];
        return $sketch;
    }

    private function hashItem($item): int
    {
        if (is_int($item)) {
            return $item;
        }
        if (is_string($item)) {
            $h = 0;
            $len = strlen($item);
            for ($i = 0; $i < $len; $i++) {
                $h = ($h * 31 + ord($item[$i])) & 0x7FFFFFFF;
            }
            return $h;
        }
        return crc32(serialize($item)) & 0x7FFFFFFF;
    }

    private function hashToColumn(int $hash, int $seed): int
    {
        // 使用乘法哈希
        return (int)((($hash ^ $seed) * 2654435761) % $this->width);
    }
}
