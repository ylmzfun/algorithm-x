<?php

namespace DataStructures\Linear;

/**
 * Deque - 双端队列数据结构实现
 * 
 * 思路：
 * 1. 使用循环数组实现
 * 2. 支持在两端进行插入和删除操作
 * 3. 维护front和rear指针
 * 4. 结合了栈和队列的特性
 * 
 * 作用：
 * - 在两端都能高效插入和删除
 * - 可以作为栈或队列使用
 * - 支持滑动窗口操作
 * - 实现某些高级算法的基础
 * 
 * 业务场景：
 * 1. 滑动窗口算法：如滑动窗口最大值问题
 * 2. 撤销重做系统：支持前进后退的操作历史
 * 3. 浏览器历史：支持前进后退导航
 * 4. 游戏开发：角色移动轨迹记录
 * 5. 数据流处理：双向数据缓冲
 * 6. 工作窃取算法：多线程任务调度
 * 7. 回文检查：从两端向中间检查
 * 8. LRU缓存：最近最少使用缓存实现
 * 9. 表达式求值：需要双向访问的算法
 * 10. 图算法：双向BFS搜索
 */
class Deque
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
        $this->rear = 0;
        $this->size = 0;
    }
    
    /**
     * 在前端添加元素
     * 时间复杂度：平均O(1)，最坏O(n)
     */
    public function addFirst($element): void
    {
        $this->ensureCapacity();
        $this->front = ($this->front - 1 + $this->capacity) % $this->capacity;
        $this->elements[$this->front] = $element;
        $this->size++;
    }
    
    /**
     * 在后端添加元素
     * 时间复杂度：平均O(1)，最坏O(n)
     */
    public function addLast($element): void
    {
        $this->ensureCapacity();
        $this->elements[$this->rear] = $element;
        $this->rear = ($this->rear + 1) % $this->capacity;
        $this->size++;
    }
    
    /**
     * 从前端删除元素
     * 时间复杂度：O(1)
     */
    public function removeFirst()
    {
        if ($this->isEmpty()) {
            throw new \RuntimeException("Deque is empty");
        }
        
        $element = $this->elements[$this->front];
        $this->elements[$this->front] = null;
        $this->front = ($this->front + 1) % $this->capacity;
        $this->size--;
        
        $this->shrinkIfNeeded();
        return $element;
    }
    
    /**
     * 从后端删除元素
     * 时间复杂度：O(1)
     */
    public function removeLast()
    {
        if ($this->isEmpty()) {
            throw new \RuntimeException("Deque is empty");
        }
        
        $this->rear = ($this->rear - 1 + $this->capacity) % $this->capacity;
        $element = $this->elements[$this->rear];
        $this->elements[$this->rear] = null;
        $this->size--;
        
        $this->shrinkIfNeeded();
        return $element;
    }
    
    /**
     * 查看前端元素（不删除）
     * 时间复杂度：O(1)
     */
    public function peekFirst()
    {
        if ($this->isEmpty()) {
            throw new \RuntimeException("Deque is empty");
        }
        
        return $this->elements[$this->front];
    }
    
    /**
     * 查看后端元素（不删除）
     * 时间复杂度：O(1)
     */
    public function peekLast()
    {
        if ($this->isEmpty()) {
            throw new \RuntimeException("Deque is empty");
        }
        
        $lastIndex = ($this->rear - 1 + $this->capacity) % $this->capacity;
        return $this->elements[$lastIndex];
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
     * 获取大小
     * 时间复杂度：O(1)
     */
    public function size(): int
    {
        return $this->size;
    }
    
    /**
     * 清空双端队列
     * 时间复杂度：O(n)
     */
    public function clear(): void
    {
        for ($i = 0; $i < $this->capacity; $i++) {
            $this->elements[$i] = null;
        }
        $this->front = 0;
        $this->rear = 0;
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
     * 转换为数组
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
     * 获取容量
     */
    public function capacity(): int
    {
        return $this->capacity;
    }
    
    // 栈操作接口
    public function push($element): void { $this->addLast($element); }
    public function pop() { return $this->removeLast(); }
    public function top() { return $this->peekLast(); }
    
    // 队列操作接口
    public function enqueue($element): void { $this->addLast($element); }
    public function dequeue() { return $this->removeFirst(); }
    public function front() { return $this->peekFirst(); }
    
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
     * 如果需要则缩容
     */
    private function shrinkIfNeeded(): void
    {
        if ($this->size > 0 && $this->size <= $this->capacity / 4) {
            $this->resize(max(1, $this->capacity / 2));
        }
    }
    
    /**
     * 调整容量
     */
    private function resize(int $newCapacity): void
    {
        $newElements = array_fill(0, $newCapacity, null);
        
        for ($i = 0; $i < $this->size; $i++) {
            $oldIndex = ($this->front + $i) % $this->capacity;
            $newElements[$i] = $this->elements[$oldIndex];
        }
        
        $this->elements = $newElements;
        $this->capacity = $newCapacity;
        $this->front = 0;
        $this->rear = $this->size;
    }
}

/**
 * MonotonicDeque - 单调双端队列
 * 
 * 思路：
 * 1. 维护队列中元素的单调性
 * 2. 可以是单调递增或单调递减
 * 3. 用于解决滑动窗口最值问题
 * 
 * 业务场景：
 * 1. 滑动窗口最大值/最小值
 * 2. 股票价格分析：滑动窗口内的最高/最低价
 * 3. 网络监控：时间窗口内的峰值检测
 * 4. 游戏开发：技能冷却时间管理
 */
class MonotonicDeque extends Deque
{
    private $comparator;
    private bool $increasing;
    
    public function __construct(bool $increasing = true, callable $comparator = null)
    {
        parent::__construct();
        $this->increasing = $increasing;
        $this->comparator = $comparator ?: function($a, $b) {
            return $a <=> $b;
        };
    }
    
    /**
     * 添加元素并维护单调性
     */
    public function push($element): void
    {
        // 移除破坏单调性的元素
        while (!$this->isEmpty()) {
            $last = $this->peekLast();
            $cmp = call_user_func($this->comparator, $last, $element);
            
            if ($this->increasing && $cmp > 0) {
                $this->removeLast();
            } elseif (!$this->increasing && $cmp < 0) {
                $this->removeLast();
            } else {
                break;
            }
        }
        
        $this->addLast($element);
    }
    
    /**
     * 获取当前最值
     */
    public function getOptimal()
    {
        if ($this->isEmpty()) {
            throw new \RuntimeException("MonotonicDeque is empty");
        }
        
        return $this->peekFirst();
    }
    
    /**
     * 滑动窗口最大值问题的解决方案
     */
    public static function slidingWindowMaximum(array $nums, int $k): array
    {
        if (empty($nums) || $k <= 0) {
            return [];
        }
        
        $deque = new self(false); // 单调递减队列
        $result = [];
        
        for ($i = 0; $i < count($nums); $i++) {
            // 移除超出窗口的元素
            while (!$deque->isEmpty() && $deque->peekFirst()['index'] <= $i - $k) {
                $deque->removeFirst();
            }
            
            // 添加当前元素
            $deque->push(['value' => $nums[$i], 'index' => $i]);
            
            // 如果窗口大小达到k，记录最大值
            if ($i >= $k - 1) {
                $result[] = $deque->getOptimal()['value'];
            }
        }
        
        return $result;
    }
}