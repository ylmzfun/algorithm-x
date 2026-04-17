<?php

namespace DataStructures\Tree;

/**
 * Heap - 堆数据结构实现
 * 
 * 思路：
 * 1. 基于完全二叉树实现
 * 2. 使用数组存储，利用索引关系表示父子关系
 * 3. 支持最大堆和最小堆
 * 4. 维护堆的性质：父节点与子节点的大小关系
 * 
 * 作用：
 * - 实现优先队列
 * - 堆排序算法的基础
 * - 快速找到最大值或最小值
 * - 动态维护数据的优先级
 * 
 * 业务场景：
 * 1. 任务调度系统：按优先级处理任务
 * 2. 操作系统：进程调度，按优先级分配CPU时间
 * 3. 网络路由：Dijkstra算法中的优先队列
 * 4. 数据流处理：实时获取最大/最小值
 * 5. 游戏开发：AI决策系统，按评分选择最优策略
 * 6. 搜索引擎：按相关性排序搜索结果
 * 7. 医院系统：急诊科按病情严重程度排队
 * 8. 股票交易：按价格优先级匹配买卖订单
 * 9. 缓存系统：LFU缓存的实现
 * 10. 数据挖掘：Top-K问题的解决
 */
class Heap
{
    protected array $heap;
    protected int $size;
    protected $comparator;
    protected bool $isMaxHeap;
    
    public function __construct(bool $isMaxHeap = true, callable $comparator = null)
    {
        $this->heap = [];
        $this->size = 0;
        $this->isMaxHeap = $isMaxHeap;
        $this->comparator = $comparator ?: function($a, $b) {
            return $a <=> $b;
        };
    }
    
    /**
     * 插入元素
     * 时间复杂度：O(log n)
     */
    public function insert($element): void
    {
        $this->heap[$this->size] = $element;
        $this->heapifyUp($this->size);
        $this->size++;
    }
    
    /**
     * 删除并返回堆顶元素
     * 时间复杂度：O(log n)
     */
    public function extract()
    {
        if ($this->isEmpty()) {
            throw new \RuntimeException("Heap is empty");
        }
        
        $root = $this->heap[0];
        $this->heap[0] = $this->heap[$this->size - 1];
        $this->size--;
        
        if ($this->size > 0) {
            $this->heapifyDown(0);
        }
        
        return $root;
    }
    
    /**
     * 查看堆顶元素（不删除）
     * 时间复杂度：O(1)
     */
    public function peek()
    {
        if ($this->isEmpty()) {
            throw new \RuntimeException("Heap is empty");
        }
        
        return $this->heap[0];
    }
    
    /**
     * 检查堆是否为空
     */
    public function isEmpty(): bool
    {
        return $this->size === 0;
    }
    
    /**
     * 获取堆的大小
     */
    public function size(): int
    {
        return $this->size;
    }
    
    /**
     * 清空堆
     */
    public function clear(): void
    {
        $this->heap = [];
        $this->size = 0;
    }
    
    /**
     * 批量构建堆
     * 时间复杂度：O(n)
     */
    public function buildHeap(array $elements): void
    {
        $this->heap = $elements;
        $this->size = count($elements);
        
        // 从最后一个非叶子节点开始向上调整
        for ($i = intval($this->size / 2) - 1; $i >= 0; $i--) {
            $this->heapifyDown($i);
        }
    }
    
    /**
     * 向上调整堆
     */
    protected function heapifyUp(int $index): void
    {
        while ($index > 0) {
            $parentIndex = intval(($index - 1) / 2);
            
            if (!$this->shouldSwap($index, $parentIndex)) {
                break;
            }
            
            $this->swap($index, $parentIndex);
            $index = $parentIndex;
        }
    }
    
    /**
     * 向下调整堆
     */
    protected function heapifyDown(int $index): void
    {
        while (true) {
            $targetIndex = $index;
            $leftChild = 2 * $index + 1;
            $rightChild = 2 * $index + 2;
            
            // 找到应该在顶部的元素
            if ($leftChild < $this->size && $this->shouldSwap($leftChild, $targetIndex)) {
                $targetIndex = $leftChild;
            }
            
            if ($rightChild < $this->size && $this->shouldSwap($rightChild, $targetIndex)) {
                $targetIndex = $rightChild;
            }
            
            if ($targetIndex === $index) {
                break;
            }
            
            $this->swap($index, $targetIndex);
            $index = $targetIndex;
        }
    }
    
    /**
     * 判断是否应该交换两个元素
     */
    private function shouldSwap(int $childIndex, int $parentIndex): bool
    {
        $cmp = call_user_func($this->comparator, $this->heap[$childIndex], $this->heap[$parentIndex]);
        return $this->isMaxHeap ? $cmp > 0 : $cmp < 0;
    }
    
    /**
     * 交换两个元素
     */
    protected function swap(int $i, int $j): void
    {
        $temp = $this->heap[$i];
        $this->heap[$i] = $this->heap[$j];
        $this->heap[$j] = $temp;
    }
    
    /**
     * 获取父节点索引
     */
    private function getParentIndex(int $index): int
    {
        return intval(($index - 1) / 2);
    }
    
    /**
     * 获取左子节点索引
     */
    private function getLeftChildIndex(int $index): int
    {
        return 2 * $index + 1;
    }
    
    /**
     * 获取右子节点索引
     */
    private function getRightChildIndex(int $index): int
    {
        return 2 * $index + 2;
    }
    
