package com.algorithmx.technique.bit;

/**
 * 位运算常用技巧
 */
public class BitManipulation {

    /** 判断奇偶 */
    public static boolean isOdd(int n) { return (n & 1) == 1; }

    /** 交换两数（不借助临时变量） */
    public static int[] swap(int a, int b) {
        a ^= b; b ^= a; a ^= b;
        return new int[]{a, b};
    }

    /** 乘/除 2：乘 <<，除 >> */
    public static int multiplyBy2(int n) { return n << 1; }
    public static int divideBy2(int n) { return n >> 1; }

    /** 消去最低位的 1：n & (n - 1) */
    public static int clearLowestOne(int n) { return n & (n - 1); }

    /** 获取最低位的 1：n & -n */
    public static int getLowestOne(int n) { return n & -n; }

    /** 统计 1 的个数 */
    public static int countOnes(int n) {
        int count = 0;
        while (n != 0) { n &= n - 1; count++; }
        return count;
    }

    /** 判断是否为 2 的幂 */
    public static boolean isPowerOfTwo(int n) { return n > 0 && (n & (n - 1)) == 0; }

    /** 将第 k 位置 1 */
    public static int setBit(int n, int k) { return n | (1 << k); }

    /** 将第 k 位清零 */
    public static int clearBit(int n, int k) { return n & ~(1 << k); }

    /** 翻转第 k 位 */
    public static int toggleBit(int n, int k) { return n ^ (1 << k); }

    /** 判断第 k 位是否为 1 */
    public static boolean testBit(int n, int k) { return (n >> k & 1) == 1; }
}

/**
 * BitMap — 用于大规模去重、排序、存在性判断（内存极省）
 *
 * 思路：用 long[] 数组的每一位表示一个整数是否存在，
 * 每个 long 有 64 位，可表示 64 个连续整数。
 */
class BitMap {
    private final long[] bits;

    /** 能表示 [0, maxVal] 范围内的数 */
    public BitMap(int maxVal) {
        bits = new long[(maxVal >> 6) + 1]; // maxVal / 64 + 1
    }

    /** 将 num 加入集合 */
    public void add(int num) {
        bits[num >> 6] |= (1L << (num & 63));
    }

    /** 从集合中移除 num */
    public void remove(int num) {
        bits[num >> 6] &= ~(1L << (num & 63));
    }

    /** num 是否存在 */
    public boolean contains(int num) {
        return (bits[num >> 6] & (1L << (num & 63))) != 0;
    }
}
