namespace AlgorithmX.Tests.DataStructures;

public class SinglyLinkedListTests
{
    [Fact]
    public void AddFirst_ShouldPrependElement()
    {
        var list = new AlgorithmX.DataStructures.LinkedList.SinglyLinkedList<int>();
        list.AddFirst(1);
        list.AddFirst(2);
        Assert.Equal(2, list.Count);
        Assert.Equal(2, list.Head!.Value);
    }

    [Fact]
    public void AddLast_ShouldAppendElement()
    {
        var list = new AlgorithmX.DataStructures.LinkedList.SinglyLinkedList<int>();
        list.AddLast(1);
        list.AddLast(2);
        Assert.Equal(2, list.Count);
        Assert.Equal(2, list.Tail!.Value);
    }

    [Fact]
    public void RemoveFirst_ShouldReturnHeadAndRemove()
    {
        var list = new AlgorithmX.DataStructures.LinkedList.SinglyLinkedList<int>();
        list.AddLast(10);
        list.AddLast(20);
        int removed = list.RemoveFirst();
        Assert.Equal(10, removed);
        Assert.Equal(1, list.Count);
    }

    [Fact]
    public void Remove_ShouldRemoveFirstMatch()
    {
        var list = new AlgorithmX.DataStructures.LinkedList.SinglyLinkedList<int>();
        list.AddLast(1);
        list.AddLast(2);
        list.AddLast(3);
        Assert.True(list.Remove(2));
        Assert.Equal(2, list.Count);
        Assert.False(list.Contains(2));
    }

    [Fact]
    public void Reverse_ShouldReverseList()
    {
        var list = new AlgorithmX.DataStructures.LinkedList.SinglyLinkedList<int>();
        list.AddLast(1);
        list.AddLast(2);
        list.AddLast(3);
        list.Reverse();
        Assert.Equal(new[] { 3, 2, 1 }, list.ToArray());
    }

    [Fact]
    public void Find_ShouldReturnNodeOrNull()
    {
        var list = new AlgorithmX.DataStructures.LinkedList.SinglyLinkedList<string>();
        list.AddLast("a");
        list.AddLast("b");
        Assert.NotNull(list.Find("a"));
        Assert.Null(list.Find("z"));
    }

    [Fact]
    public void RemoveFirst_OnEmpty_ShouldThrow()
    {
        var list = new AlgorithmX.DataStructures.LinkedList.SinglyLinkedList<int>();
        Assert.Throws<InvalidOperationException>(() => list.RemoveFirst());
    }

    [Fact]
    public void AddFirstAndLast_WithSingleElement_TailShouldEqualHead()
    {
        var list = new AlgorithmX.DataStructures.LinkedList.SinglyLinkedList<int>();
        list.AddFirst(42);
        Assert.Same(list.Head, list.Tail);
        Assert.Equal(1, list.Count);
    }
}
