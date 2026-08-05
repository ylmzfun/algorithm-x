<?php

namespace DataStructures\Tree;

/**
 * AVLTree - 自平衡二叉搜索树
 *
 * 思路：
 * 1. 每个节点维护平衡因子（左子树高度 - 右子树高度）
 * 2. 平衡因子绝对值超过1时进行旋转调整
 * 3. 四种旋转：左旋(LL)、右旋(RR)、左右旋(LR)、右左旋(RL)
 * 4. 插入和删除后自底向上维护平衡
 *
 * 作用：
 * - 保证最坏情况下 O(log n) 的查找/插入/删除
 * - 比红黑树更严格的平衡，查找性能更好
 * - 适合需要频繁查找的场景
 *
 * 业务场景：
 * 1. 数据库索引：需要稳定查找性能
 * 2. 内存数据库：频繁范围查询
 * 3. 字典/词典：有序键值存储
 * 4. 游戏引擎：空间分区和碰撞检测
 * 5. 文件系统：目录索引
 * 6. 网络路由表：IP前缀匹配
 * 7. 编译器：符号表管理
 * 8. 金融系统：订单簿维护
 * 9. 搜索引擎：文档ID排序
 * 10. 版本控制：文件差异管理
 *
 * 时间复杂度：
 * - search: O(log n)
 * - insert: O(log n)
 * - delete: O(log n)
 * - min/max: O(log n)
 */
class AVLTree
{
    private ?AVLNode $root = null;
    private int $size = 0;

    /**
     * 插入键值
     *
     * @param mixed $key
     * @param mixed $value
     */
    public function insert($key, $value = null): void
    {
        $this->root = $this->insertNode($this->root, $key, $value);
    }

    private function insertNode(?AVLNode $node, $key, $value): AVLNode
    {
        if ($node === null) {
            $this->size++;
            return new AVLNode($key, $value);
        }

        $cmp = $this->compare($key, $node->key);
        if ($cmp < 0) {
            $node->left = $this->insertNode($node->left, $key, $value);
        } elseif ($cmp > 0) {
            $node->right = $this->insertNode($node->right, $key, $value);
        } else {
            // 更新已有键的值
            $node->value = $value;
            return $node;
        }

        $node->updateHeight();
        return $this->rebalance($node);
    }

    /**
     * 查找键对应的值
     *
     * @param mixed $key
     * @return mixed|null
     */
    public function search($key)
    {
        $node = $this->searchNode($this->root, $key);
        return $node !== null ? $node->value : null;
    }

    /**
     * 判断键是否存在
     *
     * @param mixed $key
     * @return bool
     */
    public function contains($key): bool
    {
        return $this->searchNode($this->root, $key) !== null;
    }

    private function searchNode(?AVLNode $node, $key): ?AVLNode
    {
        if ($node === null) {
            return null;
        }

        $cmp = $this->compare($key, $node->key);
        if ($cmp < 0) {
            return $this->searchNode($node->left, $key);
        } elseif ($cmp > 0) {
            return $this->searchNode($node->right, $key);
        }
        return $node;
    }

    /**
     * 删除键
     *
     * @param mixed $key
     * @return bool 是否成功删除
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

    private function deleteNode(?AVLNode $node, $key): ?AVLNode
    {
        if ($node === null) {
            return null;
        }

        $cmp = $this->compare($key, $node->key);
        if ($cmp < 0) {
            $node->left = $this->deleteNode($node->left, $key);
        } elseif ($cmp > 0) {
            $node->right = $this->deleteNode($node->right, $key);
        } else {
            // 找到要删除的节点
            if ($node->left === null || $node->right === null) {
                $node = $node->left ?? $node->right;
            } else {
                // 用后继节点替换
                $successor = $this->findMin($node->right);
                $node->key = $successor->key;
                $node->value = $successor->value;
                $node->right = $this->deleteNode($node->right, $successor->key);
            }
        }

        if ($node === null) {
            return null;
        }

        $node->updateHeight();
        return $this->rebalance($node);
    }

    /**
     * 获取最小值
     *
     * @return mixed|null
     */
    public function min()
    {
        if ($this->root === null) {
            return null;
        }
        $minNode = $this->findMin($this->root);
        return ['key' => $minNode->key, 'value' => $minNode->value];
    }

