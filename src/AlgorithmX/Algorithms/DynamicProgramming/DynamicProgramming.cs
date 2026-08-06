namespace AlgorithmX.Algorithms.DynamicProgramming;

/// <summary>
/// 动态规划经典模型。
/// </summary>
public static class DynamicProgramming
{
    // ═══════════════════════════════════════════
    // 线性 DP
    // ═══════════════════════════════════════════

    /// <summary>
    /// 爬楼梯 — 每次爬 1 或 2 阶，到第 n 阶有多少种方法。O(n)，O(1)。
    /// </summary>
    public static int ClimbStairs(int n)
    {
        if (n <= 2) return n;
        int prev2 = 1, prev1 = 2;
        for (int i = 3; i <= n; i++)
        {
            int curr = prev2 + prev1;
            prev2 = prev1;
            prev1 = curr;
        }
        return prev1;
    }

    /// <summary>
    /// 最大子数组和 (Kadane)。O(n)，O(1)。
    /// </summary>
    public static int MaxSubArray(int[] nums)
    {
        int maxSoFar = nums[0];
        int maxEndingHere = nums[0];
        for (int i = 1; i < nums.Length; i++)
        {
            maxEndingHere = Math.Max(nums[i], maxEndingHere + nums[i]);
            maxSoFar = Math.Max(maxSoFar, maxEndingHere);
        }
        return maxSoFar;
    }

    /// <summary>
    /// 打家劫舍 — 不能偷相邻房屋，求最大收益。O(n)。
    /// </summary>
    public static int Rob(int[] nums)
    {
        if (nums.Length == 0) return 0;
        if (nums.Length == 1) return nums[0];
        int prev2 = nums[0];
        int prev1 = Math.Max(nums[0], nums[1]);
        for (int i = 2; i < nums.Length; i++)
        {
            int curr = Math.Max(prev1, prev2 + nums[i]);
            prev2 = prev1;
            prev1 = curr;
        }
        return prev1;
    }

    // ═══════════════════════════════════════════
    // 0-1 背包
    // ═══════════════════════════════════════════

    /// <summary>
    /// 0-1 背包 — 每件物品只能选一次，求最大价值。
    /// O(n·capacity)，空间优化至一维。
    /// </summary>
    public static int Knapsack01(int[] weights, int[] values, int capacity)
    {
        int n = weights.Length;
        var dp = new int[capacity + 1];
        for (int i = 0; i < n; i++)
        {
            for (int w = capacity; w >= weights[i]; w--)
            {
                dp[w] = Math.Max(dp[w], dp[w - weights[i]] + values[i]);
            }
        }
        return dp[capacity];
    }

    /// <summary>
    /// 完全背包 — 每件物品无限次使用。O(n·capacity)。
    /// </summary>
    public static int KnapsackComplete(int[] weights, int[] values, int capacity)
    {
        var dp = new int[capacity + 1];
        for (int i = 0; i < weights.Length; i++)
        {
            for (int w = weights[i]; w <= capacity; w++)
            {
                dp[w] = Math.Max(dp[w], dp[w - weights[i]] + values[i]);
            }
        }
        return dp[capacity];
    }

    // ═══════════════════════════════════════════
    // 最长公共子序列 (LCS)
    // ═══════════════════════════════════════════

    /// <summary>
    /// 最长公共子序列长度。O(m·n)。
    /// </summary>
    public static int LongestCommonSubsequence(string text1, string text2)
    {
        int m = text1.Length, n = text2.Length;
        var dp = new int[m + 1, n + 1];
        for (int i = 1; i <= m; i++)
        {
            for (int j = 1; j <= n; j++)
            {
                if (text1[i - 1] == text2[j - 1])
                    dp[i, j] = dp[i - 1, j - 1] + 1;
                else
                    dp[i, j] = Math.Max(dp[i - 1, j], dp[i, j - 1]);
            }
        }
        return dp[m, n];
    }

    /// <summary>
    /// 最长递增子序列 (LIS) — 贪心+二分。O(n log n)。
    /// </summary>
    public static int LengthOfLIS(int[] nums)
    {
        var tails = new List<int>();
        foreach (int x in nums)
        {
            int i = tails.BinarySearch(x);
            if (i < 0) i = ~i;
            if (i == tails.Count)
                tails.Add(x);
            else
                tails[i] = x;
        }
        return tails.Count;
    }

    /// <summary>
    /// 最长回文子序列长度。O(n²)。
    /// </summary>
    public static int LongestPalindromeSubseq(string s)
    {
        int n = s.Length;
        var dp = new int[n, n];
        for (int i = n - 1; i >= 0; i--)
        {
            dp[i, i] = 1;
            for (int j = i + 1; j < n; j++)
            {
                if (s[i] == s[j])
                    dp[i, j] = dp[i + 1, j - 1] + 2;
                else
                    dp[i, j] = Math.Max(dp[i + 1, j], dp[i, j - 1]);
            }
        }
        return dp[0, n - 1];
    }

    // ═══════════════════════════════════════════
    // 编辑距离
    // ═══════════════════════════════════════════

    /// <summary>
    /// 编辑距离 (Levenshtein) — 将 word1 变为 word2 的最少操作数（插入/删除/替换）。
    /// O(m·n)。
    /// </summary>
    public static int EditDistance(string word1, string word2)
    {
        int m = word1.Length, n = word2.Length;
        var dp = new int[m + 1, n + 1];

        for (int i = 0; i <= m; i++) dp[i, 0] = i;
        for (int j = 0; j <= n; j++) dp[0, j] = j;

        for (int i = 1; i <= m; i++)
        {
            for (int j = 1; j <= n; j++)
            {
                if (word1[i - 1] == word2[j - 1])
                    dp[i, j] = dp[i - 1, j - 1];
                else
                    dp[i, j] = 1 + Math.Min(Math.Min(dp[i - 1, j], dp[i, j - 1]), dp[i - 1, j - 1]);
            }
        }
        return dp[m, n];
    }

    // ═══════════════════════════════════════════
    // 硬币找零
    // ═══════════════════════════════════════════

    /// <summary>
    /// 零钱兑换 — 用最少的硬币凑出 amount。无法凑出返回 -1。
    /// 完全背包变种。O(n·amount)。
    /// </summary>
    public static int CoinChange(int[] coins, int amount)
    {
        var dp = new int[amount + 1];
        Array.Fill(dp, amount + 1);
        dp[0] = 0;

        foreach (int coin in coins)
        {
            for (int a = coin; a <= amount; a++)
            {
                dp[a] = Math.Min(dp[a], dp[a - coin] + 1);
            }
        }
        return dp[amount] > amount ? -1 : dp[amount];
    }
}
