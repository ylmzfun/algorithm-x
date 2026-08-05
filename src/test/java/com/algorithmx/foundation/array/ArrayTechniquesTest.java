package com.algorithmx.foundation.array;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.Test;

class ArrayTechniquesTest {

    @Test void twoSum() {
        assertArrayEquals(new int[]{0, 1}, ArrayTechniques.twoSum(new int[]{2, 7, 11, 15}, 9));
    }

    @Test void threeSum() {
        List<List<Integer>> res = ArrayTechniques.threeSum(new int[]{-1, 0, 1, 2, -1, -4});
        assertEquals(2, res.size());
        assertTrue(res.contains(List.of(-1, -1, 2)));
        assertTrue(res.contains(List.of(-1, 0, 1)));
    }

    @Test void trap() {
        assertEquals(6, ArrayTechniques.trap(new int[]{0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1}));
    }

    @Test void maxArea() {
        assertEquals(49, ArrayTechniques.maxArea(new int[]{1, 8, 6, 2, 5, 4, 8, 3, 7}));
    }

    @Test void prefixSum() {
        ArrayTechniques.PrefixSum ps = new ArrayTechniques.PrefixSum(new int[]{-2, 0, 3, -5, 2, -1});
        assertEquals(1, ps.sumRange(0, 2));
        assertEquals(-1, ps.sumRange(2, 5));
        assertEquals(-3, ps.sumRange(0, 5));
    }

    @Test void subarraySum() {
        assertEquals(2, ArrayTechniques.subarraySum(new int[]{1, 1, 1}, 2));
        assertEquals(2, ArrayTechniques.subarraySum(new int[]{1, 2, 3}, 3));
    }

    @Test void differenceArray() {
        ArrayTechniques.DifferenceArray da = new ArrayTechniques.DifferenceArray(new int[]{1, 2, 3, 4, 5});
        da.increment(1, 3, 2);
        assertArrayEquals(new int[]{1, 4, 5, 6, 5}, da.result());
    }

    @Test void lengthOfLongestSubstring() {
        assertEquals(3, ArrayTechniques.lengthOfLongestSubstring("abcabcbb"));
        assertEquals(1, ArrayTechniques.lengthOfLongestSubstring("bbbbb"));
        assertEquals(3, ArrayTechniques.lengthOfLongestSubstring("pwwkew"));
    }

    @Test void minWindow() {
        assertEquals("BANC", ArrayTechniques.minWindow("ADOBECODEBANC", "ABC"));
        assertEquals("a", ArrayTechniques.minWindow("a", "a"));
    }

    @Test void minSubArrayLen() {
        assertEquals(2, ArrayTechniques.minSubArrayLen(7, new int[]{2, 3, 1, 2, 4, 3}));
        assertEquals(0, ArrayTechniques.minSubArrayLen(100, new int[]{1, 2, 3}));
    }

    @Test void findAnagrams() {
        List<Integer> res = ArrayTechniques.findAnagrams("cbaebabacd", "abc");
        assertEquals(2, res.size());
        assertTrue(res.contains(0));
        assertTrue(res.contains(6));
    }
}
