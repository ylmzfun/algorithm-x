package com.algorithmx.algorithm.graph;

import java.util.*;

/**
 * 图论进阶：强连通分量 + 最大流
 */
public class AdvancedGraph {

    // ==================== Tarjan SCC ====================

    private int time;

    /** 返回所有强连通分量 */
    public static List<List<Integer>> tarjanSCC(int n, List<Integer>[] graph) {
        return new AdvancedGraph().scc(n, graph);
    }

    private List<List<Integer>> scc(int n, List<Integer>[] graph) {
        int[] disc = new int[n], low = new int[n];
        Arrays.fill(disc, -1);
        boolean[] onStack = new boolean[n];
        Deque<Integer> stack = new ArrayDeque<>();
        List<List<Integer>> result = new ArrayList<>();

        for (int i = 0; i < n; i++) if (disc[i] == -1) dfs(i, graph, disc, low, onStack, stack, result);
        return result;
    }

    private void dfs(int u, List<Integer>[] graph, int[] disc, int[] low,
                     boolean[] onStack, Deque<Integer> stack, List<List<Integer>> result) {
        disc[u] = low[u] = time++;
        stack.push(u);
        onStack[u] = true;
        for (int v : graph[u]) {
            if (disc[v] == -1) { dfs(v, graph, disc, low, onStack, stack, result); low[u] = Math.min(low[u], low[v]); }
            else if (onStack[v]) low[u] = Math.min(low[u], disc[v]);
        }
        if (low[u] == disc[u]) { // u 是 SCC 的根
            List<Integer> comp = new ArrayList<>();
            int v;
            do { v = stack.pop(); onStack[v] = false; comp.add(v); } while (v != u);
            result.add(comp);
        }
    }

    // ==================== 最大流 — Edmonds-Karp (BFS) ====================

    /** 返回从 s 到 t 的最大流，graph[u][v] = 剩余容量 */
    public static int maxFlow(int n, int[][] capacity, int s, int t) {
        int[][] residual = new int[n][n];
        for (int i = 0; i < n; i++) System.arraycopy(capacity[i], 0, residual[i], 0, n);

        int[] parent = new int[n];
        int maxFlow = 0;

        while (bfs(residual, s, t, parent)) {
            int pathFlow = Integer.MAX_VALUE;
            for (int v = t; v != s; v = parent[v])
                pathFlow = Math.min(pathFlow, residual[parent[v]][v]);
            for (int v = t; v != s; v = parent[v]) {
                residual[parent[v]][v] -= pathFlow;
                residual[v][parent[v]] += pathFlow;
            }
            maxFlow += pathFlow;
        }
        return maxFlow;
    }

    private static boolean bfs(int[][] r, int s, int t, int[] parent) {
        Arrays.fill(parent, -1);
        Queue<Integer> q = new LinkedList<>();
        q.offer(s); parent[s] = s;
        while (!q.isEmpty()) {
            int u = q.poll();
            for (int v = 0; v < r.length; v++) {
                if (parent[v] == -1 && r[u][v] > 0) {
                    parent[v] = u;
                    if (v == t) return true;
                    q.offer(v);
                }
            }
        }
        return false;
    }
}
