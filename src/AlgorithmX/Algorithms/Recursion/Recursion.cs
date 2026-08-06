namespace AlgorithmX.Algorithms.Recursion;

/// <summary>
/// 递归经典算法集合。
/// </summary>
public static class Recursion
{
    /// <summary>
    /// 计算斐波那契数列第 n 项（递归实现）。O(2^n)，仅作教学演示。
    /// </summary>
    public static long FibonacciRecursive(int n)
    {
        if (n < 0) throw new ArgumentOutOfRangeException(nameof(n));
        if (n <= 1) return n;
        return FibonacciRecursive(n - 1) + FibonacciRecursive(n - 2);
    }

    /// <summary>
    /// 计算斐波那契数列第 n 项（记忆化递归）。O(n)。
    /// </summary>
    public static long FibonacciMemo(int n)
    {
        if (n < 0) throw new ArgumentOutOfRangeException(nameof(n));
        if (n <= 1) return n;
        var memo = new long[n + 1];
        memo[1] = 1;
        return FibMemo(n, memo);
    }

    private static long FibMemo(int n, long[] memo)
    {
        if (n <= 1 || memo[n] != 0) return memo[n];
        memo[n] = FibMemo(n - 1, memo) + FibMemo(n - 2, memo);
        return memo[n];
    }

    /// <summary>
    /// 计算斐波那契数列第 n 项（迭代）。O(n)，O(1) 空间。
    /// </summary>
    public static long FibonacciIterative(int n)
    {
        if (n < 0) throw new ArgumentOutOfRangeException(nameof(n));
        if (n <= 1) return n;
        long prev2 = 0, prev1 = 1;
        for (int i = 2; i <= n; i++)
        {
            long curr = prev2 + prev1;
            prev2 = prev1;
            prev1 = curr;
        }
        return prev1;
    }

    /// <summary>
    /// 汉诺塔问题 — 将 n 个盘子从源柱移动到目标柱，借助辅助柱。
    /// 返回移动步骤列表。O(2^n)。
    /// </summary>
    public static IList<string> TowerOfHanoi(int n)
    {
        var steps = new List<string>();
        Hanoi(n, 'A', 'C', 'B', steps);
        return steps;
    }

    private static void Hanoi(int n, char source, char target, char auxiliary, List<string> steps)
    {
        if (n == 1)
        {
            steps.Add($"Move disk 1 from {source} to {target}");
            return;
        }
        Hanoi(n - 1, source, auxiliary, target, steps);
        steps.Add($"Move disk {n} from {source} to {target}");
        Hanoi(n - 1, auxiliary, target, source, steps);
    }

    /// <summary>
    /// 计算阶乘 n!。O(n)。
    /// </summary>
    public static long Factorial(int n)
    {
        if (n < 0) throw new ArgumentOutOfRangeException(nameof(n));
        return Fact(n);

        static long Fact(int x) => x <= 1 ? 1 : x * Fact(x - 1);
    }

    /// <summary>
    /// 递归反转字符串。O(n)。
    /// </summary>
    public static string ReverseString(string s)
    {
        if (string.IsNullOrEmpty(s) || s.Length == 1) return s;
        return ReverseString(s[1..]) + s[0];
    }
}
