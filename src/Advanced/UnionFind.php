<?php

namespace DataStructures\Advanced;

/**
 * UnionFind - 并查集（Disjoint Set Union）
 *
 * 思路：
 * 1. 每个元素初始指向自己（自成一个集合）
 * 2. find操作：查找元素所属集合的代表元素，同时进行路径压缩
 * 3. union操作：合并两个集合，按秩合并优化
 * 4. 路径压缩 + 按秩合并使均摊复杂度接近 O(α(n))
 *
 * 作用：
 * - 高效管理不相交集合的合并与查询
 * - 判断元素是否属于同一集合
 * - 统计连通分量数量
 *
 * 业务场景：
 * 1. 社交网络：判断用户是否在同一圈子
 * 2. 图连通性：动态判断节点连通性
 * 3. 最小生成树：Kruskal算法的核心
 * 4. 岛屿问题：计算连通区域数量
 * 5. 网络拓扑：检测网络分段
 * 6. 文件系统：硬链接检测
 * 7. 编译器：类型等价性判断
 * 8. 游戏开发：联盟/阵营管理
 * 9. 物流系统：配送区域合并
 * 10. 数据库：表连接等价性
 *
 * 时间复杂度：
 * - find: O(α(n)) 均摊（近乎O(1)）
 * - union: O(α(n)) 均摊
 * - connected: O(α(n)) 均摊
 */
class UnionFind
{
    private array $parent;
    private array $rank;
    private int $count;

    /**
     * @param int $n 元素数量（0 到 n-1）
     */
    public function __construct(int $n)
    {
        $this->parent = range(0, $n - 1);
        $this->rank = array_fill(0, $n, 1);
        $this->count = $n;
    }

    /**
     * 查找元素所属集合的代表元素（带路径压缩）
     *
     * @param int $x
     * @return int
     */
    public function find(int $x): int
    {
        if ($this->parent[$x] !== $x) {
            $this->parent[$x] = $this->find($this->parent[$x]);
        }
        return $this->parent[$x];
    }

    /**
     * 合并两个元素所在的集合（按秩合并）
     *
     * @param int $x
     * @param int $y
     * @return bool 如果已经在同一集合返回 false，否则返回 true
     */
    public function union(int $x, int $y): bool
    {
        $rootX = $this->find($x);
        $rootY = $this->find($y);

        if ($rootX === $rootY) {
            return false;
        }

        // 按秩合并：将秩小的树合并到秩大的树下
        if ($this->rank[$rootX] < $this->rank[$rootY]) {
            $this->parent[$rootX] = $rootY;
        } elseif ($this->rank[$rootX] > $this->rank[$rootY]) {
            $this->parent[$rootY] = $rootX;
        } else {
            $this->parent[$rootY] = $rootX;
            $this->rank[$rootX]++;
        }

        $this->count--;
        return true;
    }

    /**
     * 判断两个元素是否在同一集合
     *
     * @param int $x
     * @param int $y
     * @return bool
     */
    public function connected(int $x, int $y): bool
    {
        return $this->find($x) === $this->find($y);
    }

    /**
     * 获取集合数量
     *
     * @return int
     */
    public function getCount(): int
    {
        return $this->count;
    }

    /**
     * 获取元素所在集合的大小
     *
     * @param int $x
     * @return int
     */
    public function getSize(int $x): int
    {
        $root = $this->find($x);
        $size = 0;
        foreach ($this->parent as $i => $p) {
            if ($this->find($i) === $root) {
                $size++;
            }
        }
        return $size;
    }

    /**
     * 获取所有集合（按代表元素分组）
     *
     * @return array
     */
    public function getSets(): array
    {
        $sets = [];
        $n = count($this->parent);
        for ($i = 0; $i < $n; $i++) {
            $root = $this->find($i);
            $sets[$root][] = $i;
        }
        return array_values($sets);
    }
}
