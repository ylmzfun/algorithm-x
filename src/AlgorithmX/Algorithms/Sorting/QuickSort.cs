namespace AlgorithmX.Algorithms.Sorting;

/// <summary>
/// 快速排序 — O(n log n) 平均，O(n²) 最坏，不稳定排序。
/// 分治 + 原地分区。
/// </summary>
public static class QuickSort
{
    private static readonly Random _random = new();

    public static void Sort<T>(T[] array) where T : IComparable<T>
    {
        Sort(array, Comparer<T>.Default);
    }

    public static void Sort<T>(T[] array, IComparer<T> comparer)
    {
        Sort(array, comparer, 0, array.Length - 1);
    }

    private static void Sort<T>(T[] array, IComparer<T> comparer, int left, int right)
    {
        if (left >= right) return;

        int pivotIndex = Partition(array, comparer, left, right);
        Sort(array, comparer, left, pivotIndex - 1);
        Sort(array, comparer, pivotIndex + 1, right);
    }

    private static int Partition<T>(T[] array, IComparer<T> comparer, int left, int right)
    {
        // 随机选择 pivot，避免最坏情况
        int randomPivot = _random.Next(left, right + 1);
        Common.ArrayUtils.Swap(array, left, randomPivot);

        T pivot = array[left];
        int i = left + 1;
        int j = right;

        while (true)
        {
            while (i <= j && comparer.Compare(array[i], pivot) <= 0) i++;
            while (i <= j && comparer.Compare(array[j], pivot) >= 0) j--;
            if (i >= j) break;
            Common.ArrayUtils.Swap(array, i, j);
            i++;
            j--;
        }
        Common.ArrayUtils.Swap(array, left, j);
        return j;
    }
}
