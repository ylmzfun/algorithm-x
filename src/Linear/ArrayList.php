<?php

namespace DataStructures\Linear;

/**
 * ArrayList - 动态数组实现
 * 
 * 思路：
 * 1. 使用PHP原生数组作为底层存储
 * 2. 维护当前大小和容量
 * 3. 支持动态扩容和缩容
 * 4. 提供随机访问能力
 * 
 * 作用：
 * - 提供O(1)的随机访问
 * - 动态调整大小
 * - 内存连续存储，缓存友好
 * 
 * 业务场景：
 * 1. 电商系统：商品列表展示，支持分页和随机访问
 * 2. 用户管理：用户列表，需要频繁按索引访问
 * 3. 数据分析：存储大量数值数据，需要快速访问
 * 4. 缓存系统：LRU缓存的底层存储
 * 5. 游戏开发：存储玩家排行榜，支持快速查找特定排名
 */
class ArrayList
{
    private array $data;
    private int $size;
    private int $capacity;
    
    public function __construct(int $initialCapacity = 10)
    {
        $this->capacity = max(1, $initialCapacity);
        $this->data = array_fill(0, $this->capacity, null);
        $this->size = 0;
    }
    
    /**
     * 添加元素到末尾
     * 时间复杂度：平均O(1)，最坏O(n)
     */
    public function add($element): void
    {
        $this->ensureCapacity($this->size + 1);
        $this->data[$this->size] = $element;
        $this->size++;
    }
    
    /**
     * 在指定位置插入元素
     * 时间复杂度：O(n)
     */
    public function insert(int $index, $element): void
    {
        $this->checkIndexForAdd($index);
        $this->ensureCapacity($this->size + 1);
        
        // 将元素向后移动
        for ($i = $this->size; $i > $index; $i--) {
            $this->data[$i] = $this->data[$i - 1];
        }
        
        $this->data[$index] = $element;
        $this->size++;
    }
    
    /**
     * 获取指定位置的元素
     * 时间复杂度：O(1)
     */
    public function get(int $index)
    {
        $this->checkIndex($index);
        return $this->data[$index];
    }
    
    /**
     * 设置指定位置的元素
     * 时间复杂度：O(1)
     */
    public function set(int $index, $element)
    {
        $this->checkIndex($index);
        $oldValue = $this->data[$index];
        $this->data[$index] = $element;
        return $oldValue;
    }
    
    /**
     * 删除指定位置的元素
     * 时间复杂度：O(n)
     */
    public function remove(int $index)
    {
        $this->checkIndex($index);
        $oldValue = $this->data[$index];
        
        // 将元素向前移动
        for ($i = $index; $i < $this->size - 1; $i++) {
            $this->data[$i] = $this->data[$i + 1];
        }
        
        $this->size--;
        $this->data[$this->size] = null; // 避免内存泄漏
        
        // 如果使用空间过少，缩容
        if ($this->size > 0 && $this->size <= $this->capacity / 4) {
            $this->resize($this->capacity / 2);
        }
        
        return $oldValue;
    }
    
    /**
     * 查找元素的索引
     * 时间复杂度：O(n)
     */
    public function indexOf($element): int
    {
        for ($i = 0; $i < $this->size; $i++) {
            if ($this->data[$i] === $element) {
                return $i;
            }
        }
        return -1;
    }
    
    /**
     * 检查是否包含元素
     * 时间复杂度：O(n)
     */
    public function contains($element): bool
    {
        return $this->indexOf($element) !== -1;
    }
    
    /**
     * 获取当前大小
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
     * 清空数组
     */
    public function clear(): void
    {
        for ($i = 0; $i < $this->size; $i++) {
            $this->data[$i] = null;
        }
        $this->size = 0;
    }
    
    /**
     * 转换为PHP原生数组
     */
    public function toArray(): array
    {
        return array_slice($this->data, 0, $this->size);
    }
    
    /**
     * 确保容量足够
     */
    private function ensureCapacity(int $minCapacity): void
    {
        if ($minCapacity > $this->capacity) {
            $newCapacity = max($minCapacity, $this->capacity * 2);
            $this->resize($newCapacity);
        }
    }
    
    /**
     * 调整数组大小
     */
    private function resize(int $newCapacity): void
    {
        $newData = array_fill(0, $newCapacity, null);
        for ($i = 0; $i < $this->size; $i++) {
            $newData[$i] = $this->data[$i];
        }
        $this->data = $newData;
        $this->capacity = $newCapacity;
    }
    
    /**
     * 检查索引是否有效
     */
    private function checkIndex(int $index): void
    {
        if ($index < 0 || $index >= $this->size) {
            throw new \OutOfBoundsException("Index: $index, Size: $this->size");
        }
    }
    
    /**
     * 检查插入索引是否有效
     */
    private function checkIndexForAdd(int $index): void
    {
        if ($index < 0 || $index > $this->size) {
            throw new \OutOfBoundsException("Index: $index, Size: $this->size");
        }
    }
    
    /**
     * 获取迭代器
     */
    public function getIterator(): \ArrayIterator
    {
        return new \ArrayIterator($this->toArray());
    }
}