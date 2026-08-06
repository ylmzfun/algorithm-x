namespace AlgorithmX.Algorithms.DivideAndConquer;

/// <summary>
/// 分治法经典算法。
/// </summary>
public static class DivideAndConquer
{
    /// <summary>
    /// 最大子数组和 — Kadane 分治解法（也可用更简单的 DP 线性扫描）。
    /// O(n log n) 分治。另有 O(n) 的 Kadane 算法见 DynamicProgramming。
    /// </summary>
    public static int MaxSubArray(int[] nums)
    {
        return MaxSubArrayDivide(nums, 0, nums.Length - 1);
    }

    private static int MaxSubArrayDivide(int[] nums, int left, int right)
    {
        if (left == right) return nums[left];

        int mid = left + (right - left) / 2;
        int leftMax = MaxSubArrayDivide(nums, left, mid);
        int rightMax = MaxSubArrayDivide(nums, mid + 1, right);
        int crossMax = MaxCrossingSum(nums, left, mid, right);

        return Math.Max(Math.Max(leftMax, rightMax), crossMax);
    }

    private static int MaxCrossingSum(int[] nums, int left, int mid, int right)
    {
        int leftSum = int.MinValue;
        int sum = 0;
        for (int i = mid; i >= left; i--)
        {
            sum += nums[i];
            leftSum = Math.Max(leftSum, sum);
        }

        int rightSum = int.MinValue;
        sum = 0;
        for (int i = mid + 1; i <= right; i++)
        {
            sum += nums[i];
            rightSum = Math.Max(rightSum, sum);
        }

        return leftSum + rightSum;
    }

    /// <summary>
    /// 二分快速幂 — 计算 x^n。O(log n)。
    /// </summary>
    public static double FastPow(double x, int n)
    {
        if (n == 0) return 1.0;
        if (n < 0)
        {
            x = 1.0 / x;
            // 处理 int.MinValue 溢出
            if (n == int.MinValue)
            {
                n = int.MaxValue;
                return x * FastPow(x, n);
            }
            n = -n;
        }
        double half = FastPow(x, n / 2);
        return n % 2 == 0 ? half * half : half * half * x;
    }

    /// <summary>
    /// 矩阵快速幂（2×2 矩阵）。O(log n)。
    /// 常用于斐波那契 O(log n)：Fib(n) = [[1,1],[1,0]]^n [F1, F0]^T
    /// </summary>
    public static long[,] MatrixPow(long[,] matrix, int n)
    {
        int size = matrix.GetLength(0);
        var result = IdentityMatrix(size);

        var base_ = (long[,])matrix.Clone();
        int exp = n;
        while (exp > 0)
        {
            if ((exp & 1) == 1)
                result = MultiplyMatrix(result, base_);
            base_ = MultiplyMatrix(base_, base_);
            exp >>= 1;
        }
        return result;
    }

    private static long[,] IdentityMatrix(int n)
    {
        var identity = new long[n, n];
        for (int i = 0; i < n; i++)
            identity[i, i] = 1;
        return identity;
    }

    private static long[,] MultiplyMatrix(long[,] a, long[,] b)
    {
        int n = a.GetLength(0);
        var result = new long[n, n];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                for (int k = 0; k < n; k++)
                    result[i, j] += a[i, k] * b[k, j];
        return result;
    }

    /// <summary>
    /// 使用矩阵快速幂计算斐波那契第 n 项。O(log n)。
    /// </summary>
    public static long FibonacciMatrix(int n)
    {
        if (n < 0) throw new ArgumentOutOfRangeException(nameof(n));
        if (n <= 1) return n;
        var baseMatrix = new long[,] { { 1, 1 }, { 1, 0 } };
        var result = MatrixPow(baseMatrix, n - 1);
        return result[0, 0];
    }
}
