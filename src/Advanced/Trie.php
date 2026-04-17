<?php

namespace DataStructures\Advanced;

/**
 * Trie - 字典树（前缀树）数据结构实现
 * 
 * 思路：
 * 1. 树形结构，每个节点代表一个字符
 * 2. 从根到叶子的路径表示一个字符串
 * 3. 支持高效的前缀匹配和字符串搜索
 * 4. 节点包含字符、子节点映射、结束标记
 * 
 * 作用：
 * - 高效的字符串存储和检索
 * - 前缀匹配和自动补全
 * - 字符串去重和统计
 * 
 * 业务场景：
 * 1. 搜索引擎：关键词提示、自动补全
 * 2. 输入法：拼音联想、词语预测
 * 3. 路由系统：URL路径匹配
 * 4. 编译器：关键字识别、语法分析
 * 5. 网络安全：恶意域名检测
 * 6. 数据压缩：字符串压缩算法
 * 7. 生物信息学：DNA序列分析
 * 8. 游戏开发：敏感词过滤
 * 9. 文本处理：词频统计、文本挖掘
 * 10. 推荐系统：标签匹配、内容分类
 */

/**
 * Trie节点
 */
class TrieNode
{
    public array $children;      // 子节点映射
    public bool $isEndOfWord;   // 是否为单词结尾
    public int $count;          // 经过此节点的单词数量
    public $value;              // 节点关联的值（可选）
    
    public function __construct()
    {
        $this->children = [];
        $this->isEndOfWord = false;
        $this->count = 0;
        $this->value = null;
    }
}

class Trie
{
    private TrieNode $root;
    private int $size;          // 存储的单词数量
    
    public function __construct()
    {
        $this->root = new TrieNode();
        $this->size = 0;
    }
    
    /**
     * 插入单词
     * 时间复杂度：O(m)，m为单词长度
     */
    public function insert(string $word, $value = null): void
    {
        if (empty($word)) {
            return;
        }
        
        $node = $this->root;
        $len = strlen($word);
        
        for ($i = 0; $i < $len; $i++) {
            $char = $word[$i];
            
            if (!isset($node->children[$char])) {
                $node->children[$char] = new TrieNode();
            }
            
            $node = $node->children[$char];
            $node->count++;
        }
        
        if (!$node->isEndOfWord) {
            $node->isEndOfWord = true;
            $this->size++;
        }
        
        $node->value = $value;
    }
    
    /**
     * 搜索单词
     * 时间复杂度：O(m)，m为单词长度
     */
    public function search(string $word): bool
    {
        $node = $this->findNode($word);
        return $node !== null && $node->isEndOfWord;
    }
    
    /**
     * 检查是否存在以给定前缀开头的单词
     * 时间复杂度：O(m)，m为前缀长度
     */
    public function startsWith(string $prefix): bool
    {
        return $this->findNode($prefix) !== null;
    }
    
    /**
     * 获取单词关联的值
     * 时间复杂度：O(m)
     */
    public function getValue(string $word)
    {
        $node = $this->findNode($word);
        return ($node !== null && $node->isEndOfWord) ? $node->value : null;
    }
    
    /**
     * 删除单词
     * 时间复杂度：O(m)
     */
    public function delete(string $word): bool
    {
        if (empty($word) || !$this->search($word)) {
            return false;
        }
        
        $this->deleteHelper($this->root, $word, 0);
        $this->size--;
        return true;
    }
    
    /**
     * 删除辅助方法
     */
    private function deleteHelper(TrieNode $node, string $word, int $index): bool
    {
        if ($index === strlen($word)) {
            $node->isEndOfWord = false;
            return count($node->children) === 0;
        }
        
        $char = $word[$index];
        $childNode = $node->children[$char] ?? null;
        
        if ($childNode === null) {
            return false;
        }
        
        $shouldDeleteChild = $this->deleteHelper($childNode, $word, $index + 1);
        
        if ($shouldDeleteChild) {
            unset($node->children[$char]);
            return !$node->isEndOfWord && count($node->children) === 0;
        }
        
        return false;
    }
    
