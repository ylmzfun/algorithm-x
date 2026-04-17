<?php

namespace DataStructures\Tree;

require_once 'BinaryTree.php';

/**
 * BinarySearchTree - 二叉搜索树数据结构实现
 * 
 * 思路：
 * 1. 继承自二叉树，增加搜索特性
 * 2. 左子树所有节点值 < 根节点值 < 右子树所有节点值
 * 3. 支持高效的搜索、插入和删除操作
 * 4. 中序遍历得到有序序列
 * 
 * 作用：
 * - 提供O(log n)的搜索、插入、删除操作（平均情况）
 * - 维护数据的有序性
 * - 支持范围查询
 * - 动态维护排序数据
 * 
 * 业务场景：
 * 1. 数据库索引：B+树索引的基础结构
 * 2. 搜索引擎：关键词索引和排序
 * 3. 文件系统：目录结构的快速查找
 * 4. 游戏开发：排行榜系统，快速查找排名
 * 5. 电商系统：商品价格区间查询
 * 6. 用户管理：按ID快速查找用户
 * 7. 缓存系统：LRU缓存的有序维护
 * 8. 编译器：符号表的实现
 * 9. 网络路由：路由表的快速查找
 * 10. 数据分析：动态维护排序数据集
 */
class BinarySearchTree extends BinaryTree
{
    private $comparator;
    
    public function __construct(?callable $comparator = null)
    {
        parent::__construct();
        $this->comparator = $comparator ?: function($a, $b) {
            return $a <=> $b;
        };
    }
    
    /**
     * 插入节点
     * 时间复杂度：平均O(log n)，最坏O(n)
     */
    public function insert($data): void
    {
        $this->root = $this->insertHelper($this->root, $data);
    }
    
    private function insertHelper(?TreeNode $node, $data): TreeNode
    {
        if ($node === null) {
            return new TreeNode($data);
        }
        
        $cmp = call_user_func($this->comparator, $data, $node->data);
        
        if ($cmp < 0) {
            $node->left = $this->insertHelper($node->left, $data);
            if ($node->left !== null) {
                $node->left->parent = $node;
            }
        } elseif ($cmp > 0) {
            $node->right = $this->insertHelper($node->right, $data);
            if ($node->right !== null) {
                $node->right->parent = $node;
            }
        }
        // 如果相等，不插入重复值
        
        return $node;
    }
    
    /**
     * 搜索节点
     * 时间复杂度：平均O(log n)，最坏O(n)
     */
    public function search($data): ?TreeNode
    {
        return $this->searchHelper($this->root, $data);
    }
    
    private function searchHelper(?TreeNode $node, $data): ?TreeNode
    {
        if ($node === null) {
            return null;
        }
        
        $cmp = call_user_func($this->comparator, $data, $node->data);
        
        if ($cmp === 0) {
            return $node;
        } elseif ($cmp < 0) {
            return $this->searchHelper($node->left, $data);
        } else {
            return $this->searchHelper($node->right, $data);
        }
    }
    
    /**
     * 删除节点
     * 时间复杂度：平均O(log n)，最坏O(n)
     */
    public function delete($data): bool
    {
        $originalRoot = $this->root;
        $this->root = $this->deleteHelper($this->root, $data);
        return $originalRoot !== $this->root || $this->contains($data) === false;
    }
    
    private function deleteHelper(?TreeNode $node, $data): ?TreeNode
    {
        if ($node === null) {
            return null;
        }
        
        $cmp = call_user_func($this->comparator, $data, $node->data);
        
        if ($cmp < 0) {
            $node->left = $this->deleteHelper($node->left, $data);
            if ($node->left !== null) {
                $node->left->parent = $node;
            }
        } elseif ($cmp > 0) {
            $node->right = $this->deleteHelper($node->right, $data);
            if ($node->right !== null) {
                $node->right->parent = $node;
            }
        } else {
            // 找到要删除的节点
            if ($node->left === null) {
                return $node->right;
            } elseif ($node->right === null) {
                return $node->left;
            } else {
                // 有两个子节点，找到右子树的最小节点
                $successor = $this->findMin($node->right);
                $node->data = $successor->data;
                $node->right = $this->deleteHelper($node->right, $successor->data);
                if ($node->right !== null) {
                    $node->right->parent = $node;
                }
            }
        }
        
        return $node;
    }
    
    /**
     * 查找最小值节点
     * 时间复杂度：O(log n)
     */
    public function findMin(?TreeNode $node = null): ?TreeNode
    {
        if ($node === null) {
            $node = $this->root;
        }
        
        if ($node === null) {
            return null;
        }
        
        while ($node->left !== null) {
            $node = $node->left;
        }
        
        return $node;
    }
    
    /**
     * 查找最大值节点
     * 时间复杂度：O(log n)
     */
    public function findMax(?TreeNode $node = null): ?TreeNode
    {
        if ($node === null) {
            $node = $this->root;
        }
        
        if ($node === null) {
            return null;
        }
        
        while ($node->right !== null) {
            $node = $node->right;
        }
        
        return $node;
    }
    
    /**
     * 查找前驱节点（中序遍历中的前一个节点）
     */
    public function findPredecessor(TreeNode $node): ?TreeNode
    {
        if ($node->left !== null) {
            return $this->findMax($node->left);
        }
        
        $parent = $node->parent;
        while ($parent !== null && $node === $parent->left) {
            $node = $parent;
            $parent = $parent->parent;
        }
        
        return $parent;
    }
    
    /**
     * 查找后继节点（中序遍历中的后一个节点）
     */
    public function findSuccessor(TreeNode $node): ?TreeNode
    {
        if ($node->right !== null) {
            return $this->findMin($node->right);
        }
        
        $parent = $node->parent;
        while ($parent !== null && $node === $parent->right) {
            $node = $parent;
            $parent = $parent->parent;
        }
        
        return $parent;
    }
    
