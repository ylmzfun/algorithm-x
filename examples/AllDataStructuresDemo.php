<?php

require_once __DIR__ . '/../vendor/autoload.php';

/**
 * PHP 数据结构完整演示
 * 
 * 这个文件演示了本项目中实现的所有数据结构的基本用法
 * 包括：线性结构、树结构、图结构、哈希结构和高级结构
 */

echo "\n" . str_repeat("=", 60) . "\n";
echo "           PHP 数据结构完整演示\n";
echo str_repeat("=", 60) . "\n\n";

// 引入所有数据结构类
use DataStructures\Linear\{ArrayList, LinkedList, Stack, Queue, PriorityQueue, Deque};
use DataStructures\Tree\{BinaryTree, TreeNode, BinarySearchTree, Heap, MinHeap, MaxHeap};
use DataStructures\Graph\{Graph, WeightedGraph};
use DataStructures\Hash\{HashTable, BloomFilter};
use DataStructures\Advanced\{Trie, LRUCache, SkipList};

/**
 * 演示线性数据结构
 */
function demonstrateLinearStructures() {
    echo "📊 线性数据结构演示\n";
    echo str_repeat("-", 40) . "\n";
    
    // ArrayList
    echo "1. ArrayList (动态数组):\n";
    $list = new ArrayList();
    $list->add("苹果");
    $list->add("香蕉");
    $list->add("橙子");
    echo "   内容: [" . implode(", ", $list->toArray()) . "]\n";
    echo "   大小: {$list->size()}\n\n";
    
    // Stack
    echo "2. Stack (栈):\n";
    $stack = new Stack();
    $stack->push("第一个");
    $stack->push("第二个");
    $stack->push("第三个");
    echo "   栈顶: {$stack->peek()}\n";
    echo "   弹出: {$stack->pop()}\n";
    echo "   剩余: {$stack->size()}个元素\n\n";
    
    // Queue
    echo "3. Queue (队列):\n";
    $queue = new Queue();
    $queue->enqueue("客户A");
    $queue->enqueue("客户B");
    $queue->enqueue("客户C");
    echo "   队首: {$queue->front()}\n";
    echo "   服务: {$queue->dequeue()}\n";
    echo "   剩余: {$queue->size()}个客户\n\n";
}

/**
 * 演示树形数据结构
 */
function demonstrateTreeStructures() {
    echo "🌳 树形数据结构演示\n";
    echo str_repeat("-", 40) . "\n";
    
    // Binary Search Tree
    echo "1. Binary Search Tree (二叉搜索树):\n";
    $bst = new BinarySearchTree();
    $values = [50, 30, 70, 20, 40, 60, 80];
    foreach ($values as $val) {
        $bst->insert($val);
    }
    echo "   插入: [" . implode(", ", $values) . "]\n";
    echo "   中序遍历: [" . implode(", ", $bst->inorderTraversal()) . "]\n";
    $minNode = $bst->findMin();
    $maxNode = $bst->findMax();
    echo "   最小值: " . ($minNode ? $minNode->data : 'null') . ", 最大值: " . ($maxNode ? $maxNode->data : 'null') . "\n\n";
    
    // Min Heap
    echo "2. Min Heap (最小堆):\n";
    $heap = new Heap(false); // false表示最小堆
    $heapValues = [15, 10, 20, 8, 25];
    foreach ($heapValues as $val) {
        $heap->insert($val);
    }
    echo "   插入: [" . implode(", ", $heapValues) . "]\n";
    echo "   堆顶(最小): {$heap->peek()}\n";
    echo "   提取最小: {$heap->extract()}\n";
    echo "   新堆顶: {$heap->peek()}\n\n";
}

/**
 * 演示图数据结构
 */
function demonstrateGraphStructures() {
    echo "🕸️  图数据结构演示\n";
    echo str_repeat("-", 40) . "\n";
    
    // 无向图
    echo "1. Graph (无向图):\n";
    $graph = new Graph(false);
    $cities = ["北京", "上海", "广州", "深圳"];
    foreach ($cities as $city) {
        $graph->addVertex($city);
    }
    $graph->addEdge("北京", "上海");
    $graph->addEdge("上海", "广州");
    $graph->addEdge("广州", "深圳");
    
    echo "   城市: [" . implode(", ", $cities) . "]\n";
    echo "   连接: 北京-上海, 上海-广州, 广州-深圳\n";
    echo "   从北京BFS: [" . implode(" → ", $graph->bfs("北京")) . "]\n\n";
    
    // 加权图
    echo "2. Weighted Graph (加权图):\n";
    $wGraph = new WeightedGraph(false);
    $nodes = ["A", "B", "C"];
    foreach ($nodes as $node) {
        $wGraph->addVertex($node);
    }
    $wGraph->addEdge("A", "B", 5);
    $wGraph->addEdge("B", "C", 3);
    $wGraph->addEdge("A", "C", 10);
    
    echo "   节点: [" . implode(", ", $nodes) . "]\n";
    echo "   边权重: A-B(5), B-C(3), A-C(10)\n";
    $distances = $wGraph->dijkstra("A");
    echo "   从A的最短距离: ";
    foreach ($distances as $node => $dist) {
        if ($node !== "A") {
            echo "{$node}({$dist}) ";
        }
    }
    echo "\n\n";
}

