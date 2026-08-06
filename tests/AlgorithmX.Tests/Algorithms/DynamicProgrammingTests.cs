namespace AlgorithmX.Tests.Algorithms;

public class DynamicProgrammingTests
{
    [Fact]
    public void ClimbStairs_ShouldBeCorrect()
    {
        Assert.Equal(2, AlgorithmX.Algorithms.DynamicProgramming.DynamicProgramming.ClimbStairs(2));
        Assert.Equal(3, AlgorithmX.Algorithms.DynamicProgramming.DynamicProgramming.ClimbStairs(3));
        Assert.Equal(8, AlgorithmX.Algorithms.DynamicProgramming.DynamicProgramming.ClimbStairs(5));
    }

    [Fact]
    public void MaxSubArray_ShouldFindMax()
    {
        int[] nums = { -2, 1, -3, 4, -1, 2, 1, -5, 4 };
        Assert.Equal(6, AlgorithmX.Algorithms.DynamicProgramming.DynamicProgramming.MaxSubArray(nums));
    }

    [Fact]
    public void Rob_ShouldMaximizeLoot()
    {
        Assert.Equal(4, AlgorithmX.Algorithms.DynamicProgramming.DynamicProgramming.Rob(new[] { 1, 2, 3, 1 }));
        Assert.Equal(12, AlgorithmX.Algorithms.DynamicProgramming.DynamicProgramming.Rob(new[] { 2, 7, 9, 3, 1 }));
    }

    [Fact]
    public void Knapsack01_ShouldFindMaxValue()
    {
        int[] weights = { 2, 1, 3 };
        int[] values = { 4, 2, 3 };
        Assert.Equal(6, AlgorithmX.Algorithms.DynamicProgramming.DynamicProgramming.Knapsack01(weights, values, 4));
    }

    [Fact]
    public void KnapsackComplete_ShouldAllowReuse()
    {
        int[] weights = { 1, 3, 4 };
        int[] values = { 15, 20, 30 };
        Assert.Equal(60, AlgorithmX.Algorithms.DynamicProgramming.DynamicProgramming.KnapsackComplete(weights, values, 4));
    }

    [Fact]
    public void LCS_ShouldBeCorrect()
    {
        Assert.Equal(3, AlgorithmX.Algorithms.DynamicProgramming.DynamicProgramming.LongestCommonSubsequence("abcde", "ace"));
        Assert.Equal(0, AlgorithmX.Algorithms.DynamicProgramming.DynamicProgramming.LongestCommonSubsequence("abc", "def"));
    }

    [Fact]
    public void LengthOfLIS_ShouldBeCorrect()
    {
        Assert.Equal(4, AlgorithmX.Algorithms.DynamicProgramming.DynamicProgramming.LengthOfLIS(new[] { 10, 9, 2, 5, 3, 7, 101, 18 }));
    }

    [Fact]
    public void LongestPalindromeSubseq_ShouldBeCorrect()
    {
        Assert.Equal(4, AlgorithmX.Algorithms.DynamicProgramming.DynamicProgramming.LongestPalindromeSubseq("bbbab"));
    }

    [Fact]
    public void EditDistance_ShouldBeCorrect()
    {
        Assert.Equal(3, AlgorithmX.Algorithms.DynamicProgramming.DynamicProgramming.EditDistance("horse", "ros"));
    }

    [Fact]
    public void CoinChange_ShouldFindMinCoins()
    {
        Assert.Equal(3, AlgorithmX.Algorithms.DynamicProgramming.DynamicProgramming.CoinChange(new[] { 1, 2, 5 }, 11));
        Assert.Equal(-1, AlgorithmX.Algorithms.DynamicProgramming.DynamicProgramming.CoinChange(new[] { 2 }, 3));
    }
}
