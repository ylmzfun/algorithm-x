package com.algorithmx.datastructure.list;

/**
 * 单向链表
 */
public class SinglyLinkedList {

    static class Node {
        int val;
        Node next;
        Node(int val) { this.val = val; }
    }

    private Node head;

    // ---- 基础操作 ----

    public void addFirst(int val) {
        Node node = new Node(val);
        node.next = head;
        head = node;
    }

    public void addLast(int val) {
        Node node = new Node(val);
        if (head == null) { head = node; return; }
        Node cur = head;
        while (cur.next != null) cur = cur.next;
        cur.next = node;
    }

    public void delete(int val) {
        Node dummy = new Node(0);
        dummy.next = head;
        Node prev = dummy, cur = head;
        while (cur != null) {
            if (cur.val == val) { prev.next = cur.next; break; }
            prev = cur;
            cur = cur.next;
        }
        head = dummy.next;
    }

    // ---- 经典操作 ----

    /** 反转链表（迭代） */
    public void reverse() {
        Node prev = null, cur = head;
        while (cur != null) {
            Node next = cur.next;
            cur.next = prev;
            prev = cur;
            cur = next;
        }
        head = prev;
    }

    /** 反转链表（递归） */
    public void reverseRecursive() {
        head = reverseRecursive(head);
    }

    private Node reverseRecursive(Node node) {
        if (node == null || node.next == null) return node;
        Node newHead = reverseRecursive(node.next);
        node.next.next = node;
        node.next = null;
        return newHead;
    }

    /** 找中点（快慢指针） */
    public Node findMiddle() {
        Node slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        return slow;
    }

    /** 判环 */
    public boolean hasCycle() {
        Node slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) return true;
        }
        return false;
    }

    /** 找环入口 */
    public Node detectCycle() {
        Node slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) {
                slow = head;
                while (slow != fast) { slow = slow.next; fast = fast.next; }
                return slow;
            }
        }
        return null;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("[");
        Node cur = head;
        while (cur != null) {
            sb.append(cur.val);
            if (cur.next != null) sb.append(" -> ");
            cur = cur.next;
        }
        return sb.append("]").toString();
    }
}
