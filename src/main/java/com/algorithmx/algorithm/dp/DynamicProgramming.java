package com.algorithmx.algorithm.dp;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/**
 * 动态规划经典问题
 */
public class DynamicProgramming {

    // ==================== 背包 ====================

    /** 0-1 背包：容量 W，物品重量 wt[] 价值 val[]，求最大价值 */
    public static int knapsack01(int W, int[] wt, int[] val) {
        int n = wt.length;
        int[] dp = new int[W + 1];
        for (int i = 0; i < n; i++) {
            for (int w = W; w >= wt[i]; w--) {
                dp[w] = Math.max(dp[w], dp[w - wt[i]] + val[i]);
            }
        }
        return dp[W];
    }

    /** 完全背包：每种物品无限个 */
    public static int unboundedKnapsack(int W, int[] wt, int[] val) {
        int[] dp = new int[W + 1];
        for (int w = 0; w <= W; w++) {
            for (int i = 0; i < wt.length; i++) {
                if (w >= wt[i]) dp[w] = Math.max(dp[w], dp[w - wt[i]] + val[i]);
            }
        }
        return dp[W];
    }

    // ==================== 序列 DP ====================

    /** 最长递增子序列 LIS — O(n log n) */
    public static int lengthOfLIS(int[] nums) {
        List<Integer> tails = new ArrayList<>();
        for (int x : nums) {
            int idx = Collections.binarySearch(tails, x);
            if (idx < 0) idx = -(idx + 1);
            if (idx == tails.size()) tails.add(x);
            else tails.set(idx, x);
        }
        return tails.size();
    }

    /** 最长公共子序列 LCS */
    public static int longestCommonSubsequence(String a, String b) {
        int m = a.length(), n = b.length();
        int[][] dp = new int[m + 1][n + 1];
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (a.charAt(i - 1) == b.charAt(j - 1)) dp[i][j] = dp[i - 1][j - 1] + 1;
                else dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
        return dp[m][n];
    }

