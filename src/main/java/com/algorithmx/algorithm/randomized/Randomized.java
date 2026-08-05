package com.algorithmx.algorithm.randomized;

import java.util.*;

/**
 * 随机化算法
 */
public class Randomized {

    // ==================== Fisher-Yates 洗牌 ====================

    /** 原地洗牌，O(n)，每种排列等概率 */
    public static void shuffle(int[] arr) {
        Random rand = new Random();
        for (int i = arr.length - 1; i > 0; i--) {
            int j = rand.nextInt(i + 1);
            int tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
        }
    }

    // ==================== 蓄水池抽样 ====================

    /**
     * 从无限流中随机抽取 k 个样本。
     * 每个元素被选中的概率恒为 k / n。
     */
    public static int[] reservoirSample(Iterator<Integer> stream, int k) {
        int[] reservoir = new int[k];
        int i = 0;
        Random rand = new Random();
        while (stream.hasNext() && i < k) reservoir[i++] = stream.next();
        while (stream.hasNext()) {
            int val = stream.next();
            int j = rand.nextInt(++i);
            if (j < k) reservoir[j] = val;
        }
        return reservoir;
    }

    // ==================== 随机选择（QuickSelect） ====================

    /** 找第 k 小的元素（k 从 0 开始），O(n) 期望 */
    public static int quickSelect(int[] nums, int k) {
        return quickSelect(nums, 0, nums.length - 1, k);
    }

    private static int quickSelect(int[] nums, int left, int right, int k) {
        if (left == right) return nums[left];
        Random rand = new Random();
        int pivotIdx = left + rand.nextInt(right - left + 1);
        swap(nums, pivotIdx, right);
        int p = partition(nums, left, right);
        if (k == p) return nums[p];
        return k < p ? quickSelect(nums, left, p - 1, k) : quickSelect(nums, p + 1, right, k);
    }

    private static int partition(int[] nums, int left, int right) {
        int pivot = nums[right], i = left;
        for (int j = left; j < right; j++)
            if (nums[j] < pivot) swap(nums, i++, j);
        swap(nums, i, right);
        return i;
    }

    private static void swap(int[] arr, int i, int j) { int t = arr[i]; arr[i] = arr[j]; arr[j] = t; }
}
