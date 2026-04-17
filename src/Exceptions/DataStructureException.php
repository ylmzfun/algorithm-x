<?php

namespace DataStructures\Exceptions;

/**
 * 数据结构异常基类
 */
class DataStructureException extends \Exception
{
    public function __construct(string $message = "", int $code = 0, \Throwable $previous = null)
    {
        parent::__construct($message, $code, $previous);
    }
}

/**
 * 索引越界异常
 */
class IndexOutOfBoundsException extends DataStructureException
{
    public function __construct(int $index, int $size)
    {
        $message = "Index $index is out of bounds for size $size";
        parent::__construct($message);
    }
}

/**
 * 空容器异常
 */
class EmptyContainerException extends DataStructureException
{
    public function __construct(string $operation = "")
    {
        $message = "Cannot perform operation '$operation' on empty container";
        parent::__construct($message);
    }
}

/**
 * 容器已满异常
 */
class ContainerFullException extends DataStructureException
{
    public function __construct(int $capacity)
    {
        $message = "Container is full (capacity: $capacity)";
        parent::__construct($message);
    }
}

/**
 * 元素未找到异常
 */
class ElementNotFoundException extends DataStructureException
{
    public function __construct($element)
    {
        $message = "Element '$element' not found";
        parent::__construct($message);
    }
}

/**
 * 重复元素异常
 */
class DuplicateElementException extends DataStructureException
{
    public function __construct($element)
    {
        $message = "Duplicate element '$element' not allowed";
        parent::__construct($message);
    }
}

/**
 * 无效操作异常
 */
class InvalidOperationException extends DataStructureException
{
    public function __construct(string $operation, string $reason = "")
    {
        $message = "Invalid operation '$operation'";
        if (!empty($reason)) {
            $message .= ": $reason";
        }
        parent::__construct($message);
    }
}

/**
 * 无效参数异常
 */
class InvalidArgumentException extends DataStructureException
{
    public function __construct(string $parameter, $value, string $expected = "")
    {
        $message = "Invalid argument for parameter '$parameter': $value";
        if (!empty($expected)) {
            $message .= ". Expected: $expected";
        }
        parent::__construct($message);
    }
}

/**
 * 图相关异常
 */
class GraphException extends DataStructureException
{
    public function __construct(string $message)
    {
        parent::__construct($message);
    }
}

/**
 * 顶点不存在异常
 */
class VertexNotFoundException extends GraphException
{
    public function __construct($vertex)
    {
        $message = "Vertex '$vertex' not found in graph";
        parent::__construct($message);
    }
}

/**
 * 边不存在异常
 */
class EdgeNotFoundException extends GraphException
{
    public function __construct($from, $to)
    {
        $message = "Edge from '$from' to '$to' not found";
        parent::__construct($message);
    }
}

/**
 * 环检测异常
 */
class CycleDetectedException extends GraphException
{
    public function __construct()
    {
        $message = "Cycle detected in graph";
        parent::__construct($message);
    }
}

/**
 * 树相关异常
 */
class TreeException extends DataStructureException
{
    public function __construct(string $message)
    {
        parent::__construct($message);
    }
}

/**
 * 节点不存在异常
 */
class NodeNotFoundException extends TreeException
{
    public function __construct($value)
    {
        $message = "Node with value '$value' not found";
        parent::__construct($message);
    }
}

/**
 * 树为空异常
 */
class EmptyTreeException extends TreeException
{
    public function __construct(string $operation = "")
    {
        $message = "Cannot perform operation '$operation' on empty tree";
        parent::__construct($message);
    }
}

/**
 * 哈希表相关异常
 */
class HashTableException extends DataStructureException
{
    public function __construct(string $message)
    {
        parent::__construct($message);
    }
}

/**
 * 键不存在异常
 */
class KeyNotFoundException extends HashTableException
{
    public function __construct($key)
    {
        $message = "Key '$key' not found";
        parent::__construct($message);
    }
}

/**
 * 哈希冲突异常
 */
class HashCollisionException extends HashTableException
{
    public function __construct($key, int $attempts)
    {
        $message = "Hash collision for key '$key' after $attempts attempts";
        parent::__construct($message);
    }
}

/**
 * 缓存相关异常
 */
class CacheException extends DataStructureException
{
    public function __construct(string $message)
    {
        parent::__construct($message);
    }
}

/**
 * 缓存未命中异常
 */
class CacheMissException extends CacheException
{
    public function __construct($key)
    {
        $message = "Cache miss for key '$key'";
        parent::__construct($message);
    }
}

/**
 * 缓存过期异常
 */
class CacheExpiredException extends CacheException
{
    public function __construct($key)
    {
        $message = "Cache entry for key '$key' has expired";
        parent::__construct($message);
    }
}

/**
 * 算法相关异常
 */
class AlgorithmException extends DataStructureException
{
    public function __construct(string $message)
    {
        parent::__construct($message);
    }
}

/**
 * 排序异常
 */
class SortingException extends AlgorithmException
{
    public function __construct(string $algorithm, string $reason = "")
    {
        $message = "Sorting algorithm '$algorithm' failed";
        if (!empty($reason)) {
            $message .= ": $reason";
        }
        parent::__construct($message);
    }
}

/**
 * 搜索异常
 */
class SearchException extends AlgorithmException
{
    public function __construct(string $algorithm, string $reason = "")
    {
        $message = "Search algorithm '$algorithm' failed";
        if (!empty($reason)) {
            $message .= ": $reason";
        }
        parent::__construct($message);
    }
}

/**
 * 内存不足异常
 */
class OutOfMemoryException extends DataStructureException
{
    public function __construct(int $requestedSize, int $availableSize)
    {
        $message = "Out of memory: requested $requestedSize bytes, available $availableSize bytes";
        parent::__construct($message);
    }
}

/**
 * 超时异常
 */
class TimeoutException extends DataStructureException
{
    public function __construct(string $operation, float $timeout)
    {
        $message = "Operation '$operation' timed out after {$timeout}s";
        parent::__construct($message);
    }
}

/**
 * 并发异常
 */
class ConcurrencyException extends DataStructureException
{
    public function __construct(string $message)
    {
        parent::__construct($message);
    }
}

/**
 * 死锁异常
 */
class DeadlockException extends ConcurrencyException
{
    public function __construct()
    {
        $message = "Deadlock detected";
        parent::__construct($message);
    }
}

/**
 * 竞态条件异常
 */
class RaceConditionException extends ConcurrencyException
{
    public function __construct(string $resource)
    {
        $message = "Race condition detected on resource '$resource'";
        parent::__construct($message);
    }
}