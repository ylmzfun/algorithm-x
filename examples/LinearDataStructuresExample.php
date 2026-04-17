<?php

require_once __DIR__ . '/../vendor/autoload.php';

use DataStructures\Linear\ArrayList;
use DataStructures\Linear\LinkedList;
use DataStructures\Linear\Stack;
use DataStructures\Linear\Queue;
use DataStructures\Linear\PriorityQueue;
use DataStructures\Linear\Deque;
use DataStructures\Linear\MonotonicDeque;

/**
 * 线性数据结构使用示例
 */

echo "=== 线性数据结构示例 ===\n\n";

// 1. ArrayList 示例
echo "1. ArrayList 示例:\n";
$arrayList = new ArrayList();
$arrayList->add("Apple");
$arrayList->add("Banana");
$arrayList->add("Cherry");
$arrayList->insert(1, "Blueberry");

echo "ArrayList 内容: " . implode(", ", $arrayList->toArray()) . "\n";
echo "大小: {$arrayList->size()}\n";
echo "获取索引1的元素: {$arrayList->get(1)}\n";
echo "移除索引2的元素: {$arrayList->remove(2)}\n";
echo "移除后: " . implode(", ", $arrayList->toArray()) . "\n\n";

// 2. LinkedList 示例
echo "2. LinkedList 示例:\n";
$linkedList = new LinkedList();
$linkedList->addLast(10);
$linkedList->addLast(20);
$linkedList->addLast(30);
$linkedList->addFirst(5);

echo "LinkedList 内容: " . implode(", ", $linkedList->toArray()) . "\n";
echo "大小: {$linkedList->size()}\n";
echo "第一个元素: {$linkedList->getFirst()}\n";
echo "最后一个元素: {$linkedList->getLast()}\n";
echo "移除第一个元素: {$linkedList->removeFirst()}\n";
echo "移除后: " . implode(", ", $linkedList->toArray()) . "\n\n";

// 3. Stack 示例
echo "3. Stack 示例:\n";
$stack = new Stack();
$stack->push("First");
$stack->push("Second");
$stack->push("Third");

echo "Stack 内容: " . implode(", ", $stack->toArray()) . "\n";
echo "栈顶元素: {$stack->peek()}\n";
echo "弹出元素: {$stack->pop()}\n";
echo "弹出后栈顶: {$stack->peek()}\n";
echo "栈大小: {$stack->size()}\n\n";

// 括号匹配示例
echo "括号匹配示例:\n";
$expressions = ["(())", "(()", "()())", "[{()}]"];
foreach ($expressions as $expr) {
    $isValid = Stack::isValidParentheses($expr);
    echo "$expr: " . ($isValid ? "有效" : "无效") . "\n";
}
echo "\n";

// 4. Queue 示例
echo "4. Queue 示例:\n";
$queue = new Queue();
$queue->enqueue("Customer 1");
$queue->enqueue("Customer 2");
$queue->enqueue("Customer 3");

echo "Queue 内容: " . implode(", ", $queue->toArray()) . "\n";
echo "队首元素: {$queue->front()}\n";
echo "服务客户: {$queue->dequeue()}\n";
echo "服务后队首: {$queue->front()}\n";
echo "队列大小: {$queue->size()}\n\n";

// 5. PriorityQueue 示例
echo "5. PriorityQueue 示例:\n";
$priorityQueue = new PriorityQueue();
$priorityQueue->enqueue("低优先级任务", 1);
$priorityQueue->enqueue("高优先级任务", 5);
$priorityQueue->enqueue("中优先级任务", 3);
$priorityQueue->enqueue("紧急任务", 10);

echo "优先队列处理顺序:\n";
while (!$priorityQueue->isEmpty()) {
    $task = $priorityQueue->dequeue();
    echo "- {$task['element']} (优先级: {$task['priority']})\n";
}
echo "\n";

// 6. Deque 示例
echo "6. Deque 示例:\n";
$deque = new Deque();
$deque->addLast("Middle");
$deque->addFirst("First");
$deque->addLast("Last");
$deque->addFirst("New First");

echo "Deque 内容: " . implode(", ", $deque->toArray()) . "\n";
echo "前端元素: {$deque->peekFirst()}\n";
echo "后端元素: {$deque->peekLast()}\n";
echo "移除前端: {$deque->removeFirst()}\n";
echo "移除后端: {$deque->removeLast()}\n";
echo "移除后: " . implode(", ", $deque->toArray()) . "\n\n";

// 滑动窗口最大值示例
echo "滑动窗口最大值示例:\n";
$nums = [1, 3, -1, -3, 5, 3, 6, 7];
$k = 3;
$result = MonotonicDeque::slidingWindowMaximum($nums, $k);
echo "数组: [" . implode(", ", $nums) . "]\n";
echo "窗口大小: $k\n";
echo "滑动窗口最大值: [" . implode(", ", $result) . "]\n\n";

echo "=== 示例结束 ===\n";