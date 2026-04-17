<?php

namespace DataStructures\Advanced;

/**
 * SkipList - 跳表数据结构实现
 * 
 * 思路：
 * 1. 多层链表结构，底层包含所有元素
 * 2. 上层是下层的子集，通过随机化决定层数
 * 3. 每层都是有序链表，支持快速查找
 * 4. 平均时间复杂度O(log n)
 * 
 * 作用：
 * - 有序数据的快速插入、删除、查找
 * - 替代平衡树的简单实现
 * - 支持范围查询
 * 
 * 业务场景：
 * 1. 数据库索引：Redis的有序集合底层实现
 * 2. 内存数据库：快速范围查询
 * 3. 分布式系统：一致性哈希环
 * 4. 游戏排行榜：实时排名系统
 * 5. 时间序列数据：按时间范围查询
 * 6. 搜索引擎：倒排索引优化
 * 7. 网络路由：路由表查找
 * 8. 操作系统：进程调度队列
 * 9. 金融系统：订单簿管理
 * 10. 缓存系统：LRU缓存的有序访问
 */

/**
 * 跳表节点
 */
class SkipListNode
{
    public $key;
    public $value;
    public array $forward;      // 各层的前向指针
    public int $level;          // 节点层数
    
    public function __construct($key, $value, int $level)
    {
        $this->key = $key;
        $this->value = $value;
        $this->level = $level;
        $this->forward = array_fill(0, $level + 1, null);
    }
}

class SkipList
{
    private SkipListNode $header;   // 头节点
    private int $maxLevel;          // 最大层数
    private int $currentLevel;      // 当前最高层数
    private float $probability;     // 层数增长概率
    private int $size;              // 元素数量
    
    public function __construct(int $maxLevel = 16, float $probability = 0.5)
    {
        $this->maxLevel = $maxLevel;
        $this->probability = $probability;
        $this->currentLevel = 0;
        $this->size = 0;
        
        // 创建头节点
        $this->header = new SkipListNode(null, null, $maxLevel);
    }
    
    /**
     * 生成随机层数
     * 时间复杂度：O(log n)
     */
    private function randomLevel(): int
    {
        $level = 0;
        
        while (rand() / getrandmax() < $this->probability && $level < $this->maxLevel) {
            $level++;
        }
        
        return $level;
    }
    
    /**
     * 插入键值对
     * 平均时间复杂度：O(log n)
     */
    public function insert($key, $value): void
    {
        $update = array_fill(0, $this->maxLevel + 1, null);
        $current = $this->header;
        
        // 从最高层开始查找插入位置
        for ($i = $this->currentLevel; $i >= 0; $i--) {
            while ($current->forward[$i] !== null && 
                   $this->compareKeys($current->forward[$i]->key, $key) < 0) {
                $current = $current->forward[$i];
            }
            $update[$i] = $current;
        }
        
        $current = $current->forward[0];
        
        // 如果键已存在，更新值
        if ($current !== null && $this->compareKeys($current->key, $key) === 0) {
            $current->value = $value;
            return;
        }
        
        // 生成新节点的层数
        $newLevel = $this->randomLevel();
        
        // 如果新层数超过当前最高层，更新header的指针
        if ($newLevel > $this->currentLevel) {
            for ($i = $this->currentLevel + 1; $i <= $newLevel; $i++) {
                $update[$i] = $this->header;
            }
            $this->currentLevel = $newLevel;
        }
        
        // 创建新节点
        $newNode = new SkipListNode($key, $value, $newLevel);
        
        // 更新各层的指针
        for ($i = 0; $i <= $newLevel; $i++) {
            $newNode->forward[$i] = $update[$i]->forward[$i];
            $update[$i]->forward[$i] = $newNode;
        }
        
        $this->size++;
    }
    
    /**
     * 搜索键
     * 平均时间复杂度：O(log n)
     */
    public function search($key)
    {
        $current = $this->header;
        
        // 从最高层开始搜索
        for ($i = $this->currentLevel; $i >= 0; $i--) {
            while ($current->forward[$i] !== null && 
                   $this->compareKeys($current->forward[$i]->key, $key) < 0) {
                $current = $current->forward[$i];
            }
        }
        
        $current = $current->forward[0];
        
        if ($current !== null && $this->compareKeys($current->key, $key) === 0) {
            return $current->value;
        }
        
        return null;
    }
    
    /**
     * 检查键是否存在
     * 平均时间复杂度：O(log n)
     */
    public function contains($key): bool
    {
        return $this->search($key) !== null;
    }
    
