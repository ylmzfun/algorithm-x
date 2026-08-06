/// 栈 (Stack)
///
/// LIFO (Last In, First Out) 数据结构。
/// Rust 中 `Vec` 天然支持栈操作：`push` / `pop` / `last`。

/// 通用栈 — 基于 Vec 实现
#[derive(Debug)]
pub struct Stack<T> {
    items: Vec<T>,
}

impl<T> Stack<T> {
    pub fn new() -> Self {
        Self { items: Vec::new() }
    }

    pub fn with_capacity(cap: usize) -> Self {
        Self {
            items: Vec::with_capacity(cap),
        }
    }

    pub fn push(&mut self, item: T) {
        self.items.push(item);
    }

    pub fn pop(&mut self) -> Option<T> {
        self.items.pop()
    }

    pub fn peek(&self) -> Option<&T> {
        self.items.last()
    }

    pub fn len(&self) -> usize {
        self.items.len()
    }

    pub fn is_empty(&self) -> bool {
        self.items.is_empty()
    }
}

// ========== 栈的经典应用 ==========

/// 有效的括号匹配
///
/// 给定只包含 '()[]{}' 的字符串，判断括号是否正确闭合。
/// 时间复杂度 O(n)，空间复杂度 O(n)
pub fn is_valid_brackets(s: &str) -> bool {
    let mut stack = Vec::new();
    for c in s.chars() {
        match c {
            '(' | '[' | '{' => stack.push(c),
            ')' => {
                if stack.pop() != Some('(') {
                    return false;
                }
            }
            ']' => {
                if stack.pop() != Some('[') {
                    return false;
                }
            }
            '}' => {
                if stack.pop() != Some('{') {
                    return false;
                }
            }
            _ => (),
        }
    }
    stack.is_empty()
}

/// 后缀表达式求值（逆波兰表示法）
///
/// 输入: ["2", "1", "+", "3", "*"]  →  ((2 + 1) * 3) = 9
pub fn eval_rpn(tokens: &[&str]) -> i32 {
    let mut stack = Vec::new();
    for token in tokens {
        match *token {
            "+" => {
                let b = stack.pop().unwrap();
                let a = stack.pop().unwrap();
                stack.push(a + b);
            }
            "-" => {
                let b = stack.pop().unwrap();
                let a = stack.pop().unwrap();
                stack.push(a - b);
            }
            "*" => {
                let b = stack.pop().unwrap();
                let a = stack.pop().unwrap();
                stack.push(a * b);
            }
            "/" => {
                let b = stack.pop().unwrap();
                let a = stack.pop().unwrap();
                stack.push(a / b);
            }
            num => stack.push(num.parse::<i32>().unwrap()),
        }
    }
    stack.pop().unwrap()
}

/// 每日温度 — 单调栈经典题
///
/// 给定温度数组，返回对于每一天，需要等待多少天才能遇到更高的温度。
/// 如果没有更高的温度，则为 0。
pub fn daily_temperatures(temperatures: &[i32]) -> Vec<usize> {
    let n = temperatures.len();
    let mut result = vec![0; n];
    let mut stack: Vec<usize> = Vec::new(); // 存索引的单调递减栈

    for i in 0..n {
        while let Some(&top) = stack.last() {
            if temperatures[i] > temperatures[top] {
                result[top] = i - top;
                stack.pop();
            } else {
                break;
            }
        }
        stack.push(i);
    }
    result
}

/// 用两个栈实现队列
///
/// 核心思想：
/// - `in_stack` 负责入队（push）
/// - `out_stack` 负责出队（pop/peek）
/// - 当 `out_stack` 为空时，将 `in_stack` 全部倒入 `out_stack`
pub struct QueueUsingStacks<T> {
    in_stack: Vec<T>,
    out_stack: Vec<T>,
}

impl<T> QueueUsingStacks<T> {
    pub fn new() -> Self {
        Self {
            in_stack: Vec::new(),
            out_stack: Vec::new(),
        }
    }

    pub fn push(&mut self, item: T) {
        self.in_stack.push(item);
    }

    pub fn pop(&mut self) -> Option<T> {
        self.transfer();
        self.out_stack.pop()
    }

    pub fn peek(&mut self) -> Option<&T> {
        self.transfer();
        self.out_stack.last()
    }

    pub fn is_empty(&self) -> bool {
        self.in_stack.is_empty() && self.out_stack.is_empty()
    }

    fn transfer(&mut self) {
        if self.out_stack.is_empty() {
            while let Some(item) = self.in_stack.pop() {
                self.out_stack.push(item);
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_stack_basic() {
        let mut s = Stack::new();
        s.push(1);
        s.push(2);
        s.push(3);
        assert_eq!(s.peek(), Some(&3));
        assert_eq!(s.pop(), Some(3));
        assert_eq!(s.pop(), Some(2));
        assert_eq!(s.pop(), Some(1));
        assert_eq!(s.pop(), None);
    }

    #[test]
    fn test_is_valid_brackets() {
        assert!(is_valid_brackets("()"));
        assert!(is_valid_brackets("()[]{}"));
        assert!(is_valid_brackets("{[()]}"));
        assert!(!is_valid_brackets("(]"));
        assert!(!is_valid_brackets("([)]"));
    }

    #[test]
    fn test_eval_rpn() {
        assert_eq!(eval_rpn(&["2", "1", "+", "3", "*"]), 9);
        assert_eq!(eval_rpn(&["4", "13", "5", "/", "+"]), 6);
        assert_eq!(eval_rpn(&["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]), 22);
    }

    #[test]
    fn test_daily_temperatures() {
        assert_eq!(
            daily_temperatures(&[73, 74, 75, 71, 69, 72, 76, 73]),
            vec![1, 1, 4, 2, 1, 1, 0, 0]
        );
    }

    #[test]
    fn test_queue_using_stacks() {
        let mut q = QueueUsingStacks::new();
        q.push(1);
        q.push(2);
        q.push(3);
        assert_eq!(q.peek(), Some(&1));
        assert_eq!(q.pop(), Some(1));
        assert_eq!(q.pop(), Some(2));
        q.push(4);
        assert_eq!(q.pop(), Some(3));
        assert_eq!(q.pop(), Some(4));
        assert!(q.is_empty());
    }
}
