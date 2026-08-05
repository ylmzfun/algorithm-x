package com.algorithmx.datastructure.hash;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class CustomHashMapTest {

    @Test void basic() {
        CustomHashMap<String, Integer> map = new CustomHashMap<>();
        map.put("a", 1);
        map.put("b", 2);
        assertEquals(1, map.get("a"));
        assertEquals(2, map.get("b"));
        assertEquals(2, map.size());
    }

    @Test void overrideKey() {
        CustomHashMap<String, Integer> map = new CustomHashMap<>();
        map.put("x", 1);
        assertEquals(1, map.put("x", 100));
        assertEquals(100, map.get("x"));
    }

    @Test void remove() {
        CustomHashMap<String, Integer> map = new CustomHashMap<>();
        map.put("a", 1);
        assertEquals(1, map.remove("a"));
        assertNull(map.get("a"));
        assertEquals(0, map.size());
    }

    @Test void resize() {
        CustomHashMap<Integer, Integer> map = new CustomHashMap<>();
        for (int i = 0; i < 100; i++) map.put(i, i);
        assertEquals(100, map.size());
        for (int i = 0; i < 100; i++) assertEquals(i, map.get(i));
    }

    @Test void keySet() {
        CustomHashMap<String, Integer> map = new CustomHashMap<>();
        map.put("x", 1);
        map.put("y", 2);
        assertEquals(2, map.keySet().size());
        assertTrue(map.keySet().contains("x"));
    }
}
