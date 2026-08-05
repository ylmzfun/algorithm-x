<?php

namespace DataStructures\Tree;

/**
 * BTree - B树
 *
 * 思路：
 * 1. 多路平衡搜索树，每个节点可包含多个键
 * 2. 节点分裂：满节点插入时一分为二，中间键上提
 * 3. 节点合并/借用：删除导致节点键数不足时合并兄弟或借键
 * 4. 所有叶子节点在同一层，保证平衡
 *
 * 作用：
 * - 减少磁盘I/O（每个节点对应一个磁盘块）
 * - 数据库索引和文件系统的基础数据结构
 *
 * 业务场景：
 * 1. 数据库索引：MySQL InnoDB B+树底层
 * 2. 文件系统：NTFS, ext4, HFS+ 的目录结构
 * 3. MongoDB：索引结构
 * 4. 键值存储：LevelDB/RocksDB 的 SSTable
 * 5. 缓存系统：大规模有序缓存
 * 6. 日志系统：按时间范围查询
 * 7. 搜索引擎：倒排索引存储
 * 8. GIS系统：空间索引（R树基于B树）
 * 9. 时间序列数据库：InfluxDB 的 TSI
 * 10. 网络路由表：分层前缀匹配
 *
 * 时间复杂度：所有操作 O(log n)
 */
class BTree
{
    private int $t;             // 最小度数 (degree)
    private ?BTNode $root = null;
    private int $size = 0;

    /**
     * @param int $t 最小度数。每个节点最多 2t-1 个键，最少 t-1 个键(root除外)
     */
    public function __construct(int $t = 3)
    {
        $this->t = max(2, $t);
    }

    /**
     * 搜索键
     */
    public function search($key)
    {
        $result = $this->searchInNode($this->root, $key);
        return $result !== null ? $result[1] : null;
    }

    private function searchInNode(?BTNode $node, $key): ?array
    {
        if ($node === null) {
            return null;
        }

        $i = 0;
        while ($i < $node->n && $this->compare($key, $node->keys[$i]) > 0) {
            $i++;
        }

        if ($i < $node->n && $this->compare($key, $node->keys[$i]) === 0) {
            return [$node, $i];
        }

        if ($node->leaf) {
            return null;
        }

        return $this->searchInNode($node->children[$i], $key);
    }

    /**
     * 插入键值
     */
    public function insert($key, $value = null): void
    {
        if ($this->root === null) {
            $this->root = new BTNode(true);
        }

        // 根节点已满 → 分裂
        if ($this->root->n === 2 * $this->t - 1) {
            $newRoot = new BTNode(false);
            $newRoot->children[0] = $this->root;
            $this->splitChild($newRoot, 0);
            $this->root = $newRoot;
        }

        $this->insertNonFull($this->root, $key, $value);
        $this->size++;
    }

    /**
     * 向非满节点插入
     */
    private function insertNonFull(BTNode $node, $key, $value): void
    {
        $i = $node->n - 1;

        if ($node->leaf) {
            // 找到插入位置
            while ($i >= 0 && $this->compare($key, $node->keys[$i]) < 0) {
                $node->keys[$i + 1] = $node->keys[$i];
                $node->values[$i + 1] = $node->values[$i];
                $i--;
            }

            // 键已存在 → 更新值
            if ($i >= 0 && $this->compare($key, $node->keys[$i]) === 0) {
                $node->values[$i] = $value;
                $this->size--;
                return;
            }

            $node->keys[$i + 1] = $key;
            $node->values[$i + 1] = $value;
            $node->n++;
        } else {
            // 找到子节点
            while ($i >= 0 && $this->compare($key, $node->keys[$i]) < 0) {
                $i--;
            }
            $i++;

            // 子节点已满 → 先分裂
            if ($node->children[$i]->n === 2 * $this->t - 1) {
                $this->splitChild($node, $i);
                if ($this->compare($key, $node->keys[$i]) > 0) {
                    $i++;
                }
            }

            $this->insertNonFull($node->children[$i], $key, $value);
        }
    }

    /**
     * 分裂 node 的第 i 个子节点
     */
    private function splitChild(BTNode $parent, int $i): void
    {
        $t = $this->t;
        $child = $parent->children[$i];
        $newNode = new BTNode($child->leaf);

        // 后半部分键移到新节点
        $newNode->n = $t - 1;
        for ($j = 0; $j < $t - 1; $j++) {
            $newNode->keys[$j] = $child->keys[$j + $t];
            $newNode->values[$j] = $child->values[$j + $t];
        }

        // 如果不是叶子，移动子节点
        if (!$child->leaf) {
            for ($j = 0; $j < $t; $j++) {
                $newNode->children[$j] = $child->children[$j + $t];
            }
        }

        $child->n = $t - 1;

        // 在父节点中为新节点腾出空间
        for ($j = $parent->n; $j > $i; $j--) {
            $parent->children[$j + 1] = $parent->children[$j];
        }
        $parent->children[$i + 1] = $newNode;

        // 上提中间键
        for ($j = $parent->n - 1; $j >= $i; $j--) {
            $parent->keys[$j + 1] = $parent->keys[$j];
            $parent->values[$j + 1] = $parent->values[$j];
        }
        $parent->keys[$i] = $child->keys[$t - 1];
        $parent->values[$i] = $child->values[$t - 1];
        $parent->n++;
    }

