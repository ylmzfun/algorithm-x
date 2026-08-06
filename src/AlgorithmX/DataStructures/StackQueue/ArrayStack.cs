namespace AlgorithmX.DataStructures.StackQueue;

/// <summary>
/// 基于数组的栈实现 — LIFO（后进先出）。
/// </summary>
/// <typeparam name="T">元素类型</typeparam>
public class ArrayStack<T>
{
    private const int DefaultCapacity = 4;
    private T[] _items;
    private int _size;

    public ArrayStack() : this(DefaultCapacity) { }

    public ArrayStack(int capacity)
    {
        if (capacity < 0)
            throw new ArgumentOutOfRangeException(nameof(capacity));
        _items = new T[capacity];
        _size = 0;
    }

    public int Count => _size;
    public bool IsEmpty => _size == 0;

    /// <summary>
    /// 入栈。均摊 O(1)。
    /// </summary>
    public void Push(T item)
    {
        if (_size == _items.Length)
        {
            var newItems = new T[_items.Length * 2];
            Array.Copy(_items, newItems, _size);
            _items = newItems;
        }
        _items[_size++] = item;
    }

    /// <summary>
    /// 出栈并返回栈顶元素。O(1)。
    /// </summary>
    public T Pop()
    {
        if (_size == 0)
            throw new InvalidOperationException("Stack is empty.");
        T item = _items[--_size];
        _items[_size] = default!;
        return item;
    }

    /// <summary>
    /// 查看栈顶元素（不移除）。O(1)。
    /// </summary>
    public T Peek()
    {
        if (_size == 0)
            throw new InvalidOperationException("Stack is empty.");
        return _items[_size - 1];
    }

    /// <summary>
    /// 清空栈。O(1)。
    /// </summary>
    public void Clear()
    {
        Array.Clear(_items, 0, _size);
        _size = 0;
    }
}
