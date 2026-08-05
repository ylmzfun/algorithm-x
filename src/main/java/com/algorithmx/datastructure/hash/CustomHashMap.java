package com.algorithmx.datastructure.hash;

import java.util.*;

/**
 * 手写 HashMap — 数组 + 链表，支持自动扩容
 */
@SuppressWarnings("unchecked")
public class CustomHashMap<K, V> {

    static class Node<K, V> {
        K key; V value; Node<K, V> next;
        Node(K key, V value) { this.key = key; this.value = value; }
    }

    private Node<K, V>[] table;
    private int size;
    private static final int DEFAULT_CAP = 16;
    private static final float LOAD_FACTOR = 0.75f;

    public CustomHashMap() { table = new Node[DEFAULT_CAP]; }

    public V put(K key, V value) {
        int idx = hash(key);
        Node<K, V> cur = table[idx];
        while (cur != null) {
            if (Objects.equals(cur.key, key)) { V old = cur.value; cur.value = value; return old; }
            cur = cur.next;
        }
        Node<K, V> newNode = new Node<>(key, value);
        newNode.next = table[idx];
        table[idx] = newNode;
        if (++size > table.length * LOAD_FACTOR) resize();
        return null;
    }

    public V get(K key) {
        Node<K, V> cur = table[hash(key)];
        while (cur != null) {
            if (Objects.equals(cur.key, key)) return cur.value;
            cur = cur.next;
        }
        return null;
    }

    public V remove(K key) {
        int idx = hash(key);
        Node<K, V> cur = table[idx], prev = null;
        while (cur != null) {
            if (Objects.equals(cur.key, key)) {
                if (prev == null) table[idx] = cur.next;
                else prev.next = cur.next;
                size--;
                return cur.value;
            }
            prev = cur;
            cur = cur.next;
        }
        return null;
    }

    public int size() { return size; }

    public Set<K> keySet() {
        Set<K> keys = new HashSet<>();
        for (Node<K, V> head : table) {
            for (Node<K, V> cur = head; cur != null; cur = cur.next) keys.add(cur.key);
        }
        return keys;
    }

    private int hash(K key) {
        return (key == null ? 0 : key.hashCode() & 0x7fffffff) % table.length;
    }

    private void resize() {
        Node<K, V>[] oldTable = table;
        table = new Node[oldTable.length * 2];
        size = 0;
        for (Node<K, V> head : oldTable) {
            for (Node<K, V> cur = head; cur != null; ) {
                Node<K, V> next = cur.next;
                cur.next = null;
                put(cur.key, cur.value);
                cur = next;
            }
        }
    }
}
