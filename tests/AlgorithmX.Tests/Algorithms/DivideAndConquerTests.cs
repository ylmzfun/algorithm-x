namespace AlgorithmX.Tests.Algorithms;

public class DivideAndConquerTests
{
    [Fact]
    public void MaxSubArray_ShouldFindCorrectSum()
    {
        int[] nums = { -2, 1, -3, 4, -1, 2, 1, -5, 4 };
        Assert.Equal(6, AlgorithmX.Algorithms.DivideAndConquer.DivideAndConquer.MaxSubArray(nums));
    }

    [Fact]
    public void FastPow_ShouldBeCorrect()
    {
        Assert.Equal(8.0, AlgorithmX.Algorithms.DivideAndConquer.DivideAndConquer.FastPow(2, 3), 10);
        Assert.Equal(0.25, AlgorithmX.Algorithms.DivideAndConquer.DivideAndConquer.FastPow(2, -2), 10);
        Assert.Equal(1.0, AlgorithmX.Algorithms.DivideAndConquer.DivideAndConquer.FastPow(5, 0), 10);
    }

    [Fact]
    public void FibonacciMatrix_ShouldBeCorrect()
    {
        Assert.Equal(0, AlgorithmX.Algorithms.DivideAndConquer.DivideAndConquer.FibonacciMatrix(0));
        Assert.Equal(1, AlgorithmX.Algorithms.DivideAndConquer.DivideAndConquer.FibonacciMatrix(1));
        Assert.Equal(55, AlgorithmX.Algorithms.DivideAndConquer.DivideAndConquer.FibonacciMatrix(10));
    }
}
