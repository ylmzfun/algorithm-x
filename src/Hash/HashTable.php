<?php

namespace DataStructures\Hash;

/**
 * HashTable - 哈希表数据结构实现
 * 
 * 思路：
 * 1. 使用数组作为底层存储，通过哈希函数映射键到索引
 * 2. 处理哈希冲突：链地址法（拉链法）
 * 3. 动态扩容：当负载因子超过阈值时自动扩容
 * 4. 支持泛型键值对存储
 * 
 * 作用：
 * - 快速的键值对存储和检索
 * - 平均O(1)的插入、删除、查找操作
 * - 实现关联数组、缓存、索引等
 * 
 * 业务场景：
 * 1. 缓存系统：Redis、Memcached的底层实现
 * 2. 数据库索引：B+树索引的哈希优化
 * 3. 会话管理：用户会话信息存储
 * 4. 配置管理：应用配置项的快速访问
 * 5. 去重处理：数据去重、唯一性检查
 * 6. 计数统计：词频统计、访问计数
 * 7. 路由表：URL路由映射
 * 8. 权限控制：用户权限快速查询
 * 9. 分布式系统：一致性哈希、负载均衡
 * 10. 编译器：符号表、变量作用域管理
 */

/**
 * 哈希表节点
 */
class HashNode
{
    public $key;
    public $value;
    public ?HashNode $next;
    
    public function __construct($key, $value)
    {
        $this->key = $key;
        $this->value = $value;
        $this->next = null;
    }
}

class HashTable
{
    private array $buckets;      // 桶数组
    private int $capacity;       // 容量
    private int $size;          // 当前元素数量
    private float $loadFactor;  // 负载因子阈值
    
    public function __construct(int $initialCapacity = 16, float $loadFactor = 0.75)
    {
        $this->capacity = max(1, $initialCapacity);
        $this->size = 0;
        $this->loadFactor = $loadFactor;
        $this->buckets = array_fill(0, $this->capacity, null);
    }
    
    /**
     * 哈希函数
     * 时间复杂度：O(1)
     */
    private function hash($key): int
    {
        if (is_string($key)) {
            // 字符串哈希：DJB2算法
            $hash = 5381;
            $len = strlen($key);
            for ($i = 0; $i < $len; $i++) {
                $hash = (($hash << 5) + $hash) + ord($key[$i]);
            }
            return abs($hash) % $this->capacity;
        } elseif (is_int($key)) {
            // 整数哈希
            return abs($key) % $this->capacity;
        } elseif (is_float($key)) {
            // 浮点数哈希
            return abs((int)($key * 1000000)) % $this->capacity;
        } else {
            // 其他类型转换为字符串
            return $this->hash(serialize($key));
        }
    }
    
    /**
     * 插入或更新键值对
     * 平均时间复杂度：O(1)，最坏O(n)
     */
    public function put($key, $value): void
    {
        $index = $this->hash($key);
        $node = $this->buckets[$index];
        
        // 查找是否已存在
        while ($node !== null) {
            if ($this->keysEqual($node->key, $key)) {
                $node->value = $value; // 更新值
                return;
            }
            $node = $node->next;
        }
        
        // 插入新节点
        $newNode = new HashNode($key, $value);
        $newNode->next = $this->buckets[$index];
        $this->buckets[$index] = $newNode;
        $this->size++;
        
        // 检查是否需要扩容
        if ($this->size > $this->capacity * $this->loadFactor) {
            $this->resize();
        }
    }
    
    /**
     * 获取值
     * 平均时间复杂度：O(1)，最坏O(n)
     */
    public function get($key)
    {
        $index = $this->hash($key);
        $node = $this->buckets[$index];
        
        while ($node !== null) {
            if ($this->keysEqual($node->key, $key)) {
                return $node->value;
            }
            $node = $node->next;
        }
        
        return null;
    }
    
    /**
     * 检查键是否存在
     * 平均时间复杂度：O(1)，最坏O(n)
     */
    public function containsKey($key): bool
    {
        return $this->get($key) !== null;
    }
    
