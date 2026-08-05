package com.algorithmx.datastructure.bloom;

import java.util.BitSet;

/**
 * 布隆过滤器 — 概率型集合，判「一定不存在」/「可能存在」
 *
 * 使用 K 个哈希函数，每个元素映射到比特数组的 K 个位置。
 * 空间效率极高，允许误判（False Positive），不存在误漏（False Negative）。
 */
public class BloomFilter {
    private final BitSet bits;
    private final int size;
    private final int hashCount;

    /**
     * @param expectedInsertions 预计插入元素数量
     * @param fpp 期望误判率（如 0.01 = 1%）
     */
    public BloomFilter(int expectedInsertions, double fpp) {
        this.size = (int) (-expectedInsertions * Math.log(fpp) / (Math.log(2) * Math.log(2)));
        this.hashCount = (int) (size * Math.log(2) / expectedInsertions);
        this.bits = new BitSet(size);
    }

    public void add(String s) {
        int[] hashes = hash(s);
        for (int h : hashes) bits.set(h);
    }

    public boolean mightContain(String s) {
        for (int h : hash(s)) if (!bits.get(h)) return false;
        return true;
    }

    private int[] hash(String s) {
        int[] res = new int[hashCount];
        long h1 = murmur64(s.getBytes(), 0x9E3779B97F4A7C15L);
        long h2 = murmur64(s.getBytes(), 0xC6A4A7935BD1E995L);
        for (int i = 0; i < hashCount; i++) {
            long combined = h1 + i * h2;
            res[i] = Math.abs((int) (combined % size));
        }
        return res;
    }

    private static long murmur64(byte[] data, long seed) {
        long m = 0xC6A4A7935BD1E995L, h = seed ^ (data.length * m);
        for (int i = 0; i + 8 <= data.length; i += 8) {
            long k = bytesToLong(data, i);
            k *= m; k ^= k >>> 47; k *= m; h ^= k; h *= m;
        }
        int rem = data.length & 7;
        if (rem != 0) {
            long k = 0;
            for (int i = data.length - rem; i < data.length; i++)
                k = (k << 8) | (data[i] & 0xFFL);
            k *= m; k ^= k >>> 47; k *= m; h ^= k; h *= m;
        }
        h ^= h >>> 47; h *= m; h ^= h >>> 47;
        return h;
    }

    private static long bytesToLong(byte[] b, int off) {
        return ((long) b[off] & 0xFF) | ((long) b[off + 1] & 0xFF) << 8
             | ((long) b[off + 2] & 0xFF) << 16 | ((long) b[off + 3] & 0xFF) << 24
             | ((long) b[off + 4] & 0xFF) << 32 | ((long) b[off + 5] & 0xFF) << 40
             | ((long) b[off + 6] & 0xFF) << 48 | ((long) b[off + 7] & 0xFF) << 56;
    }
}
