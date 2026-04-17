<?php

namespace DataStructures\Linear;

/**
 * Queue - 队列数据结构实现
 * 
 * 思路：
 * 1. 使用循环数组实现，避免频繁的数组移动
 * 2. 维护front和rear指针
 * 3. 遵循FIFO（First In First Out）原则
 * 4. 支持动态扩容和缩容
 * 
 * 作用：
 * - 实现先进先出的数据访问模式
 * - 缓冲数据流
 * - 任务调度和处理
 * - 广度优先搜索的基础
 * 
 * 业务场景：
 * 1. 任务调度系统：按顺序处理用户提交的任务
 * 2. 消息队列：异步消息处理，如邮件发送队列
 * 3. 打印队列：按顺序处理打印任务
 * 4. 网络请求处理：Web服务器的请求队列
 * 5. 广度优先搜索：图算法和树遍历
 * 6. 缓存系统：LRU缓存的实现基础
 * 7. 生产者消费者模式：数据缓冲区
 * 8. 游戏开发：事件处理队列
 * 9. 客服系统：客户排队等待服务
 * 10. 数据流处理：实时数据处理管道
 */
class Queue
{
    private array $elements;
    private int $front;
    private int $rear;
    private int $size;
    private int $capacity;
    
    public function __construct(int $initialCapacity = 10)
    {
        $this->capacity = max(1, $initialCapacity);
        $this->elements = array_fill(0, $this->capacity, null);
        $this->front = 0;
        $this->rear = -1;
        $this->size = 0;
    }
    
    /**
     * 入队操作
     * 时间复杂度：平均O(1)，最坏O(n)
     */
    public function enqueue($element): void
    {
        $this->ensureCapacity();
        $this->rear = ($this->rear + 1) % $this->capacity;
        $this->elements[$this->rear] = $element;
        $this->size++;
    }
    
    /**
     * 出队操作
     * 时间复杂度：O(1)
     */
    public function dequeue()
    {
        if ($this->isEmpty()) {
            throw new \RuntimeException("Queue is empty");
        }
        
        $element = $this->elements[$this->front];
        $this->elements[$this->front] = null; // 避免内存泄漏
        $this->front = ($this->front + 1) % $this->capacity;
        $this->size--;
        
        // 如果使用空间过少，缩容
        if ($this->size > 0 && $this->size <= $this->capacity / 4) {
            $this->resize($this->capacity / 2);
        }
        
        return $element;
    }
    
    /**
     * 查看队首元素（不删除）
     * 时间复杂度：O(1)
     */
    public function front()
    {
        if ($this->isEmpty()) {
            throw new \RuntimeException("Queue is empty");
        }
        
        return $this->elements[$this->front];
    }
    
    /**
     * 查看队尾元素（不删除）
     * 时间复杂度：O(1)
     */
    public function rear()
    {
        if ($this->isEmpty()) {
            throw new \RuntimeException("Queue is empty");
        }
        
        return $this->elements[$this->rear];
    }
    
    /**
     * 检查队列是否为空
     * 时间复杂度：O(1)
     */
    public function isEmpty(): bool
    {
        return $this->size === 0;
    }
    
    /**
     * 获取队列的大小
     * 时间复杂度：O(1)
     */
    public function size(): int
    {
        return $this->size;
    }
    
    /**
     * 清空队列
     * 时间复杂度：O(n)
     */
    public function clear(): void
    {
        for ($i = 0; $i < $this->capacity; $i++) {
            $this->elements[$i] = null;
        }
        $this->front = 0;
        $this->rear = -1;
        $this->size = 0;
    }
    
    /**
     * 检查是否包含指定元素
     * 时间复杂度：O(n)
     */
    public function contains($element): bool
    {
        for ($i = 0; $i < $this->size; $i++) {
            $index = ($this->front + $i) % $this->capacity;
            if ($this->elements[$index] === $element) {
                return true;
            }
        }
        return false;
    }
    
    /**
     * 转换为数组（队首在数组开头）
     * 时间复杂度：O(n)
     */
    public function toArray(): array
    {
        $result = [];
        for ($i = 0; $i < $this->size; $i++) {
            $index = ($this->front + $i) % $this->capacity;
            $result[] = $this->elements[$index];
        }
        return $result;
    }
    
