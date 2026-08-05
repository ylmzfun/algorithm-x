<?php

namespace DataStructures\Tree;

/**
 * RedBlackTree - 红黑树
 *
 * 思路：
 * 1. 每个节点为红色或黑色，满足5条红黑性质
 * 2. 插入后通过重新着色和旋转恢复平衡
 * 3. 删除后通过"双黑"修正过程恢复平衡
 * 4. 相比AVL树，旋转次数更少，插入删除更高效
 *
 * 红黑性质：
 * 1. 每个节点是红色或黑色
 * 2. 根节点是黑色
 * 3. 叶子节点(NIL)是黑色
 * 4. 红色节点的两个子节点都是黑色
 * 5. 任意节点到其叶子节点的所有路径包含相同数量的黑色节点
 *
 * 作用：
 * - 提供近似平衡，保证最坏O(log n)
 * - 插入删除比AVL树旋转更少
 * - 广泛用于系统级数据结构
 *
 * 业务场景：
 * 1. Linux内核：CFS调度器、内存管理
 * 2. Java：TreeMap/TreeSet底层实现
 * 3. C++ STL：std::map/std::set
 * 4. 数据库：内存索引结构
 * 5. Nginx：定时器管理
 * 6. Epoll：事件管理
 * 7. 防火墙：连接跟踪
 * 8. 文件系统：ext4的目录项缓存
 * 9. 虚拟内存：VMA管理
 * 10. 编程语言运行时：符号表
 *
 * 时间复杂度：
 * - search: O(log n)
 * - insert: O(log n)
 * - delete: O(log n)
 */
class RedBlackTree
{
    private const RED = true;
    private const BLACK = false;

    private ?RBNode $root = null;
    private int $size = 0;

    /**
     * 插入键值
     */
    public function insert($key, $value = null): void
    {
        $node = new RBNode($key, $value, self::RED);

        // 标准BST插入
        $parent = null;
        $current = $this->root;

        while ($current !== null) {
            $parent = $current;
            $cmp = $key <=> $current->key;
            if ($cmp < 0) {
                $current = $current->left;
            } elseif ($cmp > 0) {
                $current = $current->right;
            } else {
                $current->value = $value;
                return;
            }
        }

        $node->parent = $parent;
        if ($parent === null) {
            $this->root = $node;
        } elseif (($key <=> $parent->key) < 0) {
            $parent->left = $node;
        } else {
            $parent->right = $node;
        }

        $this->size++;
        $this->insertFixup($node);
    }

    /**
     * 插入修复：恢复红黑性质
     */
    private function insertFixup(RBNode $node): void
    {
        // 当父节点是红色时（违反性质4）
        while ($node->parent !== null && $node->parent->color === self::RED) {
            $parent = $node->parent;
            $grandparent = $parent->parent;

            if ($grandparent === null) {
                break;
            }

            if ($parent === $grandparent->left) {
                $uncle = $grandparent->right;

                // Case 1: 叔叔是红色 → 重新着色
                if ($uncle !== null && $uncle->color === self::RED) {
                    $parent->color = self::BLACK;
                    $uncle->color = self::BLACK;
                    $grandparent->color = self::RED;
                    $node = $grandparent;
                    continue;
                }

                // Case 2: 叔叔是黑色，节点是右孩子 → 左旋
                if ($node === $parent->right) {
                    $node = $parent;
                    $this->rotateLeft($node);
                    $parent = $node->parent;
                    $grandparent = $parent->parent;
                }

                // Case 3: 叔叔是黑色，节点是左孩子 → 右旋 + 着色
                if ($parent !== null) {
                    $parent->color = self::BLACK;
                }
                if ($grandparent !== null) {
                    $grandparent->color = self::RED;
                    $this->rotateRight($grandparent);
                }
            } else {
                // 镜像情况
                $uncle = $grandparent->left;

                if ($uncle !== null && $uncle->color === self::RED) {
                    $parent->color = self::BLACK;
                    $uncle->color = self::BLACK;
                    $grandparent->color = self::RED;
                    $node = $grandparent;
                    continue;
                }

                if ($node === $parent->left) {
                    $node = $parent;
                    $this->rotateRight($node);
                    $parent = $node->parent;
                    $grandparent = $parent->parent;
                }

                if ($parent !== null) {
                    $parent->color = self::BLACK;
                }
                if ($grandparent !== null) {
                    $grandparent->color = self::RED;
                    $this->rotateLeft($grandparent);
                }
            }
        }

        if ($this->root !== null) {
            $this->root->color = self::BLACK;
        }
    }

