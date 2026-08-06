namespace AlgorithmX.Algorithms.Sorting;

/// <summary>
/// 插入排序 — O(n²)，稳定排序。
/// 适合小规模数据或近乎有序的数据。
/// </summary>
public static class InsertionSort
{
    public static void Sort<T>(T[] array) where T : IComparable<T>
    {
        Sort(array, Comparer<T>.Default);
    }

    public static void Sort<T>(T[] array, IComparer<T> comparer)
    {
        int n = array.Length;
        for (int i = 1; i < n; i++)
        {
            T key = array[i];
            int j = i - 1;
            while (j >= 0 && comparer.Compare(array[j], key) > 0)
            {
                array[j + 1] = array[j];
                j--;
            }
            array[j + 1] = key;
        }
    }
}
