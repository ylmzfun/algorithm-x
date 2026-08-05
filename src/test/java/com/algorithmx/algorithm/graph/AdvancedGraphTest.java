package com.algorithmx.algorithm.graph;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class AdvancedGraphTest {

    @Test void tarjanSCC() {
        @SuppressWarnings("unchecked")
        List<Integer>[] g = new ArrayList[5];
        for (int i = 0; i < 5; i++) g[i] = new ArrayList<>();
        g[0].add(1); g[1].add(2); g[2].add(0); // SCC: {0,1,2}
        g[1].add(3); g[3].add(4);              // SCC: {3}, {4}
        List<List<Integer>> sccs = AdvancedGraph.tarjanSCC(5, g);
        assertEquals(3, sccs.size());
    }

    @Test void maxFlow() {
        int n = 6;
        int[][] cap = new int[n][n];
        cap[0][1] = 16; cap[0][2] = 13;
        cap[1][2] = 10; cap[1][3] = 12;
        cap[2][1] = 4;  cap[2][4] = 14;
        cap[3][2] = 9;  cap[3][5] = 20;
        cap[4][3] = 7;  cap[4][5] = 4;
        assertEquals(23, AdvancedGraph.maxFlow(n, cap, 0, 5));
    }
}
