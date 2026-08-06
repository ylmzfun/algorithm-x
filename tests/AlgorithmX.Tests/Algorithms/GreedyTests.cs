namespace AlgorithmX.Tests.Algorithms;

public class GreedyTests
{
    [Fact]
    public void MaxNonOverlapping_ShouldCountCorrectly()
    {
        int[][] intervals = { new[] { 1, 2 }, new[] { 2, 3 }, new[] { 3, 4 }, new[] { 1, 3 } };
        Assert.Equal(3, AlgorithmX.Algorithms.Greedy.Greedy.MaxNonOverlappingIntervals(intervals));
    }

    [Fact]
    public void EraseOverlapIntervals_ShouldReturnMinRemovals()
    {
        int[][] intervals = { new[] { 1, 2 }, new[] { 2, 3 }, new[] { 3, 4 }, new[] { 1, 3 } };
        Assert.Equal(1, AlgorithmX.Algorithms.Greedy.Greedy.EraseOverlapIntervals(intervals));
    }

    [Fact]
    public void FindMinArrowShots_ShouldBeCorrect()
    {
        int[][] points = { new[] { 10, 16 }, new[] { 2, 8 }, new[] { 1, 6 }, new[] { 7, 12 } };
        Assert.Equal(2, AlgorithmX.Algorithms.Greedy.Greedy.FindMinArrowShots(points));
    }

    [Fact]
    public void CanJump_ShouldReturnCorrect()
    {
        Assert.True(AlgorithmX.Algorithms.Greedy.Greedy.CanJump(new[] { 2, 3, 1, 1, 4 }));
        Assert.False(AlgorithmX.Algorithms.Greedy.Greedy.CanJump(new[] { 3, 2, 1, 0, 4 }));
    }

    [Fact]
    public void Jump_ShouldReturnMinJumps()
    {
        Assert.Equal(2, AlgorithmX.Algorithms.Greedy.Greedy.Jump(new[] { 2, 3, 1, 1, 4 }));
    }

    [Fact]
    public void HuffmanCoding_ShouldReturnMinCost()
    {
        long cost = AlgorithmX.Algorithms.Greedy.Greedy.HuffmanCoding(new[] { 5, 9, 12, 13, 16, 45 });
        Assert.Equal(224, cost);
    }
}
