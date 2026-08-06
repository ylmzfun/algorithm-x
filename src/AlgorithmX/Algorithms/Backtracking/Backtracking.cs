namespace AlgorithmX.Algorithms.Backtracking;

/// <summary>
/// 回溯算法 — 通用框架与经典问题。
/// 核心思路：做选择 → 递归 → 撤销选择。
/// </summary>
public static class Backtracking
{
    // ═══════════════════════════════════════════
    // 子集
    // ═══════════════════════════════════════════

    /// <summary>
    /// 无重复元素的子集（幂集）。O(n·2^n)。
    /// </summary>
    public static IList<IList<int>> Subsets(int[] nums)
    {
        var result = new List<IList<int>>();
        SubsetsBacktrack(nums, 0, new List<int>(), result);
        return result;
    }

    private static void SubsetsBacktrack(int[] nums, int start, List<int> path, List<IList<int>> result)
    {
        result.Add(new List<int>(path));
        for (int i = start; i < nums.Length; i++)
        {
            path.Add(nums[i]);
            SubsetsBacktrack(nums, i + 1, path, result);
            path.RemoveAt(path.Count - 1);
        }
    }

    /// <summary>
    /// 包含重复元素的子集（去重）。需先排序。O(n·2^n)。
    /// </summary>
    public static IList<IList<int>> SubsetsWithDup(int[] nums)
    {
        Array.Sort(nums);
        var result = new List<IList<int>>();
        SubsetsWithDupBacktrack(nums, 0, new List<int>(), result);
        return result;
    }

    private static void SubsetsWithDupBacktrack(int[] nums, int start, List<int> path, List<IList<int>> result)
    {
        result.Add(new List<int>(path));
        for (int i = start; i < nums.Length; i++)
        {
            if (i > start && nums[i] == nums[i - 1]) continue; // 跳过同层重复
            path.Add(nums[i]);
            SubsetsWithDupBacktrack(nums, i + 1, path, result);
            path.RemoveAt(path.Count - 1);
        }
    }

    // ═══════════════════════════════════════════
    // 排列
    // ═══════════════════════════════════════════

    /// <summary>
    /// 全排列（无重复元素）。O(n·n!)。
    /// </summary>
    public static IList<IList<int>> Permute(int[] nums)
    {
        var result = new List<IList<int>>();
        var used = new bool[nums.Length];
        PermuteBacktrack(nums, used, new List<int>(), result);
        return result;
    }

    private static void PermuteBacktrack(int[] nums, bool[] used, List<int> path, List<IList<int>> result)
    {
        if (path.Count == nums.Length)
        {
            result.Add(new List<int>(path));
            return;
        }
        for (int i = 0; i < nums.Length; i++)
        {
            if (used[i]) continue;
            used[i] = true;
            path.Add(nums[i]);
            PermuteBacktrack(nums, used, path, result);
            path.RemoveAt(path.Count - 1);
            used[i] = false;
        }
    }

    /// <summary>
    /// 全排列（包含重复元素，去重）。O(n·n!)。
    /// </summary>
    public static IList<IList<int>> PermuteUnique(int[] nums)
    {
        Array.Sort(nums);
        var result = new List<IList<int>>();
        var used = new bool[nums.Length];
        PermuteUniqueBacktrack(nums, used, new List<int>(), result);
        return result;
    }

    private static void PermuteUniqueBacktrack(int[] nums, bool[] used, List<int> path, List<IList<int>> result)
    {
        if (path.Count == nums.Length)
        {
            result.Add(new List<int>(path));
            return;
        }
        for (int i = 0; i < nums.Length; i++)
        {
            if (used[i]) continue;
            if (i > 0 && nums[i] == nums[i - 1] && !used[i - 1]) continue;
            used[i] = true;
            path.Add(nums[i]);
            PermuteUniqueBacktrack(nums, used, path, result);
            path.RemoveAt(path.Count - 1);
            used[i] = false;
        }
    }

    // ═══════════════════════════════════════════
    // 组合
    // ═══════════════════════════════════════════

