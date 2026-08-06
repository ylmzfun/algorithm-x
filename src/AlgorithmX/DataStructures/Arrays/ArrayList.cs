namespace AlgorithmX.DataStructures.Arrays;

/// <summary>
/// 动态数组实现 — 自动扩容与缩容的泛型数组。
/// 类似于 .NET 中的 <see cref="System.Collections.Generic.List{T}"/>。
/// </summary>
/// <typeparam name="T">元素类型</typeparam>
public class ArrayList<T>
{
    private const int DefaultCapacity = 4;
    private const double ShrinkThreshold = 0.25; // 当元素数量低于容量 25% 时缩容

    private T[] _items;
    private int _size;

    public ArrayList() : this(DefaultCapacity) { }

    public ArrayList(int capacity)
    {
        if (capacity < 0)
            throw new ArgumentOutOfRangeException(nameof(capacity));
        _items = new T[capacity];
        _size = 0;
    }

    public int Count => _size;
    public int Capacity => _items.Length;
    public bool IsEmpty => _size == 0;

    /// <summary>
    /// 索引器 — 读取或设置指定位置的元素。
    /// </summary>
    public T this[int index]
    {
        get
        {
            if (index < 0 || index >= _size)
                throw new ArgumentOutOfRangeException(nameof(index));
            return _items[index];
        }
        set
        {
            if (index < 0 || index >= _size)
                throw new ArgumentOutOfRangeException(nameof(index));
            _items[index] = value;
        }
    }

    /// <summary>
    /// 在末尾添加元素。均摊 O(1)。
    /// </summary>
    public void Add(T item)
    {
        if (_size == _items.Length)
            Resize(_items.Length * 2);
        _items[_size++] = item;
    }

    /// <summary>
    /// 在指定位置插入元素。O(n)。
    /// </summary>
    public void Insert(int index, T item)
    {
        if (index < 0 || index > _size)
            throw new ArgumentOutOfRangeException(nameof(index));

        if (_size == _items.Length)
            Resize(_items.Length * 2);

        Array.Copy(_items, index, _items, index + 1, _size - index);
        _items[index] = item;
        _size++;
    }

    /// <summary>
    /// 移除指定位置的元素。O(n)。
    /// </summary>
    public T RemoveAt(int index)
    {
        if (index < 0 || index >= _size)
            throw new ArgumentOutOfRangeException(nameof(index));

        T removed = _items[index];
        Array.Copy(_items, index + 1, _items, index, _size - index - 1);
        _items[--_size] = default!;

        if (_size > 0 && _size < _items.Length * ShrinkThreshold)
            Resize(_items.Length / 2);

        return removed;
    }

    /// <summary>
    /// 移除第一个匹配的元素。O(n)。
    /// </summary>
    public bool Remove(T item)
    {
        int index = IndexOf(item);
        if (index < 0) return false;
        RemoveAt(index);
        return true;
    }

    /// <summary>
    /// 查找元素的索引。O(n)。
    /// </summary>
    public int IndexOf(T item)
    {
        return Array.IndexOf(_items, item, 0, _size);
    }

    /// <summary>
    /// 是否包含指定元素。O(n)。
    /// </summary>
    public bool Contains(T item) => IndexOf(item) >= 0;

    /// <summary>
    /// 清空所有元素。O(1)。
    /// </summary>
    public void Clear()
    {
        Array.Clear(_items, 0, _size);
        _size = 0;
    }

    /// <summary>
    /// 返回数组的浅拷贝。
    /// </summary>
    public T[] ToArray()
    {
        var result = new T[_size];
        Array.Copy(_items, result, _size);
        return result;
    }

    private void Resize(int newCapacity)
    {
        if (newCapacity < DefaultCapacity)
            newCapacity = DefaultCapacity;
        var newItems = new T[newCapacity];
        Array.Copy(_items, newItems, _size);
        _items = newItems;
    }
}
