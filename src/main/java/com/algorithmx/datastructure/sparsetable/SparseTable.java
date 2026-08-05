package com.algorithmx.datastructure.sparsetable;

/**
 * 稀疏表（Sparse Table）— O(1) 区间最小值查询
 *
 * 预处理 O(n log n)，查询 O(1)。
 * 不支持修改（静态数据结构）。
 */
public class SparseTable {
    private final int[][] st; // st[k][i] = min of [i, i+2^k)
    private final int[] log;

    public SparseTable(int[] arr) {
        int n = arr.length;
        log = new int[n + 1];
        for (int i = 2; i <= n; i++) log[i] = log[i / 2] + 1;

        int K = log[n] + 1;
        st = new int[K][n];
        System.arraycopy(arr, 0, st[0], 0, n);

        for (int k = 1; k < K; k++) {
            for (int i = 0; i + (1 << k) <= n; i++) {
                st[k][i] = Math.min(st[k - 1][i], st[k - 1][i + (1 << (k - 1))]);
            }
        }
    }

    /** 查询区间 [l, r] 的最小值（闭区间） */
    public int queryMin(int l, int r) {
        int k = log[r - l + 1];
        return Math.min(st[k][l], st[k][r - (1 << k) + 1]);
    }
}
