package com.algorithmx.algorithm.search;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class AStarTest {

    @Test void simplest() {
        int[][] grid = {
            {0, 0, 0},
            {0, 0, 0},
            {0, 0, 0}
        };
        assertEquals(4, AStar.shortestPath(grid, 0, 0, 2, 2));
    }

    @Test void withObstacles() {
        int[][] grid = {
            {0, 0, 0, 0, 0},
            {0, 1, 1, 1, 0},
            {0, 0, 0, 0, 0},
            {0, 1, 1, 1, 0},
            {0, 0, 0, 0, 0}
        };
        // (0,0) → (4,4): 绕路
        assertTrue(AStar.shortestPath(grid, 0, 0, 4, 4) > 0);
    }

    @Test void unreachable() {
        int[][] grid = {
            {0, 1, 0},
            {0, 1, 0},
            {0, 1, 0}
        };
        assertEquals(-1, AStar.shortestPath(grid, 0, 0, 0, 2));
    }
}