    /**
     * 查找键对应的值
     */
    public function search($key)
    {
        $node = $this->searchNode($key);
        return $node !== null ? $node->value : null;
    }

    /**
     * 判断键是否存在
     */
    public function contains($key): bool
    {
        return $this->searchNode($key) !== null;
    }

    private function searchNode($key): ?RBNode
    {
        $current = $this->root;
        while ($current !== null) {
            $cmp = $key <=> $current->key;
            if ($cmp < 0) {
                $current = $current->left;
            } elseif ($cmp > 0) {
                $current = $current->right;
            } else {
                return $current;
            }
        }
        return null;
    }

    /**
     * 删除键
     */
    public function delete($key): bool
    {
        $node = $this->searchNode($key);
        if ($node === null) {
            return false;
        }

        $this->deleteNode($node);
        $this->size--;
        return true;
    }

    private function deleteNode(RBNode $z): void
    {
        $y = $z;
        $yOriginalColor = $y->color;
        $x = null;

        if ($z->left === null) {
            $x = $z->right;
            $this->transplant($z, $z->right);
        } elseif ($z->right === null) {
            $x = $z->left;
            $this->transplant($z, $z->left);
        } else {
            // 找后继
            $y = $this->minimum($z->right);
            $yOriginalColor = $y->color;
            $x = $y->right;

            if ($y->parent === $z) {
                if ($x !== null) {
                    $x->parent = $y;
                }
            } else {
                $this->transplant($y, $y->right);
                $y->right = $z->right;
                if ($y->right !== null) {
                    $y->right->parent = $y;
                }
            }

            $this->transplant($z, $y);
            $y->left = $z->left;
            if ($y->left !== null) {
                $y->left->parent = $y;
            }
            $y->color = $z->color;
        }

        if ($yOriginalColor === self::BLACK) {
            $this->deleteFixup($x, $y->parent ?? $z->parent);
        }
    }

    /**
     * 删除修复
     */
    private function deleteFixup(?RBNode $x, ?RBNode $xParent): void
    {
        while (($x === null || $x->color === self::BLACK) && $x !== $this->root) {
            $parent = $xParent;
            if ($parent === null) {
                break;
            }

            if ($x === $parent->left) {
                $w = $parent->right;

                // Case 1: 兄弟是红色
                if ($w !== null && $w->color === self::RED) {
                    $w->color = self::BLACK;
                    $parent->color = self::RED;
                    $this->rotateLeft($parent);
                    $w = $parent->right;
                }

                // Case 2: 兄弟的两个孩子都是黑色
                if (($w === null || ($w->left === null || $w->left->color === self::BLACK))
                    && ($w === null || ($w->right === null || $w->right->color === self::BLACK))) {
                    if ($w !== null) {
                        $w->color = self::RED;
                    }
                    $x = $parent;
                    $xParent = $x->parent;
                } else {
                    // Case 3: 兄弟右孩子是黑色，左孩子是红色
                    if ($w !== null && ($w->right === null || $w->right->color === self::BLACK)) {
                        if ($w->left !== null) {
                            $w->left->color = self::BLACK;
                        }
                        $w->color = self::RED;
                        $this->rotateRight($w);
                        $w = $parent->right;
                    }

                    // Case 4: 兄弟右孩子是红色
                    if ($w !== null) {
                        $w->color = $parent->color;
                    }
                    $parent->color = self::BLACK;
                    if ($w !== null && $w->right !== null) {
                        $w->right->color = self::BLACK;
                    }
                    $this->rotateLeft($parent);
                    $x = $this->root;
                    break;
                }
            } else {
                // 镜像
                $w = $parent->left;

                if ($w !== null && $w->color === self::RED) {
                    $w->color = self::BLACK;
                    $parent->color = self::RED;
                    $this->rotateRight($parent);
                    $w = $parent->left;
                }

                if (($w === null || ($w->left === null || $w->left->color === self::BLACK))
                    && ($w === null || ($w->right === null || $w->right->color === self::BLACK))) {
                    if ($w !== null) {
                        $w->color = self::RED;
                    }
                    $x = $parent;
                    $xParent = $x->parent;
                } else {
                    if ($w !== null && ($w->left === null || $w->left->color === self::BLACK)) {
                        if ($w->right !== null) {
                            $w->right->color = self::BLACK;
                        }
                        $w->color = self::RED;
                        $this->rotateLeft($w);
                        $w = $parent->left;
                    }

                    if ($w !== null) {
                        $w->color = $parent->color;
                    }
                    $parent->color = self::BLACK;
                    if ($w !== null && $w->left !== null) {
                        $w->left->color = self::BLACK;
                    }
                    $this->rotateRight($parent);
                    $x = $this->root;
                    break;
                }
            }
        }

        if ($x !== null) {
            $x->color = self::BLACK;
        }
    }

