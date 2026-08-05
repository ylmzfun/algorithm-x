<?php

namespace DataStructures\Hash;

/**
 * CuckooHash - 布谷鸟哈希表
 *
 * 思路：
 * 1. 使用两个哈希表 T1 和 T2，各自有独立的哈希函数 h1 和 h2
 * 2. 插入时先尝试 T1[h1(key)]，若被占则踢出现有项到另一个表
 * 3. 被踢出的项再用它的另一个哈希函数尝试插入，类似布谷鸟占巢
 * 4. 若出现循环（踢出次数超限），触发 rehash
 *
 * 作用：
 * - 最坏 O(1) 查找（最多查2个位置）
 * - 高空间利用率（可达 50% 以上）
 * - 适合读多写少的场景
 *
 * 业务场景：
 * 1. 缓存系统：高性能只读缓存
 * 2. 路由器：快速转发表查找
 * 3. 编译器：符号表（确定性能）
 * 4. DNS解析：域名缓存
 * 5. 数据库：哈希索引
 * 6. 去重系统：URL去重
 * 7. 包分类：防火墙规则匹配
 * 8. 布隆过滤器替代：需要确定性结果
 * 9. 一致性哈希：分布式哈希表
 * 10. 内存数据库：键值存储引擎
 *
 * 时间复杂度：
 * - search: O(1) worst-case
 * - insert: O(1) amortized
 * - delete: O(1) worst-case
 */
class CuckooHash
{
    private array $table1;
    private array $table2;
    private int $capacity;
    private int $size;
    private int $maxKicks;

    // 每个槽位的占位标记
    private const EMPTY = "\0__CUCKOO_EMPTY__";

    /**
     * @param int $capacity 每个表的大小
     */
    public function __construct(int $capacity = 16)
    {
        $this->capacity = max(8, $capacity);
        $this->table1 = array_fill(0, $this->capacity, null);
        $this->table2 = array_fill(0, $this->capacity, null);
        $this->size = 0;
        $this->maxKicks = (int)ceil(6 * log($this->capacity));
    }

    /**
     * 哈希函数1
     */
    private function h1($key): int
    {
        if (is_string($key)) {
            $hash = 0;
            $len = strlen($key);
            for ($i = 0; $i < $len; $i++) {
                $hash = ($hash * 31 + ord($key[$i])) % $this->capacity;
            }
            return $hash;
        }
        if (is_int($key)) {
            return (int)(($key * 2654435761) % $this->capacity);
        }
        return crc32(serialize($key)) % $this->capacity;
    }

    /**
     * 哈希函数2
     */
    private function h2($key): int
    {
        if (is_string($key)) {
            $hash = 0;
            $len = strlen($key);
            for ($i = 0; $i < $len; $i++) {
                $hash = ($hash * 37 + ord($key[$i])) % $this->capacity;
            }
            return $hash;
        }
        if (is_int($key)) {
            return (int)(($key * 1566083941) % $this->capacity);
        }
        return (crc32(serialize($key)) + 1) % $this->capacity;
    }

    /**
     * 插入键值对
     */
    public function put($key, $value): void
    {
        // 键已存在 → 更新
        if ($this->contains($key)) {
            $this->update($key, $value);
            return;
        }

        // 负载因子过高 → 扩容
        if ($this->size >= $this->capacity) {
            $this->rehash($this->capacity * 2);
        }

        $entry = [$key, $value];

        for ($kicks = 0; $kicks < $this->maxKicks; $kicks++) {
            // 尝试 T1
            $pos1 = $this->h1($entry[0]);
            if ($this->table1[$pos1] === null) {
                $this->table1[$pos1] = $entry;
                $this->size++;
                return;
            }

            // 踢出 T1[pos1]
            [$this->table1[$pos1], $entry] = [$entry, $this->table1[$pos1]];

            // 尝试 T2
            $pos2 = $this->h2($entry[0]);
            if ($this->table2[$pos2] === null) {
                $this->table2[$pos2] = $entry;
                $this->size++;
                return;
            }

            // 踢出 T2[pos2]
            [$this->table2[$pos2], $entry] = [$entry, $this->table2[$pos2]];
        }

        // 循环 → rehash
        $this->rehash($this->capacity * 2);
        $this->put($entry[0], $entry[1]);
    }

    /**
     * 获取值
     */
    public function get($key)
    {
        $pos1 = $this->h1($key);
        if ($this->table1[$pos1] !== null && $this->equals($this->table1[$pos1][0], $key)) {
            return $this->table1[$pos1][1];
        }

        $pos2 = $this->h2($key);
        if ($this->table2[$pos2] !== null && $this->equals($this->table2[$pos2][0], $key)) {
            return $this->table2[$pos2][1];
        }

        return null;
    }

    /**
     * 判断键是否存在
     */
    public function contains($key): bool
    {
        $pos1 = $this->h1($key);
        if ($this->table1[$pos1] !== null && $this->equals($this->table1[$pos1][0], $key)) {
            return true;
        }

        $pos2 = $this->h2($key);
        if ($this->table2[$pos2] !== null && $this->equals($this->table2[$pos2][0], $key)) {
            return true;
        }

        return false;
    }

    /**
     * 删除键
     */
    public function remove($key): bool
    {
        $pos1 = $this->h1($key);
        if ($this->table1[$pos1] !== null && $this->equals($this->table1[$pos1][0], $key)) {
            $this->table1[$pos1] = null;
            $this->size--;
            return true;
        }

        $pos2 = $this->h2($key);
        if ($this->table2[$pos2] !== null && $this->equals($this->table2[$pos2][0], $key)) {
            $this->table2[$pos2] = null;
            $this->size--;
            return true;
        }

        return false;
    }

    /**
     * 更新已有键的值
     */
    private function update($key, $value): void
    {
        $pos1 = $this->h1($key);
        if ($this->table1[$pos1] !== null && $this->equals($this->table1[$pos1][0], $key)) {
            $this->table1[$pos1][1] = $value;
            return;
        }

        $pos2 = $this->h2($key);
        if ($this->table2[$pos2] !== null && $this->equals($this->table2[$pos2][0], $key)) {
            $this->table2[$pos2][1] = $value;
        }
    }

    /**
     * 重新哈希
     */
    private function rehash(int $newCapacity): void
    {
        $oldTable1 = $this->table1;
        $oldTable2 = $this->table2;

        $this->capacity = $newCapacity;
        $this->table1 = array_fill(0, $this->capacity, null);
        $this->table2 = array_fill(0, $this->capacity, null);
        $this->size = 0;
        $this->maxKicks = (int)ceil(6 * log($this->capacity));

        foreach ($oldTable1 as $entry) {
            if ($entry !== null) {
                $this->put($entry[0], $entry[1]);
            }
        }

        foreach ($oldTable2 as $entry) {
            if ($entry !== null) {
                $this->put($entry[0], $entry[1]);
            }
        }
    }

    private function equals($a, $b): bool
    {
        return $a === $b;
    }

    public function getSize(): int
    {
        return $this->size;
    }

    public function isEmpty(): bool
    {
        return $this->size === 0;
    }

    /**
     * 获取所有键值对
     */
    public function toArray(): array
    {
        $result = [];
        foreach ($this->table1 as $entry) {
            if ($entry !== null) {
                $result[$entry[0]] = $entry[1];
            }
        }
        foreach ($this->table2 as $entry) {
            if ($entry !== null) {
                $result[$entry[0]] = $entry[1];
            }
        }
        return $result;
    }
}