/**
 * 演示哈希数据结构
 */
function demonstrateHashStructures() {
    echo "🔗 哈希数据结构演示\n";
    echo str_repeat("-", 40) . "\n";
    
    // Hash Table
    echo "1. Hash Table (哈希表):\n";
    $hashTable = new HashTable();
    $hashTable->put("姓名", "张三");
    $hashTable->put("年龄", "25");
    $hashTable->put("城市", "北京");
    
    echo "   存储: 姓名=张三, 年龄=25, 城市=北京\n";
    echo "   获取姓名: {$hashTable->get('姓名')}\n";
    echo "   大小: {$hashTable->size()}\n\n";
    
    // Bloom Filter
    echo "2. Bloom Filter (布隆过滤器):\n";
    $bloom = new BloomFilter(1000, 0.01);
    $emails = ["user1@test.com", "user2@test.com", "admin@test.com"];
    
    foreach ($emails as $email) {
        $bloom->add($email);
    }
    
    echo "   添加邮箱: [" . implode(", ", $emails) . "]\n";
    echo "   检查user1@test.com: " . ($bloom->contains("user1@test.com") ? "可能存在" : "肯定不存在") . "\n";
    echo "   检查spam@test.com: " . ($bloom->contains("spam@test.com") ? "可能存在" : "肯定不存在") . "\n\n";
}

/**
 * 演示高级数据结构
 */
function demonstrateAdvancedStructures() {
    echo "🚀 高级数据结构演示\n";
    echo str_repeat("-", 40) . "\n";
    
    // Trie
    echo "1. Trie (前缀树):\n";
    $trie = new Trie();
    $words = ["apple", "app", "application", "apply"];
    foreach ($words as $word) {
        $trie->insert($word);
    }
    
    echo "   插入单词: [" . implode(", ", $words) . "]\n";
    echo "   搜索'app': " . ($trie->search("app") ? "存在" : "不存在") . "\n";
    echo "   前缀'app'的单词: [" . implode(", ", $trie->getWordsWithPrefix("app")) . "]\n\n";
    
    // LRU Cache
    echo "2. LRU Cache (最近最少使用缓存):\n";
    $cache = new LRUCache(3);
    $cache->put("key1", "value1");
    $cache->put("key2", "value2");
    $cache->put("key3", "value3");
    
    echo "   缓存容量: 3\n";
    echo "   添加3个键值对\n";
    echo "   当前键: [" . implode(", ", $cache->keys()) . "]\n";
    
    $cache->put("key4", "value4"); // 触发LRU淘汰
    echo "   添加key4后: [" . implode(", ", $cache->keys()) . "] (key1被淘汰)\n\n";
    
    // Skip List
    echo "3. Skip List (跳表):\n";
    $skipList = new SkipList(16);
    $values = [3, 7, 12, 25, 30];
    foreach ($values as $val) {
        $skipList->insert($val, "value_$val");
    }
    
    echo "   插入值: [" . implode(", ", $values) . "]\n";
    echo "   搜索12: " . ($skipList->search(12) ? "找到" : "未找到") . "\n";
    $rangeResult = $skipList->rangeQuery(10, 20);
    $rangeKeys = array_map(function($item) { return is_array($item) ? $item['key'] : $item; }, $rangeResult);
    echo "   范围查询[10,20]: [" . implode(", ", $rangeKeys) . "]\n\n";
}

/**
 * 实际应用场景演示
 */