    /**
     * 验证堆的性质
     */
    public function isValidHeap(): bool
    {
        for ($i = 0; $i < $this->size; $i++) {
            $leftChild = $this->getLeftChildIndex($i);
            $rightChild = $this->getRightChildIndex($i);
            
            if ($leftChild < $this->size && $this->shouldSwap($leftChild, $i)) {
                return false;
            }
            
            if ($rightChild < $this->size && $this->shouldSwap($rightChild, $i)) {
                return false;
            }
        }
        
        return true;
    }
    
    /**
     * 转换为数组
     */
    public function toArray(): array
    {
        return array_slice($this->heap, 0, $this->size);
    }
    
    /**
     * 堆排序
     * 时间复杂度：O(n log n)
     */
    public static function heapSort(array $arr, bool $ascending = true): array
    {
        $heap = new self(!$ascending); // 升序用最大堆，降序用最小堆
        $heap->buildHeap($arr);
        
        $result = [];
        while (!$heap->isEmpty()) {
            $result[] = $heap->extract();
        }
        
        return $result;
    }
    
    /**
     * 查找Top K个元素
     * 时间复杂度：O(n log k)
     */
    public static function findTopK(array $arr, int $k, bool $largest = true): array
    {
        if ($k <= 0 || empty($arr)) {
            return [];
        }
        
        $k = min($k, count($arr));
        $heap = new self(!$largest); // 找最大的k个用最小堆，找最小的k个用最大堆
        
        foreach ($arr as $element) {
            if ($heap->size() < $k) {
                $heap->insert($element);
            } else {
                $top = $heap->peek();
                $cmp = $element <=> $top;
                
                if (($largest && $cmp > 0) || (!$largest && $cmp < 0)) {
                    $heap->extract();
                    $heap->insert($element);
                }
            }
        }
        
        return $heap->toArray();
    }
    
    /**
     * 合并两个堆
     */
    public function merge(Heap $other): Heap
    {
        if ($this->isMaxHeap !== $other->isMaxHeap) {
            throw new \InvalidArgumentException("Cannot merge heaps of different types");
        }
        
        $merged = new self($this->isMaxHeap, $this->comparator);
        $elements = array_merge($this->toArray(), $other->toArray());
        $merged->buildHeap($elements);
        
        return $merged;
    }
    
    /**
     * 获取堆的高度
     */
    public function height(): int
    {
        if ($this->size === 0) {
            return -1;
        }
        
        return intval(log($this->size, 2));
    }
    
    /**
     * 检查是否包含指定元素
     * 时间复杂度：O(n)
     */
    public function contains($element): bool
    {
        for ($i = 0; $i < $this->size; $i++) {
            if ($this->heap[$i] === $element) {
                return true;
            }
        }
        return false;
    }
}

/**
 * MinHeap - 最小堆
 */
class MinHeap extends Heap
{
    public function __construct(callable $comparator = null)
    {
        parent::__construct(false, $comparator);
    }
}

/**
 * MaxHeap - 最大堆
 */
class MaxHeap extends Heap
{
    public function __construct(callable $comparator = null)
    {
        parent::__construct(true, $comparator);
    }
}

/**
 * IndexedHeap - 索引堆（支持修改元素优先级）
 * 
 * 业务场景：
 * 1. Dijkstra算法：需要修改顶点的距离值
 * 2. Prim算法：需要修改顶点的权重
 * 3. 任务调度：需要动态调整任务优先级
 */
class IndexedHeap extends Heap
{
    private array $indexMap; // 元素到堆索引的映射
    private array $reverseMap; // 堆索引到元素的映射
    
    public function __construct(bool $isMaxHeap = true, callable $comparator = null)
    {
        parent::__construct($isMaxHeap, $comparator);
        $this->indexMap = [];
        $this->reverseMap = [];
    }
    
    /**
     * 插入带索引的元素
     */
    public function insertWithIndex($key, $value): void
    {
        if (isset($this->indexMap[$key])) {
            throw new \InvalidArgumentException("Key already exists: $key");
        }
        
        $heapIndex = $this->size();
        $this->indexMap[$key] = $heapIndex;
        $this->reverseMap[$heapIndex] = $key;
        
        parent::insert($value);
    }
    
    /**
     * 更新元素的值
     */
    public function updateValue($key, $newValue): void
    {
        if (!isset($this->indexMap[$key])) {
            throw new \InvalidArgumentException("Key not found: $key");
        }
        
        $heapIndex = $this->indexMap[$key];
        $oldValue = $this->heap[$heapIndex];
        $this->heap[$heapIndex] = $newValue;
        
        // 根据新值调整堆
        $cmp = call_user_func($this->comparator, $newValue, $oldValue);
        if (($this->isMaxHeap && $cmp > 0) || (!$this->isMaxHeap && $cmp < 0)) {
            $this->heapifyUp($heapIndex);
        } else {
            $this->heapifyDown($heapIndex);
        }
    }
    
    /**
     * 检查是否包含指定键
     */
    public function containsKey($key): bool
    {
        return isset($this->indexMap[$key]);
    }
    
    /**
     * 获取指定键的值
     */
    public function getValue($key)
    {
        if (!isset($this->indexMap[$key])) {
            throw new \InvalidArgumentException("Key not found: $key");
        }
        
        $heapIndex = $this->indexMap[$key];
        return $this->heap[$heapIndex];
    }
    
    /**
     * 重写交换方法以维护索引映射
     */
    protected function swap(int $i, int $j): void
    {
        // 交换索引映射
        $keyI = $this->reverseMap[$i];
        $keyJ = $this->reverseMap[$j];
        
        $this->indexMap[$keyI] = $j;
        $this->indexMap[$keyJ] = $i;
        
        $this->reverseMap[$i] = $keyJ;
        $this->reverseMap[$j] = $keyI;
        
        // 交换堆中的值
        parent::swap($i, $j);
    }
}