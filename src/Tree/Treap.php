<?php

namespace DataStructures\Tree;

/**
 * Treap - 树堆（随机平衡二叉搜索树）
 *
 * 思路：
 * 1. 每个节点有一个键(BST顺序)和一个随机优先级(堆序)
 * 2. 插入：先按BST规则插入，然后向上旋转维护堆性质
 * 3. 删除：将节点旋转到叶子后删除
 * 4. 期望高度 O(log n)，实现简单且常数小
 *
 * 作用：
 * - 比AVL/红黑树实现简单
 * - 随机化保证期望 O(log n)
 * - 支持分裂(split)和合并(merge)操作
 * - 隐式Treap可做序列操作
 *
 * 业务场景：
 * 1. 随机化数据结构：需要简单平衡树
 * 2. 序列维护：区间翻转、区间求和
 * 3. 内存分配器：空闲块管理
 * 4. 游戏开发：随机化AI决策树
 * 5. 在线算法：动态统计
 * 6. 文本编辑器：rope数据结构
 * 7. 分布式系统：随机化负载均衡
 * 8. 密码学应用：随机化防御时序攻击
 * 9. 机器学习：随机森林节点划分
 * 10. 编译器：随机化符号表
 *
 * 时间复杂度（期望）：
 * - search: O(log n)
 * - insert: O(log n)
 * - delete: O(log n)
 */
class Treap
{
    private ?TreapNode $root = null;
    private int $size = 0;

    /**
     * 插入键值
     */
    public function insert($key, $value = null): void
    {
        $this->root = $this->insertNode($this->root, $key, $value);
    }

    private function insertNode(?TreapNode $node, $key, $value): TreapNode
    {
        if ($node === null) {
            $this->size++;
            return new TreapNode($key, $value);
        }

        $cmp = $key <=> $node->key;
        if ($cmp < 0) {
            $node->left = $this->insertNode($node->left, $key, $value);
            if ($node->left->priority > $node->priority) {
                $node = $this->rotateRight($node);
            }
        } elseif ($cmp > 0) {
            $node->right = $this->insertNode($node->right, $key, $value);
            if ($node->right->priority > $node->priority) {
                $node = $this->rotateLeft($node);
            }
        } else {
            $node->value = $value;
        }

        return $node;
    }

    /**
     * 查找键
     */
    public function search($key)
    {
        $node = $this->searchNode($this->root, $key);
        return $node !== null ? $node->value : null;
    }

    public function contains($key): bool
    {
        return $this->searchNode($this->root, $key) !== null;
    }

    private function searchNode(?TreapNode $node, $key): ?TreapNode
    {
        while ($node !== null) {
            $cmp = $key <=> $node->key;
            if ($cmp < 0) {
                $node = $node->left;
            } elseif ($cmp > 0) {
                $node = $node->right;
            } else {
                return $node;
            }
        }
        return null;
    }

    /**
     * 删除键
     */
    public function delete($key): bool
    {
        if (!$this->contains($key)) {
            return false;
        }
        $this->root = $this->deleteNode($this->root, $key);
        $this->size--;
        return true;
    }

    private function deleteNode(?TreapNode $node, $key): ?TreapNode
    {
        if ($node === null) {
            return null;
        }

        $cmp = $key <=> $node->key;
        if ($cmp < 0) {
            $node->left = $this->deleteNode($node->left, $key);
        } elseif ($cmp > 0) {
            $node->right = $this->deleteNode($node->right, $key);
        } else {
            // 叶子节点 → 直接删除
            if ($node->left === null && $node->right === null) {
                return null;
            }

            // 旋转到叶子
            if ($node->left === null) {
                $node = $this->rotateLeft($node);
            } elseif ($node->right === null) {
                $node = $this->rotateRight($node);
            } elseif ($node->left->priority > $node->right->priority) {
                $node = $this->rotateRight($node);
            } else {
                $node = $this->rotateLeft($node);
            }

            $node = $this->deleteNode($node, $key);
        }

        return $node;
    }

    /**
     * 分裂：按 key 将树分为两棵，左边所有键 ≤ key，右边所有键 > key
     *
     * @param $key
     * @return array [left Treap, right Treap]
     */
    public function split($key): array
    {
        $left = new Treap();
        $right = new Treap();

        [$left->root, $right->root] = $this->splitNode($this->root, $key);
        $left->size = $this->countNodes($left->root);
        $right->size = $this->countNodes($right->root);

        return [$left, $right];
    }

    private function splitNode(?TreapNode $node, $key): array
    {
        if ($node === null) {
            return [null, null];
        }

        if (($key <=> $node->key) >= 0) {
            [$l, $r] = $this->splitNode($node->right, $key);
            $node->right = $l;
            return [$node, $r];
        } else {
            [$l, $r] = $this->splitNode($node->left, $key);
            $node->left = $r;
            return [$l, $node];
        }
    }

    /**
     * 合并：将两棵树合并（左树所有键 ≤ 右树所有键）
     */
    public static function merge(Treap $left, Treap $right): Treap
    {
        $result = new Treap();
        $result->root = self::mergeNodes($left->root, $right->root);
        $result->size = $left->size + $right->size;
        return $result;
    }

    private static function mergeNodes(?TreapNode $left, ?TreapNode $right): ?TreapNode
    {
        if ($left === null) {
            return $right;
        }
        if ($right === null) {
            return $left;
        }

        if ($left->priority > $right->priority) {
            $left->right = self::mergeNodes($left->right, $right);
            return $left;
        } else {
            $right->left = self::mergeNodes($left, $right->left);
            return $right;
        }
    }

    /**
     * 中序遍历
     */
    public function inorderTraversal(): array
    {
        $result = [];
        $this->inorder($this->root, $result);
        return $result;
    }

    private function inorder(?TreapNode $node, array &$result): void
    {
        if ($node === null) {
            return;
        }
        $this->inorder($node->left, $result);
        $result[] = ['key' => $node->key, 'value' => $node->value, 'priority' => $node->priority];
        $this->inorder($node->right, $result);
    }

    public function getSize(): int
    {
        return $this->size;
    }

    public function isEmpty(): bool
    {
        return $this->size === 0;
    }

    private function countNodes(?TreapNode $node): int
    {
        if ($node === null) {
            return 0;
        }
        return 1 + $this->countNodes($node->left) + $this->countNodes($node->right);
    }

    /**
     * 右旋
     */
    private function rotateRight(TreapNode $y): TreapNode
    {
        $x = $y->left;
        $y->left = $x->right;
        $x->right = $y;
        return $x;
    }

    /**
     * 左旋
     */
    private function rotateLeft(TreapNode $x): TreapNode
    {
        $y = $x->right;
        $x->right = $y->left;
        $y->left = $x;
        return $y;
    }
}

/**
 * Treap节点
 */
class TreapNode
{
    public $key;
    public $value;
    public int $priority;
    public ?TreapNode $left;
    public ?TreapNode $right;

    public function __construct($key, $value)
    {
        $this->key = $key;
        $this->value = $value;
        $this->priority = random_int(1, PHP_INT_MAX);
        $this->left = null;
        $this->right = null;
    }
}
