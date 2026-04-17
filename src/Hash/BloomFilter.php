<?php

namespace DataStructures\Hash;

/**
 * BloomFilter - 布隆过滤器数据结构实现
 * 
 * 思路：
 * 1. 使用位数组和多个哈希函数
 * 2. 插入时：对元素进行多次哈希，设置对应位为1
 * 3. 查询时：检查所有哈希位置是否都为1
 * 4. 支持误判但不支持漏判
 * 
 * 作用：
 * - 快速判断元素是否可能存在
 * - 节省空间的集合成员检测
 * - 减少昂贵的精确查询操作
 * 
 * 业务场景：
 * 1. 缓存穿透防护：避免查询不存在的数据
 * 2. 爬虫去重：URL去重，避免重复抓取
 * 3. 垃圾邮件过滤：快速识别垃圾邮件特征
 * 4. 数据库查询优化：预先过滤不存在的记录
 * 5. 分布式系统：减少网络请求
 * 6. CDN缓存：判断内容是否已缓存
 * 7. 推荐系统：过滤已推荐内容
 * 8. 安全系统：恶意IP、域名检测
 * 9. 大数据处理：海量数据去重预处理
 * 10. 区块链：交易去重、双花检测
 */

class BloomFilter
{
    private array $bitArray;      // 位数组
    private int $size;           // 位数组大小
    private int $hashCount;      // 哈希函数数量
    private int $elementCount;   // 已插入元素数量
    
    /**
     * 构造函数
     * @param int $expectedElements 预期元素数量
     * @param float $falsePositiveRate 误判率
     */
    public function __construct(int $expectedElements, float $falsePositiveRate = 0.01)
    {
        if ($expectedElements <= 0) {
            throw new \InvalidArgumentException("Expected elements must be positive");
        }
        
        if ($falsePositiveRate <= 0 || $falsePositiveRate >= 1) {
            throw new \InvalidArgumentException("False positive rate must be between 0 and 1");
        }
        
        // 计算最优位数组大小
        $this->size = (int) ceil(-($expectedElements * log($falsePositiveRate)) / (log(2) ** 2));
        
        // 计算最优哈希函数数量
        $this->hashCount = (int) ceil(($this->size / $expectedElements) * log(2));
        
        // 初始化位数组
        $this->bitArray = array_fill(0, $this->size, false);
        $this->elementCount = 0;
    }
    
    /**
     * 添加元素
     * 时间复杂度：O(k)，k为哈希函数数量
     */
    public function add($element): void
    {
        $hashes = $this->getHashes($element);
        
        foreach ($hashes as $hash) {
            $this->bitArray[$hash] = true;
        }
        
        $this->elementCount++;
    }
    
    /**
     * 检查元素是否可能存在
     * 时间复杂度：O(k)，k为哈希函数数量
     * 返回false：元素一定不存在
     * 返回true：元素可能存在（有误判可能）
     */
    public function contains($element): bool
    {
        $hashes = $this->getHashes($element);
        
        foreach ($hashes as $hash) {
            if (!$this->bitArray[$hash]) {
                return false;
            }
        }
        
        return true;
    }
    
    /**
     * 批量添加元素
     * 时间复杂度：O(n*k)
     */
    public function addAll(array $elements): void
    {
        foreach ($elements as $element) {
            $this->add($element);
        }
    }
    
    /**
     * 批量检查元素
     * 时间复杂度：O(n*k)
     */
    public function containsAll(array $elements): array
    {
        $results = [];
        foreach ($elements as $element) {
            $results[] = $this->contains($element);
        }
        return $results;
    }
    
    /**
     * 获取元素的哈希值数组
     */
    private function getHashes($element): array
    {
        $hashes = [];
        $data = is_string($element) ? $element : serialize($element);
        
        // 使用双重哈希技术生成多个哈希值
        $hash1 = $this->hash1($data);
        $hash2 = $this->hash2($data);
        
        for ($i = 0; $i < $this->hashCount; $i++) {
            $hash = ($hash1 + $i * $hash2) % $this->size;
            if ($hash < 0) {
                $hash += $this->size;
            }
            $hashes[] = $hash;
        }
        
        return $hashes;
    }
    
    /**
     * 第一个哈希函数（FNV-1a）
     */
    private function hash1(string $data): int
    {
        $hash = 2166136261;
        $len = strlen($data);
        
        for ($i = 0; $i < $len; $i++) {
            $hash ^= ord($data[$i]);
            $hash *= 16777619;
        }
        
        return (int)abs($hash);
    }
    
