package com.algorithmx.algorithm.string;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.Test;

class StringMatchingTest {

    @Test void rabinKarp() {
        assertEquals(List.of(0, 7), StringMatching.rabinKarp("abracadabra", "abra"));
        assertEquals(List.of(2), StringMatching.rabinKarp("hello", "llo"));
        assertTrue(StringMatching.rabinKarp("abc", "xyz").isEmpty());
    }

    @Test void longestPalindrome() {
        assertEquals("bab", StringMatching.longestPalindrome("babad"));
        assertEquals("bb", StringMatching.longestPalindrome("cbbd"));
    }

    @Test void longestPalindromeEdge() {
        assertEquals("a", StringMatching.longestPalindrome("a"));
        assertEquals("", StringMatching.longestPalindrome(""));
    }
}

class KMPTest {

    @Test void search() {
        assertEquals(2, KMP.search("hello", "llo"));
        assertEquals(0, KMP.search("ababab", "abab"));
        assertEquals(-1, KMP.search("abc", "xyz"));
    }

    @Test void emptyPattern() {
        assertEquals(0, KMP.search("abc", ""));
    }

    @Test void buildNext() {
        int[] next = KMP.buildNext("ababc");
        assertArrayEquals(new int[]{-1, 0, -1, 0, 2}, next); // 优化版 KMP 的 next 数组
    }
}
