package com.algorithmx.datastructure.fenwick;

/**
 * 树状数组（Fenwick Tree / Binary Indexed Tree）
 * 单点更新 O(log n)，前缀和查询 O(log n)
 */
public class FenwickTree {
    private final int[] tree;
    private final int n;

    public FenwickTree(int n) { this.n = n; this.tree = new int[n + 1]; }

    /** 在位置 idx（1-based）增加 delta */
    public void update(int idx, int delta) {
        while (idx <= n) { tree[idx] += delta; idx += idx & -idx; }
    }

    /** 查询 [1..idx] 的前缀和 */
    public int query(int idx) {
        int sum = 0;
        while (idx > 0) { sum += tree[idx]; idx -= idx & -idx; }
        return sum;
    }

    /** 查询 [l, r] 的区间和 */
    public int rangeQuery(int l, int r) {
        return query(r) - query(l - 1);
    }

    /** 用数组初始化树状数组 */
    public static FenwickTree fromArray(int[] arr) {
        FenwickTree ft = new FenwickTree(arr.length);
        for (int i = 0; i < arr.length; i++) ft.update(i + 1, arr[i]);
        return ft;
    }
}