    /**
     * 删除键
     * 平均时间复杂度：O(log n)
     */
    public function delete($key): bool
    {
        $update = array_fill(0, $this->maxLevel + 1, null);
        $current = $this->header;
        
        // 查找要删除的节点
        for ($i = $this->currentLevel; $i >= 0; $i--) {
            while ($current->forward[$i] !== null && 
                   $this->compareKeys($current->forward[$i]->key, $key) < 0) {
                $current = $current->forward[$i];
            }
            $update[$i] = $current;
        }
        
        $current = $current->forward[0];
        
        if ($current === null || $this->compareKeys($current->key, $key) !== 0) {
            return false;
        }
        
        // 更新各层的指针
        for ($i = 0; $i <= $this->currentLevel; $i++) {
            if ($update[$i]->forward[$i] !== $current) {
                break;
            }
            $update[$i]->forward[$i] = $current->forward[$i];
        }
        
        // 更新当前最高层
        while ($this->currentLevel > 0 && $this->header->forward[$this->currentLevel] === null) {
            $this->currentLevel--;
        }
        
        $this->size--;
        return true;
    }
    
    /**
     * 范围查询
     * 时间复杂度：O(log n + k)，k为结果数量
     */
    public function rangeQuery($minKey, $maxKey): array
    {
        $result = [];
        $current = $this->header;
        
        // 找到第一个大于等于minKey的节点
        for ($i = $this->currentLevel; $i >= 0; $i--) {
            while ($current->forward[$i] !== null && 
                   $this->compareKeys($current->forward[$i]->key, $minKey) < 0) {
                $current = $current->forward[$i];
            }
        }
        
        $current = $current->forward[0];
        
        // 收集范围内的所有节点
        while ($current !== null && $this->compareKeys($current->key, $maxKey) <= 0) {
            $result[] = ['key' => $current->key, 'value' => $current->value];
            $current = $current->forward[0];
        }
        
        return $result;
    }
    
    /**
     * 获取第k小的元素
     * 时间复杂度：O(n)
     */
    public function getKthElement(int $k)
    {
        if ($k < 1 || $k > $this->size) {
            return null;
        }
        
        $current = $this->header->forward[0];
        $count = 1;
        
        while ($current !== null && $count < $k) {
            $current = $current->forward[0];
            $count++;
        }
        
        return $current !== null ? ['key' => $current->key, 'value' => $current->value] : null;
    }
    
    /**
     * 获取最小元素
     * 时间复杂度：O(1)
     */
    public function getMin()
    {
        $first = $this->header->forward[0];
        return $first !== null ? ['key' => $first->key, 'value' => $first->value] : null;
    }
    
    /**
     * 获取最大元素
     * 时间复杂度：O(n)
     */
    public function getMax()
    {
        if ($this->size === 0) {
            return null;
        }
        
        $current = $this->header;
        
        // 在最底层遍历到最后
        while ($current->forward[0] !== null) {
            $current = $current->forward[0];
        }
        
        return ['key' => $current->key, 'value' => $current->value];
    }
    
    /**
     * 比较键
     */
    private function compareKeys($key1, $key2): int
    {
        if ($key1 < $key2) return -1;
        if ($key1 > $key2) return 1;
        return 0;
    }
    
    /**
     * 获取所有键值对（有序）
     * 时间复杂度：O(n)
     */
    public function toArray(): array
    {
        $result = [];
        $current = $this->header->forward[0];
        
        while ($current !== null) {
            $result[$current->key] = $current->value;
            $current = $current->forward[0];
        }
        
        return $result;
    }
    
    /**
     * 获取所有键（有序）
     * 时间复杂度：O(n)
     */
    public function keys(): array
    {
        $keys = [];
        $current = $this->header->forward[0];
        
        while ($current !== null) {
            $keys[] = $current->key;
            $current = $current->forward[0];
        }
        
        return $keys;
    }
    