    /**
     * 第二个哈希函数（DJB2）
     */
    private function hash2(string $data): int
    {
        $hash = 5381;
        $len = strlen($data);
        
        for ($i = 0; $i < $len; $i++) {
            $hash = (($hash << 5) + $hash) + ord($data[$i]);
        }
        
        return (int)abs($hash);
    }
    
    /**
     * 获取当前误判率
     */
    public function getCurrentFalsePositiveRate(): float
    {
        if ($this->elementCount === 0) {
            return 0.0;
        }
        
        // 计算当前设置的位数
        $setBits = array_sum($this->bitArray);
        
        // 估算误判率：(1 - e^(-k*n/m))^k
        // 其中 k=哈希函数数量，n=元素数量，m=位数组大小
        $ratio = $setBits / $this->size;
        return pow($ratio, $this->hashCount);
    }
    
    /**
     * 获取位数组使用率
     */
    public function getBitUsageRate(): float
    {
        $setBits = array_sum($this->bitArray);
        return $this->size > 0 ? $setBits / $this->size : 0;
    }
    
    /**
     * 清空过滤器
     */
    public function clear(): void
    {
        $this->bitArray = array_fill(0, $this->size, false);
        $this->elementCount = 0;
    }
    
    /**
     * 获取统计信息
     */
    public function getStatistics(): array
    {
        return [
            'size' => $this->size,
            'hash_count' => $this->hashCount,
            'element_count' => $this->elementCount,
            'bit_usage_rate' => $this->getBitUsageRate(),
            'current_false_positive_rate' => $this->getCurrentFalsePositiveRate(),
            'memory_usage_bytes' => $this->size / 8, // 近似内存使用
        ];
    }
    
    /**
     * 获取大小
     */
    public function getSize(): int
    {
        return $this->size;
    }
    
    /**
     * 获取哈希函数数量
     */
    public function getHashCount(): int
    {
        return $this->hashCount;
    }
    
    /**
     * 获取元素数量
     */
    public function getElementCount(): int
    {
        return $this->elementCount;
    }
    
    /**
     * 检查是否为空
     */
    public function isEmpty(): bool
    {
        return $this->elementCount === 0;
    }
    
    /**
     * 合并两个布隆过滤器（OR操作）
     * 注意：只有相同配置的过滤器才能合并
     */
    public function union(BloomFilter $other): BloomFilter
    {
        if ($this->size !== $other->size || $this->hashCount !== $other->hashCount) {
            throw new \InvalidArgumentException("Cannot union filters with different configurations");
        }
        
        $result = new BloomFilter(1, 0.01); // 临时参数
        $result->size = $this->size;
        $result->hashCount = $this->hashCount;
        $result->bitArray = [];
        
        // 执行OR操作
        for ($i = 0; $i < $this->size; $i++) {
            $result->bitArray[$i] = $this->bitArray[$i] || $other->bitArray[$i];
        }
        
        $result->elementCount = $this->elementCount + $other->elementCount;
        
        return $result;
    }
    
    /**
     * 两个布隆过滤器的交集（AND操作）
     */
    public function intersect(BloomFilter $other): BloomFilter
    {
        if ($this->size !== $other->size || $this->hashCount !== $other->hashCount) {
            throw new \InvalidArgumentException("Cannot intersect filters with different configurations");
        }
        
        $result = new BloomFilter(1, 0.01); // 临时参数
        $result->size = $this->size;
        $result->hashCount = $this->hashCount;
        $result->bitArray = [];
        
        // 执行AND操作
        for ($i = 0; $i < $this->size; $i++) {
            $result->bitArray[$i] = $this->bitArray[$i] && $other->bitArray[$i];
        }
        
        $result->elementCount = min($this->elementCount, $other->elementCount);
        
        return $result;
    }
    
    /**
     * 序列化为字符串
     */
    public function serialize(): string
    {
        return json_encode([
            'size' => $this->size,
            'hash_count' => $this->hashCount,
            'element_count' => $this->elementCount,
            'bit_array' => $this->bitArray
        ]);
    }
    
    /**
     * 从字符串反序列化
     */
    public static function deserialize(string $data): BloomFilter
    {
        $decoded = json_decode($data, true);
        
        if (!$decoded) {
            throw new \InvalidArgumentException("Invalid serialized data");
        }
        
        $filter = new BloomFilter(1, 0.01); // 临时参数
        $filter->size = $decoded['size'];
        $filter->hashCount = $decoded['hash_count'];
        $filter->elementCount = $decoded['element_count'];
        $filter->bitArray = $decoded['bit_array'];
        
        return $filter;
    }
    
