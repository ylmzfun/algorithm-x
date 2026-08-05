package com.algorithmx.algorithm.string;

/**
 * 字符串匹配算法 — KMP
 */
public class KMP {

    /** 在 text 中搜索 pattern，返回首次出现的起始下标，未找到返回 -1 */
    public static int search(String text, String pattern) {
        if (pattern.isEmpty()) return 0;
        int[] next = buildNext(pattern);
        int i = 0, j = 0;
        while (i < text.length() && j < pattern.length()) {
            if (j == -1 || text.charAt(i) == pattern.charAt(j)) { i++; j++; }
            else j = next[j];
        }
        return j == pattern.length() ? i - j : -1;
    }

    /** 构建 next 数组：next[j] 表示 pattern[0..j-1] 的最长相等前后缀长度 */
    public static int[] buildNext(String pattern) {
        int n = pattern.length();
        int[] next = new int[n];
        next[0] = -1;
        int k = -1, j = 0;
        while (j < n - 1) {
            if (k == -1 || pattern.charAt(j) == pattern.charAt(k)) {
                j++; k++;
                // 优化：避免 pattern[j] == pattern[k] 时的重复比较
                next[j] = pattern.charAt(j) != pattern.charAt(k) ? k : next[k];
            } else {
                k = next[k];
            }
        }
        return next;
    }
}
