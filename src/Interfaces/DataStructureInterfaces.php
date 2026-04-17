<?php

namespace DataStructures\Interfaces;

/**
 * 容器接口 - 所有数据结构的基础接口
 */
interface ContainerInterface
{
    /**
     * 获取容器大小
     */
    public function size(): int;
    
    /**
     * 检查容器是否为空
     */
    public function isEmpty(): bool;
    
    /**
     * 清空容器
     */
    public function clear(): void;
    
    /**
     * 转换为数组
     */
    public function toArray(): array;
}

/**
 * 集合接口 - 用于存储元素的容器
 */
interface CollectionInterface extends ContainerInterface
{
    /**
     * 添加元素
     */
    public function add($element): bool;
    
    /**
     * 移除元素
     */
    public function remove($element): bool;
    
    /**
     * 检查是否包含元素
     */
    public function contains($element): bool;
}

/**
 * 列表接口 - 有序集合
 */
interface ListInterface extends CollectionInterface
{
    /**
     * 在指定位置插入元素
     */
    public function insert(int $index, $element): void;
    
    /**
     * 获取指定位置的元素
     */
    public function get(int $index);
    
    /**
     * 设置指定位置的元素
     */
    public function set(int $index, $element): void;
    
    /**
     * 移除指定位置的元素
     */
    public function removeAt(int $index);
    
    /**
     * 获取元素的索引
     */
    public function indexOf($element): int;
}

/**
 * 栈接口 - LIFO (后进先出) 数据结构
 */
interface StackInterface extends ContainerInterface
{
    /**
     * 压入元素
     */
    public function push($element): void;
    
    /**
     * 弹出元素
     */
    public function pop();
    
    /**
     * 查看栈顶元素
     */
    public function peek();
}

/**
 * 队列接口 - FIFO (先进先出) 数据结构
 */
interface QueueInterface extends ContainerInterface
{
    /**
     * 入队
     */
    public function enqueue($element): void;
    
    /**
     * 出队
     */
    public function dequeue();
    
    /**
     * 查看队首元素
     */
    public function front();
}

/**
 * 双端队列接口
 */
interface DequeInterface extends QueueInterface
{
    /**
     * 在前端添加元素
     */
    public function addFirst($element): void;
    
    /**
     * 在后端添加元素
     */
    public function addLast($element): void;
    
    /**
     * 移除前端元素
     */
    public function removeFirst();
    
    /**
     * 移除后端元素
     */
    public function removeLast();
    
    /**
     * 查看前端元素
     */
    public function peekFirst();
    
    /**
     * 查看后端元素
     */
    public function peekLast();
}

/**
 * 优先队列接口
 */
interface PriorityQueueInterface extends ContainerInterface
{
    /**
     * 插入元素
     */
    public function insert($element, int $priority): void;
    
    /**
     * 提取最高优先级元素
     */
    public function extract();
    
    /**
     * 查看最高优先级元素
     */
    public function peek();
    
    /**
     * 改变元素优先级
     */
    public function changePriority($element, int $newPriority): bool;
}

/**
 * 堆接口
 */
interface HeapInterface extends ContainerInterface
{
    /**
     * 插入元素
     */
    public function insert($element): void;
    
    /**
     * 提取根元素
     */
    public function extract();
    
    /**
     * 查看根元素
     */
    public function peek();
    
    /**
     * 堆化操作
     */
    public function heapify(): void;
}

/**
 * 树接口
 */
interface TreeInterface extends ContainerInterface
{
    /**
     * 插入节点
     */
    public function insert($value): void;
    
    /**
     * 删除节点
     */
    public function delete($value): bool;
    
    /**
     * 搜索节点
     */
    public function search($value): bool;
    
    /**
     * 获取根节点
     */
    public function getRoot();
    
    /**
     * 获取树的高度
     */
    public function getHeight(): int;
}

/**
 * 二叉搜索树接口
 */
interface BinarySearchTreeInterface extends TreeInterface
{
    /**
     * 中序遍历
     */
    public function inorderTraversal(): array;
    
    /**
     * 前序遍历
     */
    public function preorderTraversal(): array;
    
    /**
     * 后序遍历
     */
    public function postorderTraversal(): array;
    
    /**
     * 查找最小值
     */
    public function findMin();
    
    /**
     * 查找最大值
     */
    public function findMax();
}

/**
 * 图接口
 */
interface GraphInterface extends ContainerInterface
{
    /**
     * 添加顶点
     */
    public function addVertex($vertex): void;
    
    /**
     * 移除顶点
     */
    public function removeVertex($vertex): bool;
    
    /**
     * 添加边
     */
    public function addEdge($from, $to): void;
    
    /**
     * 移除边
     */
    public function removeEdge($from, $to): bool;
    
