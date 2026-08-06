namespace AlgorithmX.DataStructures.SegmentTree;

/// <summary>
/// 树状数组 (Fenwick Tree / Binary Indexed Tree)。
/// 支持单点更新 O(log n) 和前缀和查询 O(log n)。
/// 1-based 内部索引。
/// </summary>
public class FenwickTree
{
    private readonly long[] _tree;
    private readonly int _n;

    /// <param name="n">元素数量</param>
    public FenwickTree(int n)
    {
        if (n <= 0) throw new ArgumentOutOfRangeException(nameof(n));
        _n = n;
        _tree = new long[n + 1];
    }

    /// <summary>
    /// 用数组初始化。O(n log n)。
    /// </summary>
    public FenwickTree(int[] nums) : this(nums.Length)
    {
        for (int i = 0; i < nums.Length; i++)
            Add(i + 1, nums[i]);
    }

    /// <summary>
    /// 在位置 index（1-based）增加值 delta。O(log n)。
    /// </summary>
    public void Add(int index, long delta)
    {
        if (index < 1 || index > _n)
            throw new ArgumentOutOfRangeException(nameof(index));
        while (index <= _n)
        {
            _tree[index] += delta;
            index += index & -index; // lowbit
        }
    }

    /// <summary>
    /// 查询前缀和 [1..index]。O(log n)。
    /// </summary>
    public long PrefixSum(int index)
    {
        if (index < 0 || index > _n)
            throw new ArgumentOutOfRangeException(nameof(index));
        long sum = 0;
        while (index > 0)
        {
            sum += _tree[index];
            index -= index & -index;
        }
        return sum;
    }

    /// <summary>
    /// 查询区间和 [left..right]（1-based）。O(log n)。
    /// </summary>
    public long RangeSum(int left, int right)
    {
        return PrefixSum(right) - PrefixSum(left - 1);
    }

    /// <summary>
    /// 更新指定位置的值（0-based 方便调用）。
    /// </summary>
    public void Update(int zeroBasedIndex, long newValue)
    {
        int idx = zeroBasedIndex + 1;
        long oldValue = RangeSum(idx, idx);
        Add(idx, newValue - oldValue);
    }
}
