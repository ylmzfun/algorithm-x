package com.algorithmx.foundation.search;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class BinarySearchTest {

    @Test void exactFound() {
        int[] nums = {1, 3, 5, 7, 9};
        assertEquals(2, BinarySearch.search(nums, 5));
    }

    @Test void exactNotFound() {
        int[] nums = {1, 3, 5, 7, 9};
        assertEquals(-1, BinarySearch.search(nums, 4));
    }

    @Test void lowerBound() {
        int[] nums = {1, 2, 2, 2, 3, 5};
        assertEquals(1, BinarySearch.lowerBound(nums, 2));  // 第一个 >= 2
        assertEquals(5, BinarySearch.lowerBound(nums, 4));  // 第一个 >= 4 → 下标 5
        assertEquals(6, BinarySearch.lowerBound(nums, 6));  // 超范围 → nums.length
    }

    @Test void upperBound() {
        int[] nums = {1, 2, 2, 2, 3, 5};
        assertEquals(4, BinarySearch.upperBound(nums, 2));  // 第一个 > 2
        assertEquals(5, BinarySearch.upperBound(nums, 4));  // 第一个 > 4
    }

    @Test void searchRotated() {
        int[] nums = {4, 5, 6, 7, 0, 1, 2};
        assertEquals(4, BinarySearch.searchRotated(nums, 0));
        assertEquals(0, BinarySearch.searchRotated(nums, 4));
        assertEquals(6, BinarySearch.searchRotated(nums, 2));
        assertEquals(-1, BinarySearch.searchRotated(nums, 3));
    }
}
