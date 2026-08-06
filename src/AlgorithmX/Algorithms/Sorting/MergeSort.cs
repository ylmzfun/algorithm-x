namespace AlgorithmX.Algorithms.Sorting;

/// <summary>
/// 归并排序 — O(n log n)，稳定排序。
/// 需要 O(n) 额外空间，适合链表排序。
/// </summary>
public static class MergeSort
{
    public static void Sort<T>(T[] array) where T : IComparable<T>
    {
        Sort(array, Comparer<T>.Default);
    }

    public static void Sort<T>(T[] array, IComparer<T> comparer)
    {
        if (array.Length <= 1) return;
        var temp = new T[array.Length];
        Sort(array, temp, comparer, 0, array.Length - 1);
    }

    private static void Sort<T>(T[] array, T[] temp, IComparer<T> comparer, int left, int right)
    {
        if (left >= right) return;

        int mid = left + (right - left) / 2;
        Sort(array, temp, comparer, left, mid);
        Sort(array, temp, comparer, mid + 1, right);
        Merge(array, temp, comparer, left, mid, right);
    }

    private static void Merge<T>(T[] array, T[] temp, IComparer<T> comparer, int left, int mid, int right)
    {
        int i = left;
        int j = mid + 1;
        int k = left;

        while (i <= mid && j <= right)
        {
            if (comparer.Compare(array[i], array[j]) <= 0)
                temp[k++] = array[i++];
            else
                temp[k++] = array[j++];
        }
        while (i <= mid) temp[k++] = array[i++];
        while (j <= right) temp[k++] = array[j++];

        for (int idx = left; idx <= right; idx++)
            array[idx] = temp[idx];
    }
}
