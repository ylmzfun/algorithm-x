namespace AlgorithmX.Tests.DataStructures;

public class ArrayQueueTests
{
    [Fact]
    public void EnqueueDequeue_ShouldFollowFifo()
    {
        var queue = new AlgorithmX.DataStructures.StackQueue.ArrayQueue<int>();
        queue.Enqueue(1);
        queue.Enqueue(2);
        queue.Enqueue(3);
        Assert.Equal(1, queue.Dequeue());
        Assert.Equal(2, queue.Dequeue());
        Assert.Equal(3, queue.Dequeue());
        Assert.True(queue.IsEmpty);
    }

    [Fact]
    public void Peek_ShouldNotRemoveElement()
    {
        var queue = new AlgorithmX.DataStructures.StackQueue.ArrayQueue<int>();
        queue.Enqueue(99);
        Assert.Equal(99, queue.Peek());
        Assert.Equal(1, queue.Count);
    }

    [Fact]
    public void Dequeue_OnEmpty_ShouldThrow()
    {
        var queue = new AlgorithmX.DataStructures.StackQueue.ArrayQueue<int>();
        Assert.Throws<InvalidOperationException>(() => queue.Dequeue());
    }

    [Fact]
    public void CircularWrapping_ShouldWorkCorrectly()
    {
        var queue = new AlgorithmX.DataStructures.StackQueue.ArrayQueue<int>(4);
        queue.Enqueue(1);
        queue.Enqueue(2);
        queue.Enqueue(3);
        Assert.Equal(1, queue.Dequeue());
        queue.Enqueue(4);
        queue.Enqueue(5);
        Assert.Equal(2, queue.Dequeue());
        Assert.Equal(3, queue.Dequeue());
        Assert.Equal(4, queue.Dequeue());
        Assert.Equal(5, queue.Dequeue());
    }

    [Fact]
    public void Clear_ShouldResetQueue()
    {
        var queue = new AlgorithmX.DataStructures.StackQueue.ArrayQueue<int>();
        queue.Enqueue(1);
        queue.Enqueue(2);
        queue.Clear();
        Assert.True(queue.IsEmpty);
    }
}
