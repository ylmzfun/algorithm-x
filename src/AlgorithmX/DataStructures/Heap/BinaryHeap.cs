namespace AlgorithmX.DataStructures.Heap;

/// <summary>
/// 二叉堆 — 基于数组的完全二叉树实现的优先队列。
/// 默认最小堆（堆顶最小）；设置 isMaxHeap=true 为最大堆。
/// O(log n) 插入/删除，O(1) 查看堆顶。
/// </summary>
public class BinaryHeap<T> where T : IComparable<T>
{
    private T[] _items;
    private int _size;
    private readonly bool _isMaxHeap;
    private readonly IComparer<T> _comparer;

    public BinaryHeap(bool isMaxHeap = false) : this(16, isMaxHeap) { }

    public BinaryHeap(int capacity, bool isMaxHeap = false)
    {
        if (capacity <= 0)
            throw new ArgumentOutOfRangeException(nameof(capacity));
        _items = new T[capacity + 1]; // 索引从 1 开始
        _size = 0;
        _isMaxHeap = isMaxHeap;
        _comparer = isMaxHeap
            ? Comparer<T>.Create((a, b) => b.CompareTo(a))
            : Comparer<T>.Default;
    }

    public int Count => _size;
    public bool IsEmpty => _size == 0;

    /// <summary>
    /// 查看堆顶元素（不移除）。O(1)。
    /// </summary>
    public T Peek()
    {
        if (_size == 0)
            throw new InvalidOperationException("Heap is empty.");
        return _items[1];
    }

    /// <summary>
    /// 插入元素。O(log n)。
    /// </summary>
    public void Push(T item)
    {
        if (_size + 1 >= _items.Length)
            Resize(_items.Length * 2);
        _items[++_size] = item;
        Swim(_size);
    }

    /// <summary>
    /// 弹出堆顶元素。O(log n)。
    /// </summary>
    public T Pop()
    {
        if (_size == 0)
            throw new InvalidOperationException("Heap is empty.");
        T top = _items[1];
        _items[1] = _items[_size];
        _items[_size] = default!;
        _size--;
        Sink(1);

        if (_size > 0 && _size == _items.Length / 4)
            Resize(_items.Length / 2);
        return top;
    }

    /// <summary>
    /// 从给定数组构建堆（Heapify）。O(n)。
    /// </summary>
    public static BinaryHeap<T> Heapify(T[] array, bool isMaxHeap = false)
    {
        var heap = new BinaryHeap<T>(array.Length, isMaxHeap);
        heap._size = array.Length;
        heap._items = new T[array.Length + 1];
        Array.Copy(array, 0, heap._items, 1, array.Length);

        for (int i = heap._size / 2; i >= 1; i--)
            heap.Sink(i);
        return heap;
    }

    // ─── 上浮 ───────────────────────────

    private void Swim(int k)
    {
        while (k > 1 && Less(k, k / 2))
        {
            Swap(k / 2, k);
            k /= 2;
        }
    }

    // ─── 下沉 ───────────────────────────

    private void Sink(int k)
    {
        while (2 * k <= _size)
        {
            int child = 2 * k;
            if (child + 1 <= _size && Less(child + 1, child))
                child++;
            if (Less(k, child)) break;
            Swap(k, child);
            k = child;
        }
    }

    private bool Less(int i, int j) => _comparer.Compare(_items[i], _items[j]) < 0;

    private void Swap(int i, int j) => (_items[i], _items[j]) = (_items[j], _items[i]);

    private void Resize(int newCapacity)
    {
        var newItems = new T[newCapacity];
        Array.Copy(_items, newItems, Math.Min(_items.Length, newCapacity));
        _items = newItems;
    }
}
