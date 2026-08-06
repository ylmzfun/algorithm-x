namespace AlgorithmX.Tests.Algorithms;

public class TwoPointersTests
{
    [Fact]
    public void TwoSumSorted_ShouldFindPair()
    {
        var result = AlgorithmX.Algorithms.TwoPointers.TwoPointers.TwoSumSorted(new[] { 2, 7, 11, 15 }, 9);
        Assert.Equal(new[] { 1, 2 }, result);
    }

    [Fact]
    public void ThreeSum_ShouldFindAllTriplets()
    {
        var result = AlgorithmX.Algorithms.TwoPointers.TwoPointers.ThreeSum(new[] { -1, 0, 1, 2, -1, -4 });
        Assert.Equal(2, result.Count);
    }

    [Fact]
    public void MaxArea_ShouldFindMaxContainer()
    {
        Assert.Equal(49, AlgorithmX.Algorithms.TwoPointers.TwoPointers.MaxArea(new[] { 1, 8, 6, 2, 5, 4, 8, 3, 7 }));
    }

    [Fact]
    public void LengthOfLongestSubstring_ShouldBeCorrect()
    {
        Assert.Equal(3, AlgorithmX.Algorithms.TwoPointers.TwoPointers.LengthOfLongestSubstring("abcabcbb"));
        Assert.Equal(1, AlgorithmX.Algorithms.TwoPointers.TwoPointers.LengthOfLongestSubstring("bbbbb"));
    }

    [Fact]
    public void MinWindow_ShouldFindMinCoveringSubstring()
    {
        Assert.Equal("BANC",
            AlgorithmX.Algorithms.TwoPointers.TwoPointers.MinWindow("ADOBECODEBANC", "ABC"));
    }

    [Fact]
    public void FindAnagrams_ShouldReturnStartIndices()
    {
        var result = AlgorithmX.Algorithms.TwoPointers.TwoPointers.FindAnagrams("cbaebabacd", "abc");
        Assert.Equal(new[] { 0, 6 }, result);
    }
}