    /**
     * 范围查询：查找在[min, max]范围内的所有值
     * 时间复杂度：O(log n + k)，k为结果数量
     */
    public function rangeQuery($min, $max): array
    {
        $result = [];
        $this->rangeQueryHelper($this->root, $min, $max, $result);
        return $result;
    }
    
    private function rangeQueryHelper(?TreeNode $node, $min, $max, array &$result): void
    {
        if ($node === null) {
            return;
        }
        
        $cmpMin = call_user_func($this->comparator, $node->data, $min);
        $cmpMax = call_user_func($this->comparator, $node->data, $max);
        
        // 如果当前节点值大于min，搜索左子树
        if ($cmpMin > 0) {
            $this->rangeQueryHelper($node->left, $min, $max, $result);
        }
        
        // 如果当前节点在范围内，添加到结果
        if ($cmpMin >= 0 && $cmpMax <= 0) {
            $result[] = $node->data;
        }
        
        // 如果当前节点值小于max，搜索右子树
        if ($cmpMax < 0) {
            $this->rangeQueryHelper($node->right, $min, $max, $result);
        }
    }
    
    /**
     * 查找第k小的元素（1-indexed）
     * 时间复杂度：O(log n + k)
     */
    public function kthSmallest(int $k): mixed
    {
        $count = 0;
        return $this->kthSmallestHelper($this->root, $k, $count);
    }
    
    private function kthSmallestHelper(?TreeNode $node, int $k, int &$count): mixed
    {
        if ($node === null) {
            return null;
        }
        
        // 搜索左子树
        $leftResult = $this->kthSmallestHelper($node->left, $k, $count);
        if ($leftResult !== null) {
            return $leftResult;
        }
        
        // 访问当前节点
        $count++;
        if ($count === $k) {
            return $node->data;
        }
        
        // 搜索右子树
        return $this->kthSmallestHelper($node->right, $k, $count);
    }
    
    /**
     * 验证是否为有效的二叉搜索树
     */
    public function isValidBST(): bool
    {
        return $this->isValidBSTHelper($this->root, null, null);
    }
    
    private function isValidBSTHelper(?TreeNode $node, $min, $max): bool
    {
        if ($node === null) {
            return true;
        }
        
        if ($min !== null && call_user_func($this->comparator, $node->data, $min) <= 0) {
            return false;
        }
        
        if ($max !== null && call_user_func($this->comparator, $node->data, $max) >= 0) {
            return false;
        }
        
        return $this->isValidBSTHelper($node->left, $min, $node->data) &&
               $this->isValidBSTHelper($node->right, $node->data, $max);
    }
    
    /**
     * 获取有序数组（中序遍历结果）
     */
    public function getSortedArray(): array
    {
        return $this->inorderTraversal();
    }
    
    /**
     * 从有序数组构建平衡BST
     */
    public static function fromSortedArray(array $array, ?callable $comparator = null): self
    {
        $bst = new self($comparator);
        $bst->root = $bst->buildFromSortedArray($array, 0, count($array) - 1);
        return $bst;
    }
    
    private function buildFromSortedArray(array $arr, int $start, int $end): ?TreeNode
    {
        if ($start > $end) {
            return null;
        }
        
        $mid = intval(($start + $end) / 2);
        $node = new TreeNode($arr[$mid]);
        
        $node->left = $this->buildFromSortedArray($arr, $start, $mid - 1);
        if ($node->left !== null) {
            $node->left->parent = $node;
        }
        
        $node->right = $this->buildFromSortedArray($arr, $mid + 1, $end);
        if ($node->right !== null) {
            $node->right->parent = $node;
        }
        
        return $node;
    }
    
    /**
     * 计算树的平衡因子
     */
    public function getBalanceFactor(?TreeNode $node = null): int
    {
        if ($node === null) {
            $node = $this->root;
        }
        
        if ($node === null) {
            return 0;
        }
        
        $leftHeight = $this->getSubtreeHeight($node->left);
        $rightHeight = $this->getSubtreeHeight($node->right);
        
        return $leftHeight - $rightHeight;
    }
    
    /**
     * 计算子树的高度
     */
    private function getSubtreeHeight(?TreeNode $node): int
    {
        if ($node === null) {
            return -1;
        }
        
        $leftHeight = $this->getSubtreeHeight($node->left);
        $rightHeight = $this->getSubtreeHeight($node->right);
        
        return 1 + max($leftHeight, $rightHeight);
    }
    
    /**
     * 检查树是否平衡
     */
    public function isBalanced(): bool
    {
        return $this->isBalancedHelper($this->root) !== -1;
    }
    
    private function isBalancedHelper(?TreeNode $node): int
    {
        if ($node === null) {
            return 0;
        }
        
        $leftHeight = $this->isBalancedHelper($node->left);
        if ($leftHeight === -1) {
            return -1;
        }
        
        $rightHeight = $this->isBalancedHelper($node->right);
        if ($rightHeight === -1) {
            return -1;
        }
        
        if (abs($leftHeight - $rightHeight) > 1) {
            return -1;
        }
        
        return 1 + max($leftHeight, $rightHeight);
    }
    
    /**
     * 批量插入
     */
    public function insertAll(array $values): void
    {
        foreach ($values as $value) {
            $this->insert($value);
        }
    }
    
    /**
     * 获取树的统计信息
     */
    public function getStatistics(): array
    {
        return [
            'size' => $this->size(),
            'height' => $this->height(),
            'is_balanced' => $this->isBalanced(),
            'is_valid_bst' => $this->isValidBST(),
            'min_value' => $this->findMin()?->data,
            'max_value' => $this->findMax()?->data,
        ];
    }
}