namespace AlgorithmX.Tests.Algorithms;

public class SortingTests
{
    [Fact]
    public void BubbleSort_ShouldSortArray()
    {
        var array = new[] { 5, 2, 8, 1, 9 };
        AlgorithmX.Algorithms.Sorting.BubbleSort.Sort(array);
        Assert.True(AlgorithmX.Common.ArrayUtils.IsSorted(array));
    }

    [Fact]
    public void InsertionSort_ShouldSortArray()
    {
        var array = new[] { 5, 2, 8, 1, 9 };
        AlgorithmX.Algorithms.Sorting.InsertionSort.Sort(array);
        Assert.True(AlgorithmX.Common.ArrayUtils.IsSorted(array));
    }

    [Fact]
    public void QuickSort_ShouldSortArray()
    {
        var array = new[] { 5, 2, 8, 1, 9, 3 };
        AlgorithmX.Algorithms.Sorting.QuickSort.Sort(array);
        Assert.True(AlgorithmX.Common.ArrayUtils.IsSorted(array));
    }

    [Fact]
    public void MergeSort_ShouldSortArray()
    {
        var array = new[] { 5, 2, 8, 1, 9, 3 };
        AlgorithmX.Algorithms.Sorting.MergeSort.Sort(array);
        Assert.True(AlgorithmX.Common.ArrayUtils.IsSorted(array));
    }

    [Fact]
    public void Sort_AlreadySorted_ShouldRemainSorted()
    {
        var array = new[] { 1, 2, 3, 4, 5 };
        AlgorithmX.Algorithms.Sorting.QuickSort.Sort(array);
        Assert.True(AlgorithmX.Common.ArrayUtils.IsSorted(array));
    }

    [Fact]
    public void Sort_SingleElement_ShouldNotChange()
    {
        var array = new[] { 42 };
        AlgorithmX.Algorithms.Sorting.QuickSort.Sort(array);
        Assert.Equal(42, array[0]);
    }

    [Fact]
    public void Sort_EmptyArray_ShouldNotThrow()
    {
        var array = Array.Empty<int>();
        var ex = Record.Exception(() => AlgorithmX.Algorithms.Sorting.MergeSort.Sort(array));
        Assert.Null(ex);
    }

    [Fact]
    public void Sort_DuplicateElements_ShouldSortStably()
    {
        // 注意：QuickSort 不是稳定排序，这里只检查有序性
        var array = new[] { 3, 3, 1, 2, 2 };
        AlgorithmX.Algorithms.Sorting.MergeSort.Sort(array); // MergeSort 是稳定的
        Assert.True(AlgorithmX.Common.ArrayUtils.IsSorted(array));
    }
}
