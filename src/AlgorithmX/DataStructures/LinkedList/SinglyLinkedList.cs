namespace AlgorithmX.DataStructures.LinkedList;

/// <summary>
/// 单向链表节点。
/// </summary>
public class SinglyListNode<T>
{
    public T Value { get; set; }
    public SinglyListNode<T>? Next { get; set; }

    public SinglyListNode(T value, SinglyListNode<T>? next = null)
    {
        Value = value;
        Next = next;
    }
}

/// <summary>
/// 单向链表实现 — 支持头部/尾部 O(1) 插入，O(n) 查找/删除。
/// </summary>
/// <typeparam name="T">元素类型</typeparam>
public class SinglyLinkedList<T>
{
    private SinglyListNode<T>? _head;
    private SinglyListNode<T>? _tail;
    private int _size;

    public int Count => _size;
    public bool IsEmpty => _size == 0;
    public SinglyListNode<T>? Head => _head;
    public SinglyListNode<T>? Tail => _tail;

    /// <summary>
    /// 在头部添加节点。O(1)。
    /// </summary>
    public void AddFirst(T value)
    {
        var node = new SinglyListNode<T>(value, _head);
        _head = node;
        _tail ??= node;
        _size++;
    }

    /// <summary>
    /// 在尾部添加节点。O(1)。
    /// </summary>
    public void AddLast(T value)
    {
        var node = new SinglyListNode<T>(value);
        if (_tail == null)
        {
            _head = _tail = node;
        }
        else
        {
            _tail.Next = node;
            _tail = node;
        }
        _size++;
    }

    /// <summary>
    /// 移除头部节点。O(1)。
    /// </summary>
    public T RemoveFirst()
    {
        if (_head == null)
            throw new InvalidOperationException("List is empty.");

        T value = _head.Value;
        _head = _head.Next;
        if (_head == null) _tail = null;
        _size--;
        return value;
    }

    /// <summary>
    /// 移除第一个匹配的节点。O(n)。
    /// </summary>
    public bool Remove(T value)
    {
        if (_head == null) return false;

        if (EqualityComparer<T>.Default.Equals(_head.Value, value))
        {
            RemoveFirst();
            return true;
        }

        var current = _head;
        while (current.Next != null)
        {
            if (EqualityComparer<T>.Default.Equals(current.Next.Value, value))
            {
                if (current.Next == _tail)
                    _tail = current;
                current.Next = current.Next.Next;
                _size--;
                return true;
            }
            current = current.Next;
        }
        return false;
    }

    /// <summary>
    /// 反转链表（原地）。O(n)。
    /// </summary>
    public void Reverse()
    {
        if (_head == null || _head.Next == null) return;

        SinglyListNode<T>? prev = null;
        var current = _head;
        _tail = _head;

        while (current != null)
        {
            var next = current.Next;
            current.Next = prev;
            prev = current;
            current = next;
        }
        _head = prev;
    }

    /// <summary>
    /// 查找指定值的节点。O(n)。
    /// </summary>
    public SinglyListNode<T>? Find(T value)
    {
        var current = _head;
        while (current != null)
        {
            if (EqualityComparer<T>.Default.Equals(current.Value, value))
                return current;
            current = current.Next;
        }
        return null;
    }

    /// <summary>
    /// 是否包含指定元素。O(n)。
    /// </summary>
    public bool Contains(T value) => Find(value) != null;

    /// <summary>
    /// 转为数组。
    /// </summary>
    public T[] ToArray()
    {
        var result = new T[_size];
        var current = _head;
        for (int i = 0; i < _size; i++)
        {
            result[i] = current!.Value;
            current = current.Next;
        }
        return result;
    }
}
