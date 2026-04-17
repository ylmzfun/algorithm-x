<?php

namespace DataStructures\Linear;

/**
 * LinkedList - 双向链表实现
 * 
 * 思路：
 * 1. 使用节点(Node)存储数据和指针
 * 2. 维护头节点和尾节点的引用
 * 3. 支持双向遍历
 * 4. 动态分配内存，无需预分配
 * 
 * 作用：
 * - 高效的插入和删除操作O(1)
 * - 动态大小，无需预分配内存
 * - 支持双向遍历
 * 
 * 业务场景：
 * 1. 音乐播放器：播放列表，支持前进后退
 * 2. 浏览器历史：页面访问历史，支持前进后退
 * 3. 文本编辑器：撤销/重做功能的操作历史
 * 4. 任务调度：任务队列，频繁插入删除任务
 * 5. 社交媒体：动态时间线，新内容频繁插入
 * 6. 购物车：商品列表，频繁添加删除商品
 */

/**
 * 链表节点类
 */
class ListNode
{
    public $data;
    public ?ListNode $next;
    public ?ListNode $prev;
    
    public function __construct($data)
    {
        $this->data = $data;
        $this->next = null;
        $this->prev = null;
    }
}

class LinkedList
{
    private ?ListNode $head;
    private ?ListNode $tail;
    private int $size;
    
    public function __construct()
    {
        $this->head = null;
        $this->tail = null;
        $this->size = 0;
    }
    
    /**
     * 在链表头部添加元素
     * 时间复杂度：O(1)
     */
    public function addFirst($data): void
    {
        $newNode = new ListNode($data);
        
        if ($this->isEmpty()) {
            $this->head = $this->tail = $newNode;
        } else {
            $newNode->next = $this->head;
            $this->head->prev = $newNode;
            $this->head = $newNode;
        }
        
        $this->size++;
    }
    
    /**
     * 在链表尾部添加元素
     * 时间复杂度：O(1)
     */
    public function addLast($data): void
    {
        $newNode = new ListNode($data);
        
        if ($this->isEmpty()) {
            $this->head = $this->tail = $newNode;
        } else {
            $this->tail->next = $newNode;
            $newNode->prev = $this->tail;
            $this->tail = $newNode;
        }
        
        $this->size++;
    }
    
    /**
     * 在指定位置插入元素
     * 时间复杂度：O(n)
     */
    public function insert(int $index, $data): void
    {
        $this->checkIndexForAdd($index);
        
        if ($index === 0) {
            $this->addFirst($data);
            return;
        }
        
        if ($index === $this->size) {
            $this->addLast($data);
            return;
        }
        
        $newNode = new ListNode($data);
        $current = $this->getNodeAt($index);
        
        $newNode->next = $current;
        $newNode->prev = $current->prev;
        $current->prev->next = $newNode;
        $current->prev = $newNode;
        
        $this->size++;
    }
    
    /**
     * 获取指定位置的元素
     * 时间复杂度：O(n)
     */
    public function get(int $index)
    {
        $this->checkIndex($index);
        return $this->getNodeAt($index)->data;
    }
    
    /**
     * 设置指定位置的元素
     * 时间复杂度：O(n)
     */
    public function set(int $index, $data)
    {
        $this->checkIndex($index);
        $node = $this->getNodeAt($index);
        $oldData = $node->data;
        $node->data = $data;
        return $oldData;
    }
    
    /**
     * 删除头部元素
     * 时间复杂度：O(1)
     */
    public function removeFirst()
    {
        if ($this->isEmpty()) {
            throw new \RuntimeException("List is empty");
        }
        
        $data = $this->head->data;
        
        if ($this->size === 1) {
            $this->head = $this->tail = null;
        } else {
            $this->head = $this->head->next;
            $this->head->prev = null;
        }
        
        $this->size--;
        return $data;
    }
    
    /**
     * 删除尾部元素
     * 时间复杂度：O(1)
     */
    public function removeLast()
    {
        if ($this->isEmpty()) {
            throw new \RuntimeException("List is empty");
        }
        
        $data = $this->tail->data;
        
        if ($this->size === 1) {
            $this->head = $this->tail = null;
        } else {
            $this->tail = $this->tail->prev;
            $this->tail->next = null;
        }
        
        $this->size--;
        return $data;
    }
    
    /**
     * 删除指定位置的元素
     * 时间复杂度：O(n)
     */
    public function remove(int $index)
    {
        $this->checkIndex($index);
        
        if ($index === 0) {
            return $this->removeFirst();
        }
        
        if ($index === $this->size - 1) {
            return $this->removeLast();
        }
        
        $node = $this->getNodeAt($index);
        $data = $node->data;
        
        $node->prev->next = $node->next;
        $node->next->prev = $node->prev;
        
        $this->size--;
        return $data;
    }
    
    /**
     * 删除第一个匹配的元素
     * 时间复杂度：O(n)
     */
    public function removeElement($data): bool
    {
        $current = $this->head;
        
        while ($current !== null) {
            if ($current->data === $data) {
                if ($current === $this->head) {
                    $this->removeFirst();
                } elseif ($current === $this->tail) {
                    $this->removeLast();
                } else {
                    $current->prev->next = $current->next;
                    $current->next->prev = $current->prev;
                    $this->size--;
                }
                return true;
            }
            $current = $current->next;
        }
        
        return false;
    }
    
    /**
     * 查找元素的索引
     * 时间复杂度：O(n)
     */
    public function indexOf($data): int
    {
        $current = $this->head;
        $index = 0;
        
        while ($current !== null) {
            if ($current->data === $data) {
                return $index;
            }
            $current = $current->next;
            $index++;
        }
        
        return -1;
    }
    
    /**
     * 检查是否包含元素
     * 时间复杂度：O(n)
     */
    public function contains($data): bool
    {
        return $this->indexOf($data) !== -1;
    }
    
    /**
     * 获取第一个元素
     */
    public function getFirst()
    {
        if ($this->isEmpty()) {
            throw new \RuntimeException("List is empty");
        }
        return $this->head->data;
    }
    
    /**
     * 获取最后一个元素
     */
    public function getLast()
    {
        if ($this->isEmpty()) {
            throw new \RuntimeException("List is empty");
        }
        return $this->tail->data;
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
     * 清空链表
     */
    public function clear(): void
    {
        $this->head = $this->tail = null;
        $this->size = 0;
    }
    
    /**
     * 转换为数组
     */
    public function toArray(): array
    {
        $result = [];
        $current = $this->head;
        
        while ($current !== null) {
            $result[] = $current->data;
            $current = $current->next;
        }
        
        return $result;
    }
    
    /**
     * 反向转换为数组
     */
    public function toArrayReverse(): array
    {
        $result = [];
        $current = $this->tail;
        
        while ($current !== null) {
            $result[] = $current->data;
            $current = $current->prev;
        }
        
        return $result;
    }
    
    /**
     * 获取指定位置的节点
     */
    private function getNodeAt(int $index): ListNode
    {
        // 优化：从更近的一端开始遍历
        if ($index < $this->size / 2) {
            $current = $this->head;
            for ($i = 0; $i < $index; $i++) {
                $current = $current->next;
            }
        } else {
            $current = $this->tail;
            for ($i = $this->size - 1; $i > $index; $i--) {
                $current = $current->prev;
            }
        }
        
        return $current;
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
}