    /**
     * 计算最优参数
     */
    public static function calculateOptimalParameters(int $expectedElements, float $falsePositiveRate): array
    {
        $size = (int) ceil(-($expectedElements * log($falsePositiveRate)) / (log(2) ** 2));
        $hashCount = (int) ceil(($size / $expectedElements) * log(2));
        
        return [
            'size' => $size,
            'hash_count' => $hashCount,
            'memory_usage_bytes' => $size / 8
        ];
    }
    
    /**
     * 获取字符串表示
     */
    public function toString(): string
    {
        $stats = $this->getStatistics();
        
        return "BloomFilter {\n" .
               "  Size: {$stats['size']} bits\n" .
               "  Hash Functions: {$stats['hash_count']}\n" .
               "  Elements: {$stats['element_count']}\n" .
               "  Bit Usage: " . number_format($stats['bit_usage_rate'] * 100, 2) . "%\n" .
               "  False Positive Rate: " . number_format($stats['current_false_positive_rate'] * 100, 4) . "%\n" .
               "  Memory Usage: " . number_format($stats['memory_usage_bytes']) . " bytes\n" .
               "}";
    }
}

/**
 * 计数布隆过滤器
 * 支持删除操作，但会增加内存使用
 */
class CountingBloomFilter
{
    private array $counters;     // 计数器数组
    private int $size;          // 数组大小
    private int $hashCount;     // 哈希函数数量
    private int $elementCount;  // 元素数量
    
    public function __construct(int $expectedElements, float $falsePositiveRate = 0.01)
    {
        // 计算参数（与标准布隆过滤器相同）
        $this->size = (int) ceil(-($expectedElements * log($falsePositiveRate)) / (log(2) ** 2));
        $this->hashCount = (int) ceil(($this->size / $expectedElements) * log(2));
        
        // 初始化计数器数组
        $this->counters = array_fill(0, $this->size, 0);
        $this->elementCount = 0;
    }
    
    /**
     * 添加元素
     */
    public function add($element): void
    {
        $hashes = $this->getHashes($element);
        
        foreach ($hashes as $hash) {
            $this->counters[$hash]++;
        }
        
        $this->elementCount++;
    }
    
    /**
     * 删除元素
     */
    public function remove($element): bool
    {
        if (!$this->contains($element)) {
            return false;
        }
        
        $hashes = $this->getHashes($element);
        
        foreach ($hashes as $hash) {
            if ($this->counters[$hash] > 0) {
                $this->counters[$hash]--;
            }
        }
        
        $this->elementCount--;
        return true;
    }
    
    /**
     * 检查元素是否存在
     */
    public function contains($element): bool
    {
        $hashes = $this->getHashes($element);
        
        foreach ($hashes as $hash) {
            if ($this->counters[$hash] === 0) {
                return false;
            }
        }
        
        return true;
    }
    
    /**
     * 获取哈希值（复用BloomFilter的逻辑）
     */
    private function getHashes($element): array
    {
        $hashes = [];
        $data = is_string($element) ? $element : serialize($element);
        
        $hash1 = $this->hash1($data);
        $hash2 = $this->hash2($data);
        
        for ($i = 0; $i < $this->hashCount; $i++) {
            $hash = ($hash1 + $i * $hash2) % $this->size;
            if ($hash < 0) {
                $hash += $this->size;
            }
            $hashes[] = $hash;
        }
        
        return $hashes;
    }
    
    private function hash1(string $data): int
    {
        $hash = 2166136261;
        $len = strlen($data);
        
        for ($i = 0; $i < $len; $i++) {
            $hash ^= ord($data[$i]);
            $hash *= 16777619;
        }
        
        return (int)abs($hash);
    }
    
    private function hash2(string $data): int
    {
        $hash = 5381;
        $len = strlen($data);
        
        for ($i = 0; $i < $len; $i++) {
            $hash = (($hash << 5) + $hash) + ord($data[$i]);
        }
        
        return (int)abs($hash);
    }
    
    /**
     * 清空过滤器
     */
    public function clear(): void
    {
        $this->counters = array_fill(0, $this->size, 0);
        $this->elementCount = 0;
    }
    
    /**
     * 获取统计信息
     */
    public function getStatistics(): array
    {
        $nonZeroCounters = count(array_filter($this->counters, function($c) { return $c > 0; }));
        $maxCounter = max($this->counters);
        $avgCounter = $this->size > 0 ? array_sum($this->counters) / $this->size : 0;
        
        return [
            'size' => $this->size,
            'hash_count' => $this->hashCount,
            'element_count' => $this->elementCount,
            'non_zero_counters' => $nonZeroCounters,
            'max_counter' => $maxCounter,
            'avg_counter' => $avgCounter,
            'memory_usage_bytes' => $this->size * 4, // 假设每个计数器4字节
        ];
    }
}