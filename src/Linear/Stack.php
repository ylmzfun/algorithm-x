<?php

namespace DataStructures\Linear;

/**
 * Stack - 栈数据结构实现
 * 
 * 思路：
 * 1. 基于动态数组实现
 * 2. 只允许在一端（栈顶）进行插入和删除操作
 * 3. 遵循LIFO（Last In First Out）原则
 * 4. 提供push、pop、peek等基本操作
 * 
 * 作用：
 * - 实现后进先出的数据访问模式
 * - 支持递归调用的实现
 * - 提供撤销操作的基础
 * - 表达式求值和语法分析
 * 
 * 业务场景：
 * 1. 函数调用栈：程序执行时的函数调用管理
 * 2. 浏览器历史：页面访问历史的后退功能
 * 3. 文本编辑器：撤销(Undo)操作的实现
 * 4. 表达式计算：中缀表达式转后缀表达式
 * 5. 语法检查：括号匹配检查
 * 6. 深度优先搜索：DFS算法的实现
 * 7. 内存管理：程序运行时的内存分配
 * 8. 游戏开发：游戏状态的保存和回退
 */
class Stack
{
    private array $elements;
    private int $top;
    private int $capacity;
    
    public function __construct(int $initialCapacity = 10)
    {
        $this->capacity = max(1, $initialCapacity);
        $this->elements = array_fill(0, $this->capacity, null);
        $this->top = -1;
    }
    
    /**
     * 入栈操作
     * 时间复杂度：平均O(1)，最坏O(n)
     */
    public function push($element): void
    {
        $this->ensureCapacity();
        $this->elements[++$this->top] = $element;
    }
    
    /**
     * 出栈操作
     * 时间复杂度：O(1)
     */
    public function pop()
    {
        if ($this->isEmpty()) {
            throw new \RuntimeException("Stack is empty");
        }
        
        $element = $this->elements[$this->top];
        $this->elements[$this->top] = null; // 避免内存泄漏
        $this->top--;
        
        // 如果使用空间过少，缩容
        if ($this->size() > 0 && $this->size() <= $this->capacity / 4) {
            $this->resize($this->capacity / 2);
        }
        
        return $element;
    }
    
    /**
     * 查看栈顶元素（不删除）
     * 时间复杂度：O(1)
     */
    public function peek()
    {
        if ($this->isEmpty()) {
            throw new \RuntimeException("Stack is empty");
        }
        
        return $this->elements[$this->top];
    }
    
    /**
     * 检查栈是否为空
     * 时间复杂度：O(1)
     */
    public function isEmpty(): bool
    {
        return $this->top === -1;
    }
    
    /**
     * 获取栈的大小
     * 时间复杂度：O(1)
     */
    public function size(): int
    {
        return $this->top + 1;
    }
    
    /**
     * 清空栈
     * 时间复杂度：O(n)
     */
    public function clear(): void
    {
        for ($i = 0; $i <= $this->top; $i++) {
            $this->elements[$i] = null;
        }
        $this->top = -1;
    }
    
    /**
     * 搜索元素在栈中的位置（从栈顶开始计算）
     * 时间复杂度：O(n)
     */
    public function search($element): int
    {
        for ($i = $this->top; $i >= 0; $i--) {
            if ($this->elements[$i] === $element) {
                return $this->top - $i + 1; // 返回从栈顶开始的位置
            }
        }
        return -1;
    }
    
    /**
     * 检查是否包含指定元素
     * 时间复杂度：O(n)
     */
    public function contains($element): bool
    {
        return $this->search($element) !== -1;
    }
    
    /**
     * 转换为数组（栈顶在数组末尾）
     * 时间复杂度：O(n)
     */
    public function toArray(): array
    {
        return array_slice($this->elements, 0, $this->size());
    }
    
