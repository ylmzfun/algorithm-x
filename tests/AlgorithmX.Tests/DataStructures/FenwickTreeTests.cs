namespace AlgorithmX.Tests.DataStructures;

public class FenwickTreeTests
{
    [Fact]
    public void PrefixSum_ShouldBeCorrect()
    {
        var ft = new AlgorithmX.DataStructures.SegmentTree.FenwickTree(new[] { 1, 2, 3, 4, 5 });
        Assert.Equal(1, ft.PrefixSum(1));
        Assert.Equal(3, ft.PrefixSum(2));
        Assert.Equal(10, ft.PrefixSum(4));
        Assert.Equal(15, ft.PrefixSum(5));
    }

    [Fact]
    public void RangeSum_ShouldBeCorrect()
    {
        var ft = new AlgorithmX.DataStructures.SegmentTree.FenwickTree(new[] { 1, 3, 5, 7, 9 });
        Assert.Equal(8, ft.RangeSum(2, 3)); // 3 + 5 = 8
        Assert.Equal(1, ft.RangeSum(1, 1));
        Assert.Equal(24, ft.RangeSum(2, 5)); // 3+5+7+9 = 24
    }

    [Fact]
    public void Add_ShouldUpdateCorrectly()
    {
        var ft = new AlgorithmX.DataStructures.SegmentTree.FenwickTree(new[] { 1, 2, 3, 4, 5 });
        ft.Add(3, 10); // 在位置 3 加 10
        Assert.Equal(3, ft.PrefixSum(2));  // 1 + 2 = 3 不变
        Assert.Equal(16, ft.PrefixSum(3)); // 1 + 2 + 13 = 16
    }

    [Fact]
    public void Update_ShouldReplaceValue()
    {
        var ft = new AlgorithmX.DataStructures.SegmentTree.FenwickTree(new[] { 1, 2, 3 });
        ft.Update(1, 99); // 将索引 1（值为 2）替换为 99
        Assert.Equal(100, ft.PrefixSum(2)); // 1 + 99 = 100
    }
}
