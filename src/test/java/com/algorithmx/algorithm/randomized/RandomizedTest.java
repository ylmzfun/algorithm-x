package com.algorithmx.algorithm.randomized;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.Test;

class RandomizedTest {

    @Test void shuffle() {
        int[] arr = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        Randomized.shuffle(arr);
        // 排序后应与原数组一致，证明内容未丢失
        int[] sorted = arr.clone();
        Arrays.sort(sorted);
        assertArrayEquals(new int[]{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}, sorted);
    }

    @Test void reservoirSample() {
        List<Integer> data = new ArrayList<>();
        for (int i = 0; i < 100; i++) data.add(i);
        int[] sample = Randomized.reservoirSample(data.iterator(), 5);
        assertEquals(5, sample.length);
        // 所有值在 [0, 99]
        for (int v : sample) assertTrue(v >= 0 && v < 100);
    }

    @Test void quickSelect() {
        int[] nums = {3, 1, 4, 1, 5, 9, 2, 6};
        assertEquals(1, Randomized.quickSelect(nums, 0)); // 第 0 小
        assertEquals(3, Randomized.quickSelect(nums, 3)); // 第 3 小
        assertEquals(9, Randomized.quickSelect(nums, 7)); // 最大
    }
}
