<?php

require_once __DIR__ . '/../vendor/autoload.php';

use DataStructures\Hash\HashTable;
use DataStructures\Hash\ConsistentHash;
use DataStructures\Hash\BloomFilter;
use DataStructures\Hash\CountingBloomFilter;
use DataStructures\Advanced\Trie;
use DataStructures\Advanced\CompressedTrie;
use DataStructures\Advanced\LRUCache;
use DataStructures\Advanced\LFUCache;
use DataStructures\Advanced\TTLCache;
use DataStructures\Advanced\SkipList;

/**
 * 哈希表和高级数据结构使用示例
 */

echo "=== 哈希表和高级数据结构示例 ===\n\n";

// 1. HashTable 示例
echo "1. HashTable 示例:\n";
$hashTable = new HashTable();

// 添加键值对
$hashTable->put("name", "张三");
$hashTable->put("age", 25);
$hashTable->put("city", "北京");
$hashTable->put("job", "工程师");

echo "哈希表大小: {$hashTable->size()}\n";
echo "负载因子: " . number_format($hashTable->getLoadFactor(), 2) . "\n";
echo "容量: {$hashTable->getCapacity()}\n";
echo "获取name: {$hashTable->get('name')}\n";
echo "获取age: {$hashTable->get('age')}\n";
echo "是否包含city: " . ($hashTable->containsKey('city') ? "是" : "否") . "\n";

// 遍历所有键值对
echo "所有键值对:\n";
foreach ($hashTable->entries() as $entry) {
    echo "  {$entry['key']} => {$entry['value']}\n";
}

// 删除键
$hashTable->remove('job');
echo "删除job后大小: {$hashTable->size()}\n";
echo "\n";

// 2. ConsistentHash 示例
echo "2. ConsistentHash 示例:\n";
$consistentHash = new ConsistentHash();

// 添加服务器节点
$servers = ['server1', 'server2', 'server3'];
foreach ($servers as $server) {
    $consistentHash->addNode($server);
}

echo "服务器节点: " . implode(", ", $servers) . "\n";

// 测试数据分布
$testKeys = ['user1', 'user2', 'user3', 'user4', 'user5', 'user6'];
echo "数据分布:\n";
foreach ($testKeys as $key) {
    $server = $consistentHash->getNode($key);
    echo "  {$key} -> {$server}\n";
}

// 添加新服务器
echo "\n添加新服务器 server4:\n";
$consistentHash->addNode('server4');
foreach ($testKeys as $key) {
    $server = $consistentHash->getNode($key);
    echo "  {$key} -> {$server}\n";
}
echo "\n";

// 3. BloomFilter 示例
echo "3. BloomFilter 示例:\n";
$bloomFilter = new BloomFilter(1000, 0.01); // 预期1000个元素，1%误报率

echo "布隆过滤器参数:\n";
echo "  位数组大小: {$bloomFilter->getSize()}\n";
echo "  哈希函数数量: {$bloomFilter->getHashCount()}\n";
echo "  预期误报率: 1%\n";

// 添加元素
$emails = [
    'user1@example.com',
    'user2@example.com', 
    'user3@example.com',
    'admin@example.com',
    'test@example.com'
];

foreach ($emails as $email) {
    $bloomFilter->add($email);
}

echo "\n已添加邮箱: " . implode(", ", $emails) . "\n";
echo "布隆过滤器中元素数量: {$bloomFilter->getElementCount()}\n";

// 测试包含性
$testEmails = [
    'user1@example.com',    // 应该存在
    'user4@example.com',    // 不存在
    'admin@example.com',    // 应该存在
    'spam@example.com'      // 不存在
];

echo "\n包含性测试:\n";
foreach ($testEmails as $email) {
    $contains = $bloomFilter->contains($email);
    echo "  {$email}: " . ($contains ? "可能存在" : "肯定不存在") . "\n";
}
echo "\n";

// 4. Trie 示例
echo "4. Trie (前缀树) 示例:\n";
$trie = new Trie();

