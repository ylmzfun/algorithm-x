using System.Security.Cryptography;

namespace AlgorithmX.DataStructures.BloomFilter;

/// <summary>
/// 布隆过滤器 — 空间高效的概率性集合数据结构。
/// 可能存在误报（false positive），但不会漏报（false negative）。
/// 
/// 使用 k 个独立哈希函数（通过 SHA256 生成）在位图中标记元素。
/// </summary>
public class BloomFilter<T>
{
    private readonly bool[] _bits;
    private readonly int _hashCount;
    private readonly int _size;

    /// <param name="expectedItems">预期插入元素数量</param>
    /// <param name="falsePositiveRate">可接受的误报率（如 0.01 表示 1%）</param>
    public BloomFilter(int expectedItems, double falsePositiveRate = 0.01)
    {
        if (expectedItems <= 0)
            throw new ArgumentOutOfRangeException(nameof(expectedItems));
        if (falsePositiveRate <= 0 || falsePositiveRate >= 1)
            throw new ArgumentOutOfRangeException(nameof(falsePositiveRate));

        _size = (int)Math.Ceiling(-expectedItems * Math.Log(falsePositiveRate) / (Math.Log(2) * Math.Log(2)));
        _hashCount = (int)Math.Ceiling((_size / (double)expectedItems) * Math.Log(2));
        _bits = new bool[_size];
    }

    /// <summary>
    /// 添加元素。O(k)，k 为哈希函数数量。
    /// </summary>
    public void Add(T item)
    {
        var hash = GetHashBytes(item);
        for (int i = 0; i < _hashCount; i++)
        {
            int index = GetIndex(hash, i);
            _bits[index] = true;
        }
    }

    /// <summary>
    /// 检查元素是否可能存在于集合中。
    /// 返回 true 表示"可能存在"，false 表示"一定不存在"。
    /// </summary>
    public bool MightContain(T item)
    {
        var hash = GetHashBytes(item);
        for (int i = 0; i < _hashCount; i++)
        {
            int index = GetIndex(hash, i);
            if (!_bits[index]) return false;
        }
        return true;
    }

    /// <summary>
    /// 已使用的 bit 数量。
    /// </summary>
    public int SetBitCount => _bits.Count(b => b);

    /// <summary>
    /// 位图大小。
    /// </summary>
    public int Size => _size;

    /// <summary>
    /// 哈希函数数量。
    /// </summary>
    public int HashCount => _hashCount;

    private byte[] GetHashBytes(T item)
    {
        var bytes = System.Text.Encoding.UTF8.GetBytes(item?.ToString() ?? "");
        return SHA256.HashData(bytes);
    }

    private int GetIndex(byte[] hash, int seed)
    {
        int value = BitConverter.ToInt32(hash, (seed * 4) % (hash.Length - 3));
        return Math.Abs(value) % _size;
    }
}
