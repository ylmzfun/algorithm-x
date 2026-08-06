namespace AlgorithmX.DataStructures.DisjointSet;

/// <summary>
/// 并查集 (Union-Find / Disjoint Set Union)。
/// 支持按秩合并与路径压缩，均摊时间复杂度接近 O(α(n))（阿克曼反函数，实际可视为 O(1)）。
/// </summary>
public class UnionFind
{
    private readonly int[] _parent;
    private readonly int[] _rank;
    private int _components;

    /// <param name="n">元素数量（0 ~ n-1）</param>
    public UnionFind(int n)
    {
        if (n <= 0)
            throw new ArgumentOutOfRangeException(nameof(n));
        _parent = new int[n];
        _rank = new int[n];
        for (int i = 0; i < n; i++)
        {
            _parent[i] = i;
            _rank[i] = 1;
        }
        _components = n;
    }

    /// <summary>
    /// 连通分量数量。
    /// </summary>
    public int Components => _components;

    /// <summary>
    /// 查找 x 所属集合的代表元（路径压缩）。
    /// </summary>
    public int Find(int x)
    {
        if (x < 0 || x >= _parent.Length)
            throw new ArgumentOutOfRangeException(nameof(x));

        if (_parent[x] != x)
            _parent[x] = Find(_parent[x]);
        return _parent[x];
    }

    /// <summary>
    /// 合并 x 和 y 所在的集合（按秩合并）。
    /// 返回 true 表示实际发生了合并，false 表示已在同一集合。
    /// </summary>
    public bool Union(int x, int y)
    {
        int rootX = Find(x);
        int rootY = Find(y);

        if (rootX == rootY) return false;

        if (_rank[rootX] < _rank[rootY])
        {
            _parent[rootX] = rootY;
        }
        else if (_rank[rootX] > _rank[rootY])
        {
            _parent[rootY] = rootX;
        }
        else
        {
            _parent[rootY] = rootX;
            _rank[rootX]++;
        }
        _components--;
        return true;
    }

    /// <summary>
    /// 判断 x 和 y 是否连通。
    /// </summary>
    public bool IsConnected(int x, int y) => Find(x) == Find(y);

    /// <summary>
    /// 获取 x 所在集合的大小。
    /// O(n) 遍历 — 实际项目中可维护一个 size 数组优化。
    /// </summary>
    public int GetSetSize(int x)
    {
        int root = Find(x);
        int size = 0;
        for (int i = 0; i < _parent.Length; i++)
            if (Find(i) == root)
                size++;
        return size;
    }
}
