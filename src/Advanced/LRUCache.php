<?php

namespace DataStructures\Advanced;

/**
 * LRUCache - 最近最少使用缓存数据结构实现
 * 
 * 思路：
 * 1. 结合哈希表和双向链表
 * 2. 哈希表提供O(1)的查找
 * 3. 双向链表维护访问顺序
 * 4. 头部为最近访问，尾部为最久未访问
 * 
 * 作用：
 * - 固定容量的缓存管理
 * - 自动淘汰最久未使用的数据
 * - 高效的读写操作
 * 
 * 业务场景：
 * 1. 操作系统：页面置换算法
 * 2. CPU缓存：缓存行替换策略
 * 3. 数据库：缓冲池管理
 * 4. Web缓存：浏览器缓存、CDN缓存
 * 5. 应用缓存：Redis、Memcached
 * 6. 移动应用：图片缓存、数据缓存
 * 7. 编译器：符号表缓存
 * 8. 游戏开发：资源缓存管理
 * 9. 分布式系统：本地缓存层
 * 10. 机器学习：模型缓存、特征缓存
 */

/**
 * 双向链表节点
 */
class LRUNode
{
    public $key;
    public $value;
    public ?LRUNode $prev;
    public ?LRUNode $next;
    public int $timestamp;      // 访问时间戳
    public int $accessCount;    // 访问次数
    
    public function __construct($key, $value)
    {
        $this->key = $key;
        $this->value = $value;
        $this->prev = null;
        $this->next = null;
        $this->timestamp = time();
        $this->accessCount = 1;
    }
}

class LRUCache
{
    private int $capacity;              // 缓存容量
    private int $size;                  // 当前大小
    private array $cache;               // 哈希表
    private LRUNode $head;              // 虚拟头节点
    private LRUNode $tail;              // 虚拟尾节点
    private int $hits;                  // 命中次数
    private int $misses;                // 未命中次数
    private array $evictionCallbacks;   // 淘汰回调函数
    
    public function __construct(int $capacity)
    {
        if ($capacity <= 0) {
            throw new \InvalidArgumentException("Capacity must be positive");
        }
        
        $this->capacity = $capacity;
        $this->size = 0;
        $this->cache = [];
        $this->hits = 0;
        $this->misses = 0;
        $this->evictionCallbacks = [];
        
        // 创建虚拟头尾节点
        $this->head = new LRUNode(null, null);
        $this->tail = new LRUNode(null, null);
        $this->head->next = $this->tail;
        $this->tail->prev = $this->head;
    }
    
    /**
     * 获取值
     * 时间复杂度：O(1)
     */
    public function get($key)
    {
        if (isset($this->cache[$key])) {
            $node = $this->cache[$key];
            
            // 更新访问信息
            $node->timestamp = time();
            $node->accessCount++;
            
            // 移动到头部
            $this->moveToHead($node);
            
            $this->hits++;
            return $node->value;
        }
        
        $this->misses++;
        return null;
    }
    
    /**
     * 设置值
     * 时间复杂度：O(1)
     */
    public function put($key, $value): void
    {
        if (isset($this->cache[$key])) {
            // 更新现有节点
            $node = $this->cache[$key];
            $node->value = $value;
            $node->timestamp = time();
            $node->accessCount++;
            $this->moveToHead($node);
        } else {
            // 创建新节点
            $newNode = new LRUNode($key, $value);
            
            if ($this->size >= $this->capacity) {
                // 淘汰尾部节点
                $evicted = $this->removeTail();
                $this->triggerEvictionCallbacks($evicted->key, $evicted->value);
            } else {
                $this->size++;
            }
            
            $this->cache[$key] = $newNode;
            $this->addToHead($newNode);
        }
    }
    
    /**
     * 删除键
     * 时间复杂度：O(1)
     */
    public function delete($key): bool
    {
        if (isset($this->cache[$key])) {
            $node = $this->cache[$key];
            $this->removeNode($node);
            unset($this->cache[$key]);
            $this->size--;
            return true;
        }
        
        return false;
    }
    
    /**
     * 检查键是否存在
     * 时间复杂度：O(1)
     */
    public function contains($key): bool
    {
        return isset($this->cache[$key]);
    }
    
    /**
     * 获取所有键（按访问顺序）
     * 时间复杂度：O(n)
     */
    public function keys(): array
    {
        $keys = [];
        $current = $this->head->next;
        
        while ($current !== $this->tail) {
            $keys[] = $current->key;
            $current = $current->next;
        }
        
        return $keys;
    }
    
    /**
     * 获取所有值（按访问顺序）
     * 时间复杂度：O(n)
     */
    public function values(): array
    {
        $values = [];
        $current = $this->head->next;
        
        while ($current !== $this->tail) {
            $values[] = $current->value;
            $current = $current->next;
        }
        
        return $values;
    }
    
    /**
     * 移动节点到头部
     */
    private function moveToHead(LRUNode $node): void
    {
        $this->removeNode($node);
        $this->addToHead($node);
    }
    