    /**
     * 用 v 替换 u 的位置
     */
    private function transplant(?RBNode $u, ?RBNode $v): void
    {
        if ($u->parent === null) {
            $this->root = $v;
        } elseif ($u === $u->parent->left) {
            $u->parent->left = $v;
        } else {
            $u->parent->right = $v;
        }
        if ($v !== null) {
            $v->parent = $u->parent;
        }
    }

    private function minimum(RBNode $node): RBNode
    {
        while ($node->left !== null) {
            $node = $node->left;
        }
        return $node;
    }

    /**
     * 左旋
     */
    private function rotateLeft(RBNode $x): void
    {
        $y = $x->right;
        if ($y === null) {
            return;
        }

        $x->right = $y->left;
        if ($y->left !== null) {
            $y->left->parent = $x;
        }

        $y->parent = $x->parent;
        if ($x->parent === null) {
            $this->root = $y;
        } elseif ($x === $x->parent->left) {
            $x->parent->left = $y;
        } else {
            $x->parent->right = $y;
        }

        $y->left = $x;
        $x->parent = $y;
    }

    /**
     * 右旋
     */
    private function rotateRight(RBNode $x): void
    {
        $y = $x->left;
        if ($y === null) {
            return;
        }

        $x->left = $y->right;
        if ($y->right !== null) {
            $y->right->parent = $x;
        }

        $y->parent = $x->parent;
        if ($x->parent === null) {
            $this->root = $y;
        } elseif ($x === $x->parent->right) {
            $x->parent->right = $y;
        } else {
            $x->parent->left = $y;
        }

        $y->right = $x;
        $x->parent = $y;
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

    private function inorder(?RBNode $node, array &$result): void
    {
        if ($node === null) {
            return;
        }
        $this->inorder($node->left, $result);
        $result[] = ['key' => $node->key, 'value' => $node->value];
        $this->inorder($node->right, $result);
    }

    /**
     * 获取最小值
     */
    public function min()
    {
        if ($this->root === null) {
            return null;
        }
        $minNode = $this->minimum($this->root);
        return ['key' => $minNode->key, 'value' => $minNode->value];
    }

    /**
     * 获取最大值
     */
    public function max()
    {
        if ($this->root === null) {
            return null;
        }
        $current = $this->root;
        while ($current->right !== null) {
            $current = $current->right;
        }
        return ['key' => $current->key, 'value' => $current->value];
    }

    public function getSize(): int
    {
        return $this->size;
    }

    public function isEmpty(): bool
    {
        return $this->size === 0;
    }
}

/**
 * 红黑树节点
 */
class RBNode
{
    public $key;
    public $value;
    public bool $color; // true = RED, false = BLACK
    public ?RBNode $left;
    public ?RBNode $right;
    public ?RBNode $parent;

    public function __construct($key, $value, bool $color)
    {
        $this->key = $key;
        $this->value = $value;
        $this->color = $color;
        $this->left = null;
        $this->right = null;
        $this->parent = null;
    }
}