    /**
     * 删除键值对
     * 平均时间复杂度：O(1)，最坏O(n)
     */
    public function remove($key): bool
    {
        $index = $this->hash($key);
        $node = $this->buckets[$index];
        $prev = null;
        
        while ($node !== null) {
            if ($this->keysEqual($node->key, $key)) {
                if ($prev === null) {
                    $this->buckets[$index] = $node->next;
                } else {
                    $prev->next = $node->next;
                }
                $this->size--;
                return true;
            }
            $prev = $node;
            $node = $node->next;
        }
        
        return false;
    }
    
    /**
     * 获取所有键
     * 时间复杂度：O(n)
     */
    public function keys(): array
    {
        $keys = [];
        
        for ($i = 0; $i < $this->capacity; $i++) {
            $node = $this->buckets[$i];
            while ($node !== null) {
                $keys[] = $node->key;
                $node = $node->next;
            }
        }
        
        return $keys;
    }
    
    /**
     * 获取所有值
     * 时间复杂度：O(n)
     */
    public function values(): array
    {
        $values = [];
        
        for ($i = 0; $i < $this->capacity; $i++) {
            $node = $this->buckets[$i];
            while ($node !== null) {
                $values[] = $node->value;
                $node = $node->next;
            }
        }
        
        return $values;
    }
    
    /**
     * 获取所有键值对
     * 时间复杂度：O(n)
     */
    public function entries(): array
    {
        $entries = [];
        
        for ($i = 0; $i < $this->capacity; $i++) {
            $node = $this->buckets[$i];
            while ($node !== null) {
                $entries[] = ['key' => $node->key, 'value' => $node->value];
                $node = $node->next;
            }
        }
        
        return $entries;
    }
    
    /**
     * 获取大小
     * 时间复杂度：O(1)
     */
    public function size(): int
    {
        return $this->size;
    }
    
    /**
     * 检查是否为空
     * 时间复杂度：O(1)
     */
    public function isEmpty(): bool
    {
        return $this->size === 0;
    }
    
    /**
     * 清空哈希表
     * 时间复杂度：O(1)
     */
    public function clear(): void
    {
        $this->buckets = array_fill(0, $this->capacity, null);
        $this->size = 0;
    }
    
    /**
     * 获取负载因子
     * 时间复杂度：O(1)
     */
    public function getLoadFactor(): float
    {
        return $this->capacity > 0 ? $this->size / $this->capacity : 0;
    }
    
    /**
     * 获取容量
     * 时间复杂度：O(1)
     */
    public function getCapacity(): int
    {
        return $this->capacity;
    }
    
    /**
     * 扩容
     * 时间复杂度：O(n)
     */
    private function resize(): void
    {
        $oldBuckets = $this->buckets;
        $oldCapacity = $this->capacity;
        
        $this->capacity *= 2;
        $this->buckets = array_fill(0, $this->capacity, null);
        $this->size = 0;
        
        // 重新哈希所有元素
        for ($i = 0; $i < $oldCapacity; $i++) {
            $node = $oldBuckets[$i];
            while ($node !== null) {
                $this->put($node->key, $node->value);
                $node = $node->next;
            }
        }
    }
    
    /**
     * 比较键是否相等
     */
    private function keysEqual($key1, $key2): bool
    {
        if (gettype($key1) !== gettype($key2)) {
            return false;
        }
        
        if (is_array($key1) || is_object($key1)) {
            return serialize($key1) === serialize($key2);
        }
        
        return $key1 === $key2;
    }
    
    /**
     * 获取桶的分布统计
     */
    public function getBucketDistribution(): array
    {
        $distribution = [];
        $maxChainLength = 0;
        $emptyBuckets = 0;
        
        for ($i = 0; $i < $this->capacity; $i++) {
            $chainLength = 0;
            $node = $this->buckets[$i];
            
            while ($node !== null) {
                $chainLength++;
                $node = $node->next;
            }
            
            if ($chainLength === 0) {
                $emptyBuckets++;
            }
            
            $distribution[$i] = $chainLength;
            $maxChainLength = max($maxChainLength, $chainLength);
        }
        
        return [
            'distribution' => $distribution,
            'max_chain_length' => $maxChainLength,
            'empty_buckets' => $emptyBuckets,
            'load_factor' => $this->getLoadFactor()
        ];
    }
    
