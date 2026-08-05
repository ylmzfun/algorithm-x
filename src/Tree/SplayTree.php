<?php

namespace DataStructures\Tree;

/**
 * SplayTree - 伸展树
 *
 * 思路：
 * 1. 每次访问节点后通过旋转将其推至根节点（splay操作）
 * 2. zig-zig / zig-zag / zig 三种旋转模式
 * 3. 摊还复杂度 O(log n)
 * 4. 最近访问的元素靠近根，适合局部性访问模式
 *
 * 作用：
 * - 缓存友好的自调整结构
 * - 无需存储平衡信息，节省空间
 * - 实现比AVL/红黑树简单
 *
 * 业务场景：
 * 1. 缓存系统：访问频率自适应
 * 2. 网络路由：最近使用路由优先
 * 3. 垃圾回收：分代回收
 * 4. 数据压缩：Huffman编码辅助
 * 5. 搜索引擎：热门查询缓存
 * 6. 内存分配器：空闲块管理
 * 7. 编译器：近期符号快速查找
 * 8. 数据库：自适应索引
 * 9. 文件系统：目录缓存
 * 10. 机器学习：特征选择
 *
 * 时间复杂度：均摊 O(log n)
 */
class SplayTree
{
    private ?SplayNode $root = null;
    private int $size = 0;

    /**
     * 插入键值，插入后 splay 新节点到根
     */
    public function insert($key, $value = null): void
    {
        if ($this->root === null) {
            $this->root = new SplayNode($key, $value);
            $this->size++;
            return;
        }

        $this->root = $this->splay($this->root, $key);

        $cmp = $key <=> $this->root->key;
        if ($cmp === 0) {
            $this->root->value = $value;
            return;
        }

        $node = new SplayNode($key, $value);
        if ($cmp < 0) {
            $node->left = $this->root->left;
            $this->root->left = null;
            $node->right = $this->root;
        } else {
            $node->right = $this->root->right;
            $this->root->right = null;
            $node->left = $this->root;
        }
        $this->root = $node;
        $this->size++;
    }

    /**
     * 查找键，splay 找到的节点（或其前驱/后继）到根
     */
    public function search($key)
    {
        if ($this->root === null) {
            return null;
        }
        $this->root = $this->splay($this->root, $key);
        return ($key <=> $this->root->key) === 0 ? $this->root->value : null;
    }

    public function contains($key): bool
    {
        return $this->search($key) !== null;
    }

    /**
     * 删除键
     */
    public function delete($key): bool
    {
        if ($this->root === null) {
            return false;
        }

        $this->root = $this->splay($this->root, $key);
        if (($key <=> $this->root->key) !== 0) {
            return false;
        }

        // 移除根节点
        if ($this->root->left === null) {
            $this->root = $this->root->right;
        } else {
            $rightChild = $this->root->right;
            $this->root = $this->splay($this->root->left, $key);
            $this->root->right = $rightChild;
        }

        $this->size--;
        return true;
    }

    /**
     * 核心 splay 操作：将键为 key 的节点旋转到子树的根
     * 如果 key 不存在，则将最后一个访问的节点旋转到根
     */
    private function splay(SplayNode $node, $key): SplayNode
    {
        if ($node === null) {
            return $node;
        }

        // 使用临时头节点简化旋转
        $header = new SplayNode(null, null);
        $leftTree = $header;   // 最终放小于 key 的节点
        $rightTree = $header;  // 最终放大于 key 的节点

        while (true) {
            $cmp = $key <=> $node->key;

            if ($cmp < 0) {
                if ($node->left === null) {
                    break;
                }
                $cmp2 = $key <=> $node->left->key;

                if ($cmp2 < 0) {
                    // zig-zig
                    $node = $this->rotateRight($node);
                    if ($node->left === null) {
                        break;
                    }
                }
                // link right
                $rightTree->left = $node;
                $rightTree = $node;
                $node = $node->left;
            } elseif ($cmp > 0) {
                if ($node->right === null) {
                    break;
                }
                $cmp2 = $key <=> $node->right->key;

                if ($cmp2 > 0) {
                    // zag-zag
                    $node = $this->rotateLeft($node);
                    if ($node->right === null) {
                        break;
                    }
                }
                // link left
                $leftTree->right = $node;
                $leftTree = $node;
                $node = $node->right;
            } else {
                break;
            }
        }

        // 重组
        $leftTree->right = $node->left;
        $rightTree->left = $node->right;
        $node->left = $header->right;
        $node->right = $header->left;

        return $node;
    }

    private function rotateRight(SplayNode $x): SplayNode
    {
        $y = $x->left;
        $x->left = $y->right;
        $y->right = $x;
        return $y;
    }

    private function rotateLeft(SplayNode $x): SplayNode
    {
        $y = $x->right;
        $x->right = $y->left;
        $y->left = $x;
        return $y;
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

    private function inorder(?SplayNode $node, array &$result): void
    {
        if ($node === null) {
            return;
        }
        $this->inorder($node->left, $result);
        $result[] = ['key' => $node->key, 'value' => $node->value];
        $this->inorder($node->right, $result);
    }

    public function getSize(): int { return $this->size; }
    public function isEmpty(): bool { return $this->size === 0; }
}

class SplayNode
{
    public $key;
    public $value;
    public ?SplayNode $left;
    public ?SplayNode $right;

    public function __construct($key, $value)
    {
        $this->key = $key;
        $this->value = $value;
        $this->left = null;
        $this->right = null;
    }
}
