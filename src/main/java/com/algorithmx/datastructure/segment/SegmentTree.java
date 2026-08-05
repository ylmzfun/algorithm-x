package com.algorithmx.datastructure.segment;

/**
 * 线段树（Segment Tree）
 * 支持区间求和，区间更新（惰性标记）
 */
public class SegmentTree {
    private final int[] tree;
    private final int[] lazy;
    private final int n;

    public SegmentTree(int[] arr) {
        n = arr.length;
        tree = new int[4 * n];
        lazy = new int[4 * n];
        build(arr, 1, 0, n - 1);
    }

    private void build(int[] arr, int node, int l, int r) {
        if (l == r) { tree[node] = arr[l]; return; }
        int mid = l + (r - l) / 2;
        build(arr, node * 2, l, mid);
        build(arr, node * 2 + 1, mid + 1, r);
        tree[node] = tree[node * 2] + tree[node * 2 + 1];
    }

    // ---- 区间查询 ----

    public int rangeQuery(int ql, int qr) {
        return rangeQuery(1, 0, n - 1, ql, qr);
    }

    private int rangeQuery(int node, int l, int r, int ql, int qr) {
        pushDown(node, l, r);
        if (ql > r || qr < l) return 0;
        if (ql <= l && r <= qr) return tree[node];
        int mid = l + (r - l) / 2;
        return rangeQuery(node * 2, l, mid, ql, qr)
             + rangeQuery(node * 2 + 1, mid + 1, r, ql, qr);
    }

    // ---- 区间更新（加 val） ----

    public void rangeAdd(int ql, int qr, int val) {
        rangeAdd(1, 0, n - 1, ql, qr, val);
    }

    private void rangeAdd(int node, int l, int r, int ql, int qr, int val) {
        pushDown(node, l, r);
        if (ql > r || qr < l) return;
        if (ql <= l && r <= qr) {
            lazy[node] += val;
            pushDown(node, l, r);
            return;
        }
        int mid = l + (r - l) / 2;
        rangeAdd(node * 2, l, mid, ql, qr, val);
        rangeAdd(node * 2 + 1, mid + 1, r, ql, qr, val);
        tree[node] = tree[node * 2] + tree[node * 2 + 1];
    }

    private void pushDown(int node, int l, int r) {
        if (lazy[node] != 0) {
            tree[node] += (r - l + 1) * lazy[node];
            if (l != r) {
                lazy[node * 2] += lazy[node];
                lazy[node * 2 + 1] += lazy[node];
            }
            lazy[node] = 0;
        }
    }
}
