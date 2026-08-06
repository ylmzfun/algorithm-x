namespace AlgorithmX.Tests.Algorithms;

public class BinarySearchTests
{
    [Fact]
    public void Search_ShouldFindExistingElement()
    {
        var array = new[] { 1, 3, 5, 7, 9, 11 };
        int index = AlgorithmX.Algorithms.Searching.BinarySearch.Search(array, 7);
        Assert.Equal(3, index);
    }

    [Fact]
    public void Search_ShouldReturnNegativeForMissing()
    {
        var array = new[] { 1, 3, 5, 7, 9, 11 };
        int index = AlgorithmX.Algorithms.Searching.BinarySearch.Search(array, 4);
        Assert.Equal(-1, index);
    }

    [Fact]
    public void Search_SingleElement()
    {
        var array = new[] { 42 };
        Assert.Equal(0, AlgorithmX.Algorithms.Searching.BinarySearch.Search(array, 42));
        Assert.Equal(-1, AlgorithmX.Algorithms.Searching.BinarySearch.Search(array, 7));
    }

    [Fact]
    public void LowerBound_ShouldFindFirstEqualOrGreater()
    {
        var array = new[] { 1, 2, 2, 2, 3, 4 };
        Assert.Equal(1, AlgorithmX.Algorithms.Searching.BinarySearch.LowerBound(array, 2));
        Assert.Equal(0, AlgorithmX.Algorithms.Searching.BinarySearch.LowerBound(array, 1));
        Assert.Equal(6, AlgorithmX.Algorithms.Searching.BinarySearch.LowerBound(array, 5)); // 不存在，大于所有
    }

    [Fact]
    public void UpperBound_ShouldFindFirstGreater()
    {
        var array = new[] { 1, 2, 2, 2, 3, 4 };
        Assert.Equal(4, AlgorithmX.Algorithms.Searching.BinarySearch.UpperBound(array, 2));
        Assert.Equal(1, AlgorithmX.Algorithms.Searching.BinarySearch.UpperBound(array, 1));
        Assert.Equal(6, AlgorithmX.Algorithms.Searching.BinarySearch.UpperBound(array, 4));
    }
}