    /**
     * 获取队列的容量
     */
    public function capacity(): int
    {
        return $this->capacity;
    }
    
    /**
     * 确保容量足够
     */
    private function ensureCapacity(): void
    {
        if ($this->size >= $this->capacity) {
            $this->resize($this->capacity * 2);
        }
    }
    
    /**
     * 调整队列的容量
     */
    private function resize(int $newCapacity): void
    {
        $newElements = array_fill(0, $newCapacity, null);
        
        // 复制元素到新数组
        for ($i = 0; $i < $this->size; $i++) {
            $oldIndex = ($this->front + $i) % $this->capacity;
            $newElements[$i] = $this->elements[$oldIndex];
        }
        
        $this->elements = $newElements;
        $this->capacity = $newCapacity;
        $this->front = 0;
        $this->rear = $this->size - 1;
    }
}

/**
 * PriorityQueue - 优先队列实现
 * 
 * 思路：
 * 1. 基于最小堆实现
 * 2. 每个元素都有优先级
 * 3. 优先级高的元素先出队
 * 4. 支持自定义比较函数
 * 
 * 业务场景：
 * 1. 任务调度：根据优先级处理任务
 * 2. Dijkstra算法：最短路径算法
 * 3. A*搜索算法：启发式搜索
 * 4. 事件驱动系统：按时间顺序处理事件
 * 5. 医院急诊：按病情严重程度排队
 */
class PriorityQueue
{
    private array $heap;
    private int $size;
    private $comparator;
    
    public function __construct(callable $comparator = null)
    {
        $this->heap = [];
        $this->size = 0;
        $this->comparator = $comparator ?: function($a, $b) {
            return $a <=> $b; // 默认最小堆
        };
    }
    
    /**
     * 入队操作
     * 时间复杂度：O(log n)
     */
    public function enqueue($element): void
    {
        $this->heap[$this->size] = $element;
        $this->heapifyUp($this->size);
        $this->size++;
    }
    
    /**
     * 出队操作
     * 时间复杂度：O(log n)
     */
    public function dequeue()
    {
        if ($this->isEmpty()) {
            throw new \RuntimeException("Priority queue is empty");
        }
        
        $min = $this->heap[0];
        $this->heap[0] = $this->heap[$this->size - 1];
        $this->size--;
        
        if ($this->size > 0) {
            $this->heapifyDown(0);
        }
        
        return $min;
    }
    
    /**
     * 查看队首元素
     * 时间复杂度：O(1)
     */
    public function peek()
    {
        if ($this->isEmpty()) {
            throw new \RuntimeException("Priority queue is empty");
        }
        
        return $this->heap[0];
    }
    
    /**
     * 检查是否为空
     */
    public function isEmpty(): bool
    {
        return $this->size === 0;
    }
    
    /**
     * 获取大小
     */
    public function size(): int
    {
        return $this->size;
    }
    
    /**
     * 向上调整堆
     */
    private function heapifyUp(int $index): void
    {
        while ($index > 0) {
            $parentIndex = intval(($index - 1) / 2);
            
            if (call_user_func($this->comparator, $this->heap[$index], $this->heap[$parentIndex]) >= 0) {
                break;
            }
            
            $this->swap($index, $parentIndex);
            $index = $parentIndex;
        }
    }
    
    /**
     * 向下调整堆
     */
    private function heapifyDown(int $index): void
    {
        while (true) {
            $leftChild = 2 * $index + 1;
            $rightChild = 2 * $index + 2;
            $smallest = $index;
            
            if ($leftChild < $this->size && 
                call_user_func($this->comparator, $this->heap[$leftChild], $this->heap[$smallest]) < 0) {
                $smallest = $leftChild;
            }
            
            if ($rightChild < $this->size && 
                call_user_func($this->comparator, $this->heap[$rightChild], $this->heap[$smallest]) < 0) {
                $smallest = $rightChild;
            }
            
            if ($smallest === $index) {
                break;
            }
            
            $this->swap($index, $smallest);
            $index = $smallest;
        }
    }
    
    /**
     * 交换两个元素
     */
    private function swap(int $i, int $j): void
    {
        $temp = $this->heap[$i];
        $this->heap[$i] = $this->heap[$j];
        $this->heap[$j] = $temp;
    }
}