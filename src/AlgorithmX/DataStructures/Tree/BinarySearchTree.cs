namespace AlgorithmX.DataStructures.Tree;

/// <summary>
/// 二叉搜索树 (BST) 实现。
/// 左子树所有节点 &lt; 根 &lt; 右子树所有节点。
/// 平均 O(log n)，最坏 O(n)（退化为链表）。
/// </summary>
public class BinarySearchTree<T> where T : IComparable<T>
{
    private BinaryTreeNode<T>? _root;
    private int _size;

    public int Count => _size;
    public bool IsEmpty => _size == 0;
    public BinaryTreeNode<T>? Root => _root;

    /// <summary>
    /// 插入值。O(log n) 平均。
    /// </summary>
    public void Insert(T value)
    {
        _root = Insert(_root, value);
    }

    private BinaryTreeNode<T> Insert(BinaryTreeNode<T>? node, T value)
    {
        if (node == null)
        {
            _size++;
            return new BinaryTreeNode<T>(value);
        }

        int cmp = value.CompareTo(node.Value);
        if (cmp < 0)
            node.Left = Insert(node.Left, value);
        else if (cmp > 0)
            node.Right = Insert(node.Right, value);
        // 相等时不插入（或可更新，此处选择忽略）

        return node;
    }

    /// <summary>
    /// 查找值是否存在。O(log n) 平均。
    /// </summary>
    public bool Contains(T value)
    {
        var node = _root;
        while (node != null)
        {
            int cmp = value.CompareTo(node.Value);
            if (cmp == 0) return true;
            node = cmp < 0 ? node.Left : node.Right;
        }
        return false;
    }

    /// <summary>
    /// 查找最小值。O(log n) 平均。
    /// </summary>
    public T? Min()
    {
        if (_root == null) return default;
        var node = _root;
        while (node.Left != null)
            node = node.Left;
        return node.Value;
    }

    /// <summary>
    /// 查找最大值。O(log n) 平均。
    /// </summary>
    public T? Max()
    {
        if (_root == null) return default;
        var node = _root;
        while (node.Right != null)
            node = node.Right;
        return node.Value;
    }

    /// <summary>
    /// 删除节点。O(log n) 平均。
    /// </summary>
    public bool Remove(T value)
    {
        int oldSize = _size;
        _root = Remove(_root, value);
        return _size < oldSize;
    }

    private BinaryTreeNode<T>? Remove(BinaryTreeNode<T>? node, T value)
    {
        if (node == null) return null;

        int cmp = value.CompareTo(node.Value);
        if (cmp < 0)
        {
            node.Left = Remove(node.Left, value);
        }
        else if (cmp > 0)
        {
            node.Right = Remove(node.Right, value);
        }
        else
        {
            // 找到了要删除的节点
            if (node.Left == null)
            {
                _size--;
                return node.Right;
            }
            if (node.Right == null)
            {
                _size--;
                return node.Left;
            }

            // 有两个子节点：用后继节点（右子树最小节点）替换
            var successor = FindMin(node.Right);
            node.Value = successor.Value;
            node.Right = Remove(node.Right, successor.Value);
        }
        return node;
    }

    /// <summary>
    /// 验证是否为合法 BST。
    /// </summary>
    public bool IsValidBst()
    {
#pragma warning disable CS8604 // hasMin/hasMax 控制比较，default 值不会被使用
        return IsValidBst(_root, default, default, false, false);
#pragma warning restore CS8604
    }

    private bool IsValidBst(BinaryTreeNode<T>? node, T min, T max, bool hasMin, bool hasMax)
    {
        if (node == null) return true;

        if (hasMin && node.Value.CompareTo(min) <= 0) return false;
        if (hasMax && node.Value.CompareTo(max) >= 0) return false;

        return IsValidBst(node.Left, min, node.Value, hasMin, true)
            && IsValidBst(node.Right, node.Value, max, true, hasMax);
    }

    /// <summary>
    /// 中序遍历（升序序列）。
    /// </summary>
    public IEnumerable<T> Inorder()
    {
        var result = new List<T>();
        Inorder(_root, result);
        return result;
    }

    private void Inorder(BinaryTreeNode<T>? node, List<T> result)
    {
        if (node == null) return;
        Inorder(node.Left, result);
        result.Add(node.Value);
        Inorder(node.Right, result);
    }

    private BinaryTreeNode<T> FindMin(BinaryTreeNode<T> node)
    {
        while (node.Left != null)
            node = node.Left;
        return node;
    }
}
