package com.algorithmx.algorithm.graph;

import java.util.*;

/**
 * 最短路径进阶：Bellman-Ford、Floyd-Warshall、SPFA
 */
public class ShortestPath {

    // ==================== Bellman-Ford ====================

    /** Bellman-Ford — 可处理负权边，检测负环。O(VE) */
    public static int[] bellmanFord(int n, int[][] edges, int start) {
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[start] = 0;
        for (int i = 0; i < n - 1; i++) {
            boolean updated = false;
            for (int[] e : edges) {
                int u = e[0], v = e[1], w = e[2];
                if (dist[u] != Integer.MAX_VALUE && dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                    updated = true;
                }
            }
            if (!updated) break;
        }
        // 第 n 轮检测负环
        for (int[] e : edges) {
            if (dist[e[0]] != Integer.MAX_VALUE && dist[e[0]] + e[2] < dist[e[1]]) {
                return null; // 有负环
            }
        }
        return dist;
    }

    // ==================== Floyd-Warshall ====================

    /** Floyd-Warshall — 全源最短路径。O(V³) */
    public static int[][] floydWarshall(int n, int[][] edges) {
        int INF = Integer.MAX_VALUE / 2;
        int[][] dist = new int[n][n];
        for (int i = 0; i < n; i++) Arrays.fill(dist[i], INF);
        for (int i = 0; i < n; i++) dist[i][i] = 0;
        for (int[] e : edges) dist[e[0]][e[1]] = Math.min(dist[e[0]][e[1]], e[2]);

        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (dist[i][k] + dist[k][j] < dist[i][j])
                        dist[i][j] = dist[i][k] + dist[k][j];
        return dist;
    }

    // ==================== SPFA ====================

    /** SPFA — Bellman-Ford 的队列优化，平均 O(E) */
    public static int[] spfa(int n, int[][] edges, int start) {
        List<int[]>[] graph = new ArrayList[n];
        for (int i = 0; i < n; i++) graph[i] = new ArrayList<>();
        for (int[] e : edges) graph[e[0]].add(new int[]{e[1], e[2]});

        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[start] = 0;

        int[] count = new int[n]; // 入队次数，用于检测负环
        boolean[] inQueue = new boolean[n];
        Queue<Integer> q = new LinkedList<>();
        q.offer(start);
        inQueue[start] = true;

        while (!q.isEmpty()) {
            int u = q.poll();
            inQueue[u] = false;
            for (int[] edge : graph[u]) {
                int v = edge[0], w = edge[1];
                if (dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                    if (!inQueue[v]) {
                        q.offer(v);
                        inQueue[v] = true;
                        if (++count[v] >= n) return null; // 负环
                    }
                }
            }
        }
        return dist;
    }
}