    /**
     * 获取统计信息
     */
    public function getStatistics(): array
    {
        $bucketStats = $this->getBucketDistribution();
        
        return [
            'size' => $this->size,
            'capacity' => $this->capacity,
            'load_factor' => $this->getLoadFactor(),
            'max_chain_length' => $bucketStats['max_chain_length'],
            'empty_buckets' => $bucketStats['empty_buckets'],
            'collision_rate' => $this->capacity > 0 ? 
                ($this->capacity - $bucketStats['empty_buckets']) / $this->capacity : 0
        ];
    }
    
    /**
     * 转换为数组
     */
    public function toArray(): array
    {
        $result = [];
        
        for ($i = 0; $i < $this->capacity; $i++) {
            $node = $this->buckets[$i];
            while ($node !== null) {
                $result[$node->key] = $node->value;
                $node = $node->next;
            }
        }
        
        return $result;
    }
    
    /**
     * 从数组创建哈希表
     */
    public static function fromArray(array $array, int $initialCapacity = 16): HashTable
    {
        $hashTable = new HashTable($initialCapacity);
        
        foreach ($array as $key => $value) {
            $hashTable->put($key, $value);
        }
        
        return $hashTable;
    }
    
    /**
     * 获取字符串表示
     */
    public function toString(): string
    {
        $result = "HashTable {\n";
        $result .= "  Size: {$this->size}, Capacity: {$this->capacity}\n";
        $result .= "  Load Factor: " . number_format($this->getLoadFactor(), 3) . "\n";
        
        $entries = $this->entries();
        foreach ($entries as $entry) {
            $key = is_string($entry['key']) ? "'{$entry['key']}'" : $entry['key'];
            $value = is_string($entry['value']) ? "'{$entry['value']}'" : $entry['value'];
            $result .= "  $key => $value\n";
        }
        
        $result .= "}";
        return $result;
    }
}

/**
 * 一致性哈希实现
 * 用于分布式系统中的负载均衡
 */
class ConsistentHash
{
    private array $ring;         // 哈希环
    private array $nodes;        // 节点列表
    private int $virtualNodes;   // 虚拟节点数量
    
    public function __construct(int $virtualNodes = 150)
    {
        $this->ring = [];
        $this->nodes = [];
        $this->virtualNodes = $virtualNodes;
    }
    
    /**
     * 添加节点
     */
    public function addNode(string $node): void
    {
        $this->nodes[] = $node;
        
        for ($i = 0; $i < $this->virtualNodes; $i++) {
            $virtualNode = $node . ':' . $i;
            $hash = $this->hash($virtualNode);
            $this->ring[$hash] = $node;
        }
        
        ksort($this->ring);
    }
    
    /**
     * 删除节点
     */
    public function removeNode(string $node): void
    {
        $this->nodes = array_filter($this->nodes, function($n) use ($node) {
            return $n !== $node;
        });
        
        for ($i = 0; $i < $this->virtualNodes; $i++) {
            $virtualNode = $node . ':' . $i;
            $hash = $this->hash($virtualNode);
            unset($this->ring[$hash]);
        }
    }
    
    /**
     * 获取键对应的节点
     */
    public function getNode(string $key): ?string
    {
        if (empty($this->ring)) {
            return null;
        }
        
        $hash = $this->hash($key);
        $keys = array_keys($this->ring);
        
        // 找到第一个大于等于hash的节点
        foreach ($keys as $ringHash) {
            if ($ringHash >= $hash) {
                return $this->ring[$ringHash];
            }
        }
        
        // 如果没找到，返回第一个节点（环形）
        return $this->ring[$keys[0]];
    }
    
    /**
     * 哈希函数
     */
    private function hash(string $key): int
    {
        return crc32($key);
    }
    
    /**
     * 获取节点分布
     */
    public function getDistribution(array $keys): array
    {
        $distribution = [];
        
        foreach ($this->nodes as $node) {
            $distribution[$node] = 0;
        }
        
        foreach ($keys as $key) {
            $node = $this->getNode($key);
            if ($node !== null) {
                $distribution[$node]++;
            }
        }
        
        return $distribution;
    }
}