    /**
     * 获取栈的容量
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
        if ($this->top + 1 >= $this->capacity) {
            $this->resize($this->capacity * 2);
        }
    }
    
    /**
     * 调整栈的容量
     */
    private function resize(int $newCapacity): void
    {
        $newElements = array_fill(0, $newCapacity, null);
        for ($i = 0; $i <= $this->top; $i++) {
            $newElements[$i] = $this->elements[$i];
        }
        $this->elements = $newElements;
        $this->capacity = $newCapacity;
    }
    
    /**
     * 实用方法：括号匹配检查
     * 业务场景：代码编辑器的语法检查
     */
    public static function isValidParentheses(string $expression): bool
    {
        $stack = new self();
        $pairs = ['(' => ')', '[' => ']', '{' => '}'];
        
        for ($i = 0; $i < strlen($expression); $i++) {
            $char = $expression[$i];
            
            if (isset($pairs[$char])) {
                // 开括号，入栈
                $stack->push($char);
            } elseif (in_array($char, $pairs)) {
                // 闭括号，检查匹配
                if ($stack->isEmpty()) {
                    return false;
                }
                
                $openBracket = $stack->pop();
                if ($pairs[$openBracket] !== $char) {
                    return false;
                }
            }
        }
        
        return $stack->isEmpty();
    }
    
    /**
     * 实用方法：中缀表达式转后缀表达式
     * 业务场景：计算器应用
     */
    public static function infixToPostfix(string $expression): string
    {
        $stack = new self();
        $result = '';
        $precedence = ['+' => 1, '-' => 1, '*' => 2, '/' => 2, '^' => 3];
        
        for ($i = 0; $i < strlen($expression); $i++) {
            $char = $expression[$i];
            
            if (ctype_alnum($char)) {
                // 操作数，直接输出
                $result .= $char;
            } elseif ($char === '(') {
                // 左括号，入栈
                $stack->push($char);
            } elseif ($char === ')') {
                // 右括号，弹出直到左括号
                while (!$stack->isEmpty() && $stack->peek() !== '(') {
                    $result .= $stack->pop();
                }
                $stack->pop(); // 弹出左括号
            } elseif (isset($precedence[$char])) {
                // 操作符
                while (!$stack->isEmpty() && 
                       $stack->peek() !== '(' && 
                       isset($precedence[$stack->peek()]) &&
                       $precedence[$stack->peek()] >= $precedence[$char]) {
                    $result .= $stack->pop();
                }
                $stack->push($char);
            }
        }
        
        // 弹出剩余操作符
        while (!$stack->isEmpty()) {
            $result .= $stack->pop();
        }
        
        return $result;
    }
    
    /**
     * 实用方法：计算后缀表达式
     * 业务场景：表达式求值
     */
    public static function evaluatePostfix(string $expression): float
    {
        $stack = new self();
        
        for ($i = 0; $i < strlen($expression); $i++) {
            $char = $expression[$i];
            
            if (ctype_digit($char)) {
                // 数字，入栈
                $stack->push((float)$char);
            } else {
                // 操作符，弹出两个操作数
                if ($stack->size() < 2) {
                    throw new \InvalidArgumentException("Invalid postfix expression");
                }
                
                $operand2 = $stack->pop();
                $operand1 = $stack->pop();
                
                switch ($char) {
                    case '+':
                        $stack->push($operand1 + $operand2);
                        break;
                    case '-':
                        $stack->push($operand1 - $operand2);
                        break;
                    case '*':
                        $stack->push($operand1 * $operand2);
                        break;
                    case '/':
                        if ($operand2 == 0) {
                            throw new \DivisionByZeroError("Division by zero");
                        }
                        $stack->push($operand1 / $operand2);
                        break;
                    case '^':
                        $stack->push(pow($operand1, $operand2));
                        break;
                    default:
                        throw new \InvalidArgumentException("Unknown operator: $char");
                }
            }
        }
        
        if ($stack->size() !== 1) {
            throw new \InvalidArgumentException("Invalid postfix expression");
        }
        
        return $stack->pop();
    }
}