package com.algorithmx.datastructure.cache;

import java.util.*;

/**
 * LFU 缓存 — 最不经常使用
 */
public class LFUCache {
    private final int capacity;
    private int minFreq;
    private final Map<Integer, Node> keyMap;          // key → 节点
    private final Map<Integer, LinkedHashSet<Integer>> freqMap; // freq → key 集合

    static class Node { int key, val, freq; Node(int k, int v) { key = k; val = v; freq = 1; } }

    public LFUCache(int capacity) {
        this.capacity = capacity;
        this.minFreq = 0;
        this.keyMap = new HashMap<>();
        this.freqMap = new HashMap<>();
    }

    public int get(int key) {
        Node node = keyMap.get(key);
        if (node == null) return -1;
        incrFreq(node);
        return node.val;
    }

    public void put(int key, int val) {
        if (capacity == 0) return;
        Node node = keyMap.get(key);
        if (node != null) { node.val = val; incrFreq(node); return; }
        if (keyMap.size() == capacity) evict();
        node = new Node(key, val);
        keyMap.put(key, node);
        freqMap.computeIfAbsent(1, k -> new LinkedHashSet<>()).add(key);
        minFreq = 1;
    }

    private void incrFreq(Node node) {
        int oldFreq = node.freq;
        freqMap.get(oldFreq).remove(node.key);
        if (freqMap.get(oldFreq).isEmpty() && oldFreq == minFreq) minFreq++;
        freqMap.computeIfAbsent(++node.freq, k -> new LinkedHashSet<>()).add(node.key);
    }

    private void evict() {
        LinkedHashSet<Integer> keys = freqMap.get(minFreq);
        int oldest = keys.iterator().next();
        keys.remove(oldest);
        keyMap.remove(oldest);
    }
}
