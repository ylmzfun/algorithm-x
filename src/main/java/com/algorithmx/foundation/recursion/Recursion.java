package com.algorithmx.foundation.recursion;

import java.util.*;

/**
 * 递归经典问题
 */
public class Recursion {

    // ==================== 基础 ====================

    /** 阶乘 */
    public static long factorial(int n) {
        if (n <= 1) return 1;
        return n * factorial(n - 1);
    }

    /** 斐波那契（递归） */
    public static int fibRecursive(int n) {
        if (n <= 1) return n;
        return fibRecursive(n - 1) + fibRecursive(n - 2);
    }

    /** 斐波那契（记忆化） */
    public static int fibMemo(int n) {
        return fibMemo(n, new int[n + 1]);
    }

    private static int fibMemo(int n, int[] memo) {
        if (n <= 1) return n;
        if (memo[n] != 0) return memo[n];
        return memo[n] = fibMemo(n - 1, memo) + fibMemo(n - 2, memo);
    }

    // ==================== 分治 ====================

    /** 快速幂：计算 x^n */
    public static double fastPow(double x, int n) {
        if (n == 0) return 1;
        if (n < 0) return 1 / fastPowHelper(x, -(long) n);
        return fastPowHelper(x, n);
    }

    private static double fastPowHelper(double x, long n) {
        if (n == 0) return 1;
        double half = fastPowHelper(x, n / 2);
        return n % 2 == 0 ? half * half : half * half * x;
    }

    /** 汉诺塔 */
    public static List<String> hanoi(int n) {
        List<String> moves = new ArrayList<>();
        hanoi(n, 'A', 'C', 'B', moves);
        return moves;
    }

    private static void hanoi(int n, char from, char to, char aux, List<String> moves) {
        if (n == 1) { moves.add(from + " -> " + to); return; }
        hanoi(n - 1, from, aux, to, moves);
        moves.add(from + " -> " + to);
        hanoi(n - 1, aux, to, from, moves);
    }

    // ==================== 生成 ====================

    /** 生成括号 — 给定 n，生成所有合法括号组合 */
    public static List<String> generateParenthesis(int n) {
        List<String> res = new ArrayList<>();
        genParen(new StringBuilder(), n, n, res);
        return res;
    }

    private static void genParen(StringBuilder sb, int left, int right, List<String> res) {
        if (left == 0 && right == 0) { res.add(sb.toString()); return; }
        if (left > 0) { sb.append('('); genParen(sb, left - 1, right, res); sb.deleteCharAt(sb.length() - 1); }
        if (right > left) { sb.append(')'); genParen(sb, left, right - 1, res); sb.deleteCharAt(sb.length() - 1); }
    }

    /** 电话号码的字母组合 */
    private static final String[] DIGIT_MAP = {"", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};

    public static List<String> letterCombinations(String digits) {
        List<String> res = new ArrayList<>();
        if (digits.isEmpty()) return res;
        combine(digits, 0, new StringBuilder(), res);
        return res;
    }

    private static void combine(String digits, int idx, StringBuilder sb, List<String> res) {
        if (idx == digits.length()) { res.add(sb.toString()); return; }
        for (char c : DIGIT_MAP[digits.charAt(idx) - '0'].toCharArray()) {
            sb.append(c);
            combine(digits, idx + 1, sb, res);
            sb.deleteCharAt(sb.length() - 1);
        }
    }
}
