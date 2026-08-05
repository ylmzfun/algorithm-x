package com.algorithmx.algorithm.string;

import java.util.*;

/**
 * Rabin-Karp 滚动哈希 & Manacher 最长回文子串
 */
public class StringMatching {

    // ==================== Rabin-Karp ====================

    private static final int BASE = 256;
    private static final int MOD = 1_000_000_007;

    /** 返回 pattern 在 text 中出现的所有起始下标 */
    public static List<Integer> rabinKarp(String text, String pattern) {
        List<Integer> res = new ArrayList<>();
        int n = text.length(), m = pattern.length();
        if (m > n) return res;

        long pHash = 0, tHash = 0, highestPow = 1;
        for (int i = 0; i < m; i++) {
            pHash = (pHash * BASE + pattern.charAt(i)) % MOD;
            tHash = (tHash * BASE + text.charAt(i)) % MOD;
            if (i < m - 1) highestPow = (highestPow * BASE) % MOD;
        }

        for (int i = 0; i <= n - m; i++) {
            if (pHash == tHash && text.substring(i, i + m).equals(pattern)) res.add(i);
            if (i < n - m) {
                tHash = (tHash - text.charAt(i) * highestPow % MOD + MOD) % MOD;
                tHash = (tHash * BASE + text.charAt(i + m)) % MOD;
            }
        }
        return res;
    }

    // ==================== Manacher — 最长回文子串 ====================

    /** 返回最长回文子串 */
    public static String longestPalindrome(String s) {
        if (s.isEmpty()) return s;
        // 预处理：插入 # 使得奇偶统一
        StringBuilder sb = new StringBuilder("^#");
        for (char c : s.toCharArray()) sb.append(c).append('#');
        sb.append('$');
        String t = sb.toString();

        int n = t.length();
        int[] pal = new int[n]; // 回文半径
        int center = 0, right = 0, maxLen = 0, maxCenter = 0;

        for (int i = 1; i < n - 1; i++) {
            int mirror = 2 * center - i;
            if (i < right) pal[i] = Math.min(right - i, pal[mirror]);
            while (t.charAt(i + pal[i] + 1) == t.charAt(i - pal[i] - 1)) pal[i]++;
            if (i + pal[i] > right) { center = i; right = i + pal[i]; }
            if (pal[i] > maxLen) { maxLen = pal[i]; maxCenter = i; }
        }
        int start = (maxCenter - maxLen) / 2;
        return s.substring(start, start + maxLen);
    }

    /** 返回最长回文子串长度 */
    public static int longestPalindromeLength(String s) {
        return longestPalindrome(s).length();
    }
}
