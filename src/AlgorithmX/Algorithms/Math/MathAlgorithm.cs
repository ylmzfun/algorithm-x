namespace AlgorithmX.Algorithms.MathLib;

/// <summary>
/// 数论、组合数学、素数相关算法。
/// </summary>
public static class MathAlgorithm
{
    // ═══════════════════════════════════════════
    // GCD / LCM
    // ═══════════════════════════════════════════

    /// <summary>
    /// 最大公约数（辗转相除法 / 欧几里得算法）。O(log min(a,b))。
    /// </summary>
    public static long Gcd(long a, long b)
    {
        while (b != 0)
        {
            (a, b) = (b, a % b);
        }
        return a;
    }

    /// <summary>
    /// 最小公倍数。O(log min(a,b))。
    /// </summary>
    public static long Lcm(long a, long b) => a / Gcd(a, b) * b;

    /// <summary>
    /// 扩展欧几里得算法 — 求 ax + by = gcd(a, b) 的一组整数解。
    /// 返回 (gcd, x, y)。
    /// </summary>
    public static (long gcd, long x, long y) ExtendedGcd(long a, long b)
    {
        if (b == 0) return (a, 1, 0);
        var (gcd, x1, y1) = ExtendedGcd(b, a % b);
        return (gcd, y1, x1 - a / b * y1);
    }

    /// <summary>
    /// 求 a 在模 m 下的乘法逆元（要求 gcd(a, m) = 1）。
    /// </summary>
    public static long ModInverse(long a, long m)
    {
        var (gcd, x, _) = ExtendedGcd(a, m);
        if (gcd != 1) throw new ArgumentException("a 和 m 不互质，逆元不存在");
        return (x % m + m) % m;
    }

    // ═══════════════════════════════════════════
    // 素数
    // ═══════════════════════════════════════════

    /// <summary>
    /// 判断 n 是否为素数。O(√n)。
    /// </summary>
    public static bool IsPrime(int n)
    {
        if (n < 2) return false;
        if (n == 2 || n == 3) return true;
        if (n % 2 == 0) return false;
        for (int i = 3; (long)i * i <= n; i += 2)
            if (n % i == 0) return false;
        return true;
    }

    /// <summary>
    /// 埃拉托斯特尼筛法 — 找出 [2, n] 中所有素数。O(n log log n)。
    /// </summary>
    public static IList<int> SieveOfEratosthenes(int n)
    {
        var isPrime = new bool[n + 1];
        Array.Fill(isPrime, true);
        isPrime[0] = isPrime[1] = false;

        for (int i = 2; (long)i * i <= n; i++)
        {
            if (!isPrime[i]) continue;
            for (int j = i * i; j <= n; j += i)
                isPrime[j] = false;
        }

        var primes = new List<int>();
        for (int i = 2; i <= n; i++)
            if (isPrime[i]) primes.Add(i);
        return primes;
    }

    /// <summary>
    /// 欧拉线性筛 — O(n)，每个合数只被最小质因子标记一次。
    /// </summary>
    public static IList<int> LinearSieve(int n)
    {
        var isPrime = new bool[n + 1];
        Array.Fill(isPrime, true);
        var primes = new List<int>();

        for (int i = 2; i <= n; i++)
        {
            if (isPrime[i]) primes.Add(i);
            for (int j = 0; j < primes.Count && (long)i * primes[j] <= n; j++)
            {
                isPrime[i * primes[j]] = false;
                if (i % primes[j] == 0) break;
            }
        }
        return primes;
    }

    // ═══════════════════════════════════════════
    // 快速幂（取模）
    // ═══════════════════════════════════════════

    /// <summary>
    /// 模意义下的快速幂 — (base^exp) % mod。O(log exp)。
    /// </summary>
    public static long ModPow(long baseVal, long exp, long mod)
    {
        long result = 1;
        baseVal %= mod;
        while (exp > 0)
        {
            if ((exp & 1) == 1)
                result = (result * baseVal) % mod;
            baseVal = (baseVal * baseVal) % mod;
            exp >>= 1;
        }
        return result;
    }

    // ═══════════════════════════════════════════
    // 组合数
    // ═══════════════════════════════════════════

    /// <summary>
    /// 计算组合数 C(n, k) — 大数版（long 范围内）。
    /// </summary>
    public static long Combination(int n, int k)
    {
        if (k < 0 || k > n) return 0;
        if (k > n - k) k = n - k;
        long result = 1;
        for (int i = 1; i <= k; i++)
        {
            result = result * (n - k + i) / i;
        }
        return result;
    }

    /// <summary>
    /// 前 n 行的组合数表（杨辉三角）。O(n²)。
    /// </summary>
    public static long[][] PascalTriangle(int n)
    {
        var triangle = new long[n + 1][];
        for (int i = 0; i <= n; i++)
        {
            triangle[i] = new long[i + 1];
            triangle[i][0] = triangle[i][i] = 1;
            for (int j = 1; j < i; j++)
                triangle[i][j] = triangle[i - 1][j - 1] + triangle[i - 1][j];
        }
        return triangle;
    }

    // ═══════════════════════════════════════════
    // 卡特兰数
    // ═══════════════════════════════════════════

    /// <summary>
    /// 第 n 个卡特兰数。C_n = C(2n, n) / (n + 1)。
    /// 应用：进出栈序列数、二叉树形态数、括号匹配数。
    /// </summary>
    public static long Catalan(int n) => Combination(2 * n, n) / (n + 1);
}
