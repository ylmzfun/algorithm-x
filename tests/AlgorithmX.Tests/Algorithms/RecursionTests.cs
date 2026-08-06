namespace AlgorithmX.Tests.Algorithms;

public class RecursionTests
{
    [Fact]
    public void FibonacciIterative_ShouldBeCorrect()
    {
        Assert.Equal(0, AlgorithmX.Algorithms.Recursion.Recursion.FibonacciIterative(0));
        Assert.Equal(1, AlgorithmX.Algorithms.Recursion.Recursion.FibonacciIterative(1));
        Assert.Equal(1, AlgorithmX.Algorithms.Recursion.Recursion.FibonacciIterative(2));
        Assert.Equal(55, AlgorithmX.Algorithms.Recursion.Recursion.FibonacciIterative(10));
    }

    [Fact]
    public void FibonacciMemo_ShouldMatchIterative()
    {
        for (int i = 0; i <= 20; i++)
        {
            Assert.Equal(
                AlgorithmX.Algorithms.Recursion.Recursion.FibonacciIterative(i),
                AlgorithmX.Algorithms.Recursion.Recursion.FibonacciMemo(i));
        }
    }

    [Fact]
    public void TowerOfHanoi_StepsCount_ShouldBe2nMinus1()
    {
        var steps = AlgorithmX.Algorithms.Recursion.Recursion.TowerOfHanoi(3);
        Assert.Equal(7, steps.Count); // 2^3 - 1 = 7
    }

    [Fact]
    public void Factorial_ShouldBeCorrect()
    {
        Assert.Equal(1, AlgorithmX.Algorithms.Recursion.Recursion.Factorial(0));
        Assert.Equal(1, AlgorithmX.Algorithms.Recursion.Recursion.Factorial(1));
        Assert.Equal(120, AlgorithmX.Algorithms.Recursion.Recursion.Factorial(5));
    }

    [Fact]
    public void ReverseString_ShouldReverse()
    {
        Assert.Equal("cba", AlgorithmX.Algorithms.Recursion.Recursion.ReverseString("abc"));
        Assert.Equal("", AlgorithmX.Algorithms.Recursion.Recursion.ReverseString(""));
    }
}