    /**
     * 删除键
     */
    public function delete($key): bool
    {
        if ($this->root === null) {
            return false;
        }

        $deleted = $this->deleteFromNode($this->root, $key);

        if ($this->root->n === 0) {
            $this->root = $this->root->leaf ? null : $this->root->children[0];
        }

        if ($deleted) {
            $this->size--;
        }

        return $deleted;
    }

    private function deleteFromNode(BTNode $node, $key): bool
    {
        $t = $this->t;
        $idx = 0;

        // 找到键在节点中的位置或应去的子节点
        while ($idx < $node->n && $this->compare($key, $node->keys[$idx]) > 0) {
            $idx++;
        }

        // Case 1: 键在当前节点
        if ($idx < $node->n && $this->compare($key, $node->keys[$idx]) === 0) {
            if ($node->leaf) {
                // Case 1a: 叶子节点 → 直接删除
                $this->removeFromNode($node, $idx);
                return true;
            } else {
                // Case 1b: 内部节点
                return $this->deleteFromInternalNode($node, $idx);
            }
        }

        // Case 2: 键不在当前节点
        if ($node->leaf) {
            return false;
        }

        // 确保子节点至少有 t 个键
        $child = $node->children[$idx];
        if ($child->n < $t) {
            $this->fillChild($node, $idx);
            // 重新定位（可能键被下移了）
            if ($idx > $node->n) {
                $idx--;
            }
            if ($idx < $node->n && $this->compare($key, $node->keys[$idx]) === 0) {
                if ($node->leaf) {
                    $this->removeFromNode($node, $idx);
                    return true;
                }
                return $this->deleteFromInternalNode($node, $idx);
            }
            $child = $node->children[$idx];
        }

        return $this->deleteFromNode($child, $key);
    }

    private function deleteFromInternalNode(BTNode $node, int $idx): bool
    {
        $t = $this->t;
        $key = $node->keys[$idx];

        // Case 2a: 左子节点有足够键
        if ($node->children[$idx]->n >= $t) {
            $pred = $this->getPredecessor($node, $idx);
            $node->keys[$idx] = $pred[0];
            $node->values[$idx] = $pred[1];
            return $this->deleteFromNode($node->children[$idx], $pred[0]);
        }

        // Case 2b: 右子节点有足够键
        if ($node->children[$idx + 1]->n >= $t) {
            $succ = $this->getSuccessor($node, $idx);
            $node->keys[$idx] = $succ[0];
            $node->values[$idx] = $succ[1];
            return $this->deleteFromNode($node->children[$idx + 1], $succ[0]);
        }

        // Case 2c: 合并两个子节点
        $this->mergeChildren($node, $idx);
        return $this->deleteFromNode($node->children[$idx], $key);
    }

    private function getPredecessor(BTNode $node, int $idx): array
    {
        $cur = $node->children[$idx];
        while (!$cur->leaf) {
            $cur = $cur->children[$cur->n];
        }
        return [$cur->keys[$cur->n - 1], $cur->values[$cur->n - 1]];
    }

    private function getSuccessor(BTNode $node, int $idx): array
    {
        $cur = $node->children[$idx + 1];
        while (!$cur->leaf) {
            $cur = $cur->children[0];
        }
        return [$cur->keys[0], $cur->values[0]];
    }

    /**
     * 确保 node->children[idx] 至少有 t 个键
     */
    private function fillChild(BTNode $node, int $idx): void
    {
        $t = $this->t;

        // 从左兄弟借
        if ($idx > 0 && $node->children[$idx - 1]->n >= $t) {
            $this->borrowFromLeft($node, $idx);
        }
        // 从右兄弟借
        elseif ($idx < $node->n && $node->children[$idx + 1]->n >= $t) {
            $this->borrowFromRight($node, $idx);
        }
        // 合并
        else {
            if ($idx < $node->n) {
                $this->mergeChildren($node, $idx);
            } else {
                $this->mergeChildren($node, $idx - 1);
            }
        }
    }

    private function borrowFromLeft(BTNode $parent, int $idx): void
    {
        $child = $parent->children[$idx];
        $leftSibling = $parent->children[$idx - 1];

        // 为 child 腾出空间
        for ($i = $child->n; $i > 0; $i--) {
            $child->keys[$i] = $child->keys[$i - 1];
            $child->values[$i] = $child->values[$i - 1];
        }
        if (!$child->leaf) {
            for ($i = $child->n + 1; $i > 0; $i--) {
                $child->children[$i] = $child->children[$i - 1];
            }
        }

        // 父键下移到 child
        $child->keys[0] = $parent->keys[$idx - 1];
        $child->values[0] = $parent->values[$idx - 1];
        $child->n++;

        // 左兄弟最大键上移到父节点
        $parent->keys[$idx - 1] = $leftSibling->keys[$leftSibling->n - 1];
        $parent->values[$idx - 1] = $leftSibling->values[$leftSibling->n - 1];

        // 左兄弟最大子节点移到 child
        if (!$child->leaf) {
            $child->children[0] = $leftSibling->children[$leftSibling->n];
        }

        $leftSibling->n--;
    }

