<?php

require_once 'vendor/autoload.php';

use DataStructures\Linear\ArrayList;
use DataStructures\Linear\Stack;
use DataStructures\Tree\BinarySearchTree;
use DataStructures\Hash\HashTable;
use DataStructures\Advanced\LRUCache;

echo "=== PHP 数据结构库基础测试 ===\n\n";

// 测试 ArrayList
echo "1. ArrayList 测试:\n";
$list = new ArrayList();
$list->add(1);
$list->add(2);
$list->add(3);
echo "   添加元素: [1, 2, 3]\n";
echo "   大小: {$list->size()}\n";
echo "   获取索引1: {$list->get(1)}\n";
echo "   包含2: " . ($list->contains(2) ? '是' : '否') . "\n\n";

// 测试 Stack
echo "2. Stack 测试:\n";
$stack = new Stack();
$stack->push('A');
$stack->push('B');
$stack->push('C');
echo "   压入元素: [A, B, C]\n";
echo "   栈顶: {$stack->peek()}\n";
echo "   弹出: {$stack->pop()}\n";
echo "   新栈顶: {$stack->peek()}\n\n";

// 测试 BST
echo "3. BinarySearchTree 测试:\n";
$bst = new BinarySearchTree();
$values = [50, 30, 70, 20, 40];
foreach ($values as $val) {
    $bst->insert($val);
}
echo "   插入元素: [" . implode(', ', $values) . "]\n";
echo "   中序遍历: [" . implode(', ', $bst->inorderTraversal()) . "]\n";
echo "   搜索30: " . ($bst->search(30) ? '找到' : '未找到') . "\n\n";

// 测试 HashTable
echo "4. HashTable 测试:\n";
$hash = new HashTable();
$hash->put('name', 'Alice');
$hash->put('age', 25);
$hash->put('city', 'Beijing');
echo "   添加键值对: name=Alice, age=25, city=Beijing\n";
echo "   获取name: {$hash->get('name')}\n";
echo "   包含age: " . ($hash->containsKey('age') ? '是' : '否') . "\n";
echo "   大小: {$hash->size()}\n\n";

// 测试 LRU Cache
echo "5. LRUCache 测试:\n";
$cache = new LRUCache(3);
$cache->put('key1', 'value1');
$cache->put('key2', 'value2');
$cache->put('key3', 'value3');
echo "   添加3个缓存项\n";
echo "   当前键: [" . implode(', ', $cache->keys()) . "]\n";
$cache->put('key4', 'value4'); // 这会淘汰 key1
echo "   添加key4后: [" . implode(', ', $cache->keys()) . "]\n";
echo "   获取key2: {$cache->get('key2')}\n\n";

echo "=== 所有测试完成！ ===\n";