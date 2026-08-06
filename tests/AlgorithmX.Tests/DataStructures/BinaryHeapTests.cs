namespace AlgorithmX.Tests.DataStructures;

public class BinaryHeapTests
{
    [Fact]
    public void MinHeap_ShouldPopInAscendingOrder()
    {
        var heap = new AlgorithmX.DataStructures.Heap.BinaryHeap<int>();
        int[] values = { 5, 3, 8, 1, 9, 2 };
        foreach (int v in values) heap.Push(v);

        var sorted = new List<int>();
        while (!heap.IsEmpty)
            sorted.Add(heap.Pop());

        Assert.Equal(new[] { 1, 2, 3, 5, 8, 9 }, sorted);
    }

    [Fact]
    public void MaxHeap_ShouldPopInDescendingOrder()
    {
        var heap = new AlgorithmX.DataStructures.Heap.BinaryHeap<int>(isMaxHeap: true);
        int[] values = { 5, 3, 8, 1, 9, 2 };
        foreach (int v in values) heap.Push(v);

        var sorted = new List<int>();
        while (!heap.IsEmpty)
            sorted.Add(heap.Pop());

        Assert.Equal(new[] { 9, 8, 5, 3, 2, 1 }, sorted);
    }

    [Fact]
    public void Peek_ShouldNotRemove()
    {
        var heap = new AlgorithmX.DataStructures.Heap.BinaryHeap<int>();
        heap.Push(42);
        Assert.Equal(42, heap.Peek());
        Assert.Equal(1, heap.Count);
    }

    [Fact]
    public void Pop_OnEmpty_ShouldThrow()
    {
        var heap = new AlgorithmX.DataStructures.Heap.BinaryHeap<int>();
        Assert.Throws<InvalidOperationException>(() => heap.Pop());
    }

    [Fact]
    public void Heapify_ShouldBuildValidHeap()
    {
        int[] array = { 9, 3, 7, 1, 5, 8, 2, 6, 4 };
        var heap = AlgorithmX.DataStructures.Heap.BinaryHeap<int>.Heapify(array);
        var sorted = new List<int>();
        while (!heap.IsEmpty)
            sorted.Add(heap.Pop());
        Assert.Equal(new[] { 1, 2, 3, 4, 5, 6, 7, 8, 9 }, sorted);
    }

    [Fact]
    public void LargeInput_ShouldWork()
    {
        var heap = new AlgorithmX.DataStructures.Heap.BinaryHeap<int>();
        var random = new Random(42);
        for (int i = 0; i < 1000; i++)
            heap.Push(random.Next(10000));

        int prev = heap.Pop();
        while (!heap.IsEmpty)
        {
            int curr = heap.Pop();
            Assert.True(prev <= curr);
            prev = curr;
        }
    }
}
