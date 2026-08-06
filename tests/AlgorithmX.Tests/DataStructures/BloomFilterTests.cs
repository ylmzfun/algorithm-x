namespace AlgorithmX.Tests.DataStructures;

public class BloomFilterTests
{
    [Fact]
    public void MightContain_ShouldReturnTrueForAddedItems()
    {
        var bf = new AlgorithmX.DataStructures.BloomFilter.BloomFilter<string>(1000);
        bf.Add("hello");
        bf.Add("world");
        Assert.True(bf.MightContain("hello"));
        Assert.True(bf.MightContain("world"));
    }

    [Fact]
    public void MightContain_ShouldReturnFalseForDefinitelyNotAdded()
    {
        var bf = new AlgorithmX.DataStructures.BloomFilter.BloomFilter<string>(1000);
        bf.Add("hello");
        // 对于未添加的元素，大概率返回 false
        Assert.False(bf.MightContain("definitely_not_added_xyz_12345"));
    }

    [Fact]
    public void SizeAndHashCount_ShouldBeCalculatedCorrectly()
    {
        // 预期 1000 个元素，1% 误报率
        var bf = new AlgorithmX.DataStructures.BloomFilter.BloomFilter<int>(1000, 0.01);
        Assert.True(bf.Size > 0);
        Assert.True(bf.HashCount > 0);
    }

    [Fact]
    public void SetBitCount_ShouldTrackUsage()
    {
        var bf = new AlgorithmX.DataStructures.BloomFilter.BloomFilter<string>(100);
        bf.Add("test");
        Assert.True(bf.SetBitCount > 0);
    }
}
