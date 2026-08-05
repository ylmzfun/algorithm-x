package com.algorithmx.datastructure.cache;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class LRUCacheTest {

    @Test void basic() {
        LRUCacheManual cache = new LRUCacheManual(2);
        cache.put(1, 1);
        cache.put(2, 2);
        assertEquals(1, cache.get(1));
        cache.put(3, 3); // evicts key 2
        assertEquals(-1, cache.get(2));
        cache.put(4, 4); // evicts key 1
        assertEquals(-1, cache.get(1));
        assertEquals(3, cache.get(3));
        assertEquals(4, cache.get(4));
    }
}

class LFUCacheTest {

    @Test void basic() {
        LFUCache cache = new LFUCache(2);
        cache.put(1, 1);
        cache.put(2, 2);
        assertEquals(1, cache.get(1));
        cache.put(3, 3); // evicts key 2 (freq=1 < 2)
        assertEquals(-1, cache.get(2));
        assertEquals(3, cache.get(3));
        cache.put(4, 4); // evicts key 1 (freq 1 == 4 freq 1, 1 is oldest)
        assertEquals(-1, cache.get(1));
        assertEquals(3, cache.get(3));
        assertEquals(4, cache.get(4));
    }
}
