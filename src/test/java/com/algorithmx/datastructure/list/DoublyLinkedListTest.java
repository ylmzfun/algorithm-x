package com.algorithmx.datastructure.list;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class DoublyLinkedListTest {

    @Test void addAndGet() {
        DoublyLinkedList list = new DoublyLinkedList();
        list.addLast(1);
        list.addLast(2);
        list.addLast(3);
        assertEquals(1, list.get(0));
        assertEquals(2, list.get(1));
        assertEquals(3, list.get(2));
        assertEquals(3, list.size());
    }

    @Test void addFirst() {
        DoublyLinkedList list = new DoublyLinkedList();
        list.addFirst(3);
        list.addFirst(2);
        list.addFirst(1);
        assertEquals("[1 <-> 2 <-> 3]", list.toString());
    }

    @Test void addAt() {
        DoublyLinkedList list = new DoublyLinkedList();
        list.addLast(1);
        list.addLast(3);
        list.addAt(1, 2);
        assertEquals("[1 <-> 2 <-> 3]", list.toString());
    }

    @Test void deleteAt() {
        DoublyLinkedList list = new DoublyLinkedList();
        list.addLast(1);
        list.addLast(2);
        list.addLast(3);
        assertEquals(2, list.deleteAt(1));
        assertEquals("[1 <-> 3]", list.toString());
    }
}