    /**
     * 查找节点
     */
    private function findNode(string $word): ?TrieNode
    {
        $node = $this->root;
        $len = strlen($word);
        
        for ($i = 0; $i < $len; $i++) {
            $char = $word[$i];
            
            if (!isset($node->children[$char])) {
                return null;
            }
            
            $node = $node->children[$char];
        }
        
        return $node;
    }
    
    /**
     * 获取所有以指定前缀开头的单词
     * 时间复杂度：O(p + n)，p为前缀长度，n为结果数量
     */
    public function getWordsWithPrefix(string $prefix): array
    {
        $prefixNode = $this->findNode($prefix);
        
        if ($prefixNode === null) {
            return [];
        }
        
        $words = [];
        $this->collectWords($prefixNode, $prefix, $words);
        
        return $words;
    }
    
    /**
     * 收集单词（DFS）
     */
    private function collectWords(TrieNode $node, string $prefix, array &$words): void
    {
        if ($node->isEndOfWord) {
            $words[] = $prefix;
        }
        
        foreach ($node->children as $char => $childNode) {
            $this->collectWords($childNode, $prefix . $char, $words);
        }
    }
    
    /**
     * 获取所有单词
     * 时间复杂度：O(n)，n为所有字符总数
     */
    public function getAllWords(): array
    {
        return $this->getWordsWithPrefix('');
    }
    
    /**
     * 获取最长公共前缀
     */
    public function getLongestCommonPrefix(): string
    {
        if ($this->size === 0) {
            return '';
        }
        
        $prefix = '';
        $node = $this->root;
        
        while (count($node->children) === 1 && !$node->isEndOfWord) {
            $char = array_keys($node->children)[0];
            $prefix .= $char;
            $node = $node->children[$char];
        }
        
        return $prefix;
    }
    
    /**
     * 计算前缀出现次数
     */
    public function countWordsWithPrefix(string $prefix): int
    {
        $node = $this->findNode($prefix);
        return $node !== null ? $node->count : 0;
    }
    
    /**
     * 模糊搜索（支持通配符?）
     * 时间复杂度：O(n * m)，最坏情况
     */
    public function fuzzySearch(string $pattern): array
    {
        $results = [];
        $this->fuzzySearchHelper($this->root, $pattern, 0, '', $results);
        return $results;
    }
    
    /**
     * 模糊搜索辅助方法
     */
    private function fuzzySearchHelper(TrieNode $node, string $pattern, int $index, string $current, array &$results): void
    {
        if ($index === strlen($pattern)) {
            if ($node->isEndOfWord) {
                $results[] = $current;
            }
            return;
        }
        
        $char = $pattern[$index];
        
        if ($char === '?') {
            // 通配符，匹配任意字符
            foreach ($node->children as $c => $childNode) {
                $this->fuzzySearchHelper($childNode, $pattern, $index + 1, $current . $c, $results);
            }
        } else {
            // 精确匹配
            if (isset($node->children[$char])) {
                $this->fuzzySearchHelper($node->children[$char], $pattern, $index + 1, $current . $char, $results);
            }
        }
    }
    
    /**
     * 编辑距离搜索（近似匹配）
     * 查找编辑距离不超过maxDistance的单词
     */
    public function searchWithEditDistance(string $word, int $maxDistance): array
    {
        $results = [];
        $wordLen = strlen($word);
        
        // 初始化第一行
        $previousRow = range(0, $wordLen);
        
        $this->editDistanceHelper($this->root, '', $word, $previousRow, $maxDistance, $results);
        
        return $results;
    }
    