function demonstrateRealWorldApplications() {
    echo "💼 实际应用场景演示\n";
    echo str_repeat("-", 40) . "\n";
    
    // 1. 表达式求值 (Stack)
    echo "1. 表达式求值 (使用Stack):\n";
    $expression = "((2+3)*4)";
    $isValid = Stack::isValidParentheses($expression);
    echo "   表达式: {$expression}\n";
    echo "   括号匹配: " . ($isValid ? "有效" : "无效") . "\n\n";
    
    // 2. 任务调度 (Priority Queue)
    echo "2. 任务调度 (使用Priority Queue):\n";
    $pq = new PriorityQueue();
    $pq->enqueue("普通任务", 3);
    $pq->enqueue("紧急任务", 1);
    $pq->enqueue("重要任务", 2);
    
    echo "   任务队列: 普通(3), 紧急(1), 重要(2)\n";
    echo "   执行顺序: ";
    while (!$pq->isEmpty()) {
        $task = $pq->dequeue();
        if (is_array($task)) {
            echo "{$task['element']}({$task['priority']}) ";
        } else {
            echo $task . " ";
        }
    }
    echo "\n\n";
    
    // 3. 网页缓存 (LRU Cache)
    echo "3. 网页缓存 (使用LRU Cache):\n";
    $webCache = new LRUCache(3);
    $pages = ["home.html", "about.html", "contact.html", "home.html", "news.html"];
    
    echo "   访问页面顺序: [" . implode(", ", $pages) . "]\n";
    echo "   缓存变化:\n";
    
    foreach ($pages as $page) {
        if ($webCache->contains($page)) {
            $webCache->get($page); // 更新访问时间
            echo "     访问 {$page} (缓存命中)\n";
        } else {
            $webCache->put($page, "content of {$page}");
            echo "     加载 {$page} (缓存未命中)\n";
        }
        echo "     当前缓存: [" . implode(", ", $webCache->keys()) . "]\n";
    }
    echo "\n";
    
    // 4. 搜索建议 (Trie)
    echo "4. 搜索建议 (使用Trie):\n";
    $searchTrie = new Trie();
    $keywords = ["javascript", "java", "python", "php", "programming"];
    
    foreach ($keywords as $keyword) {
        $searchTrie->insert($keyword);
    }
    
    $userInput = "java";
    echo "   用户输入: '{$userInput}'\n";
    echo "   搜索建议: [" . implode(", ", $searchTrie->getWordsWithPrefix($userInput)) . "]\n\n";
}

/**
 * 性能对比演示
 */
function demonstratePerformanceComparison() {
    echo "⚡ 性能对比演示\n";
    echo str_repeat("-", 40) . "\n";
    
    $testSize = 1000;
    
    // ArrayList vs LinkedList 插入性能
    echo "1. ArrayList vs LinkedList 插入性能 ({$testSize}个元素):\n";
    
    // ArrayList
    $start = microtime(true);
    $arrayList = new ArrayList();
    for ($i = 0; $i < $testSize; $i++) {
        $arrayList->add($i);
    }
    $arrayListTime = (microtime(true) - $start) * 1000;
    
    // LinkedList
    $start = microtime(true);
    $linkedList = new LinkedList();
    for ($i = 0; $i < $testSize; $i++) {
        $linkedList->addLast($i);
    }
    $linkedListTime = (microtime(true) - $start) * 1000;
    
    echo "   ArrayList: " . number_format($arrayListTime, 2) . "ms\n";
    echo "   LinkedList: " . number_format($linkedListTime, 2) . "ms\n\n";
    
    // HashTable vs Array 查找性能
    echo "2. HashTable vs PHP Array 查找性能 ({$testSize}次查找):\n";
    
    // 准备数据
    $hashTable = new HashTable();
    $phpArray = [];
    for ($i = 0; $i < $testSize; $i++) {
        $key = "key{$i}";
        $value = "value{$i}";
        $hashTable->put($key, $value);
        $phpArray[$key] = $value;
    }
    
    // HashTable查找
    $start = microtime(true);
    for ($i = 0; $i < $testSize; $i++) {
        $hashTable->get("key{$i}");
    }
    $hashTableTime = (microtime(true) - $start) * 1000;
    
    // PHP Array查找
    $start = microtime(true);
    for ($i = 0; $i < $testSize; $i++) {
        $value = $phpArray["key{$i}"];
    }
    $phpArrayTime = (microtime(true) - $start) * 1000;
    
    echo "   HashTable: " . number_format($hashTableTime, 2) . "ms\n";
    echo "   PHP Array: " . number_format($phpArrayTime, 2) . "ms\n\n";
}

// 执行所有演示
try {
    demonstrateLinearStructures();
    demonstrateTreeStructures();
    demonstrateGraphStructures();
    demonstrateHashStructures();
    demonstrateAdvancedStructures();
    demonstrateRealWorldApplications();
    demonstratePerformanceComparison();
    
    echo str_repeat("=", 60) . "\n";
    echo "           演示完成！\n";
    echo "\n📚 更多详细示例请查看 examples/ 目录下的其他文件\n";
    echo "📖 完整文档请参考 README.md\n";
    echo str_repeat("=", 60) . "\n\n";
    
} catch (Exception $e) {
    echo "❌ 演示过程中发生错误: " . $e->getMessage() . "\n";
    echo "📍 错误位置: " . $e->getFile() . ":" . $e->getLine() . "\n";
}