    /** 编辑距离 */
    public static int editDistance(String a, String b) {
        int m = a.length(), n = b.length();
        int[][] dp = new int[m + 1][n + 1];
        for (int i = 0; i <= m; i++) dp[i][0] = i;
        for (int j = 0; j <= n; j++) dp[0][j] = j;
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (a.charAt(i - 1) == b.charAt(j - 1)) dp[i][j] = dp[i - 1][j - 1];
                else dp[i][j] = 1 + Math.min(dp[i - 1][j - 1],
                                   Math.min(dp[i - 1][j], dp[i][j - 1]));
            }
        }
        return dp[m][n];
    }

    // ==================== 打家劫舍 ====================

    /** 打家劫舍 I — 不能偷相邻 */
    public static int rob(int[] nums) {
        int prev = 0, curr = 0;
        for (int x : nums) {
            int tmp = curr;
            curr = Math.max(curr, prev + x);
            prev = tmp;
        }
        return curr;
    }

    /** 打家劫舍 II — 环形 */
    public static int robCircle(int[] nums) {
        if (nums.length == 1) return nums[0];
        return Math.max(robRange(nums, 0, nums.length - 2),
                        robRange(nums, 1, nums.length - 1));
    }

    private static int robRange(int[] nums, int start, int end) {
        int prev = 0, curr = 0;
        for (int i = start; i <= end; i++) {
            int tmp = curr;
            curr = Math.max(curr, prev + nums[i]);
            prev = tmp;
        }
        return curr;
    }

    // ==================== 爬楼梯 ====================

    /** 爬楼梯 — n 级台阶，一次 1 或 2 步 */
    public static int climbStairs(int n) {
        if (n <= 2) return n;
        int a = 1, b = 2;
        for (int i = 3; i <= n; i++) {
            int c = a + b; a = b; b = c;
        }
        return b;
    }

    /** 最小路径和 — m × n 网格 */
    public static int minPathSum(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int[] dp = new int[n];
        dp[0] = grid[0][0];
        for (int j = 1; j < n; j++) dp[j] = dp[j - 1] + grid[0][j];
        for (int i = 1; i < m; i++) {
            dp[0] += grid[i][0];
            for (int j = 1; j < n; j++) {
                dp[j] = Math.min(dp[j], dp[j - 1]) + grid[i][j];
            }
        }
        return dp[n - 1];
    }

    // ==================== 多重背包 ====================

    /** 多重背包：每种物品最多有 limit[i] 件，二进制优化 O(W·Σlog(limit)) */
    public static int knapsackBounded(int W, int[] wt, int[] val, int[] limit) {
        int[] dp = new int[W + 1];
        for (int i = 0; i < wt.length; i++) {
            int count = limit[i];
            for (int k = 1; count > 0; k <<= 1) {
                int take = Math.min(k, count);
                count -= take;
                int w = take * wt[i], v = take * val[i];
                for (int j = W; j >= w; j--) {
                    dp[j] = Math.max(dp[j], dp[j - w] + v);
                }
            }
        }
        return dp[W];
    }

    // ==================== 区间 DP ====================

    /** 矩阵链乘法 — 最小标量乘法次数：
     *  dimensions[i] 表示第 i 个矩阵的行数，dimensions[i+1] 是其列数 */
    public static int matrixChainOrder(int[] dims) {
        int n = dims.length - 1;
        int[][] dp = new int[n][n];
        for (int len = 2; len <= n; len++) {
            for (int i = 0; i + len - 1 < n; i++) {
                int j = i + len - 1;
                dp[i][j] = Integer.MAX_VALUE;
                for (int k = i; k < j; k++) {
                    int cost = dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1];
                    dp[i][j] = Math.min(dp[i][j], cost);
                }
            }
        }
        return dp[0][n - 1];
    }

    /** 戳气球 — 区间 DP 变体 */
    public static int burstBalloons(int[] nums) {
        int n = nums.length;
        int[] arr = new int[n + 2];
        arr[0] = arr[n + 1] = 1;
        System.arraycopy(nums, 0, arr, 1, n);
        int[][] dp = new int[n + 2][n + 2];
        for (int len = 1; len <= n; len++) {
            for (int i = 1; i + len - 1 <= n; i++) {
                int j = i + len - 1;
                for (int k = i; k <= j; k++) {
                    dp[i][j] = Math.max(dp[i][j],
                        dp[i][k - 1] + dp[k + 1][j] + arr[i - 1] * arr[k] * arr[j + 1]);
                }
            }
        }
        return dp[1][n];
    }

    // ==================== 状态压缩 DP ====================

    /** 旅行商问题 TSP — 最短路径遍历所有城市返回起点 */
    public static int tsp(int[][] dist) {
        int n = dist.length, fullMask = (1 << n) - 1;
        int[][] dp = new int[1 << n][n];
        for (int[] row : dp) Arrays.fill(row, Integer.MAX_VALUE / 2);
        dp[1][0] = 0;
        for (int mask = 1; mask <= fullMask; mask++) {
            for (int u = 0; u < n; u++) {
                if ((mask & (1 << u)) == 0) continue;
                for (int v = 0; v < n; v++) {
                    if ((mask & (1 << v)) != 0) continue;
                    dp[mask | (1 << v)][v] = Math.min(dp[mask | (1 << v)][v],
                                                       dp[mask][u] + dist[u][v]);
                }
            }
        }
        int ans = Integer.MAX_VALUE / 2;
        for (int u = 1; u < n; u++) ans = Math.min(ans, dp[fullMask][u] + dist[u][0]);
        return ans;
    }

    /** 最大子数组和 — Kadane 算法 */
    public static int maxSubArray(int[] nums) {
        int cur = nums[0], max = nums[0];
        for (int i = 1; i < nums.length; i++) {
            cur = Math.max(nums[i], cur + nums[i]);
            max = Math.max(max, cur);
        }
        return max;
    }
}
