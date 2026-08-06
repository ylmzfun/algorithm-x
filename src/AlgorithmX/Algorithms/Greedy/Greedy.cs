namespace AlgorithmX.Algorithms.Greedy;

/// <summary>
/// 贪心算法经典问题。
/// </summary>
public static class Greedy
{
    // ═══════════════════════════════════════════
    // 区间调度
    // ═══════════════════════════════════════════

    /// <summary>
    /// 无重叠区间 — 移除最少区间使剩余区间互不重叠。返回需要移除的数量。
    /// 贪心：按右端点排序，每次选最早结束的。O(n log n)。
    /// </summary>
    public static int EraseOverlapIntervals(int[][] intervals)
    {
        if (intervals.Length == 0) return 0;
        Array.Sort(intervals, (a, b) => a[1].CompareTo(b[1]));

        int count = 0;
        int end = intervals[0][1];
        for (int i = 1; i < intervals.Length; i++)
        {
            if (intervals[i][0] < end)
                count++;
            else
                end = intervals[i][1];
        }
        return count;
    }

    /// <summary>
    /// 最大不重叠区间数 — 贪心按结束时间排序选取。O(n log n)。
    /// </summary>
    public static int MaxNonOverlappingIntervals(int[][] intervals)
    {
        if (intervals.Length == 0) return 0;
        Array.Sort(intervals, (a, b) => a[1].CompareTo(b[1]));

        int count = 1;
        int end = intervals[0][1];
        for (int i = 1; i < intervals.Length; i++)
        {
            if (intervals[i][0] >= end)
            {
                count++;
                end = intervals[i][1];
            }
        }
        return count;
    }

    /// <summary>
    /// 用最少数量的箭引爆气球。与无重叠区间等价。
    /// O(n log n)。
    /// </summary>
    public static int FindMinArrowShots(int[][] points)
    {
        if (points.Length == 0) return 0;
        Array.Sort(points, (a, b) => a[1].CompareTo(b[1]));

        int arrows = 1;
        int shoot = points[0][1];
        for (int i = 1; i < points.Length; i++)
        {
            if (points[i][0] > shoot)
            {
                arrows++;
                shoot = points[i][1];
            }
        }
        return arrows;
    }

    // ═══════════════════════════════════════════
    // 跳跃游戏
    // ═══════════════════════════════════════════

    /// <summary>
    /// 跳跃游戏 — 判断是否能到达最后一个位置。O(n)。
    /// </summary>
    public static bool CanJump(int[] nums)
    {
        int maxReach = 0;
        for (int i = 0; i < nums.Length; i++)
        {
            if (i > maxReach) return false;
            maxReach = Math.Max(maxReach, i + nums[i]);
            if (maxReach >= nums.Length - 1) return true;
        }
        return true;
    }

    /// <summary>
    /// 跳跃游戏 II — 最少跳跃次数。O(n)。
    /// </summary>
    public static int Jump(int[] nums)
    {
        int jumps = 0, curEnd = 0, curFarthest = 0;
        for (int i = 0; i < nums.Length - 1; i++)
        {
            curFarthest = Math.Max(curFarthest, i + nums[i]);
            if (i == curEnd)
            {
                jumps++;
                curEnd = curFarthest;
            }
        }
        return jumps;
    }

    // ═══════════════════════════════════════════
    // 哈夫曼编码
    // ═══════════════════════════════════════════

    /// <summary>
    /// 哈夫曼编码 — 最小加权路径长度。
    /// 返回编码总代价（所有叶节点深度×频率之和）。
    /// O(n log n)。
    /// </summary>
    public static long HuffmanCoding(int[] frequencies)
    {
        var pq = new PriorityQueue<long, long>();
        foreach (int f in frequencies)
            pq.Enqueue(f, f);

        long totalCost = 0;
        while (pq.Count > 1)
        {
            long a = pq.Dequeue();
            long b = pq.Dequeue();
            long merged = a + b;
            totalCost += merged;
            pq.Enqueue(merged, merged);
        }
        return totalCost;
    }
}
