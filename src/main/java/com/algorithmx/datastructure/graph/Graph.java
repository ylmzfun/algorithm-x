package com.algorithmx.datastructure.graph;

import java.util.*;

/**
 * 图的表示与遍历
 */
public class Graph {
    private final int V;
    private final List<Integer>[] adj;

    @SuppressWarnings("unchecked")
    public Graph(int V) {
        this.V = V;
        adj = new ArrayList[V];
        for (int i = 0; i < V; i++) adj[i] = new ArrayList<>();
    }

    // 无向图加边
    public void addEdge(int u, int v) { adj[u].add(v); adj[v].add(u); }

    public int V() { return V; }
    public List<Integer> adj(int v) { return adj[v]; }

    // ---- 遍历 ----

    /** DFS（递归） */
    public List<Integer> dfs(int start) {
        List<Integer> res = new ArrayList<>();
        boolean[] visited = new boolean[V];
        dfs(start, visited, res);
        return res;
    }

    private void dfs(int v, boolean[] visited, List<Integer> res) {
        visited[v] = true;
        res.add(v);
        for (int w : adj[v]) {
            if (!visited[w]) dfs(w, visited, res);
        }
    }

    /** BFS */
    public List<Integer> bfs(int start) {
        List<Integer> res = new ArrayList<>();
        boolean[] visited = new boolean[V];
        Queue<Integer> q = new LinkedList<>();
        visited[start] = true;
        q.offer(start);
        while (!q.isEmpty()) {
            int v = q.poll();
            res.add(v);
            for (int w : adj[v]) {
                if (!visited[w]) { visited[w] = true; q.offer(w); }
            }
        }
        return res;
    }

    /** 连通分量个数 */
    public int connectedComponents() {
        boolean[] visited = new boolean[V];
        int count = 0;
        for (int v = 0; v < V; v++) {
            if (!visited[v]) { count++; dfs(v, visited, new ArrayList<>()); }
        }
        return count;
    }

    // ---- 拓扑排序（Kahn BFS） ----
    // 注意：拓扑排序需要在有向图上，这里单独提供一个静态方法

    public static List<Integer> topologicalSort(int V, int[][] edges) {
        List<Integer>[] adj = new ArrayList[V];
        int[] indegree = new int[V];
        for (int i = 0; i < V; i++) adj[i] = new ArrayList<>();
        for (int[] e : edges) { adj[e[0]].add(e[1]); indegree[e[1]]++; }

        Queue<Integer> q = new LinkedList<>();
        for (int i = 0; i < V; i++) if (indegree[i] == 0) q.offer(i);

        List<Integer> res = new ArrayList<>();
        while (!q.isEmpty()) {
            int v = q.poll();
            res.add(v);
            for (int w : adj[v]) {
                if (--indegree[w] == 0) q.offer(w);
            }
        }
        return res.size() == V ? res : new ArrayList<>(); // size < V 说明有环
    }
}
