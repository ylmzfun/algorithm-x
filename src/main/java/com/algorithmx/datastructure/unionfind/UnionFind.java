package com.algorithmx.datastructure.unionfind;

/**
 * 并查集 — 路径压缩 + 按秩合并
 */
public class UnionFind {
    private final int[] parent;
    private final int[] rank;
    private int count; // 连通分量数

    public UnionFind(int n) {
        parent = new int[n];
        rank = new int[n];
        count = n;
        for (int i = 0; i < n; i++) parent[i] = i;
    }

    public int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]); // 路径压缩
        return parent[x];
    }

    public void union(int x, int y) {
        int rootX = find(x), rootY = find(y);
        if (rootX == rootY) return;
        // 按秩合并
        if (rank[rootX] < rank[rootY]) {
            parent[rootX] = rootY;
        } else if (rank[rootX] > rank[rootY]) {
            parent[rootY] = rootX;
        } else {
            parent[rootY] = rootX;
            rank[rootX]++;
        }
        count--;
    }

    public boolean connected(int x, int y) { return find(x) == find(y); }
    public int count() { return count; }
}
