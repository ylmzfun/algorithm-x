namespace AlgorithmX.Tests.DataStructures;

public class SegmentTreeTests
{
    [Fact]
    public void Query_ShouldReturnRangeSum()
    {
        var st = new AlgorithmX.DataStructures.SegmentTree.SegmentTree(new[] { 1, 3, 5, 7, 9, 11 });
        Assert.Equal(1, st.Query(0, 0));
        Assert.Equal(36, st.Query(0, 5));
        Assert.Equal(8, st.Query(1, 2)); // 3 + 5
        Assert.Equal(27, st.Query(3, 5)); // 7+9+11
    }

    [Fact]
    public void Update_ShouldChangeValue()
    {
        var st = new AlgorithmX.DataStructures.SegmentTree.SegmentTree(new[] { 1, 2, 3, 4 });
        st.Update(2, 99);
        Assert.Equal(99, st.Query(2, 2));
        Assert.Equal(106, st.Query(0, 3)); // 1+2+99+4
    }

    [Fact]
    public void UpdateRange_ShouldAddDeltaToRange()
    {
        var st = new AlgorithmX.DataStructures.SegmentTree.SegmentTree(new[] { 1, 2, 3, 4, 5 }, enableLazy: true);
        st.UpdateRange(1, 3, 10); // [2, 3, 4] 都加 10
        Assert.Equal(1, st.Query(0, 0));
        Assert.Equal(12, st.Query(1, 1));
        Assert.Equal(13, st.Query(2, 2));
        Assert.Equal(14, st.Query(3, 3));
        Assert.Equal(5, st.Query(4, 4));
        Assert.Equal(45, st.Query(0, 4)); // 1+12+13+14+5
    }
}