    /**
     * 获取所有值（按键排序）
     * 时间复杂度：O(n)
     */
    public function values(): array
    {
        $values = [];
        $current = $this->header->forward[0];
        
        while ($current !== null) {
            $values[] = $current->value;
            $current = $current->forward[0];
        }
        
        return $values;
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
     * 清空跳表
     */
    public function clear(): void
    {
        $this->header = new SkipListNode(null, null, $this->maxLevel);
        $this->currentLevel = 0;
        $this->size = 0;
    }
    
    /**
     * 获取统计信息
     */
    public function getStatistics(): array
    {
        $levelCounts = array_fill(0, $this->maxLevel + 1, 0);
        $current = $this->header->forward[0];
        
        while ($current !== null) {
            for ($i = 0; $i <= $current->level; $i++) {
                $levelCounts[$i]++;
            }
            $current = $current->forward[0];
        }
        
        $avgLevel = 0;
        if ($this->size > 0) {
            $totalLevels = 0;
            $current = $this->header->forward[0];
            while ($current !== null) {
                $totalLevels += $current->level + 1;
                $current = $current->forward[0];
            }
            $avgLevel = $totalLevels / $this->size;
        }
        
        return [
            'size' => $this->size,
            'max_level' => $this->maxLevel,
            'current_level' => $this->currentLevel,
            'probability' => $this->probability,
            'level_counts' => $levelCounts,
            'avg_level' => $avgLevel,
            'theoretical_avg_level' => 1 / (1 - $this->probability)
        ];
    }
    
    /**
     * 验证跳表结构的正确性
     */
    public function validate(): bool
    {
        // 检查每层的有序性
        for ($level = 0; $level <= $this->currentLevel; $level++) {
            $current = $this->header->forward[$level];
            
            while ($current !== null && $current->forward[$level] !== null) {
                if ($this->compareKeys($current->key, $current->forward[$level]->key) >= 0) {
                    return false;
                }
                $current = $current->forward[$level];
            }
        }
        
        // 检查节点数量
        $count = 0;
        $current = $this->header->forward[0];
        while ($current !== null) {
            $count++;
            $current = $current->forward[0];
        }
        
        return $count === $this->size;
    }
    
    /**
     * 获取字符串表示
     */
    public function toString(): string
    {
        $result = "SkipList {\n";
        $result .= "  Size: {$this->size}\n";
        $result .= "  Current Level: {$this->currentLevel}\n";
        $result .= "  Max Level: {$this->maxLevel}\n";
        $result .= "  Probability: {$this->probability}\n";
        
        // 显示每层的结构
        for ($level = $this->currentLevel; $level >= 0; $level--) {
            $result .= "  Level $level: ";
            $current = $this->header->forward[$level];
            $keys = [];
            
            while ($current !== null) {
                $keys[] = $current->key;
                $current = $current->forward[$level];
            }
            
            $result .= "[" . implode(', ', $keys) . "]\n";
        }
        
        $result .= "}";
        return $result;
    }
    
    /**
     * 从数组创建跳表
     */
    public static function fromArray(array $data): SkipList
    {
        $skipList = new SkipList();
        
        foreach ($data as $key => $value) {
            $skipList->insert($key, $value);
        }
        
        return $skipList;
    }
}

/**
 * 并发安全的跳表（简化版本）
 * 在实际应用中需要更复杂的锁机制
 */
class ConcurrentSkipList extends SkipList
{
    private $lock;
    
    public function __construct(int $maxLevel = 16, float $probability = 0.5)
    {
        parent::__construct($maxLevel, $probability);
        $this->lock = fopen('php://memory', 'r+');
    }
    
    /**
     * 线程安全的插入
     */
    public function insert($key, $value): void
    {
        if (flock($this->lock, LOCK_EX)) {
            parent::insert($key, $value);
            flock($this->lock, LOCK_UN);
        }
    }
    
    /**
     * 线程安全的搜索
     */
    public function search($key)
    {
        if (flock($this->lock, LOCK_SH)) {
            $result = parent::search($key);
            flock($this->lock, LOCK_UN);
            return $result;
        }
        return null;
    }
    
    /**
     * 线程安全的删除
     */
    public function delete($key): bool
    {
        if (flock($this->lock, LOCK_EX)) {
            $result = parent::delete($key);
            flock($this->lock, LOCK_UN);
            return $result;
        }
        return false;
    }
    
    public function __destruct()
    {
        if (is_resource($this->lock)) {
            fclose($this->lock);
        }
    }
}

/**
 * 带权重的跳表
 * 支持按权重进行概率性选择
 */
class WeightedSkipList
{
    private SkipList $skipList;
    private array $weights;     // key -> weight
    private float $totalWeight;
    
    public function __construct()
    {
        $this->skipList = new SkipList();
        $this->weights = [];
        $this->totalWeight = 0;
    }
    
    /**
     * 插入带权重的元素
     */
    public function insert($key, $value, float $weight): void
    {
        if (isset($this->weights[$key])) {
            $this->totalWeight -= $this->weights[$key];
        }
        
        $this->skipList->insert($key, $value);
        $this->weights[$key] = $weight;
        $this->totalWeight += $weight;
    }
    
    /**
     * 按权重随机选择元素
     */
    public function weightedRandom()
    {
        if ($this->totalWeight <= 0) {
            return null;
        }
        
        $random = rand() / getrandmax() * $this->totalWeight;
        $current = 0;
        
        foreach ($this->weights as $key => $weight) {
            $current += $weight;
            if ($current >= $random) {
                return ['key' => $key, 'value' => $this->skipList->search($key)];
            }
        }
        
        return null;
    }
    
    /**
     * 获取权重
     */
    public function getWeight($key): ?float
    {
        return $this->weights[$key] ?? null;
    }
    
    /**
     * 获取总权重
     */
    public function getTotalWeight(): float
    {
        return $this->totalWeight;
    }
    
    /**
     * 删除元素
     */
    public function delete($key): bool
    {
        if (isset($this->weights[$key])) {
            $this->totalWeight -= $this->weights[$key];
            unset($this->weights[$key]);
            return $this->skipList->delete($key);
        }
        
        return false;
    }
    
    /**
     * 获取大小
     */
    public function size(): int
    {
        return $this->skipList->size();
    }
}