    /// <summary>
    /// 从 n 个元素中选 k 个的组合。O(C(n,k))。
    /// </summary>
    public static IList<IList<int>> Combine(int n, int k)
    {
        var result = new List<IList<int>>();
        CombineBacktrack(1, n, k, new List<int>(), result);
        return result;
    }

    private static void CombineBacktrack(int start, int n, int k, List<int> path, List<IList<int>> result)
    {
        if (path.Count == k)
        {
            result.Add(new List<int>(path));
            return;
        }
        for (int i = start; i <= n; i++)
        {
            path.Add(i);
            CombineBacktrack(i + 1, n, k, path, result);
            path.RemoveAt(path.Count - 1);
        }
    }

    /// <summary>
    /// 组合总和 — 从 candidates 中找出所有和为 target 的组合（可无限次使用同一元素）。
    /// </summary>
    public static IList<IList<int>> CombinationSum(int[] candidates, int target)
    {
        var result = new List<IList<int>>();
        CombinationSumBacktrack(candidates, target, 0, 0, new List<int>(), result);
        return result;
    }

    private static void CombinationSumBacktrack(int[] nums, int target, int start, int sum,
        List<int> path, List<IList<int>> result)
    {
        if (sum == target)
        {
            result.Add(new List<int>(path));
            return;
        }
        if (sum > target) return;
        for (int i = start; i < nums.Length; i++)
        {
            path.Add(nums[i]);
            CombinationSumBacktrack(nums, target, i, sum + nums[i], path, result);
            path.RemoveAt(path.Count - 1);
        }
    }

    // ═══════════════════════════════════════════
    // N 皇后
    // ═══════════════════════════════════════════

    /// <summary>
    /// N 皇后问题 — 返回所有合法解（每个解是每行皇后所在的列号）。
    /// </summary>
    public static IList<IList<string>> SolveNQueens(int n)
    {
        var result = new List<IList<string>>();
        var board = new int[n];
        for (int i = 0; i < n; i++) board[i] = -1;
        NQueensBacktrack(n, 0, board, new HashSet<int>(), new HashSet<int>(), new HashSet<int>(), result);
        return result;
    }

    private static void NQueensBacktrack(int n, int row, int[] board,
        HashSet<int> cols, HashSet<int> diag1, HashSet<int> diag2, List<IList<string>> result)
    {
        if (row == n)
        {
            var solution = new List<string>();
            for (int r = 0; r < n; r++)
            {
                var chars = new char[n];
                Array.Fill(chars, '.');
                chars[board[r]] = 'Q';
                solution.Add(new string(chars));
            }
            result.Add(solution);
            return;
        }

        for (int col = 0; col < n; col++)
        {
            int d1 = row - col;
            int d2 = row + col;
            if (cols.Contains(col) || diag1.Contains(d1) || diag2.Contains(d2)) continue;

            cols.Add(col);
            diag1.Add(d1);
            diag2.Add(d2);
            board[row] = col;

            NQueensBacktrack(n, row + 1, board, cols, diag1, diag2, result);

            cols.Remove(col);
            diag1.Remove(d1);
            diag2.Remove(d2);
        }
    }

    // ═══════════════════════════════════════════
    // 分割回文串
    // ═══════════════════════════════════════════

    /// <summary>
    /// 分割回文串 — 将 s 分割成若干回文子串，返回所有可能方案。
    /// </summary>
    public static IList<IList<string>> Partition(string s)
    {
        var result = new List<IList<string>>();
        PartitionBacktrack(s, 0, new List<string>(), result);
        return result;
    }

    private static void PartitionBacktrack(string s, int start, List<string> path, List<IList<string>> result)
    {
        if (start == s.Length)
        {
            result.Add(new List<string>(path));
            return;
        }
        for (int end = start; end < s.Length; end++)
        {
            if (IsPalindrome(s, start, end))
            {
                path.Add(s[start..(end + 1)]);
                PartitionBacktrack(s, end + 1, path, result);
                path.RemoveAt(path.Count - 1);
            }
        }
    }

    private static bool IsPalindrome(string s, int left, int right)
    {
        while (left < right)
        {
            if (s[left++] != s[right--]) return false;
        }
        return true;
    }
}
