namespace AlgorithmX.Algorithms.Sorting;

/// <summary>
/// 冒泡排序 — O(n²)，稳定排序。
/// 每轮将最大元素"冒泡"到末尾。
/// </summary>
public static class BubbleSort
{
    public static void Sort<T>(T[] array) where T : IComparable<T>
    {
        Sort(array, Comparer<T>.Default);
    }

    public static void Sort<T>(T[] array, IComparer<T> comparer)
    {
        int n = array.Length;
        for (int i = 0; i < n - 1; i++)
        {
            bool swapped = false;
            for (int j = 0; j < n - 1 - i; j++)
            {
                if (comparer.Compare(array[j], array[j + 1]) > 0)
                {
                    Common.ArrayUtils.Swap(array, j, j + 1);
                    swapped = true;
                }
            }
            // 如果没有发生交换，说明已经有序，提前退出
            if (!swapped) break;
        }
    }
}
