<?php

namespace DataStructures\Tree;

/**
 * BinaryTree - 二叉树数据结构实现
 * 
 * 思路：
 * 1. 每个节点最多有两个子节点（左子节点和右子节点）
 * 2. 使用递归方式实现各种操作
 * 3. 支持前序、中序、后序和层序遍历
 * 4. 提供基本的树操作方法
 * 
 * 作用：
 * - 层次化数据存储
 * - 快速搜索和排序
 * - 表达式树的构建
 * - 决策树的实现
 * 
 * 业务场景：
 * 1. 文件系统：目录结构的表示
 * 2. 组织架构：公司层级结构管理
 * 3. 决策系统：决策树算法
 * 4. 表达式解析：数学表达式的语法树
 * 5. 游戏开发：游戏场景的空间分割
 * 6. 数据库索引：B树索引的基础
 * 7. 编译器：抽象语法树(AST)
 * 8. 人工智能：搜索树和博弈树
 * 9. 网络路由：路由表的树形结构
 * 10. 分类系统：商品分类、知识分类
 */

/**
 * 二叉树节点类
 */
class TreeNode
{
    public $data;
    public ?TreeNode $left;
    public ?TreeNode $right;
    public ?TreeNode $parent;
    
    public function __construct($data)
    {
        $this->data = $data;
        $this->left = null;
        $this->right = null;
        $this->parent = null;
    }
    
    /**
     * 检查是否为叶子节点
     */
    public function isLeaf(): bool
    {
        return $this->left === null && $this->right === null;
    }
    
    /**
     * 检查是否有左子节点
     */
    public function hasLeft(): bool
    {
        return $this->left !== null;
    }
    
    /**
     * 检查是否有右子节点
     */
    public function hasRight(): bool
    {
        return $this->right !== null;
    }
    
    /**
     * 获取子节点数量
     */
    public function getChildrenCount(): int
    {
        $count = 0;
        if ($this->left !== null) $count++;
        if ($this->right !== null) $count++;
        return $count;
    }
}

class BinaryTree
{
    protected ?TreeNode $root;
    protected int $size;
    
    public function __construct()
    {
        $this->root = null;
        $this->size = 0;
    }
    
    /**
     * 获取根节点
     */
    public function getRoot(): ?TreeNode
    {
        return $this->root;
    }
    
    /**
     * 设置根节点
     */
    public function setRoot(?TreeNode $root): void
    {
        $this->root = $root;
        if ($root !== null) {
            $root->parent = null;
        }
    }
    
    /**
     * 检查树是否为空
     */
    public function isEmpty(): bool
    {
        return $this->root === null;
    }
    
    /**
     * 获取树的大小
     */
    public function size(): int
    {
        return $this->calculateSize($this->root);
    }
    
    /**
     * 计算子树的大小
     */
    private function calculateSize(?TreeNode $node): int
    {
        if ($node === null) {
            return 0;
        }
        return 1 + $this->calculateSize($node->left) + $this->calculateSize($node->right);
    }
    
    /**
     * 获取树的高度
     * 时间复杂度：O(n)
     */
    public function height(): int
    {
        return $this->calculateHeight($this->root);
    }
    
    /**
     * 计算子树的高度
     */
    private function calculateHeight(?TreeNode $node): int
    {
        if ($node === null) {
            return -1; // 空树高度为-1，单节点树高度为0
        }
        
        $leftHeight = $this->calculateHeight($node->left);
        $rightHeight = $this->calculateHeight($node->right);
        
        return 1 + max($leftHeight, $rightHeight);
    }
    
    /**
     * 前序遍历（根-左-右）
     * 时间复杂度：O(n)
     */
    public function preorderTraversal(): array
    {
        $result = [];
        $this->preorderHelper($this->root, $result);
        return $result;
    }
    
