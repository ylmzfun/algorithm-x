package com.algorithmx.datastructure.skiplist;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class SkipListTest {

    @Test void basic() {
        SkipList sl = new SkipList();
        sl.add(1);
        sl.add(2);
        sl.add(3);
        assertTrue(sl.search(1));
        assertTrue(sl.search(2));
        assertFalse(sl.search(4));
    }

    @Test void erase() {
        SkipList sl = new SkipList();
        sl.add(1); sl.add(2); sl.add(3);
        assertTrue(sl.erase(2));
        assertFalse(sl.search(2));
        assertTrue(sl.search(1));
        assertTrue(sl.search(3));
    }

    @Test void largeSet() {
        SkipList sl = new SkipList();
        for (int i = 0; i < 1000; i++) sl.add(i);
        for (int i = 0; i < 1000; i++) assertTrue(sl.search(i));
        assertFalse(sl.search(1000));
    }
}