    /**
     * 添加节点到头部
     */
    private function addToHead(LRUNode $node): void
    {
        $node->prev = $this->head;
        $node->next = $this->head->next;
        $this->head->next->prev = $node;
        $this->head->next = $node;
    }
    
    /**
     * 移除节点
     */
    private function removeNode(LRUNode $node): void
    {
        $node->prev->next = $node->next;
        $node->next->prev = $node->prev;
    }
    
    /**
     * 移除尾部节点
     */
    private function removeTail(): LRUNode
    {
        $lastNode = $this->tail->prev;
        $this->removeNode($lastNode);
        unset($this->cache[$lastNode->key]);
        return $lastNode;
    }
    
    /**
     * 获取大小
     */
    public function size(): int
    {
        return $this->size;
    }
    
    /**
     * 获取容量
     */
    public function capacity(): int
    {
        return $this->capacity;
    }
    
    /**
     * 检查是否为空
     */
    public function isEmpty(): bool
    {
        return $this->size === 0;
    }
    
    /**
     * 检查是否已满
     */
    public function isFull(): bool
    {
        return $this->size >= $this->capacity;
    }
    
    /**
     * 清空缓存
     */
    public function clear(): void
    {
        $this->cache = [];
        $this->size = 0;
        $this->head->next = $this->tail;
        $this->tail->prev = $this->head;
        $this->hits = 0;
        $this->misses = 0;
    }
    
    /**
     * 获取命中率
     */
    public function getHitRate(): float
    {
        $total = $this->hits + $this->misses;
        return $total > 0 ? $this->hits / $total : 0.0;
    }
    
    /**
     * 获取统计信息
     */
    public function getStatistics(): array
    {
        $accessCounts = [];
        $current = $this->head->next;
        
        while ($current !== $this->tail) {
            $accessCounts[] = $current->accessCount;
            $current = $current->next;
        }
        
        return [
            'size' => $this->size,
            'capacity' => $this->capacity,
            'hits' => $this->hits,
            'misses' => $this->misses,
            'hit_rate' => $this->getHitRate(),
            'usage_rate' => $this->capacity > 0 ? $this->size / $this->capacity : 0,
            'avg_access_count' => !empty($accessCounts) ? array_sum($accessCounts) / count($accessCounts) : 0,
            'max_access_count' => !empty($accessCounts) ? max($accessCounts) : 0
        ];
    }
    
    /**
     * 添加淘汰回调
     */
    public function addEvictionCallback(callable $callback): void
    {
        $this->evictionCallbacks[] = $callback;
    }
    
    /**
     * 触发淘汰回调
     */
    private function triggerEvictionCallbacks($key, $value): void
    {
        foreach ($this->evictionCallbacks as $callback) {
            $callback($key, $value);
        }
    }
    
    /**
     * 获取最近访问的N个键
     */
    public function getMostRecentKeys(int $n): array
    {
        $keys = [];
        $current = $this->head->next;
        $count = 0;
        
        while ($current !== $this->tail && $count < $n) {
            $keys[] = $current->key;
            $current = $current->next;
            $count++;
        }
        
        return $keys;
    }
    
    /**
     * 获取最久未访问的N个键
     */
    public function getLeastRecentKeys(int $n): array
    {
        $keys = [];
        $current = $this->tail->prev;
        $count = 0;
        
        while ($current !== $this->head && $count < $n) {
            $keys[] = $current->key;
            $current = $current->prev;
            $count++;
        }
        
        return $keys;
    }
    
    /**
     * 预热缓存
     */
    public function warmUp(array $data): void
    {
        foreach ($data as $key => $value) {
            $this->put($key, $value);
        }
    }
    
    /**
     * 转换为数组
     */
    public function toArray(): array
    {
        $result = [];
        $current = $this->head->next;
        
        while ($current !== $this->tail) {
            $result[$current->key] = $current->value;
            $current = $current->next;
        }
        
        return $result;
    }
    
    /**
     * 获取字符串表示
     */
    public function toString(): string
    {
        $stats = $this->getStatistics();
        $keys = $this->keys();
        
        $result = "LRUCache {\n";
        $result .= "  Capacity: {$this->capacity}\n";
        $result .= "  Size: {$this->size}\n";
        $result .= "  Hit Rate: " . number_format($stats['hit_rate'] * 100, 2) . "%\n";
        $result .= "  Usage: " . number_format($stats['usage_rate'] * 100, 2) . "%\n";
        $result .= "  Keys (MRU to LRU): [" . implode(', ', array_slice($keys, 0, 10));
        
        if (count($keys) > 10) {
            $result .= ", ..." . (count($keys) - 10) . " more";
        }
        
        $result .= "]\n}";
        
        return $result;
    }
}

/**
 * LFU缓存（最少使用频率）
 * 当缓存满时，淘汰使用频率最低的项
 */
