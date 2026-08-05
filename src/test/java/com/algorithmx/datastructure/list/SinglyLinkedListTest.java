package com.algorithmx.datastructure.list;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class SinglyLinkedListTest {

    @Test void addAndToString() {
        SinglyLinkedList list = new SinglyLinkedList();
        list.addLast(1);
        list.addLast(2);
        list.addLast(3);
        assertEquals("[1 -> 2 -> 3]", list.toString());
    }

    @Test void reverse() {
        SinglyLinkedList list = new SinglyLinkedList();
        list.addLast(1);
        list.addLast(2);
        list.addLast(3);
        list.reverse();
        assertEquals("[3 -> 2 -> 1]", list.toString());
    }

    @Test void reverseRecursive() {
        SinglyLinkedList list = new SinglyLinkedList();
        list.addLast(1);
        list.addLast(2);
        list.addLast(3);
        list.reverseRecursive();
        assertEquals("[3 -> 2 -> 1]", list.toString());
    }

    @Test void findMiddle() {
        SinglyLinkedList list = new SinglyLinkedList();
        list.addLast(1);
        list.addLast(2);
        list.addLast(3);
        list.addLast(4);
        list.addLast(5);
        assertEquals(3, list.findMiddle().val);
    }

    @Test void delete() {
        SinglyLinkedList list = new SinglyLinkedList();
        list.addLast(1);
        list.addLast(2);
        list.addLast(3);
        list.delete(2);
        assertEquals("[1 -> 3]", list.toString());
    }

    @Test void noCycle_hasCycle() {
        SinglyLinkedList list = new SinglyLinkedList();
        list.addLast(1);
        list.addLast(2);
        list.addLast(3);
        assertFalse(list.hasCycle());
    }
}
