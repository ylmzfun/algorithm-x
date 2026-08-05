<?php

namespace DataStructures\Tree;

/**
 * BPlusTree - B+树
 *
 * 思路：
 * 1. 所有数据仅存储在叶子节点
 * 2. 内部节点仅存储索引键，用于路由
 * 3. 叶子节点通过链表连接，支持高效范围查询
 * 4. 分裂/合并机制与B树类似
 *
 * 作用：
 * - 数据库索引的核心数据结构
 * - 高效范围查询和顺序扫描
 *
 * 业务场景：
 * 1. MySQL InnoDB：聚簇索引
 * 2. 文件系统：ext4目录项
 * 3. 键值存储：LSM-Tree的SSTable索引
 * 4. 时间序列数据库：范围查询
 * 5. 全文搜索引擎：倒排索引
 *
 * 时间复杂度：所有操作 O(log n)
 */
class BPlusTree
{
    private int $order;         // 阶数（最大子节点数）
    private ?BPNode $root = null;
    private ?BPNode $leafHead = null;
    private int $size = 0;

    public function __construct(int $order = 4)
    {
        $this->order = max(3, $order);
    }

    /**
     * 插入键值
     */
    public function insert($key, $value): void
    {
        if ($this->root === null) {
            $this->root = new BPLeafNode();
            $this->leafHead = $this->root;
        }

        $result = $this->insertRecursive($this->root, $key, $value);

        if ($result !== null) {
            // 根分裂
            $newRoot = new BPInternalNode();
            $newRoot->keys[0] = $result[0];
            $newRoot->children[0] = $result[1];
            $newRoot->children[1] = $result[2];
            $newRoot->num = 1;
            $this->root = $newRoot;
        }

        $this->size++;
    }

    /**
     * @return null|array [promotedKey, leftNode, rightNode]
     */
    private function insertRecursive($node, $key, $value)
    {
        if ($node instanceof BPLeafNode) {
            return $node->insert($key, $value, $this->order);
        }

        // 内部节点：找到子节点
        $childIdx = $node->findChild($key);
        $result = $this->insertRecursive($node->children[$childIdx], $key, $value);

        if ($result === null) {
            return null;
        }

        return $node->insertKey($result[0], $result[1], $result[2], $this->order);
    }

    /**
     * 搜索键
     */
    public function search($key)
    {
        $leaf = $this->findLeaf($key);
        if ($leaf === null) {
            return null;
        }
        return $leaf->get($key);
    }

    private function findLeaf($key): ?BPLeafNode
    {
        if ($this->root === null) {
            return null;
        }

        $node = $this->root;
        while ($node instanceof BPInternalNode) {
            $node = $node->children[$node->findChild($key)];
        }
        return $node;
    }

    /**
     * 范围查询 [low, high]
     */
    public function rangeSearch($low, $high): array
    {
        $result = [];
        $leaf = $this->findLeaf($low);

        while ($leaf !== null) {
            for ($i = 0; $i < $leaf->num; $i++) {
                $k = $leaf->keys[$i];
                if (($k <=> $low) >= 0 && ($k <=> $high) <= 0) {
                    $result[] = ['key' => $k, 'value' => $leaf->values[$i]];
                }
                if (($k <=> $high) > 0) {
                    return $result;
                }
            }
            $leaf = $leaf->next;
        }

        return $result;
    }

    /**
     * 顺序遍历
     */
    public function scan(): array
    {
        $result = [];
        $leaf = $this->leafHead;
        while ($leaf !== null) {
            for ($i = 0; $i < $leaf->num; $i++) {
                $result[] = ['key' => $leaf->keys[$i], 'value' => $leaf->values[$i]];
            }
            $leaf = $leaf->next;
        }
        return $result;
    }

    public function getSize(): int { return $this->size; }
    public function isEmpty(): bool { return $this->size === 0; }
}

/**
 * B+树节点基类
 */
abstract class BPNode
{
    public array $keys = [];
    public int $num = 0;
}

/**
 * B+树叶子节点
 */
class BPLeafNode extends BPNode
{
    public array $values = [];
    public ?BPLeafNode $next = null;

    /**
     * 插入并返回分裂信息 [promotedKey, leftNode, rightNode] 或 null
     */
    public function insert($key, $value, int $order): ?array
    {
        // 找到插入位置
        $pos = 0;
        while ($pos < $this->num && ($key <=> $this->keys[$pos]) > 0) {
            $pos++;
        }

        // 已存在 → 更新
        if ($pos < $this->num && ($key <=> $this->keys[$pos]) === 0) {
            $this->values[$pos] = $value;
            return null;
        }

        // 插入
        array_splice($this->keys, $pos, 0, [$key]);
        array_splice($this->values, $pos, 0, [$value]);
        $this->num++;

        // 不需要分裂
        if ($this->num <= $order) {
            return null;
        }

        // 分裂
        $splitPoint = (int)ceil($order / 2);
        $newLeaf = new BPLeafNode();

        // 移动后半部分
        $newLeaf->keys = array_splice($this->keys, $splitPoint);
        $newLeaf->values = array_splice($this->values, $splitPoint);
        $newLeaf->num = count($newLeaf->keys);
        $this->num = count($this->keys);

        // 维护链表
        $newLeaf->next = $this->next;
        $this->next = $newLeaf;

        return [$newLeaf->keys[0], $this, $newLeaf];
    }

    public function get($key)
    {
        for ($i = 0; $i < $this->num; $i++) {
            if (($key <=> $this->keys[$i]) === 0) {
                return $this->values[$i];
            }
        }
        return null;
    }
}

/**
 * B+树内部节点
 */
class BPInternalNode extends BPNode
{
    public array $children = [];

    /**
     * 找到 key 应该去的子节点索引
     */
    public function findChild($key): int
    {
        $i = 0;
        while ($i < $this->num && ($key <=> $this->keys[$i]) >= 0) {
            $i++;
        }
        return $i;
    }

    /**
     * 插入分裂后的新键和子节点
     */
    public function insertKey($promotedKey, $leftChild, $rightChild, int $order): ?array
    {
        // 找到旧子节点的位置并替换
        $pos = 0;
        while ($pos <= $this->num && $this->children[$pos] !== $leftChild) {
            $pos++;
        }

        // 在 pos 处插入 promotedKey，子节点 [pos]=left, [pos+1]=right
        array_splice($this->keys, $pos, 0, [$promotedKey]);
        $this->children[$pos] = $leftChild;
        array_splice($this->children, $pos + 1, 0, [$rightChild]);
        $this->num++;

        if ($this->num < $order) {
            return null;
        }

        // 分裂
        $splitPoint = (int)($order / 2);
        $promoted = $this->keys[$splitPoint];

        $newNode = new BPInternalNode();
        $newNode->keys = array_splice($this->keys, $splitPoint + 1);
        $newNode->children = array_splice($this->children, $splitPoint + 1);
        $newNode->num = count($newNode->keys);

        // 移除上提的键
        array_pop($this->keys);
        $this->num = count($this->keys);

        return [$promoted, $this, $newNode];
    }
}
