namespace AlgorithmX.Algorithms.Randomization;

/// <summary>
/// 随机化算法。
/// </summary>
public static class Randomization
{
    private static readonly Random _random = new();

    /// <summary>
    /// Fisher-Yates 洗牌算法 — 生成均匀随机排列。O(n)。
    /// </summary>
    public static void Shuffle<T>(T[] array)
    {
        for (int i = array.Length - 1; i > 0; i--)
        {
            int j = _random.Next(i + 1);
            (array[i], array[j]) = (array[j], array[i]);
        }
    }

    /// <summary>
    /// 蓄水池抽样 — 从未知大小的流中等概率抽取 k 个元素。
    /// O(n)。
    /// </summary>
    public static T[] ReservoirSample<T>(IEnumerable<T> stream, int k)
    {
        var reservoir = new T[k];
        var enumerator = stream.GetEnumerator();

        int i;
        for (i = 0; i < k && enumerator.MoveNext(); i++)
            reservoir[i] = enumerator.Current;

        int count = k;
        while (enumerator.MoveNext())
        {
            count++;
            int j = _random.Next(count);
            if (j < k)
                reservoir[j] = enumerator.Current;
        }
        return i == k ? reservoir : reservoir[..i];
    }

    /// <summary>
    /// 生成 [minInclusive, maxExclusive) 范围内的随机整数。
    /// </summary>
    public static int RandomInt(int minInclusive, int maxExclusive)
    {
        return _random.Next(minInclusive, maxExclusive);
    }

    /// <summary>
    /// 以 probability 的概率返回 true。
    /// </summary>
    public static bool RandomBool(double probability = 0.5)
    {
        return _random.NextDouble() < probability;
    }
}
