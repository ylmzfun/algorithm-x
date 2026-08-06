namespace AlgorithmX.DataStructures.SegmentTree;

/// <summary>
/// 线段树 — 支持区间查询与区间修改的通用数据结构。
/// 默认实现区间求和，可通过传入 Func 自定义合并操作。
/// O(log n) 查询，O(log n) 单点更新，O(log n) 区间更新（带懒惰标记）。
/// </summary>
public class SegmentTree
{
    private readonly long[] _tree;
    private readonly long[] _lazy;
    private readonly int _n;
    private readonly bool _hasLazy;

    /// <param name="n">元素数量</param>
    /// <param name="enableLazy">是否启用懒惰传播（支持区间修改）</param>
    public SegmentTree(int n, bool enableLazy = false)
    {
        if (n <= 0) throw new ArgumentOutOfRangeException(nameof(n));
        _n = n;
        _tree = new long[4 * n];
        _lazy = enableLazy ? new long[4 * n] : Array.Empty<long>();
        _hasLazy = enableLazy;
    }

    /// <summary>
    /// 用数组构建线段树。O(n)。
    /// </summary>
    public SegmentTree(int[] nums, bool enableLazy = false) : this(nums.Length, enableLazy)
    {
        Build(nums, 1, 0, _n - 1);
    }

    /// <summary>
    /// 查询区间和 [l, r]（0-based）。O(log n)。
    /// </summary>
    public long Query(int l, int r)
    {
        if (l < 0 || r >= _n || l > r)
            throw new ArgumentOutOfRangeException();
        return Query(1, 0, _n - 1, l, r);
    }

    /// <summary>
    /// 单点更新 — 将 index 的值设为 value。O(log n)。
    /// </summary>
    public void Update(int index, long value)
    {
        if (index < 0 || index >= _n)
            throw new ArgumentOutOfRangeException(nameof(index));
        UpdatePoint(1, 0, _n - 1, index, value);
    }

    /// <summary>
    /// 区间更新 — 将 [l, r] 中每个值增加 delta（需要 enableLazy=true）。O(log n)。
    /// </summary>
    public void UpdateRange(int l, int r, long delta)
    {
        if (!_hasLazy)
            throw new InvalidOperationException("Lazy propagation is not enabled.");
        if (l < 0 || r >= _n || l > r)
            throw new ArgumentOutOfRangeException();
        UpdateRange(1, 0, _n - 1, l, r, delta);
    }

    private void Build(int[] nums, int node, int start, int end)
    {
        if (start == end)
        {
            _tree[node] = nums[start];
            return;
        }
        int mid = (start + end) / 2;
        Build(nums, node * 2, start, mid);
        Build(nums, node * 2 + 1, mid + 1, end);
        _tree[node] = _tree[node * 2] + _tree[node * 2 + 1];
    }

    private long Query(int node, int start, int end, int l, int r)
    {
        if (_hasLazy && _lazy[node] != 0)
            Propagate(node, start, end);

        if (l > end || r < start) return 0;
        if (l <= start && end <= r) return _tree[node];

        int mid = (start + end) / 2;
        return Query(node * 2, start, mid, l, r)
             + Query(node * 2 + 1, mid + 1, end, l, r);
    }

    private void UpdatePoint(int node, int start, int end, int index, long value)
    {
        if (start == end)
        {
            _tree[node] = value;
            return;
        }
        int mid = (start + end) / 2;
        if (index <= mid)
            UpdatePoint(node * 2, start, mid, index, value);
        else
            UpdatePoint(node * 2 + 1, mid + 1, end, index, value);
        _tree[node] = _tree[node * 2] + _tree[node * 2 + 1];
    }

    private void UpdateRange(int node, int start, int end, int l, int r, long delta)
    {
        if (_lazy[node] != 0)
            Propagate(node, start, end);

        if (l > end || r < start) return;
        if (l <= start && end <= r)
        {
            _tree[node] += delta * (end - start + 1);
            if (start != end)
            {
                _lazy[node * 2] += delta;
                _lazy[node * 2 + 1] += delta;
            }
            return;
        }

        int mid = (start + end) / 2;
        UpdateRange(node * 2, start, mid, l, r, delta);
        UpdateRange(node * 2 + 1, mid + 1, end, l, r, delta);
        _tree[node] = _tree[node * 2] + _tree[node * 2 + 1];
    }

    private void Propagate(int node, int start, int end)
    {
        long pending = _lazy[node];
        if (start != end)
        {
            _lazy[node * 2] += pending;
            _lazy[node * 2 + 1] += pending;
        }
        _tree[node] += pending * (end - start + 1);
        _lazy[node] = 0;
    }
}
