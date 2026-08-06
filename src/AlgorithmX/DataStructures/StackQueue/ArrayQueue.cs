namespace AlgorithmX.DataStructures.StackQueue;

/// <summary>
/// 基于循环数组的队列实现 — FIFO（先进先出）。
/// </summary>
/// <typeparam name="T">元素类型</typeparam>
public class ArrayQueue<T>
{
    private const int DefaultCapacity = 4;
    private T[] _items;
    private int _head;  // 队首索引
    private int _tail;  // 队尾索引（下一个插入位置）
    private int _size;

    public ArrayQueue() : this(DefaultCapacity) { }

    public ArrayQueue(int capacity)
    {
        if (capacity < 0)
            throw new ArgumentOutOfRangeException(nameof(capacity));
        _items = new T[capacity];
        _head = 0;
        _tail = 0;
        _size = 0;
    }

    public int Count => _size;
    public bool IsEmpty => _size == 0;

    /// <summary>
    /// 入队。均摊 O(1)。
    /// </summary>
    public void Enqueue(T item)
    {
        if (_size == _items.Length)
            Resize(_items.Length * 2);
        _items[_tail] = item;
        _tail = (_tail + 1) % _items.Length;
        _size++;
    }

    /// <summary>
    /// 出队并返回队首元素。均摊 O(1)。
    /// </summary>
    public T Dequeue()
    {
        if (_size == 0)
            throw new InvalidOperationException("Queue is empty.");
        T item = _items[_head];
        _items[_head] = default!;
        _head = (_head + 1) % _items.Length;
        _size--;

        if (_size > 0 && _size == _items.Length / 4)
            Resize(_items.Length / 2);

        return item;
    }

    /// <summary>
    /// 查看队首元素（不移除）。O(1)。
    /// </summary>
    public T Peek()
    {
        if (_size == 0)
            throw new InvalidOperationException("Queue is empty.");
        return _items[_head];
    }

    /// <summary>
    /// 清空队列。O(1)。
    /// </summary>
    public void Clear()
    {
        Array.Clear(_items, 0, _items.Length);
        _head = 0;
        _tail = 0;
        _size = 0;
    }

    private void Resize(int newCapacity)
    {
        if (newCapacity < DefaultCapacity)
            newCapacity = DefaultCapacity;
        var newItems = new T[newCapacity];
        if (_size > 0)
        {
            if (_head < _tail)
            {
                Array.Copy(_items, _head, newItems, 0, _size);
            }
            else
            {
                Array.Copy(_items, _head, newItems, 0, _items.Length - _head);
                Array.Copy(_items, 0, newItems, _items.Length - _head, _tail);
            }
        }
        _items = newItems;
        _head = 0;
        _tail = _size;
    }
}
