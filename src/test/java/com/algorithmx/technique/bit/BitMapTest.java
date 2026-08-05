package com.algorithmx.technique.bit;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class BitMapTest {

    @Test void basic() {
        BitMap bm = new BitMap(1000);
        assertFalse(bm.contains(5));
        bm.add(5);
        assertTrue(bm.contains(5));
        bm.remove(5);
        assertFalse(bm.contains(5));
    }

    @Test void largeRange() {
        BitMap bm = new BitMap(100_000);
        bm.add(99999);
        bm.add(0);
        assertTrue(bm.contains(0));
        assertTrue(bm.contains(99999));
        assertFalse(bm.contains(50000));
    }
}