    private function preorderHelper(?TreeNode $node, array &$result): void
    {
        if ($node !== null) {
            $result[] = $node->data;
            $this->preorderHelper($node->left, $result);
            $this->preorderHelper($node->right, $result);
        }
    }
    
    /**
     * 中序遍历（左-根-右）
     * 时间复杂度：O(n)
     */
    public function inorderTraversal(): array
    {
        $result = [];
        $this->inorderHelper($this->root, $result);
        return $result;
    }
    
    private function inorderHelper(?TreeNode $node, array &$result): void
    {
        if ($node !== null) {
            $this->inorderHelper($node->left, $result);
            $result[] = $node->data;
            $this->inorderHelper($node->right, $result);
        }
    }
    
    /**
     * 后序遍历（左-右-根）
     * 时间复杂度：O(n)
     */
    public function postorderTraversal(): array
    {
        $result = [];
        $this->postorderHelper($this->root, $result);
        return $result;
    }
    
    private function postorderHelper(?TreeNode $node, array &$result): void
    {
        if ($node !== null) {
            $this->postorderHelper($node->left, $result);
            $this->postorderHelper($node->right, $result);
            $result[] = $node->data;
        }
    }
    
    /**
     * 层序遍历（广度优先）
     * 时间复杂度：O(n)
     */
    public function levelOrderTraversal(): array
    {
        if ($this->root === null) {
            return [];
        }
        
        $result = [];
        $queue = [$this->root];
        
        while (!empty($queue)) {
            $node = array_shift($queue);
            $result[] = $node->data;
            
            if ($node->left !== null) {
                $queue[] = $node->left;
            }
            if ($node->right !== null) {
                $queue[] = $node->right;
            }
        }
        
        return $result;
    }
    
    /**
     * 按层返回遍历结果
     */
    public function levelOrderByLevels(): array
    {
        if ($this->root === null) {
            return [];
        }
        
        $result = [];
        $queue = [$this->root];
        
        while (!empty($queue)) {
            $levelSize = count($queue);
            $currentLevel = [];
            
            for ($i = 0; $i < $levelSize; $i++) {
                $node = array_shift($queue);
                $currentLevel[] = $node->data;
                
                if ($node->left !== null) {
                    $queue[] = $node->left;
                }
                if ($node->right !== null) {
                    $queue[] = $node->right;
                }
            }
            
            $result[] = $currentLevel;
        }
        
        return $result;
    }
    
    /**
     * 搜索节点
     * 时间复杂度：O(n)
     */
    public function search($data): ?TreeNode
    {
        return $this->searchHelper($this->root, $data);
    }
    
    private function searchHelper(?TreeNode $node, $data): ?TreeNode
    {
        if ($node === null || $node->data === $data) {
            return $node;
        }
        
        $leftResult = $this->searchHelper($node->left, $data);
        if ($leftResult !== null) {
            return $leftResult;
        }
        
        return $this->searchHelper($node->right, $data);
    }
    
    /**
     * 检查是否包含指定数据
     */
    public function contains($data): bool
    {
        return $this->search($data) !== null;
    }
    
    /**
     * 获取所有叶子节点
     */
    public function getLeaves(): array
    {
        $leaves = [];
        $this->getLeavesHelper($this->root, $leaves);
        return $leaves;
    }
    
    private function getLeavesHelper(?TreeNode $node, array &$leaves): void
    {
        if ($node !== null) {
            if ($node->isLeaf()) {
                $leaves[] = $node->data;
            } else {
                $this->getLeavesHelper($node->left, $leaves);
                $this->getLeavesHelper($node->right, $leaves);
            }
        }
    }
    
    /**
     * 检查两棵树是否相等
     */
    public function equals(BinaryTree $other): bool
    {
        return $this->nodesEqual($this->root, $other->root);
    }
    
