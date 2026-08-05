package com.algorithmx.algorithm.expression;

import java.util.*;

/**
 * 表达式求值（计算器）
 *
 * 支持：+, -, *, / 和括号 ()
 * 不支持负数（如 -1 需写成 0-1）
 */
public class ExpressionEval {

    /**
     * 双栈法 — 一个操作数栈，一个运算符栈
     */
    public static int calculate(String s) {
        Deque<Integer> nums = new ArrayDeque<>();
        Deque<Character> ops = new ArrayDeque<>();
        int i = 0;
        while (i < s.length()) {
            char ch = s.charAt(i);
            if (ch == ' ') { i++; continue; }
            if (Character.isDigit(ch)) {
                int num = 0;
                while (i < s.length() && Character.isDigit(s.charAt(i)))
                    num = num * 10 + (s.charAt(i++) - '0');
                nums.push(num);
                continue;
            }
            if (ch == '(') { ops.push(ch); }
            else if (ch == ')') {
                while (ops.peek() != '(') eval(nums, ops);
                ops.pop(); // 弹出 '('
            } else {
                // 处理优先级：栈顶运算符优先级 ≥ 当前运算符时先计算
                while (!ops.isEmpty() && precedence(ops.peek()) >= precedence(ch))
                    eval(nums, ops);
                ops.push(ch);
            }
            i++;
        }
        while (!ops.isEmpty()) eval(nums, ops);
        return nums.pop();
    }

    private static void eval(Deque<Integer> nums, Deque<Character> ops) {
        int b = nums.pop(), a = nums.pop();
        char op = ops.pop();
        switch (op) {
            case '+' -> nums.push(a + b);
            case '-' -> nums.push(a - b);
            case '*' -> nums.push(a * b);
            case '/' -> nums.push(a / b);
        }
    }

    private static int precedence(char op) {
        return (op == '+' || op == '-') ? 1 : (op == '*' || op == '/') ? 2 : 0;
    }

    // ==================== 逆波兰表达式（后缀表达式）求值 ====================

    /** 计算逆波兰表达式：["2","1","+","3","*"] → 9 */
    public static int evalRPN(String[] tokens) {
        Deque<Integer> stack = new ArrayDeque<>();
        for (String t : tokens) {
            switch (t) {
                case "+" -> stack.push(stack.pop() + stack.pop());
                case "-" -> { int b = stack.pop(); stack.push(stack.pop() - b); }
                case "*" -> stack.push(stack.pop() * stack.pop());
                case "/" -> { int b = stack.pop(); stack.push(stack.pop() / b); }
                default -> stack.push(Integer.parseInt(t));
            }
        }
        return stack.pop();
    }

    /** 中缀 → 后缀（调度场算法） */
    public static List<String> infixToPostfix(String s) {
        List<String> output = new ArrayList<>();
        Deque<Character> ops = new ArrayDeque<>();
        int i = 0;
        while (i < s.length()) {
            char ch = s.charAt(i);
            if (ch == ' ') { i++; continue; }
            if (Character.isDigit(ch)) {
                int num = 0;
                while (i < s.length() && Character.isDigit(s.charAt(i)))
                    num = num * 10 + (s.charAt(i++) - '0');
                output.add(String.valueOf(num));
                continue;
            }
            if (ch == '(') { ops.push(ch); }
            else if (ch == ')') {
                while (ops.peek() != '(') output.add(String.valueOf(ops.pop()));
                ops.pop();
            } else {
                while (!ops.isEmpty() && precedence(ops.peek()) >= precedence(ch))
                    output.add(String.valueOf(ops.pop()));
                ops.push(ch);
            }
            i++;
        }
        while (!ops.isEmpty()) output.add(String.valueOf(ops.pop()));
        return output;
    }
}
