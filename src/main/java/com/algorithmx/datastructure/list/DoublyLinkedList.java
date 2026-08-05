package com.algorithmx.datastructure.list;

/**
 * 双向链表 + 循环链表
 */
public class DoublyLinkedList {

    static class Node {
        int val;
        Node prev, next;
        Node(int val) { this.val = val; }
    }

    private final Node head; // 哨兵头
    private final Node tail; // 哨兵尾
    private int size;

    public DoublyLinkedList() {
        head = new Node(0);
        tail = new Node(0);
        head.next = tail;
        tail.prev = head;
    }

    public void addFirst(int val) {
        Node node = new Node(val);
        node.next = head.next; node.prev = head;
        head.next.prev = node; head.next = node;
        size++;
    }

    public void addLast(int val) {
        Node node = new Node(val);
        node.prev = tail.prev; node.next = tail;
        tail.prev.next = node; tail.prev = node;
        size++;
    }

    public void addAt(int index, int val) {
        if (index < 0 || index > size) return;
        Node cur = head;
        for (int i = 0; i < index; i++) cur = cur.next;
        Node node = new Node(val);
        node.next = cur.next; node.prev = cur;
        cur.next.prev = node; cur.next = node;
        size++;
    }

    public int deleteAt(int index) {
        if (index < 0 || index >= size) return -1;
        Node cur = head.next;
        for (int i = 0; i < index; i++) cur = cur.next;
        cur.prev.next = cur.next;
        cur.next.prev = cur.prev;
        size--;
        return cur.val;
    }

    public int get(int index) {
        if (index < 0 || index >= size) return -1;
        Node cur = head.next;
        for (int i = 0; i < index; i++) cur = cur.next;
        return cur.val;
    }

    public int size() { return size; }

    // ---- 循环链表：将双向链表首尾相连 ----

    /** 转为循环链表（tail 和 head 哨兵相连） */
    public void toCircular() {
        if (size == 0) return;
        Node first = head.next, last = tail.prev;
        head.next = first; first.prev = head;
        last.next = head; head.prev = last;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("[");
        Node cur = head.next;
        while (cur != tail) {
            sb.append(cur.val);
            if (cur.next != tail) sb.append(" <-> ");
            cur = cur.next;
        }
        return sb.append("]").toString();
    }
}
