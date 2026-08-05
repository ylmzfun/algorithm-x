package com.algorithmx.algorithm.string;

/**
 * Z Algorithm — 线性时间字符串匹配
 *
 * z[i] = s[i..] 与 s 的最长公共前缀长度。
 * 可用于 O(n+m) 时间在 text 中匹配 pattern：
 *   构造 P + "$" + T，查找 z[i] == P.length() 的位置。
 */
public class ZAlgorithm {

    /** 计算 Z 数组 */
    public static int[] computeZ(String s) {
        int n = s.length();
        int[] z = new int[n];
        int l = 0, r = 0;
        for (int i = 1; i < n; i++) {
            if (i <= r) z[i] = Math.min(r - i + 1, z[i - l]);
            while (i + z[i] < n && s.charAt(z[i]) == s.charAt(i + z[i])) z[i]++;
            if (i + z[i] - 1 > r) { l = i; r = i + z[i] - 1; }
        }
        return z;
    }

    /** 在 text 中搜索 pattern，返回所有匹配起始下标 */
    public static java.util.List<Integer> search(String text, String pattern) {
        String combined = pattern + "$" + text;
        int[] z = computeZ(combined);
        java.util.List<Integer> res = new java.util.ArrayList<>();
        int plen = pattern.length();
        for (int i = plen + 1; i < z.length; i++) {
            if (z[i] == plen) res.add(i - plen - 1);
        }
        return res;
    }
}
