package com.algorithmx.datastructure.cache;

import java.util.*;

/**
 * LRU 缓存 — 最近最少使用
 */
public class LRUCache<K, V> extends LinkedHashMap<K, V> {
    private final int capacity;

    public LRUCache(int capacity) {
        super(capacity, 0.75f, true); // accessOrder = true
        this.capacity = capacity;
    }

    @Override
    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
        return size() > capacity;
    }
}

/**
 * LRU 缓存 — 手写实现（哈希表 + 双向链表）
 */
class LRUCacheManual {
    static class Node {
        int key, val;
        Node prev, next;
        Node(int k, int v) { key = k; val = v; }
    }

    private final int capacity;
    private final Map<Integer, Node> map = new HashMap<>();
    private final Node head = new Node(0, 0); // 哨兵头
    private final Node tail = new Node(0, 0); // 哨兵尾

    public LRUCacheManual(int capacity) {
        this.capacity = capacity;
        head.next = tail; tail.prev = head;
    }

    public int get(int key) {
        Node node = map.get(key);
        if (node == null) return -1;
        moveToHead(node);
        return node.val;
    }

    public void put(int key, int val) {
        Node node = map.get(key);
        if (node != null) { node.val = val; moveToHead(node); return; }
        if (map.size() == capacity) {
            Node last = tail.prev;
            removeNode(last);
            map.remove(last.key);
        }
        Node newNode = new Node(key, val);
        map.put(key, newNode);
        addToHead(newNode);
    }

    private void addToHead(Node node) {
        node.next = head.next; node.prev = head;
        head.next.prev = node; head.next = node;
    }

    private void removeNode(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void moveToHead(Node node) { removeNode(node); addToHead(node); }
}
