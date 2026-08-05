package com.algorithmx.algorithm.search;

import java.util.*;

/**
 * A* 寻路算法 — 启发式搜索
 *
 * f(n) = g(n) + h(n)
 *   g(n): 从起点到 n 的实际代价
 *   h(n): n 到终点的估算代价（启发函数，必须 ≤ 实际代价 = 可采纳性）
 *
 * 本实现基于网格地图，h(n) 使用曼哈顿距离。
 */
public class AStar {
    private static final int[][] DIRS = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};

    /**
     * @param grid 0 = 可通行, 1 = 障碍
     * @return 从 (sr, sc) 到 (tr, tc) 的最短路径步数，不可达返回 -1
     */
    public static int shortestPath(int[][] grid, int sr, int sc, int tr, int tc) {
        int h = grid.length, w = grid[0].length;
        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[2]));
        int[][] gCost = new int[h][w];
        for (int[] row : gCost) Arrays.fill(row, Integer.MAX_VALUE);
        gCost[sr][sc] = 0;
        pq.offer(new int[]{sr, sc, heuristic(sr, sc, tr, tc)});

        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            int r = cur[0], c = cur[1];
            if (r == tr && c == tc) return gCost[r][c];
            for (int[] d : DIRS) {
                int nr = r + d[0], nc = c + d[1];
                if (nr < 0 || nr >= h || nc < 0 || nc >= w || grid[nr][nc] == 1) continue;
                int newG = gCost[r][c] + 1;
                if (newG < gCost[nr][nc]) {
                    gCost[nr][nc] = newG;
                    pq.offer(new int[]{nr, nc, newG + heuristic(nr, nc, tr, tc)});
                }
            }
        }
        return -1;
    }

    /** 曼哈顿距离 */
    private static int heuristic(int r, int c, int tr, int tc) {
        return Math.abs(r - tr) + Math.abs(c - tc);
    }
}
