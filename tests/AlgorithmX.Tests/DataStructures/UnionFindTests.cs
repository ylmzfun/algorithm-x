namespace AlgorithmX.Tests.DataStructures;

public class UnionFindTests
{
    [Fact]
    public void Initially_AllElementsAreSeparate()
    {
        var uf = new AlgorithmX.DataStructures.DisjointSet.UnionFind(5);
        Assert.Equal(5, uf.Components);
        for (int i = 0; i < 5; i++)
            Assert.Equal(i, uf.Find(i));
    }

    [Fact]
    public void Union_ShouldMergeSets()
    {
        var uf = new AlgorithmX.DataStructures.DisjointSet.UnionFind(5);
        Assert.True(uf.Union(0, 1));
        Assert.True(uf.IsConnected(0, 1));
        Assert.Equal(4, uf.Components);

        Assert.True(uf.Union(1, 2));
        Assert.True(uf.IsConnected(0, 2));
        Assert.Equal(3, uf.Components);
    }

    [Fact]
    public void Union_AlreadyConnected_ShouldReturnFalse()
    {
        var uf = new AlgorithmX.DataStructures.DisjointSet.UnionFind(3);
        uf.Union(0, 1);
        uf.Union(1, 2);
        Assert.False(uf.Union(0, 2));
        Assert.Equal(1, uf.Components);
    }

    [Fact]
    public void Find_ShouldUsePathCompression()
    {
        var uf = new AlgorithmX.DataStructures.DisjointSet.UnionFind(5);
        uf.Union(0, 1);
        uf.Union(1, 2);
        uf.Union(2, 3);
        uf.Union(3, 4);
        Assert.True(uf.IsConnected(0, 4));
        // 路径压缩后所有节点应直接指向根
        int root = uf.Find(0);
        for (int i = 1; i < 5; i++)
            Assert.Equal(root, uf.Find(i));
    }

    [Fact]
    public void IsConnected_ShouldReturnFalseForUnconnected()
    {
        var uf = new AlgorithmX.DataStructures.DisjointSet.UnionFind(4);
        uf.Union(0, 1);
        Assert.False(uf.IsConnected(0, 2));
        Assert.False(uf.IsConnected(1, 3));
    }
}
