package com.algorithmx.algorithm.string;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.Test;

class ZAlgorithmTest {

    @Test void computeZ() {
        // "abacabad": z[i] = s[i..] 与 s 的最长公共前缀
        // i=0: skip, i=1: "b..." vs "a..." → 0, i=2: "a..." vs "ab..." → 1
        // i=3: "c..." vs "a..." → 0, i=4: "a..." vs "abac..." → 3? no let me recalculate
        // s[4..]="abad", s="abacabad": a=a, b=b, a=a, d≠c → z[4]=3
        // i=5: "b..." vs "a..." → 0, i=6: "a..." vs "a..." → 1, i=7: "d" vs "a" → 0
        assertArrayEquals(new int[]{0, 0, 1, 0, 3, 0, 1, 0},
            ZAlgorithm.computeZ("abacabad"));
    }

    @Test void search() {
        assertEquals(List.of(0, 7), ZAlgorithm.search("abracadabra", "abra"));
        assertEquals(List.of(2), ZAlgorithm.search("hello", "llo"));
        assertTrue(ZAlgorithm.search("abc", "xyz").isEmpty());
    }
}
