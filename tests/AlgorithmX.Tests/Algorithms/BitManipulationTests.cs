namespace AlgorithmX.Tests.Algorithms;

public class BitManipulationTests
{
    [Fact]
    public void IsPowerOfTwo_ShouldWork()
    {
        Assert.True(AlgorithmX.Algorithms.BitManipulation.BitManipulation.IsPowerOfTwo(1));
        Assert.True(AlgorithmX.Algorithms.BitManipulation.BitManipulation.IsPowerOfTwo(2));
        Assert.True(AlgorithmX.Algorithms.BitManipulation.BitManipulation.IsPowerOfTwo(1024));
        Assert.False(AlgorithmX.Algorithms.BitManipulation.BitManipulation.IsPowerOfTwo(3));
        Assert.False(AlgorithmX.Algorithms.BitManipulation.BitManipulation.IsPowerOfTwo(0));
    }

    [Fact]
    public void CountBits_ShouldBeCorrect()
    {
        Assert.Equal(0, AlgorithmX.Algorithms.BitManipulation.BitManipulation.CountBits(0));
        Assert.Equal(3, AlgorithmX.Algorithms.BitManipulation.BitManipulation.CountBits(7)); // 111
        Assert.Equal(1, AlgorithmX.Algorithms.BitManipulation.BitManipulation.CountBits(8)); // 1000
    }

    [Fact]
    public void LowBit_ShouldReturnLowestSetBit()
    {
        Assert.Equal(4, AlgorithmX.Algorithms.BitManipulation.BitManipulation.LowBit(12)); // 1100 → 100 = 4
        Assert.Equal(1, AlgorithmX.Algorithms.BitManipulation.BitManipulation.LowBit(7));  // 0111 → 001 = 1
    }

    [Fact]
    public void SingleNumber_ShouldFindUnique()
    {
        Assert.Equal(4, AlgorithmX.Algorithms.BitManipulation.BitManipulation.SingleNumber(new[] { 1, 2, 1, 3, 2, 4, 3 }));
    }

    [Fact]
    public void SingleNumberII_ShouldFindUniqueInTriplets()
    {
        Assert.Equal(3,
            AlgorithmX.Algorithms.BitManipulation.BitManipulation.SingleNumberII(new[] { 2, 2, 3, 2 }));
    }

    [Fact]
    public void EnumerateSubmasks_ShouldCoverAllSubsets()
    {
        int mask = 5; // 101
        var subs = AlgorithmX.Algorithms.BitManipulation.BitManipulation.EnumerateSubmasks(mask).ToList();
        Assert.Equal(3, subs.Count); // 101, 100, 001
        Assert.Contains(5, subs);
        Assert.Contains(4, subs);
        Assert.Contains(1, subs);
    }

    [Fact]
    public void Bitset_SetGet_ShouldWork()
    {
        var bs = new AlgorithmX.Algorithms.BitManipulation.Bitset(100);
        bs.Set(5);
        bs.Set(99);
        Assert.True(bs.Get(5));
        Assert.True(bs.Get(99));
        Assert.False(bs.Get(0));
        Assert.Equal(2, bs.Count);
    }

    [Fact]
    public void Bitset_Reset_ShouldClear()
    {
        var bs = new AlgorithmX.Algorithms.BitManipulation.Bitset(64);
        bs.Set(10);
        bs.Reset(10);
        Assert.False(bs.Get(10));
    }
}