    private function borrowFromRight(BTNode $parent, int $idx): void
    {
        $child = $parent->children[$idx];
        $rightSibling = $parent->children[$idx + 1];

        // 父键下移到 child
        $child->keys[$child->n] = $parent->keys[$idx];
        $child->values[$child->n] = $parent->values[$idx];
        $child->n++;

        // 右兄弟最小键上移到父节点
        $parent->keys[$idx] = $rightSibling->keys[0];
        $parent->values[$idx] = $rightSibling->values[0];

        // 右兄弟最小子节点移到 child
        if (!$child->leaf) {
            $child->children[$child->n] = $rightSibling->children[0];
        }

        // 右兄弟移除第一个元素
        for ($i = 0; $i < $rightSibling->n - 1; $i++) {
            $rightSibling->keys[$i] = $rightSibling->keys[$i + 1];
            $rightSibling->values[$i] = $rightSibling->values[$i + 1];
        }
        if (!$rightSibling->leaf) {
            for ($i = 0; $i < $rightSibling->n; $i++) {
                $rightSibling->children[$i] = $rightSibling->children[$i + 1];
            }
        }

        $rightSibling->n--;
    }

    private function mergeChildren(BTNode $parent, int $idx): void
    {
        $left = $parent->children[$idx];
        $right = $parent->children[$idx + 1];
        $t = $this->t;

        // 父键下移到左子节点
        $left->keys[$t - 1] = $parent->keys[$idx];
        $left->values[$t - 1] = $parent->values[$idx];

        // 右子节点所有键复制到左子节点
        for ($j = 0; $j < $right->n; $j++) {
            $left->keys[$j + $t] = $right->keys[$j];
            $left->values[$j + $t] = $right->values[$j];
        }

        // 复制子节点指针
        if (!$left->leaf) {
            for ($j = 0; $j <= $right->n; $j++) {
                $left->children[$j + $t] = $right->children[$j];
            }
        }

        $left->n = 2 * $t - 1;

        // 从父节点移除键和右子节点
        $this->removeFromNode($parent, $idx);
        for ($j = $idx + 1; $j < $parent->n + 1; $j++) {
            $parent->children[$j] = $parent->children[$j + 1];
        }
    }

    private function removeFromNode(BTNode $node, int $idx): void
    {
        for ($i = $idx; $i < $node->n - 1; $i++) {
            $node->keys[$i] = $node->keys[$i + 1];
            $node->values[$i] = $node->values[$i + 1];
        }
        $node->n--;
    }

    /**
     * 中序遍历所有键值
     */
    public function inorderTraversal(): array
    {
        $result = [];
        $this->inorder($this->root, $result);
        return $result;
    }

    private function inorder(?BTNode $node, array &$result): void
    {
        if ($node === null) {
            return;
        }
        for ($i = 0; $i < $node->n; $i++) {
            if (!$node->leaf) {
                $this->inorder($node->children[$i], $result);
            }
            $result[] = ['key' => $node->keys[$i], 'value' => $node->values[$i]];
        }
        if (!$node->leaf) {
            $this->inorder($node->children[$node->n], $result);
        }
    }

    /**
     * 范围查询 [low, high]
     */
    public function rangeSearch($low, $high): array
    {
        $result = [];
        $this->rangeSearchUtil($this->root, $low, $high, $result);
        return $result;
    }

    private function rangeSearchUtil(?BTNode $node, $low, $high, array &$result): void
    {
        if ($node === null) {
            return;
        }

        $i = 0;
        while ($i < $node->n && $this->compare($node->keys[$i], $low) < 0) {
            $i++;
        }

        if (!$node->leaf) {
            $this->rangeSearchUtil($node->children[$i], $low, $high, $result);
        }

        while ($i < $node->n && $this->compare($node->keys[$i], $high) <= 0) {
            $result[] = ['key' => $node->keys[$i], 'value' => $node->values[$i]];
            if (!$node->leaf) {
                $this->rangeSearchUtil($node->children[$i + 1], $low, $high, $result);
            }
            $i++;
        }
    }

    public function getSize(): int
    {
        return $this->size;
    }

    public function isEmpty(): bool
    {
        return $this->size === 0;
    }

    private function compare($a, $b): int
    {
        return $a <=> $b;
    }
}

/**
 * B树节点
 */
class BTNode
{
    public array $keys;
    public array $values;
    public array $children;
    public int $n;          // 当前键数量
    public bool $leaf;

    public function __construct(bool $leaf)
    {
        $this->leaf = $leaf;
        $this->keys = [];
        $this->values = [];
        $this->children = [];
        $this->n = 0;
    }
}
