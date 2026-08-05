package com.algorithmx.algorithm.greedy;

import java.util.*;

/**
 * 贪心算法经典问题
 */
public class Greedy {

    // ==================== 区间调度 ====================

    /** 最多不重叠区间 — 按结束时间贪心 */
    public static int maxNonOverlap(int[][] intervals) {
        Arrays.sort(intervals, Comparator.comparingInt(a -> a[1]));
        int count = 0, lastEnd = Integer.MIN_VALUE;
        for (int[] iv : intervals) {
            if (iv[0] >= lastEnd) { count++; lastEnd = iv[1]; }
        }
        return count;
    }

    /** 用最少数量的箭引爆气球 — 等价于找最大重叠 */
    public static int findMinArrowShots(int[][] points) {
        Arrays.sort(points, Comparator.comparingInt(a -> a[1]));
        int arrows = 1, shot = points[0][1];
        for (int i = 1; i < points.length; i++) {
            if (points[i][0] > shot) { arrows++; shot = points[i][1]; }
        }
        return arrows;
    }

    /** 合并区间 */
    public static int[][] merge(int[][] intervals) {
        Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));
        List<int[]> res = new ArrayList<>();
        int[] cur = intervals[0];
        for (int i = 1; i < intervals.length; i++) {
            if (intervals[i][0] <= cur[1]) cur[1] = Math.max(cur[1], intervals[i][1]);
            else { res.add(cur); cur = intervals[i]; }
        }
        res.add(cur);
        return res.toArray(new int[0][]);
    }

    // ==================== 跳跃游戏 ====================

    /** 跳跃游戏 I — 能否到达终点 */
    public static boolean canJump(int[] nums) {
        int farthest = 0;
        for (int i = 0; i < nums.length; i++) {
            if (i > farthest) return false;
            farthest = Math.max(farthest, i + nums[i]);
        }
        return true;
    }

    /** 跳跃游戏 II — 最少跳跃次数 */
    public static int jump(int[] nums) {
        int jumps = 0, curEnd = 0, farthest = 0;
        for (int i = 0; i < nums.length - 1; i++) {
            farthest = Math.max(farthest, i + nums[i]);
            if (i == curEnd) { jumps++; curEnd = farthest; }
        }
        return jumps;
    }

    // ==================== 其他经典 ====================

    /** 分发糖果 — 左右各扫描一次 */
    public static int candy(int[] ratings) {
        int n = ratings.length;
        int[] candies = new int[n];
        Arrays.fill(candies, 1);
        for (int i = 1; i < n; i++) if (ratings[i] > ratings[i - 1]) candies[i] = candies[i - 1] + 1;
        for (int i = n - 2; i >= 0; i--) if (ratings[i] > ratings[i + 1]) candies[i] = Math.max(candies[i], candies[i + 1] + 1);
        return Arrays.stream(candies).sum();
    }

    /** 加油站 — 能否绕一圈 */
    public static int canCompleteCircuit(int[] gas, int[] cost) {
        int total = 0, tank = 0, start = 0;
        for (int i = 0; i < gas.length; i++) {
            int diff = gas[i] - cost[i];
            total += diff; tank += diff;
            if (tank < 0) { start = i + 1; tank = 0; }
        }
        return total >= 0 ? start : -1;
    }
}