class LFUCache
{
    private int $capacity;
    private int $size;
    private array $cache;           // key -> node
    private array $frequencies;     // frequency -> doubly linked list
    private int $minFrequency;
    
    public function __construct(int $capacity)
    {
        $this->capacity = $capacity;
        $this->size = 0;
        $this->cache = [];
        $this->frequencies = [];
        $this->minFrequency = 1;
    }
    
    /**
     * 获取值
     */
    public function get($key)
    {
        if (!isset($this->cache[$key])) {
            return null;
        }
        
        $node = $this->cache[$key];
        $this->updateFrequency($node);
        
        return $node->value;
    }
    
    /**
     * 设置值
     */
    public function put($key, $value): void
    {
        if ($this->capacity <= 0) {
            return;
        }
        
        if (isset($this->cache[$key])) {
            $node = $this->cache[$key];
            $node->value = $value;
            $this->updateFrequency($node);
            return;
        }
        
        if ($this->size >= $this->capacity) {
            $this->evictLFU();
        }
        
        $node = new LFUNode($key, $value);
        $this->cache[$key] = $node;
        $this->addToFrequency($node, 1);
        $this->minFrequency = 1;
        $this->size++;
    }
    
    /**
     * 更新频率
     */
    private function updateFrequency(LFUNode $node): void
    {
        $oldFreq = $node->frequency;
        $newFreq = $oldFreq + 1;
        
        // 从旧频率列表中移除
        $this->removeFromFrequency($node, $oldFreq);
        
        // 添加到新频率列表
        $this->addToFrequency($node, $newFreq);
        
        // 更新最小频率
        if ($oldFreq === $this->minFrequency && empty($this->frequencies[$oldFreq])) {
            $this->minFrequency++;
        }
    }
    
    /**
     * 添加到频率列表
     */
    private function addToFrequency(LFUNode $node, int $frequency): void
    {
        $node->frequency = $frequency;
        
        if (!isset($this->frequencies[$frequency])) {
            $this->frequencies[$frequency] = [];
        }
        
        $this->frequencies[$frequency][] = $node;
    }
    
    /**
     * 从频率列表中移除
     */
    private function removeFromFrequency(LFUNode $node, int $frequency): void
    {
        if (!isset($this->frequencies[$frequency])) {
            return;
        }
        
        $index = array_search($node, $this->frequencies[$frequency], true);
        if ($index !== false) {
            array_splice($this->frequencies[$frequency], $index, 1);
        }
    }
    
    /**
     * 淘汰LFU项
     */
    private function evictLFU(): void
    {
        if (empty($this->frequencies[$this->minFrequency])) {
            return;
        }
        
        $node = array_shift($this->frequencies[$this->minFrequency]);
        unset($this->cache[$node->key]);
        $this->size--;
    }
    
    /**
     * 获取大小
     */
    public function size(): int
    {
        return $this->size;
    }
    
    /**
     * 清空缓存
     */
    public function clear(): void
    {
        $this->cache = [];
        $this->frequencies = [];
        $this->size = 0;
        $this->minFrequency = 1;
    }
}

/**
 * LFU节点
 */
class LFUNode
{
    public $key;
    public $value;
    public int $frequency;
    
    public function __construct($key, $value)
    {
        $this->key = $key;
        $this->value = $value;
        $this->frequency = 1;
    }
}

/**
 * TTL缓存（带过期时间）
 */
class TTLCache
{
    private array $cache;       // key -> [value, expiry_time]
    private int $defaultTTL;    // 默认TTL（秒）
    
    public function __construct(int $defaultTTL = 3600)
    {
        $this->cache = [];
        $this->defaultTTL = $defaultTTL;
    }
    
    /**
     * 设置值（带TTL）
     */
    public function put($key, $value, ?int $ttl = null): void
    {
        $ttl = $ttl ?? $this->defaultTTL;
        $expiryTime = time() + $ttl;
        $this->cache[$key] = [$value, $expiryTime];
    }
    
    /**
     * 获取值
     */
    public function get($key)
    {
        if (!isset($this->cache[$key])) {
            return null;
        }
        
        [$value, $expiryTime] = $this->cache[$key];
        
        if (time() > $expiryTime) {
            unset($this->cache[$key]);
            return null;
        }
        
        return $value;
    }
    
    /**
     * 清理过期项
     */
    public function cleanup(): int
    {
        $removed = 0;
        $currentTime = time();
        
        foreach ($this->cache as $key => [$value, $expiryTime]) {
            if ($currentTime > $expiryTime) {
                unset($this->cache[$key]);
                $removed++;
            }
        }
        
        return $removed;
    }
    
    /**
     * 获取剩余TTL
     */
    public function getTTL($key): ?int
    {
        if (!isset($this->cache[$key])) {
            return null;
        }
        
        [$value, $expiryTime] = $this->cache[$key];
        $remaining = $expiryTime - time();
        
        return $remaining > 0 ? $remaining : null;
    }
    
    /**
     * 获取大小
     */
    public function size(): int
    {
        return count($this->cache);
    }
}