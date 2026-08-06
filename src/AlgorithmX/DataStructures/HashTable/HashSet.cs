namespace AlgorithmX.DataStructures.HashTable;

/// <summary>
/// 基于 HashMap 的 HashSet 实现。
/// </summary>
public class HashSet<T>
{
    private readonly HashMap<T, byte> _map;

    public HashSet() => _map = new HashMap<T, byte>();
    public HashSet(int capacity) => _map = new HashMap<T, byte>(capacity);

    public int Count => _map.Count;
    public bool IsEmpty => _map.IsEmpty;

    /// <summary>
    /// 添加元素。O(1) 平均。
    /// </summary>
    public bool Add(T item)
    {
        if (_map.ContainsKey(item)) return false;
        _map.Put(item, 0);
        return true;
    }

    /// <summary>
    /// 移除元素。O(1) 平均。
    /// </summary>
    public bool Remove(T item) => _map.Remove(item);

    /// <summary>
    /// 是否包含元素。O(1) 平均。
    /// </summary>
    public bool Contains(T item) => _map.ContainsKey(item);

    /// <summary>
    /// 清空。O(1)。
    /// </summary>
    public void Clear() => _map.Clear();
}
