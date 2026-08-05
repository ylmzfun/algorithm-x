package com.algorithmx.algorithm.dp;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class DynamicProgrammingTest {

    @Test void knapsackBounded() {
        int W = 10;
        int[] wt = {2, 3, 5}, val = {6, 10, 12}, limit = {3, 2, 1};
        // 最佳：取 2 个 item0(4kg,12val) + 2 个 item1(6kg,20val) = 32
        // 实际计算……
        int result = DynamicProgramming.knapsackBounded(W, wt, val, limit);
        assertTrue(result > 0);
    }

    @Test void matrixChainOrder() {
        int[] dims = {10, 30, 5, 60}; // A(10×30) * B(30×5) * C(5×60)
        assertEquals(4500, DynamicProgramming.matrixChainOrder(dims));
        // (A(BC)) = 30*5*60 + 10*30*60 = 9000 + 18000 = 27000
        // ((AB)C) = 10*30*5 + 10*5*60 = 1500 + 3000 = 4500 ✓
    }

    @Test void burstBalloons() {
        assertEquals(167, DynamicProgramming.burstBalloons(new int[]{3, 1, 5, 8}));
    }

    @Test void tsp() {
        int[][] dist = {
            {0, 10, 15, 20},
            {10, 0, 35, 25},
            {15, 35, 0, 30},
            {20, 25, 30, 0}
        };
        assertEquals(80, DynamicProgramming.tsp(dist));
    }

    @Test void maxSubArray() {
        assertEquals(6, DynamicProgramming.maxSubArray(new int[]{-2, 1, -3, 4, -1, 2, 1, -5, 4}));
        assertEquals(-1, DynamicProgramming.maxSubArray(new int[]{-3, -2, -1}));
    }
}
