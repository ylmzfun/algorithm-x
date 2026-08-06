namespace AlgorithmX.Tests.Algorithms;

public class BacktrackingTests
{
    [Fact]
    public void Subsets_ShouldReturnPowerSet()
    {
        var result = AlgorithmX.Algorithms.Backtracking.Backtracking.Subsets(new[] { 1, 2, 3 });
        Assert.Equal(8, result.Count); // 2^3 = 8
        Assert.Contains(result, s => s.SequenceEqual(new[] { 1, 2 }));
        Assert.Contains(result, s => s.SequenceEqual(new[] { 3 }));
        Assert.Contains(result, s => s.Count == 0); // 空集
    }

    [Fact]
    public void Permute_ShouldReturnAllPermutations()
    {
        var result = AlgorithmX.Algorithms.Backtracking.Backtracking.Permute(new[] { 1, 2, 3 });
        Assert.Equal(6, result.Count); // 3! = 6
        Assert.Contains(result, p => p.SequenceEqual(new[] { 1, 2, 3 }));
        Assert.Contains(result, p => p.SequenceEqual(new[] { 3, 2, 1 }));
    }

    [Fact]
    public void PermuteUnique_WithDuplicates_ShouldDeduplicate()
    {
        var result = AlgorithmX.Algorithms.Backtracking.Backtracking.PermuteUnique(new[] { 1, 1, 2 });
        Assert.Equal(3, result.Count); // 3!/2! = 3
    }

    [Fact]
    public void Combine_ShouldReturnCombinations()
    {
        var result = AlgorithmX.Algorithms.Backtracking.Backtracking.Combine(4, 2);
        Assert.Equal(6, result.Count); // C(4,2) = 6
    }

    [Fact]
    public void CombinationSum_ShouldFindAll()
    {
        var result = AlgorithmX.Algorithms.Backtracking.Backtracking.CombinationSum(new[] { 2, 3, 6, 7 }, 7);
        Assert.Equal(2, result.Count);
        Assert.Contains(result, c => c.SequenceEqual(new[] { 2, 2, 3 }));
        Assert.Contains(result, c => c.SequenceEqual(new[] { 7 }));
    }

    [Fact]
    public void SolveNQueens_4Queens_ShouldReturn2Solutions()
    {
        var result = AlgorithmX.Algorithms.Backtracking.Backtracking.SolveNQueens(4);
        Assert.Equal(2, result.Count);
    }

    [Fact]
    public void Partition_ShouldReturnAllPalindromePartitions()
    {
        var result = AlgorithmX.Algorithms.Backtracking.Backtracking.Partition("aab");
        Assert.Equal(2, result.Count);
        Assert.Contains(result, p => p.SequenceEqual(new[] { "aa", "b" }));
        Assert.Contains(result, p => p.SequenceEqual(new[] { "a", "a", "b" }));
    }
}