// 插入单词
$words = ['apple', 'app', 'application', 'apply', 'banana', 'band', 'bandana'];
foreach ($words as $word) {
    $trie->insert($word);
}

echo "插入单词: " . implode(", ", $words) . "\n";
echo "Trie大小: {$trie->size()}\n";

// 搜索单词
$searchWords = ['app', 'apple', 'application', 'appl', 'orange'];
echo "\n单词搜索:\n";
foreach ($searchWords as $word) {
    $exists = $trie->search($word);
    echo "  {$word}: " . ($exists ? "存在" : "不存在") . "\n";
}

// 前缀搜索
echo "\n前缀搜索:\n";
$prefixes = ['app', 'ban', 'xyz'];
foreach ($prefixes as $prefix) {
    $hasPrefix = $trie->startsWith($prefix);
    echo "  前缀'{$prefix}': " . ($hasPrefix ? "存在" : "不存在") . "\n";
    
    if ($hasPrefix) {
        $wordsWithPrefix = $trie->getWordsWithPrefix($prefix);
        echo "    包含此前缀的单词: " . implode(", ", $wordsWithPrefix) . "\n";
    }
}

// 最长公共前缀
$lcp = $trie->getLongestCommonPrefix();
echo "\n最长公共前缀: '{$lcp}'\n";
echo "\n";

// 5. LRUCache 示例
echo "5. LRUCache 示例:\n";
$lruCache = new LRUCache(3); // 容量为3

echo "LRU缓存容量: {$lruCache->capacity()}\n";

// 添加数据
$lruCache->put('key1', 'value1');
$lruCache->put('key2', 'value2');
$lruCache->put('key3', 'value3');

echo "添加3个元素后:\n";
echo "  缓存大小: {$lruCache->size()}\n";
echo "  最近使用的键: " . implode(", ", $lruCache->getMostRecentKeys(3)) . "\n";

// 访问key1
$value = $lruCache->get('key1');
echo "\n访问key1: {$value}\n";
echo "访问后最近使用的键: " . implode(", ", $lruCache->getMostRecentKeys(3)) . "\n";

// 添加新元素，触发LRU淘汰
$lruCache->put('key4', 'value4');
echo "\n添加key4后 (触发LRU淘汰):\n";
echo "  缓存大小: {$lruCache->size()}\n";
echo "  当前键: " . implode(", ", $lruCache->keys()) . "\n";
echo "  最近使用的键: " . implode(", ", $lruCache->getMostRecentKeys(3)) . "\n";

// 缓存统计
$stats = $lruCache->getStatistics();
echo "\n缓存统计:\n";
echo "  命中次数: {$stats['hits']}\n";
echo "  未命中次数: {$stats['misses']}\n";
echo "  命中率: " . number_format($lruCache->getHitRate() * 100, 2) . "%\n";
echo "\n";

// 6. SkipList 示例
echo "6. SkipList 示例:\n";
$skipList = new SkipList(16, 0.5);

// 插入数据
$values = [3, 6, 7, 9, 12, 19, 17, 26, 21, 25];
foreach ($values as $value) {
    $skipList->insert($value);
}

echo "插入值: " . implode(", ", $values) . "\n";
echo "跳表大小: {$skipList->size()}\n";

// 搜索
$searchValues = [7, 15, 21, 30];
echo "\n搜索测试:\n";
foreach ($searchValues as $value) {
    $found = $skipList->search($value);
    echo "  搜索{$value}: " . ($found ? "找到" : "未找到") . "\n";
}

// 范围查询
echo "\n范围查询 [10, 20]:\n";
$rangeResult = $skipList->rangeQuery(10, 20);
echo "  结果: " . implode(", ", $rangeResult) . "\n";

// 查找最小值和最大值
$minResult = $skipList->getMin();
$maxResult = $skipList->getMax();
echo "\n最小值: " . ($minResult ? $minResult['key'] : 'null') . "\n";
echo "最大值: " . ($maxResult ? $maxResult['key'] : 'null') . "\n";