    /**
     * 编辑距离搜索辅助方法
     */
    private function editDistanceHelper(TrieNode $node, string $current, string $target, array $previousRow, int $maxDistance, array &$results): void
    {
        $targetLen = strlen($target);
        $currentRow = [strlen($current)];
        
        // 计算当前行的编辑距离
        for ($i = 1; $i <= $targetLen; $i++) {
            $insertCost = $currentRow[$i - 1] + 1;
            $deleteCost = $previousRow[$i] + 1;
            $replaceCost = $previousRow[$i - 1];
            
            if ($current[strlen($current) - 1] !== $target[$i - 1]) {
                $replaceCost++;
            }
            
            $currentRow[] = min($insertCost, $deleteCost, $replaceCost);
        }
        
        // 如果当前单词的最小编辑距离在范围内且是完整单词
        if ($node->isEndOfWord && $currentRow[$targetLen] <= $maxDistance) {
            $results[] = $current;
        }
        
        // 如果当前行的最小值小于等于maxDistance，继续搜索
        if (min($currentRow) <= $maxDistance) {
            foreach ($node->children as $char => $childNode) {
                $this->editDistanceHelper($childNode, $current . $char, $target, $currentRow, $maxDistance, $results);
            }
        }
    }
    
    /**
     * 获取大小
     */
    public function size(): int
    {
        return $this->size;
    }
    
    /**
     * 检查是否为空
     */
    public function isEmpty(): bool
    {
        return $this->size === 0;
    }
    
    /**
     * 清空Trie
     */
    public function clear(): void
    {
        $this->root = new TrieNode();
        $this->size = 0;
    }
    
    /**
     * 获取统计信息
     */
    public function getStatistics(): array
    {
        $nodeCount = 0;
        $maxDepth = 0;
        $totalChars = 0;
        
        $this->calculateStats($this->root, 0, $nodeCount, $maxDepth, $totalChars);
        
        return [
            'word_count' => $this->size,
            'node_count' => $nodeCount,
            'max_depth' => $maxDepth,
            'total_characters' => $totalChars,
            'avg_word_length' => $this->size > 0 ? $totalChars / $this->size : 0,
            'compression_ratio' => $totalChars > 0 ? $nodeCount / $totalChars : 0
        ];
    }
    
    /**
     * 计算统计信息辅助方法
     */
    private function calculateStats(TrieNode $node, int $depth, int &$nodeCount, int &$maxDepth, int &$totalChars): void
    {
        $nodeCount++;
        $maxDepth = max($maxDepth, $depth);
        
        if ($node->isEndOfWord) {
            $totalChars += $depth;
        }
        
        foreach ($node->children as $childNode) {
            $this->calculateStats($childNode, $depth + 1, $nodeCount, $maxDepth, $totalChars);
        }
    }
    
    /**
     * 序列化为数组
     */
    public function toArray(): array
    {
        return $this->getAllWords();
    }
    
    /**
     * 从数组创建Trie
     */
    public static function fromArray(array $words): Trie
    {
        $trie = new Trie();
        
        foreach ($words as $word) {
            if (is_string($word)) {
                $trie->insert($word);
            }
        }
        
        return $trie;
    }
    
    /**
     * 获取字符串表示
     */
    public function toString(): string
    {
        $words = $this->getAllWords();
        $stats = $this->getStatistics();
        
        $result = "Trie {\n";
        $result .= "  Words: {$stats['word_count']}\n";
        $result .= "  Nodes: {$stats['node_count']}\n";
        $result .= "  Max Depth: {$stats['max_depth']}\n";
        $result .= "  Avg Word Length: " . number_format($stats['avg_word_length'], 2) . "\n";
        $result .= "  Words: [" . implode(', ', array_slice($words, 0, 10));
        
        if (count($words) > 10) {
            $result .= ", ..." . (count($words) - 10) . " more";
        }
        
        $result .= "]\n}";
        
        return $result;
    }
}

/**
 * 压缩Trie（Patricia Trie）
 * 通过合并只有一个子节点的节点来节省空间
 */
class CompressedTrie
{
    private array $nodes;       // 节点存储
    private int $nextId;        // 下一个节点ID
    private int $rootId;        // 根节点ID
    private int $size;          // 单词数量
    
    public function __construct()
    {
        $this->nodes = [];
        $this->nextId = 0;
        $this->rootId = $this->createNode('', false);
        $this->size = 0;
    }
    
