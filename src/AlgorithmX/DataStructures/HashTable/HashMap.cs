namespace AlgorithmX.DataStructures.HashTable;

/// <summary>
/// 基于链地址法的哈希表实现。
/// 支持泛型 Key/Value，使用 EqualityComparer 进行键比较。
/// </summary>
public class HashMap<TKey, TValue>
{
    private const double LoadFactor = 0.75;
    private const int DefaultCapacity = 16;

    private Bucket[] _buckets;
    private int _size;

    public HashMap() : this(DefaultCapacity) { }

    public HashMap(int capacity)
    {
        if (capacity <= 0)
            throw new ArgumentOutOfRangeException(nameof(capacity));
        _buckets = new Bucket[capacity];
        _size = 0;
    }

    public int Count => _size;
    public bool IsEmpty => _size == 0;

    /// <summary>
    /// 索引器 — 获取或设置键对应的值。
    /// </summary>
    public TValue this[TKey key]
    {
        get
        {
            if (TryGetValue(key, out var value))
                return value;
            throw new KeyNotFoundException($"Key '{key}' not found.");
        }
        set => Put(key, value);
    }

    /// <summary>
    /// 插入或更新键值对。均摊 O(1)。
    /// </summary>
    public void Put(TKey key, TValue value)
    {
        if (_size >= _buckets.Length * LoadFactor)
            Resize(_buckets.Length * 2);

        int index = GetBucketIndex(key);
        ref Bucket bucket = ref _buckets[index];

        // 查找是否已存在
        var node = bucket?.First;
        while (node != null)
        {
            if (EqualityComparer<TKey>.Default.Equals(node.Key, key))
            {
                node.Value = value;
                return;
            }
            node = node.Next;
        }

        // 头部插入新节点
        bucket = new Bucket(new Node(key, value, bucket?.First), bucket?.Count + 1 ?? 1);
        _size++;
    }

    /// <summary>
    /// 尝试获取键对应的值。O(1) 平均。
    /// </summary>
    public bool TryGetValue(TKey key, out TValue value)
    {
        int index = GetBucketIndex(key);
        var node = _buckets[index]?.First;

        while (node != null)
        {
            if (EqualityComparer<TKey>.Default.Equals(node.Key, key))
            {
                value = node.Value;
                return true;
            }
            node = node.Next;
        }

        value = default!;
        return false;
    }

    /// <summary>
    /// 是否包含指定的键。O(1) 平均。
    /// </summary>
    public bool ContainsKey(TKey key) => TryGetValue(key, out _);

    /// <summary>
    /// 移除指定的键值对。O(1) 平均。
    /// </summary>
    public bool Remove(TKey key)
    {
        int index = GetBucketIndex(key);
        var bucket = _buckets[index];
        if (bucket?.First == null) return false;

        // 头部匹配
        if (EqualityComparer<TKey>.Default.Equals(bucket.First.Key, key))
        {
            _buckets[index] = bucket.First.Next == null
                ? null!
                : new Bucket(bucket.First.Next, bucket.Count - 1);
            _size--;
            return true;
        }

        // 遍历链表
        var prev = bucket.First;
        var curr = prev.Next;
        while (curr != null)
        {
            if (EqualityComparer<TKey>.Default.Equals(curr.Key, key))
            {
                prev.Next = curr.Next;
                _buckets[index] = new Bucket(bucket.First, bucket.Count - 1);
                _size--;
                return true;
            }
            prev = curr;
            curr = curr.Next;
        }
        return false;
    }

    /// <summary>
    /// 清空所有键值对。O(n)。
    /// </summary>
    public void Clear()
    {
        Array.Clear(_buckets, 0, _buckets.Length);
        _size = 0;
    }

    /// <summary>
    /// 返回所有键的集合。
    /// </summary>
    public IEnumerable<TKey> Keys
    {
        get
        {
            foreach (var bucket in _buckets)
            {
                var node = bucket?.First;
                while (node != null)
                {
                    yield return node.Key;
                    node = node.Next;
                }
            }
        }
    }

    /// <summary>
    /// 返回所有值的集合。
    /// </summary>
    public IEnumerable<TValue> Values
    {
        get
        {
            foreach (var bucket in _buckets)
            {
                var node = bucket?.First;
                while (node != null)
                {
                    yield return node.Value;
                    node = node.Next;
                }
            }
        }
    }

    private int GetBucketIndex(TKey key)
    {
        int hash = key is null ? 0 : EqualityComparer<TKey>.Default.GetHashCode(key);
        return (hash & 0x7FFFFFFF) % _buckets.Length;
    }

    private void Resize(int newCapacity)
    {
        var oldBuckets = _buckets;
        _buckets = new Bucket[newCapacity];
        _size = 0;

        foreach (var bucket in oldBuckets)
        {
            var node = bucket?.First;
            while (node != null)
            {
                Put(node.Key, node.Value);
                node = node.Next;
            }
        }
    }

    /// <summary>
    /// 哈希桶结构（只包含链表头），减少链表遍历。
    /// </summary>
    private sealed class Bucket
    {
        public Node First { get; }
        public int Count { get; }

        public Bucket(Node first, int count)
        {
            First = first;
            Count = count;
        }
    }

    /// <summary>
    /// 哈希表链表节点。
    /// </summary>
    private sealed class Node
    {
        public TKey Key { get; }
        public TValue Value { get; set; }
        public Node? Next { get; set; }

        public Node(TKey key, TValue value, Node? next = null)
        {
            Key = key;
            Value = value;
            Next = next;
        }
    }
}
