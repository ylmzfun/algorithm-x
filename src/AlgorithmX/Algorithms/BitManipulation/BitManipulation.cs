namespace AlgorithmX.Algorithms.BitManipulation;

/// <summary>
/// 位运算技巧与 Bitset 实现。
/// </summary>
public static class BitManipulation
{
    // ═══════════════════════════════════════════
    // 基础技巧
    // ═══════════════════════════════════════════

    /// <summary>
    /// 判断 n 是否为 2 的幂。O(1)。
    /// </summary>
    public static bool IsPowerOfTwo(int n) => n > 0 && (n & (n - 1)) == 0;

    /// <summary>
    /// 计算 n 中 1 的个数（Hamming Weight / Brian Kernighan 算法）。
    /// </summary>
    public static int CountBits(int n)
    {
        int count = 0;
        while (n != 0)
        {
            n &= n - 1; // 消去最低位的 1
            count++;
        }
        return count;
    }

    /// <summary>
    /// 获取最低位的 1 的值 (lowbit)。
    /// </summary>
    public static int LowBit(int n) => n & -n;

    /// <summary>
    /// 获取最高位的 1 的值。
    /// </summary>
    public static int HighBit(int n)
    {
        n |= n >> 1;
        n |= n >> 2;
        n |= n >> 4;
        n |= n >> 8;
        n |= n >> 16;
        return n - (n >> 1);
    }

    /// <summary>
    /// 反转 32 位整数的二进制位。O(1)。
    /// </summary>
    public static uint ReverseBits(uint n)
    {
        n = (n >> 1) & 0x55555555 | (n << 1) & 0xaaaaaaaa;
        n = (n >> 2) & 0x33333333 | (n << 2) & 0xcccccccc;
        n = (n >> 4) & 0x0f0f0f0f | (n << 4) & 0xf0f0f0f0;
        n = (n >> 8) & 0x00ff00ff | (n << 8) & 0xff00ff00;
        n = (n >> 16) | (n << 16);
        return n;
    }

    /// <summary>
    /// 异或运算：数组中只有一个数字出现一次，其余都出现两次，找出它。O(n)。
    /// </summary>
    public static int SingleNumber(int[] nums)
    {
        int result = 0;
        foreach (int n in nums) result ^= n;
        return result;
    }

    /// <summary>
    /// 异或运算：数组中只有一个数字出现一次，其余都出现三次，找出它。
    /// </summary>
    public static int SingleNumberII(int[] nums)
    {
        int ones = 0, twos = 0;
        foreach (int n in nums)
        {
            ones = (ones ^ n) & ~twos;
            twos = (twos ^ n) & ~ones;
        }
        return ones;
    }

    // ═══════════════════════════════════════════
    // 状态压缩枚举子集
    // ═══════════════════════════════════════════

    /// <summary>
    /// 枚举 mask 的所有非空子集（二进制状态压缩）。O(3^n)。
    /// </summary>
    public static IEnumerable<int> EnumerateSubmasks(int mask)
    {
        for (int sub = mask; sub > 0; sub = (sub - 1) & mask)
            yield return sub;
    }

    /// <summary>
    /// 生成 [0, n) 的所有子集对应的 bitmask。
    /// </summary>
    public static IEnumerable<int> AllMasks(int n)
    {
        for (int mask = 0; mask < (1 << n); mask++)
            yield return mask;
    }
}

/// <summary>
/// 简易 Bitset 实现 — 位图存储布尔值。
/// </summary>
public class Bitset
{
    private readonly long[] _bits;
    private int _count;

    public int Size { get; }
    public int Count => _count;

    public Bitset(int size)
    {
        if (size <= 0) throw new ArgumentOutOfRangeException(nameof(size));
        Size = size;
        _bits = new long[(size + 63) / 64];
        _count = 0;
    }

    public void Set(int index, bool value = true)
    {
        if (index < 0 || index >= Size)
            throw new ArgumentOutOfRangeException(nameof(index));
        int bucket = index / 64;
        int offset = index % 64;
        long mask = 1L << offset;

        bool wasSet = (_bits[bucket] & mask) != 0;
        if (value && !wasSet)
        {
            _bits[bucket] |= mask;
            _count++;
        }
        else if (!value && wasSet)
        {
            _bits[bucket] &= ~mask;
            _count--;
        }
    }

    public bool Get(int index)
    {
        if (index < 0 || index >= Size)
            throw new ArgumentOutOfRangeException(nameof(index));
        return (_bits[index / 64] & (1L << (index % 64))) != 0;
    }

    public void Reset(int index) => Set(index, false);

    public void Clear()
    {
        Array.Clear(_bits, 0, _bits.Length);
        _count = 0;
    }
}
