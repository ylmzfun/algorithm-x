namespace AlgorithmX.Common;

/// <summary>
/// 数组相关的实用工具方法。
/// </summary>
public static class ArrayUtils
{
    /// <summary>
    /// 交换数组中的两个元素。
    /// </summary>
    public static void Swap<T>(T[] array, int i, int j)
    {
        (array[i], array[j]) = (array[j], array[i]);
    }

    /// <summary>
    /// 判断数组是否按非递减顺序排列。
    /// </summary>
    public static bool IsSorted<T>(T[] array) where T : IComparable<T>
    {
        for (int i = 1; i < array.Length; i++)
        {
            if (array[i].CompareTo(array[i - 1]) < 0)
                return false;
        }
        return true;
    }

    /// <summary>
    /// 判断数组是否按 comparer 定义的顺序排列。
    /// </summary>
    public static bool IsSorted<T>(T[] array, IComparer<T> comparer)
    {
        for (int i = 1; i < array.Length; i++)
        {
            if (comparer.Compare(array[i], array[i - 1]) < 0)
                return false;
        }
        return true;
    }

    /// <summary>
    /// 打印数组内容，以逗号分隔。
    /// </summary>
    public static string ToString<T>(T[] array)
    {
        return string.Join(", ", array);
    }
}