// 删除元素
echo "\n删除元素9\n";
$skipList->delete(9);
echo "删除后大小: {$skipList->size()}\n";
echo "删除后范围查询 [5, 15]: " . implode(", ", $skipList->rangeQuery(5, 15)) . "\n";
echo "\n";

// 7. 实际应用场景示例
echo "7. 实际应用场景示例:\n";

// 网站访问统计（布隆过滤器）
echo "网站访问统计 (布隆过滤器去重):\n";
$visitFilter = new BloomFilter(10000, 0.01);
$uniqueVisitors = 0;

// 模拟访问日志
$accessLogs = [
    '192.168.1.1', '192.168.1.2', '192.168.1.1', // 重复访问
    '10.0.0.1', '10.0.0.2', '192.168.1.2',        // 重复访问
    '172.16.0.1', '172.16.0.2'
];

foreach ($accessLogs as $ip) {
    if (!$visitFilter->contains($ip)) {
        $visitFilter->add($ip);
        $uniqueVisitors++;
        echo "  新访客: {$ip}\n";
    } else {
        echo "  重复访客: {$ip}\n";
    }
}
echo "估计独立访客数: {$uniqueVisitors}\n\n";

// 搜索引擎自动补全（Trie）
echo "搜索引擎自动补全 (Trie):\n";
$searchTrie = new Trie();

// 添加搜索关键词
$keywords = [
    'javascript', 'java', 'python', 'php', 'programming',
    'algorithm', 'data structure', 'machine learning', 'artificial intelligence'
];

foreach ($keywords as $keyword) {
    $searchTrie->insert($keyword);
}

// 模拟用户输入
$userInputs = ['java', 'prog', 'data', 'art'];
foreach ($userInputs as $input) {
    echo "用户输入 '{$input}' 的建议:\n";
    $suggestions = $searchTrie->getWordsWithPrefix($input);
    if (!empty($suggestions)) {
        foreach ($suggestions as $suggestion) {
            echo "  - {$suggestion}\n";
        }
    } else {
        echo "  无建议\n";
    }
    echo "\n";
}

// 数据库查询缓存（LRU）
echo "数据库查询缓存 (LRU):\n";
$queryCache = new LRUCache(5);

// 模拟数据库查询
function simulateDbQuery($sql) {
    // 模拟数据库查询延迟
    usleep(1000); // 1ms
    return "Result for: " . substr($sql, 0, 30) . "...";
}

$queries = [
    'SELECT * FROM users WHERE id = 1',
    'SELECT * FROM products WHERE category = "electronics"',
    'SELECT * FROM orders WHERE date > "2023-01-01"',
    'SELECT * FROM users WHERE id = 1', // 重复查询
    'SELECT * FROM categories',
    'SELECT * FROM products WHERE category = "electronics"', // 重复查询
];

foreach ($queries as $i => $sql) {
    $cacheKey = md5($sql);
    
    $startTime = microtime(true);
    if ($queryCache->contains($cacheKey)) {
        $result = $queryCache->get($cacheKey);
        $source = "缓存";
    } else {
        $result = simulateDbQuery($sql);
        $queryCache->put($cacheKey, $result);
        $source = "数据库";
    }
    $endTime = microtime(true);
    
    $queryTime = round(($endTime - $startTime) * 1000, 2);
    echo "查询" . ($i + 1) . " (来源: {$source}, 耗时: {$queryTime}ms)\n";
    echo "  SQL: " . substr($sql, 0, 40) . "...\n";
    echo "  结果: {$result}\n\n";
}

$cacheStats = $queryCache->getStatistics();
echo "缓存统计: 命中{$cacheStats['hits']}次, 未命中{$cacheStats['misses']}次, 命中率" . number_format($queryCache->getHitRate() * 100, 1) . "%\n\n";

echo "=== 示例结束 ===\n";