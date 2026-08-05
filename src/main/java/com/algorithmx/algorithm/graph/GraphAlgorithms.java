package com.algorithmx.algorithm.graph;

import java.util.*;

/**
 * 图论经典算法
 */
public class GraphAlgorithms {

    // ==================== Dijkstra — 单源最短路径 ====================

    /** 邻接表 + 优先队列，O(E log V) */
    public static int[] dijkstra(int n, int[][] edges, int start) {
        // 建图
        List<int[]>[] graph = new ArrayList[n];
        for (int i = 0; i < n; i++) graph[i] = new ArrayList<>();
        for (int[] e : edges) graph[e[0]].add(new int[]{e[1], e[2]});

        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[start] = 0;

        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[1]));
        pq.offer(new int[]{start, 0});

        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            int u = cur[0], d = cur[1];
            if (d > dist[u]) continue;
            for (int[] edge : graph[u]) {
                int v = edge[0], w = edge[1];
                if (dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                    pq.offer(new int[]{v, dist[v]});
                }
            }
        }
        return dist;
    }

    // ==================== Kruskal — 最小生成树 ====================

    public static int kruskal(int n, int[][] edges) {
        Arrays.sort(edges, Comparator.comparingInt(e -> e[2]));
        // 并查集
        int[] parent = new int[n];
        int[] rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;

        int totalWeight = 0, edgesUsed = 0;
        for (int[] e : edges) {
            int u = e[0], v = e[1], w = e[2];
            if (find(parent, u) != find(parent, v)) {
                union(parent, rank, u, v);
                totalWeight += w;
                edgesUsed++;
                if (edgesUsed == n - 1) break;
            }
        }
        return totalWeight;
    }

    private static int find(int[] parent, int x) {
        if (parent[x] != x) parent[x] = find(parent, parent[x]);
        return parent[x];
    }

    private static void union(int[] parent, int[] rank, int x, int y) {
        int rx = find(parent, x), ry = find(parent, y);
        if (rx == ry) return;
        if (rank[rx] < rank[ry]) parent[rx] = ry;
        else if (rank[rx] > rank[ry]) parent[ry] = rx;
        else { parent[ry] = rx; rank[rx]++; }
    }

    // ==================== Prim — 最小生成树 ====================

    public static int prim(int n, int[][] edges) {
        List<int[]>[] graph = new ArrayList[n];
        for (int i = 0; i < n; i++) graph[i] = new ArrayList<>();
        for (int[] e : edges) {
            graph[e[0]].add(new int[]{e[1], e[2]});
            graph[e[1]].add(new int[]{e[0], e[2]});
        }

        boolean[] visited = new boolean[n];
        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[1]));
        pq.offer(new int[]{0, 0}); // {node, weight}

        int totalWeight = 0, nodesInTree = 0;
        while (!pq.isEmpty() && nodesInTree < n) {
            int[] cur = pq.poll();
            int u = cur[0], w = cur[1];
            if (visited[u]) continue;
            visited[u] = true;
            totalWeight += w;
            nodesInTree++;
            for (int[] edge : graph[u]) {
                if (!visited[edge[0]]) pq.offer(edge);
            }
        }
        return totalWeight;
    }
}
