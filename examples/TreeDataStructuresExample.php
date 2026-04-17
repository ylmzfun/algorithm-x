<?php

require_once __DIR__ . '/../vendor/autoload.php';

use DataStructures\Tree\BinaryTree;
use DataStructures\Tree\TreeNode;
use DataStructures\Tree\BinarySearchTree;
use DataStructures\Tree\Heap;
use DataStructures\Tree\MinHeap;
use DataStructures\Tree\MaxHeap;

/**
 * 树形数据结构使用示例
 */

echo "=== 树形数据结构示例 ===\n\n";

// 1. BinaryTree 示例
echo "1. BinaryTree 示例:\n";
$binaryTree = new BinaryTree();

// 手动构建二叉树
//       1
//      / \
//     2   3
//    / \
//   4   5
$root = new TreeNode(1);
$root->left = new TreeNode(2);
$root->right = new TreeNode(3);
$root->left->left = new TreeNode(4);
$root->left->right = new TreeNode(5);
$binaryTree->setRoot($root);

echo "树的大小: {$binaryTree->size()}\n";
echo "树的高度: {$binaryTree->height()}\n";
echo "前序遍历: " . implode(", ", $binaryTree->preorderTraversal()) . "\n";
echo "中序遍历: " . implode(", ", $binaryTree->inorderTraversal()) . "\n";
echo "后序遍历: " . implode(", ", $binaryTree->postorderTraversal()) . "\n";
echo "层序遍历: " . implode(", ", $binaryTree->levelOrderTraversal()) . "\n";
echo "搜索值3: " . ($binaryTree->search(3) ? "找到" : "未找到") . "\n";
echo "搜索值6: " . ($binaryTree->search(6) ? "找到" : "未找到") . "\n\n";

// 2. BinarySearchTree 示例
echo "2. BinarySearchTree 示例:\n";
$bst = new BinarySearchTree();
$values = [50, 30, 70, 20, 40, 60, 80];

foreach ($values as $value) {
    $bst->insert($value);
}

echo "BST 插入值: " . implode(", ", $values) . "\n";
echo "中序遍历 (有序): " . implode(", ", $bst->inorderTraversal()) . "\n";
echo "最小值: {$bst->findMin()}\n";
echo "最大值: {$bst->findMax()}\n";
echo "搜索40: " . ($bst->search(40) ? "找到" : "未找到") . "\n";
echo "搜索25: " . ($bst->search(25) ? "找到" : "未找到") . "\n";

// 范围查询
$rangeResult = $bst->rangeQuery(35, 65);
echo "范围查询 [35, 65]: " . implode(", ", $rangeResult) . "\n";

// 删除节点
echo "删除节点30\n";
$bst->delete(30);
echo "删除后中序遍历: " . implode(", ", $bst->inorderTraversal()) . "\n";

// 第k小元素
echo "第3小的元素: {$bst->kthSmallest(3)}\n";
echo "BST是否平衡: " . ($bst->isBalanced() ? "是" : "否") . "\n\n";

// 3. MinHeap 示例
echo "3. MinHeap 示例:\n";
$minHeap = new MinHeap();
$heapValues = [10, 4, 15, 20, 25, 30];

foreach ($heapValues as $value) {
    $minHeap->insert($value);
}

echo "MinHeap 插入值: " . implode(", ", $heapValues) . "\n";
echo "堆大小: {$minHeap->size()}\n";
echo "最小值 (堆顶): {$minHeap->peek()}\n";

echo "依次提取最小值: ";
while (!$minHeap->isEmpty()) {
    echo $minHeap->extract() . " ";
}
echo "\n\n";

// 4. MaxHeap 示例
echo "4. MaxHeap 示例:\n";
$maxHeap = new MaxHeap();
$heapValues = [10, 4, 15, 20, 25, 30];

foreach ($heapValues as $value) {
    $maxHeap->insert($value);
}

echo "MaxHeap 插入值: " . implode(", ", $heapValues) . "\n";
echo "堆大小: {$maxHeap->size()}\n";
echo "最大值 (堆顶): {$maxHeap->peek()}\n";

echo "依次提取最大值: ";
while (!$maxHeap->isEmpty()) {
    echo $maxHeap->extract() . " ";
}
echo "\n\n";

// 5. 堆排序示例
echo "5. 堆排序示例:\n";
$unsorted = [64, 34, 25, 12, 22, 11, 90];
echo "原数组: " . implode(", ", $unsorted) . "\n";

$sorted = Heap::heapSort($unsorted);
echo "堆排序后: " . implode(", ", $sorted) . "\n";

// Top K 元素
$topK = Heap::findTopK($unsorted, 3);
echo "前3大元素: " . implode(", ", $topK) . "\n\n";

// 6. 实际应用场景示例
echo "6. 实际应用场景示例:\n";

// 任务调度系统（优先队列）
echo "任务调度系统:\n";
$taskScheduler = new MinHeap();

// 添加任务 (优先级越小越重要)
class Task {
    public string $name;
    public int $priority;
    public string $description;
    
    public function __construct(string $name, int $priority, string $description) {
        $this->name = $name;
        $this->priority = $priority;
        $this->description = $description;
    }
    
    public function __toString(): string {
        return "{$this->name} (优先级: {$this->priority})";
    }
}

$tasks = [
    new Task("紧急修复", 1, "修复生产环境bug"),
    new Task("功能开发", 5, "开发新功能"),
    new Task("代码审查", 3, "审查代码"),
    new Task("安全更新", 2, "安全补丁更新"),
    new Task("文档更新", 8, "更新文档")
];

// 使用自定义比较器
$taskHeap = new class extends MinHeap {
    protected function compare($a, $b): int {
        return $a->priority <=> $b->priority;
    }
};

foreach ($tasks as $task) {
    $taskHeap->insert($task);
}

echo "任务执行顺序:\n";
while (!$taskHeap->isEmpty()) {
    $task = $taskHeap->extract();
    echo "- {$task}\n";
}
echo "\n";

// 文件系统目录结构（树结构）
echo "文件系统目录结构:\n";
$fileSystem = new BinaryTree();

// 构建目录树
$rootDir = new TreeNode("/");
$rootDir->left = new TreeNode("home");
$rootDir->right = new TreeNode("var");
$rootDir->left->left = new TreeNode("user1");
$rootDir->left->right = new TreeNode("user2");
$rootDir->right->left = new TreeNode("log");
$rootDir->right->right = new TreeNode("tmp");

$fileSystem->setRoot($rootDir);

echo "目录结构 (层序遍历): " . implode(" -> ", $fileSystem->levelOrderTraversal()) . "\n";
echo "目录深度: {$fileSystem->height()}\n";
echo "总目录数: {$fileSystem->size()}\n\n";

echo "=== 示例结束 ===\n";