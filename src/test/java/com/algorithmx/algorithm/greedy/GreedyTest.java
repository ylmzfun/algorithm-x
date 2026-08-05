package com.algorithmx.algorithm.greedy;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.Arrays;

class GreedyTest {

    @Test void maxNonOverlap() {
        int[][] intervals = {{1, 2}, {2, 3}, {3, 4}, {1, 3}};
        assertEquals(3, Greedy.maxNonOverlap(intervals));
    }

    @Test void findMinArrowShots() {
        int[][] points = {{10, 16}, {2, 8}, {1, 6}, {7, 12}};
        assertEquals(2, Greedy.findMinArrowShots(points));
    }

    @Test void merge() {
        int[][] intervals = {{1, 3}, {2, 6}, {8, 10}, {15, 18}};
        int[][] res = Greedy.merge(intervals);
        assertEquals(3, res.length);
        assertArrayEquals(new int[]{1, 6}, res[0]);
        assertArrayEquals(new int[]{8, 10}, res[1]);
    }

    @Test void canJump() {
        assertTrue(Greedy.canJump(new int[]{2, 3, 1, 1, 4}));
        assertFalse(Greedy.canJump(new int[]{3, 2, 1, 0, 4}));
    }

    @Test void jump() {
        assertEquals(2, Greedy.jump(new int[]{2, 3, 1, 1, 4}));
    }

    @Test void candy() {
        assertEquals(5, Greedy.candy(new int[]{1, 0, 2}));
        assertEquals(4, Greedy.candy(new int[]{1, 2, 2}));
    }

    @Test void canCompleteCircuit() {
        assertEquals(3, Greedy.canCompleteCircuit(new int[]{1, 2, 3, 4, 5}, new int[]{3, 4, 5, 1, 2}));
    }
}
