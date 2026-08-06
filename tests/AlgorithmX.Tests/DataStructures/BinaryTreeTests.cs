namespace AlgorithmX.Tests.DataStructures;

public class BinaryTreeTests
{
    // 构建测试树:
    //       1
    //      / \
    //     2   3
    //    / \   \
    //   4   5   6
    private static AlgorithmX.DataStructures.Tree.BinaryTree<int> CreateTestTree()
    {
        var root = new AlgorithmX.DataStructures.Tree.BinaryTreeNode<int>(1,
            new AlgorithmX.DataStructures.Tree.BinaryTreeNode<int>(2,
                new AlgorithmX.DataStructures.Tree.BinaryTreeNode<int>(4),
                new AlgorithmX.DataStructures.Tree.BinaryTreeNode<int>(5)),
            new AlgorithmX.DataStructures.Tree.BinaryTreeNode<int>(3,
                null,
                new AlgorithmX.DataStructures.Tree.BinaryTreeNode<int>(6))
        );
        return new AlgorithmX.DataStructures.Tree.BinaryTree<int>(root);
    }

    [Fact]
    public void Preorder_ShouldBeRootLeftRight()
    {
        var tree = CreateTestTree();
        Assert.Equal(new[] { 1, 2, 4, 5, 3, 6 }, tree.Preorder());
    }

    [Fact]
    public void Inorder_ShouldBeLeftRootRight()
    {
        var tree = CreateTestTree();
        Assert.Equal(new[] { 4, 2, 5, 1, 3, 6 }, tree.Inorder());
    }

    [Fact]
    public void Postorder_ShouldBeLeftRightRoot()
    {
        var tree = CreateTestTree();
        Assert.Equal(new[] { 4, 5, 2, 6, 3, 1 }, tree.Postorder());
    }

    [Fact]
    public void LevelOrder_ShouldBeByLevel()
    {
        var tree = CreateTestTree();
        Assert.Equal(new[] { 1, 2, 3, 4, 5, 6 }, tree.LevelOrder());
    }

    [Fact]
    public void LevelOrderByLevel_ShouldGroupByLevel()
    {
        var tree = CreateTestTree();
        var levels = tree.LevelOrderByLevel().ToList();
        Assert.Equal(3, levels.Count);
        Assert.Equal(new[] { 1 }, levels[0]);
        Assert.Equal(new[] { 2, 3 }, levels[1]);
        Assert.Equal(new[] { 4, 5, 6 }, levels[2]);
    }

    [Fact]
    public void Height_ShouldReturnCorrectValue()
    {
        var tree = CreateTestTree();
        Assert.Equal(2, tree.Height()); // 边数
    }

    [Fact]
    public void PreorderIterative_ShouldMatchRecursive()
    {
        var tree = CreateTestTree();
        Assert.Equal(tree.Preorder(), tree.PreorderIterative());
    }

    [Fact]
    public void InorderIterative_ShouldMatchRecursive()
    {
        var tree = CreateTestTree();
        Assert.Equal(tree.Inorder(), tree.InorderIterative());
    }

    [Fact]
    public void Count_ShouldReturnCorrectNodeCount()
    {
        var tree = CreateTestTree();
        Assert.Equal(6, tree.Count());
    }

    [Fact]
    public void LeafCount_ShouldReturnCorrectCount()
    {
        var tree = CreateTestTree();
        Assert.Equal(3, tree.LeafCount()); // 4, 5, 6
    }
}