    private function nodesEqual(?TreeNode $node1, ?TreeNode $node2): bool
    {
        if ($node1 === null && $node2 === null) {
            return true;
        }
        
        if ($node1 === null || $node2 === null) {
            return false;
        }
        
        return $node1->data === $node2->data &&
               $this->nodesEqual($node1->left, $node2->left) &&
               $this->nodesEqual($node1->right, $node2->right);
    }
    
    /**
     * 镜像翻转树
     */
    public function mirror(): void
    {
        $this->mirrorHelper($this->root);
    }
    
    private function mirrorHelper(?TreeNode $node): void
    {
        if ($node !== null) {
            // 交换左右子树
            $temp = $node->left;
            $node->left = $node->right;
            $node->right = $temp;
            
            // 递归处理子树
            $this->mirrorHelper($node->left);
            $this->mirrorHelper($node->right);
        }
    }
    
    /**
     * 获取树的直径（最长路径）
     */
    public function diameter(): int
    {
        $maxDiameter = 0;
        $this->diameterHelper($this->root, $maxDiameter);
        return $maxDiameter;
    }
    
    private function diameterHelper(?TreeNode $node, int &$maxDiameter): int
    {
        if ($node === null) {
            return 0;
        }
        
        $leftHeight = $this->diameterHelper($node->left, $maxDiameter);
        $rightHeight = $this->diameterHelper($node->right, $maxDiameter);
        
        // 更新最大直径
        $maxDiameter = max($maxDiameter, $leftHeight + $rightHeight);
        
        return 1 + max($leftHeight, $rightHeight);
    }
    
    /**
     * 从数组构建完全二叉树
     */
    public static function fromArray(array $arr): BinaryTree
    {
        $tree = new self();
        if (empty($arr)) {
            return $tree;
        }
        
        $tree->root = new TreeNode($arr[0]);
        $queue = [$tree->root];
        $i = 1;
        
        while (!empty($queue) && $i < count($arr)) {
            $node = array_shift($queue);
            
            // 添加左子节点
            if ($i < count($arr) && $arr[$i] !== null) {
                $node->left = new TreeNode($arr[$i]);
                $node->left->parent = $node;
                $queue[] = $node->left;
            }
            $i++;
            
            // 添加右子节点
            if ($i < count($arr) && $arr[$i] !== null) {
                $node->right = new TreeNode($arr[$i]);
                $node->right->parent = $node;
                $queue[] = $node->right;
            }
            $i++;
        }
        
        return $tree;
    }
    
    /**
     * 将树转换为数组表示
     */
    public function toArray(): array
    {
        if ($this->root === null) {
            return [];
        }
        
        $result = [];
        $queue = [$this->root];
        
        while (!empty($queue)) {
            $node = array_shift($queue);
            
            if ($node !== null) {
                $result[] = $node->data;
                $queue[] = $node->left;
                $queue[] = $node->right;
            } else {
                $result[] = null;
            }
        }
        
        // 移除末尾的null值
        while (!empty($result) && end($result) === null) {
            array_pop($result);
        }
        
        return $result;
    }
    
    /**
     * 清空树
     */
    public function clear(): void
    {
        $this->root = null;
        $this->size = 0;
    }
    
    /**
     * 打印树的结构（用于调试）
     */
    public function printTree(): string
    {
        if ($this->root === null) {
            return "Empty tree";
        }
        
        return $this->printHelper($this->root, "", true);
    }
    
    private function printHelper(?TreeNode $node, string $prefix, bool $isLast): string
    {
        if ($node === null) {
            return "";
        }
        
        $result = $prefix . ($isLast ? "└── " : "├── ") . $node->data . "\n";
        
        $children = [];
        if ($node->left !== null) $children[] = $node->left;
        if ($node->right !== null) $children[] = $node->right;
        
        for ($i = 0; $i < count($children); $i++) {
            $isLastChild = ($i === count($children) - 1);
            $newPrefix = $prefix . ($isLast ? "    " : "│   ");
            $result .= $this->printHelper($children[$i], $newPrefix, $isLastChild);
        }
        
        return $result;
    }
}