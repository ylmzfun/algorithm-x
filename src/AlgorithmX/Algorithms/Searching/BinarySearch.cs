namespace AlgorithmX.Algorithms.Searching;

/// <summary>
/// 二分搜索 — O(log n)。
/// 要求数组已按升序排列。
/// </summary>
public static class BinarySearch
{
    /// <summary>
    /// 在有序数组中查找目标值，返回索引；未找到则返回 -1。
    /// </summary>
    public static int Search<T>(T[] array, T target) where T : IComparable<T>
    {
        return Search(array, target, Comparer<T>.Default);
    }

    /// <summary>
    /// 在有序数组中查找目标值，返回索引；未找到则返回 -1。
    /// </summary>
    public static int Search<T>(T[] array, T target, IComparer<T> comparer)
    {
        int left = 0;
        int right = array.Length - 1;

        while (left <= right)
        {
            int mid = left + (right - left) / 2;
            int cmp = comparer.Compare(array[mid], target);

            if (cmp == 0) return mid;
            if (cmp < 0) left = mid + 1;
            else right = mid - 1;
        }
        return -1;
    }

    /// <summary>
    /// 查找第一个等于 target 的索引（下界）。
    /// </summary>
    public static int LowerBound<T>(T[] array, T target) where T : IComparable<T>
    {
        return LowerBound(array, target, Comparer<T>.Default);
    }

    public static int LowerBound<T>(T[] array, T target, IComparer<T> comparer)
    {
        int left = 0;
        int right = array.Length;
        while (left < right)
        {
            int mid = left + (right - left) / 2;
            if (comparer.Compare(array[mid], target) < 0)
                left = mid + 1;
            else
                right = mid;
        }
        return left;
    }

    /// <summary>
    /// 查找第一个大于 target 的索引（上界）。
    /// </summary>
    public static int UpperBound<T>(T[] array, T target) where T : IComparable<T>
    {
        return UpperBound(array, target, Comparer<T>.Default);
    }

    public static int UpperBound<T>(T[] array, T target, IComparer<T> comparer)
    {
        int left = 0;
        int right = array.Length;
        while (left < right)
        {
            int mid = left + (right - left) / 2;
            if (comparer.Compare(array[mid], target) <= 0)
                left = mid + 1;
            else
                right = mid;
        }
        return left;
    }
}
