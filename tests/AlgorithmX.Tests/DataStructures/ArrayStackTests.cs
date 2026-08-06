namespace AlgorithmX.Tests.DataStructures;

public class ArrayStackTests
{
    [Fact]
    public void PushPop_ShouldFollowLifo()
    {
        var stack = new AlgorithmX.DataStructures.StackQueue.ArrayStack<int>();
        stack.Push(1);
        stack.Push(2);
        stack.Push(3);
        Assert.Equal(3, stack.Pop());
        Assert.Equal(2, stack.Pop());
        Assert.Equal(1, stack.Pop());
        Assert.True(stack.IsEmpty);
    }

    [Fact]
    public void Peek_ShouldNotRemoveElement()
    {
        var stack = new AlgorithmX.DataStructures.StackQueue.ArrayStack<int>();
        stack.Push(42);
        Assert.Equal(42, stack.Peek());
        Assert.Equal(1, stack.Count);
    }

    [Fact]
    public void Pop_OnEmpty_ShouldThrow()
    {
        var stack = new AlgorithmX.DataStructures.StackQueue.ArrayStack<int>();
        Assert.Throws<InvalidOperationException>(() => stack.Pop());
    }

    [Fact]
    public void Push_BeyondCapacity_ShouldResize()
    {
        var stack = new AlgorithmX.DataStructures.StackQueue.ArrayStack<int>(2);
        for (int i = 0; i < 100; i++)
            stack.Push(i);
        Assert.Equal(100, stack.Count);
    }

    [Fact]
    public void Clear_ShouldMakeStackEmpty()
    {
        var stack = new AlgorithmX.DataStructures.StackQueue.ArrayStack<int>();
        stack.Push(1);
        stack.Push(2);
        stack.Clear();
        Assert.True(stack.IsEmpty);
    }
}