    private function findMin(AVLNode $node): AVLNode
    {
        while ($node->left !== null) {
            $node = $node->left;
        }
        return $node;
    }

    /**
     * 获取最大值
     *
     * @return mixed|null
     */
    public function max()
    {
        if ($this->root === null) {
            return null;
        }
        $maxNode = $this->findMax($this->root);
        return ['key' => $maxNode->key, 'value' => $maxNode->value];
    }

    private function findMax(AVLNode $node): AVLNode
    {
        while ($node->right !== null) {
            $node = $node->right;
        }
        return $node;
    }

    /**
     * 中序遍历（按键升序）
     *
     * @return array
     */
    public function inorderTraversal(): array
    {
        $result = [];
        $this->inorder($this->root, $result);
        return $result;
    }

    private function inorder(?AVLNode $node, array &$result): void
    {
        if ($node === null) {
            return;
        }
        $this->inorder($node->left, $result);
        $result[] = ['key' => $node->key, 'value' => $node->value];
        $this->inorder($node->right, $result);
    }

    /**
     * 获取元素数量
     *
     * @return int
     */
    public function getSize(): int
    {
        return $this->size;
    }

    /**
     * 判断是否为空
     *
     * @return bool
     */
    public function isEmpty(): bool
    {
        return $this->size === 0;
    }

    /**
     * 获取树的高度
     *
     * @return int
     */
    public function getHeight(): int
    {
        return $this->root !== null ? $this->root->height : 0;
    }

    // ---------- 旋转操作 ----------

    private function rebalance(AVLNode $node): AVLNode
    {
        $balance = $node->getBalanceFactor();

        // LL: 左子树过高
        if ($balance > 1 && $node->left->getBalanceFactor() >= 0) {
            return $this->rotateRight($node);
        }

        // LR: 左子树的右子树过高
        if ($balance > 1 && $node->left->getBalanceFactor() < 0) {
            $node->left = $this->rotateLeft($node->left);
            return $this->rotateRight($node);
        }

        // RR: 右子树过高
        if ($balance < -1 && $node->right->getBalanceFactor() <= 0) {
            return $this->rotateLeft($node);
        }

        // RL: 右子树的左子树过高
        if ($balance < -1 && $node->right->getBalanceFactor() > 0) {
            $node->right = $this->rotateRight($node->right);
            return $this->rotateLeft($node);
        }

        return $node;
    }

    /**
     * 右旋
     */
    private function rotateRight(AVLNode $y): AVLNode
    {
        $x = $y->left;
        $T2 = $x->right;

        $x->right = $y;
        $y->left = $T2;

        $y->updateHeight();
        $x->updateHeight();

        return $x;
    }

    /**
     * 左旋
     */
    private function rotateLeft(AVLNode $x): AVLNode
    {
        $y = $x->right;
        $T2 = $y->left;

        $y->left = $x;
        $x->right = $T2;

        $x->updateHeight();
        $y->updateHeight();

        return $y;
    }

    private function compare($a, $b): int
    {
        return $a <=> $b;
    }
}

/**
 * AVL树节点
 */
class AVLNode
{
    public $key;
    public $value;
    public int $height;
    public ?AVLNode $left;
    public ?AVLNode $right;

    public function __construct($key, $value)
    {
        $this->key = $key;
        $this->value = $value;
        $this->height = 1;
        $this->left = null;
        $this->right = null;
    }

    /**
     * 更新节点高度
     */
    public function updateHeight(): void
    {
        $leftHeight = $this->left !== null ? $this->left->height : 0;
        $rightHeight = $this->right !== null ? $this->right->height : 0;
        $this->height = max($leftHeight, $rightHeight) + 1;
    }

    /**
     * 获取平衡因子
     *
     * @return int
     */
    public function getBalanceFactor(): int
    {
        $leftHeight = $this->left !== null ? $this->left->height : 0;
        $rightHeight = $this->right !== null ? $this->right->height : 0;
        return $leftHeight - $rightHeight;
    }
}