    /**
     * 检查是否存在边
     */
    public function hasEdge($from, $to): bool;
    
    /**
     * 获取所有顶点
     */
    public function getVertices(): array;
    
    /**
     * 获取邻居顶点
     */
    public function getNeighbors($vertex): array;
    
    /**
     * 获取顶点度数
     */
    public function getDegree($vertex): int;
}

/**
 * 加权图接口
 */
interface WeightedGraphInterface extends GraphInterface
{
    /**
     * 添加加权边
     */
    public function addWeightedEdge($from, $to, float $weight): void;
    
    /**
     * 获取边的权重
     */
    public function getWeight($from, $to): ?float;
    
    /**
     * 设置边的权重
     */
    public function setWeight($from, $to, float $weight): bool;
}

/**
 * 哈希表接口
 */
interface HashTableInterface extends ContainerInterface
{
    /**
     * 存储键值对
     */
    public function put($key, $value): void;
    
    /**
     * 获取值
     */
    public function get($key);
    
    /**
     * 移除键值对
     */
    public function remove($key): bool;
    
    /**
     * 检查是否包含键
     */
    public function containsKey($key): bool;
    
    /**
     * 获取所有键
     */
    public function keys(): array;
    
    /**
     * 获取所有值
     */
    public function values(): array;
}

/**
 * 缓存接口
 */
interface CacheInterface extends ContainerInterface
{
    /**
     * 存储缓存项
     */
    public function put($key, $value, int $ttl = 0): void;
    
    /**
     * 获取缓存项
     */
    public function get($key);
    
    /**
     * 删除缓存项
     */
    public function delete($key): bool;
    
    /**
     * 检查缓存项是否存在
     */
    public function has($key): bool;
    
    /**
     * 获取缓存命中率
     */
    public function getHitRate(): float;
}

/**
 * 布隆过滤器接口
 */
interface BloomFilterInterface extends ContainerInterface
{
    /**
     * 添加元素
     */
    public function add($element): void;
    
    /**
     * 检查元素是否可能存在
     */
    public function mightContain($element): bool;
    
    /**
     * 获取误判率
     */
    public function getFalsePositiveRate(): float;
}

/**
 * 前缀树接口
 */
interface TrieInterface extends ContainerInterface
{
    /**
     * 插入单词
     */
    public function insert(string $word): void;
    
    /**
     * 搜索单词
     */
    public function search(string $word): bool;
    
    /**
     * 检查前缀是否存在
     */
    public function startsWith(string $prefix): bool;
    
    /**
     * 删除单词
     */
    public function delete(string $word): bool;
    
    /**
     * 获取所有以指定前缀开始的单词
     */
    public function getWordsWithPrefix(string $prefix): array;
}

/**
 * 跳表接口
 */
interface SkipListInterface extends ContainerInterface
{
    /**
     * 插入键值对
     */
    public function insert($key, $value): void;
    
    /**
     * 搜索键
     */
    public function search($key): bool;
    
    /**
     * 删除键
     */
    public function delete($key): bool;
    
    /**
     * 范围查询
     */
    public function rangeQuery($minKey, $maxKey): array;
}

/**
 * 比较器接口
 */
interface ComparatorInterface
{
    /**
     * 比较两个元素
     * 返回值: < 0 如果 $a < $b, 0 如果 $a == $b, > 0 如果 $a > $b
     */
    public function compare($a, $b): int;
}

/**
 * 哈希函数接口
 */
interface HashFunctionInterface
{
    /**
     * 计算哈希值
     */
    public function hash($key): int;
}

/**
 * 迭代器接口扩展
 */
interface DataStructureIteratorInterface extends \Iterator
{
    /**
     * 检查是否有下一个元素
     */
    public function hasNext(): bool;
    
    /**
     * 重置迭代器
     */
    public function reset(): void;
}

/**
 * 可序列化接口
 */
interface SerializableDataStructureInterface
{
    /**
     * 序列化为字符串
     */
    public function serialize(): string;
    
    /**
     * 从字符串反序列化
     */
    public function unserialize(string $data): void;
    
    /**
     * 转换为JSON
     */
    public function toJson(): string;
    
    /**
     * 从JSON创建
     */
    public static function fromJson(string $json): self;
}

/**
 * 可克隆接口
 */
interface CloneableDataStructureInterface
{
    /**
     * 深度克隆
     */
    public function deepClone(): self;
    
    /**
     * 浅克隆
     */
    public function shallowClone(): self;
}

/**
 * 线程安全接口
 */
interface ThreadSafeInterface
{
    /**
     * 获取锁
     */
    public function lock(): void;
    
    /**
     * 释放锁
     */
    public function unlock(): void;
    
    /**
     * 尝试获取锁
     */
    public function tryLock(int $timeout = 0): bool;
}