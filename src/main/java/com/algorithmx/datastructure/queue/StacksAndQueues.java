package com.algorithmx.datastructure.queue;

import java.util.*;

/**
 * 栈与队列经典实现
 */
public class StacksAndQueues {

    // ==================== 栈 ====================

    /** 用两个队列实现栈 */
    public static class MyStack {
        private final Queue<Integer> q = new LinkedList<>();

        public void push(int x) {
            q.offer(x);
            for (int i = 0; i < q.size() - 1; i++) q.offer(q.poll());
        }

        public int pop() { return q.poll(); }
        public int top() { return q.peek(); }
        public boolean empty() { return q.isEmpty(); }
    }

    /** 用两个栈实现队列 */
    public static class MyQueue {
        private final Deque<Integer> inStack = new ArrayDeque<>();
        private final Deque<Integer> outStack = new ArrayDeque<>();

        public void push(int x) { inStack.push(x); }

        public int pop() {
            transferIfNeeded();
            return outStack.pop();
        }

        public int peek() {
            transferIfNeeded();
            return outStack.peek();
        }

        public boolean empty() { return inStack.isEmpty() && outStack.isEmpty(); }

        private void transferIfNeeded() {
            if (outStack.isEmpty()) {
                while (!inStack.isEmpty()) outStack.push(inStack.pop());
            }
        }
    }

    /** 最小栈 — 常数时间获取最小值 */
    public static class MinStack {
        private final Deque<Integer> stack = new ArrayDeque<>();
        private final Deque<Integer> minStack = new ArrayDeque<>();

        public void push(int x) {
            stack.push(x);
            minStack.push(minStack.isEmpty() ? x : Math.min(x, minStack.peek()));
        }

        public void pop() { stack.pop(); minStack.pop(); }
        public int top() { return stack.peek(); }
        public int getMin() { return minStack.peek(); }
    }

    // ==================== 单调栈 ====================

    /** 下一个更大元素（无重复） */
    public static int[] nextGreaterElement(int[] nums) {
        int n = nums.length;
        int[] res = new int[n];
        Arrays.fill(res, -1);
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && nums[stack.peek()] < nums[i]) {
                res[stack.pop()] = nums[i];
            }
            stack.push(i);
        }
        return res;
    }

    /** 每日温度 — 下一个更高温度的天数间隔 */
    public static int[] dailyTemperatures(int[] t) {
        int n = t.length;
        int[] res = new int[n];
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && t[stack.peek()] < t[i]) {
                int idx = stack.pop();
                res[idx] = i - idx;
            }
            stack.push(i);
        }
        return res;
    }

    // ==================== 单调队列 ====================

    /** 滑动窗口最大值 */
    public static int[] maxSlidingWindow(int[] nums, int k) {
        int n = nums.length;
        if (n == 0) return new int[0];
        int[] res = new int[n - k + 1];
        Deque<Integer> deque = new ArrayDeque<>(); // 存下标，单调递减
        for (int i = 0; i < n; i++) {
            // 移除窗口外元素
            if (!deque.isEmpty() && deque.peekFirst() <= i - k) deque.pollFirst();
            // 维护单调递减
            while (!deque.isEmpty() && nums[deque.peekLast()] < nums[i]) deque.pollLast();
            deque.offerLast(i);
            // 记录结果
            if (i >= k - 1) res[i - k + 1] = nums[deque.peekFirst()];
        }
        return res;
    }
}
