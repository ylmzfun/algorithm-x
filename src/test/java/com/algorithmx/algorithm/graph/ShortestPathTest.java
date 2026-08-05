package com.algorithmx.algorithm.graph;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.Arrays;

class ShortestPathTest {

    @Test void bellmanFord() {
        int[][] edges = {{0, 1, 4}, {0, 2, 2}, {1, 2, -3}, {1, 3, 2}, {2, 3, 3}};
        int[] dist = ShortestPath.bellmanFord(4, edges, 0);
        assertNotNull(dist);
        assertArrayEquals(new int[]{0, 4, 1, 4}, dist);
    }

    @Test void bellmanFordNegativeCycle() {
        int[][] edges = {{0, 1, 1}, {1, 2, -1}, {2, 0, -1}};
        assertNull(ShortestPath.bellmanFord(3, edges, 0));
    }

    @Test void floydWarshall() {
        int[][] edges = {{0, 1, 4}, {1, 2, 3}, {0, 2, 10}};
        int[][] dist = ShortestPath.floydWarshall(3, edges);
        assertEquals(0, dist[0][0]);
        assertEquals(4, dist[0][1]);
        assertEquals(7, dist[0][2]); // 0→1→2 = 4+3 = 7
    }

    @Test void spfa() {
        int[][] edges = {{0, 1, 4}, {0, 2, 2}, {1, 2, -3}, {1, 3, 2}, {2, 3, 3}};
        int[] dist = ShortestPath.spfa(4, edges, 0);
        assertNotNull(dist);
        assertArrayEquals(new int[]{0, 4, 1, 4}, dist);
    }
}