    /**
     * 创建节点
     */
    private function createNode(string $edge, bool $isEndOfWord): int
    {
        $id = $this->nextId++;
        $this->nodes[$id] = [
            'edge' => $edge,
            'is_end' => $isEndOfWord,
            'children' => [],
            'value' => null
        ];
        return $id;
    }
    
    /**
     * 插入单词
     */
    public function insert(string $word, $value = null): void
    {
        if (empty($word)) {
            return;
        }
        
        $nodeId = $this->rootId;
        $remaining = $word;
        
        while (!empty($remaining)) {
            $found = false;
            
            foreach ($this->nodes[$nodeId]['children'] as $childId) {
                $edge = $this->nodes[$childId]['edge'];
                $commonLen = $this->getCommonPrefixLength($remaining, $edge);
                
                if ($commonLen > 0) {
                    if ($commonLen === strlen($edge)) {
                        // 完全匹配边，继续向下
                        $nodeId = $childId;
                        $remaining = substr($remaining, $commonLen);
                        $found = true;
                        break;
                    } else {
                        // 部分匹配，需要分裂节点
                        $this->splitNode($childId, $commonLen);
                        $nodeId = $childId;
                        $remaining = substr($remaining, $commonLen);
                        $found = true;
                        break;
                    }
                }
            }
            
            if (!$found) {
                // 创建新的子节点
                $newNodeId = $this->createNode($remaining, true);
                $this->nodes[$newNodeId]['value'] = $value;
                $this->nodes[$nodeId]['children'][] = $newNodeId;
                $this->size++;
                return;
            }
        }
        
        // 标记为单词结尾
        if (!$this->nodes[$nodeId]['is_end']) {
            $this->nodes[$nodeId]['is_end'] = true;
            $this->size++;
        }
        $this->nodes[$nodeId]['value'] = $value;
    }
    
    /**
     * 分裂节点
     */
    private function splitNode(int $nodeId, int $splitPos): void
    {
        $node = &$this->nodes[$nodeId];
        $oldEdge = $node['edge'];
        
        // 创建新的子节点
        $newChildId = $this->createNode(substr($oldEdge, $splitPos), $node['is_end']);
        $this->nodes[$newChildId]['children'] = $node['children'];
        $this->nodes[$newChildId]['value'] = $node['value'];
        
        // 修改当前节点
        $node['edge'] = substr($oldEdge, 0, $splitPos);
        $node['is_end'] = false;
        $node['children'] = [$newChildId];
        $node['value'] = null;
    }
    
    /**
     * 获取公共前缀长度
     */
    private function getCommonPrefixLength(string $str1, string $str2): int
    {
        $len = min(strlen($str1), strlen($str2));
        $commonLen = 0;
        
        for ($i = 0; $i < $len; $i++) {
            if ($str1[$i] === $str2[$i]) {
                $commonLen++;
            } else {
                break;
            }
        }
        
        return $commonLen;
    }
    
    /**
     * 搜索单词
     */
    public function search(string $word): bool
    {
        $nodeId = $this->findNode($word);
        return $nodeId !== null && $this->nodes[$nodeId]['is_end'];
    }
    
    /**
     * 查找节点
     */
    private function findNode(string $word): ?int
    {
        $nodeId = $this->rootId;
        $remaining = $word;
        
        while (!empty($remaining)) {
            $found = false;
            
            foreach ($this->nodes[$nodeId]['children'] as $childId) {
                $edge = $this->nodes[$childId]['edge'];
                
                if (strpos($remaining, $edge) === 0) {
                    $nodeId = $childId;
                    $remaining = substr($remaining, strlen($edge));
                    $found = true;
                    break;
                }
            }
            
            if (!$found) {
                return null;
            }
        }
        
        return $nodeId;
    }
    
    /**
     * 获取大小
     */
    public function size(): int
    {
        return $this->size;
    }
    
    /**
     * 获取统计信息
     */
    public function getStatistics(): array
    {
        return [
            'word_count' => $this->size,
            'node_count' => count($this->nodes),
            'compression_ratio' => count($this->nodes) > 0 ? $this->size / count($this->nodes) : 0
        ];
    }
}