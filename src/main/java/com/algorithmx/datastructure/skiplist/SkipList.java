package com.algorithmx.datastructure.skiplist;

import java.util.Random;

/**
 * 跳表（Skip List）— 概率型数据结构，期望 O(log n) 增删查
 *
 * 参考 Redis 有序集合的实现思路：
 * 多层索引通过随机层数构建，每层概率 1/2。
 */
public class SkipList {
    private static final int MAX_LEVEL = 16;
    private static final Random RAND = new Random();

    static class Node {
        int val;
        Node[] next; // next[i] = 第 i 层的后继
        Node(int val, int level) { this.val = val; this.next = new Node[level]; }
    }

    private final Node head = new Node(Integer.MIN_VALUE, MAX_LEVEL);
    private int curLevel = 1;

    private int randomLevel() {
        int level = 1;
        while (level < MAX_LEVEL && RAND.nextBoolean()) level++;
        return level;
    }

    public boolean search(int target) {
        Node cur = head;
        for (int i = curLevel - 1; i >= 0; i--) {
            while (cur.next[i] != null && cur.next[i].val < target) cur = cur.next[i];
        }
        return cur.next[0] != null && cur.next[0].val == target;
    }

    public void add(int num) {
        int newLevel = randomLevel();
        curLevel = Math.max(curLevel, newLevel);
        Node newNode = new Node(num, newLevel);

        Node cur = head;
        for (int i = curLevel - 1; i >= 0; i--) {
            while (cur.next[i] != null && cur.next[i].val < num) cur = cur.next[i];
            if (i < newLevel) {
                newNode.next[i] = cur.next[i];
                cur.next[i] = newNode;
            }
        }
    }

    public boolean erase(int num) {
        Node cur = head;
        boolean found = false;
        for (int i = curLevel - 1; i >= 0; i--) {
            while (cur.next[i] != null && cur.next[i].val < num) cur = cur.next[i];
            if (cur.next[i] != null && cur.next[i].val == num) {
                cur.next[i] = cur.next[i].next[i];
                found = true;
            }
        }
        return found;
    }
}
