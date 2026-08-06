namespace AlgorithmX.Tests.DataStructures;

public class BinarySearchTreeTests
{
    [Fact]
    public void Insert_ShouldMaintainBstProperty()
    {
        var bst = new AlgorithmX.DataStructures.Tree.BinarySearchTree<int>();
        bst.Insert(5);
        bst.Insert(3);
        bst.Insert(7);
        bst.Insert(2);
        bst.Insert(4);
        bst.Insert(6);
        bst.Insert(8);

        Assert.Equal(7, bst.Count);
        Assert.True(bst.IsValidBst());
    }

    [Fact]
    public void Inorder_ShouldBeSorted()
    {
        var bst = new AlgorithmX.DataStructures.Tree.BinarySearchTree<int>();
        int[] values = { 5, 3, 7, 2, 8, 1, 9 };
        foreach (int v in values) bst.Insert(v);

        var inorder = bst.Inorder().ToList();
        Assert.Equal(new[] { 1, 2, 3, 5, 7, 8, 9 }, inorder);
    }

    [Fact]
    public void Contains_ShouldFindExistingAndMissing()
    {
        var bst = new AlgorithmX.DataStructures.Tree.BinarySearchTree<int>();
        bst.Insert(10);
        bst.Insert(5);
        bst.Insert(15);
        Assert.True(bst.Contains(10));
        Assert.True(bst.Contains(5));
        Assert.False(bst.Contains(99));
    }

    [Fact]
    public void MinMax_ShouldReturnCorrectValues()
    {
        var bst = new AlgorithmX.DataStructures.Tree.BinarySearchTree<int>();
        bst.Insert(50);
        bst.Insert(30);
        bst.Insert(70);
        bst.Insert(10);
        bst.Insert(90);
        Assert.Equal(10, bst.Min());
        Assert.Equal(90, bst.Max());
    }

    [Fact]
    public void Remove_LeafNode_ShouldWork()
    {
        var bst = new AlgorithmX.DataStructures.Tree.BinarySearchTree<int>();
        bst.Insert(5);
        bst.Insert(3);
        bst.Insert(7);
        Assert.True(bst.Remove(3));
        Assert.False(bst.Contains(3));
        Assert.Equal(2, bst.Count);
        Assert.True(bst.IsValidBst());
    }

    [Fact]
    public void Remove_NodeWithOneChild_ShouldReplaceWithChild()
    {
        var bst = new AlgorithmX.DataStructures.Tree.BinarySearchTree<int>();
        bst.Insert(5);
        bst.Insert(3);
        bst.Insert(4); // 3 的右子节点
        Assert.True(bst.Remove(3));
        Assert.True(bst.Contains(4));
        Assert.False(bst.Contains(3));
        Assert.True(bst.IsValidBst());
    }

    [Fact]
    public void Remove_NodeWithTwoChildren_ShouldUseSuccessor()
    {
        var bst = new AlgorithmX.DataStructures.Tree.BinarySearchTree<int>();
        bst.Insert(5);
        bst.Insert(3);
        bst.Insert(8);
        bst.Insert(2);
        bst.Insert(4);
        bst.Insert(7);
        bst.Insert(9);
        Assert.True(bst.Remove(8)); // 有左右子节点
        Assert.False(bst.Contains(8));
        Assert.Equal(6, bst.Count);
        Assert.True(bst.IsValidBst());
    }

    [Fact]
    public void Remove_NonExistent_ShouldReturnFalse()
    {
        var bst = new AlgorithmX.DataStructures.Tree.BinarySearchTree<int>();
        bst.Insert(1);
        Assert.False(bst.Remove(999));
    }
}
