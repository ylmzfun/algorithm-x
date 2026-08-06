namespace AlgorithmX.DataStructures.Tree;

/// <summary>
/// 二叉树节点。
/// </summary>
public class BinaryTreeNode<T>
{
    public T Value { get; set; }
    public BinaryTreeNode<T>? Left { get; set; }
    public BinaryTreeNode<T>? Right { get; set; }

    public BinaryTreeNode(T value, BinaryTreeNode<T>? left = null, BinaryTreeNode<T>? right = null)
    {
        Value = value;
        Left = left;
        Right = right;
    }
}

/// <summary>
/// 二叉树实现 — 支持构建、四种遍历（前序/中序/后序/层序）、高度计算。
/// </summary>
public class BinaryTree<T>
{
    public BinaryTreeNode<T>? Root { get; private set; }

    public BinaryTree(BinaryTreeNode<T>? root = null)
    {
        Root = root;
    }

    // ─── 递归遍历 ─────────────────────────

    /// <summary>
    /// 前序遍历：根 → 左 → 右
    /// </summary>
    public IEnumerable<T> Preorder()
    {
        var result = new List<T>();
        Preorder(Root, result);
        return result;
    }

    private void Preorder(BinaryTreeNode<T>? node, List<T> result)
    {
        if (node == null) return;
        result.Add(node.Value);
        Preorder(node.Left, result);
        Preorder(node.Right, result);
    }

    /// <summary>
    /// 中序遍历：左 → 根 → 右（BST 中序遍历结果为有序序列）
    /// </summary>
    public IEnumerable<T> Inorder()
    {
        var result = new List<T>();
        Inorder(Root, result);
        return result;
    }

    private void Inorder(BinaryTreeNode<T>? node, List<T> result)
    {
        if (node == null) return;
        Inorder(node.Left, result);
        result.Add(node.Value);
        Inorder(node.Right, result);
    }

    /// <summary>
    /// 后序遍历：左 → 右 → 根
    /// </summary>
    public IEnumerable<T> Postorder()
    {
        var result = new List<T>();
        Postorder(Root, result);
        return result;
    }

    private void Postorder(BinaryTreeNode<T>? node, List<T> result)
    {
        if (node == null) return;
        Postorder(node.Left, result);
        Postorder(node.Right, result);
        result.Add(node.Value);
    }

    /// <summary>
    /// 层序遍历（BFS）。O(n)。
    /// </summary>
    public IEnumerable<T> LevelOrder()
    {
        var result = new List<T>();
        if (Root == null) return result;

        var queue = new Queue<BinaryTreeNode<T>>();
        queue.Enqueue(Root);

        while (queue.Count > 0)
        {
            var node = queue.Dequeue();
            result.Add(node.Value);
            if (node.Left != null) queue.Enqueue(node.Left);
            if (node.Right != null) queue.Enqueue(node.Right);
        }
        return result;
    }

    /// <summary>
    /// 层序遍历，按层分组返回。
    /// </summary>
    public IEnumerable<IList<T>> LevelOrderByLevel()
    {
        var result = new List<IList<T>>();
        if (Root == null) return result;

        var queue = new Queue<BinaryTreeNode<T>>();
        queue.Enqueue(Root);

        while (queue.Count > 0)
        {
            int size = queue.Count;
            var level = new List<T>();
            for (int i = 0; i < size; i++)
            {
                var node = queue.Dequeue();
                level.Add(node.Value);
                if (node.Left != null) queue.Enqueue(node.Left);
                if (node.Right != null) queue.Enqueue(node.Right);
            }
            result.Add(level);
        }
        return result;
    }

    // ─── 迭代遍历（栈） ─────────────────────

    /// <summary>
    /// 迭代前序遍历。
    /// </summary>
    public IEnumerable<T> PreorderIterative()
    {
        var result = new List<T>();
        if (Root == null) return result;

        var stack = new Stack<BinaryTreeNode<T>>();
        stack.Push(Root);

        while (stack.Count > 0)
        {
            var node = stack.Pop();
            result.Add(node.Value);
            if (node.Right != null) stack.Push(node.Right);
            if (node.Left != null) stack.Push(node.Left);
        }
        return result;
    }

    /// <summary>
    /// 迭代中序遍历。
    /// </summary>
    public IEnumerable<T> InorderIterative()
    {
        var result = new List<T>();
        var stack = new Stack<BinaryTreeNode<T>>();
        var current = Root;

        while (current != null || stack.Count > 0)
        {
            while (current != null)
            {
                stack.Push(current);
                current = current.Left;
            }
            current = stack.Pop();
            result.Add(current.Value);
            current = current.Right;
        }
        return result;
    }

    // ─── 属性计算 ─────────────────────────

    /// <summary>
    /// 树的高度（从根到最远叶子的边数）。空树高度为 -1。
    /// </summary>
    public int Height() => Height(Root);

    private int Height(BinaryTreeNode<T>? node)
    {
        if (node == null) return -1;
        return 1 + Math.Max(Height(node.Left), Height(node.Right));
    }

    /// <summary>
    /// 节点总数。O(n)。
    /// </summary>
    public int Count()
    {
        int count = 0;
        CountNodes(Root, ref count);
        return count;
    }

    private void CountNodes(BinaryTreeNode<T>? node, ref int count)
    {
        if (node == null) return;
        count++;
        CountNodes(node.Left, ref count);
        CountNodes(node.Right, ref count);
    }

    /// <summary>
    /// 叶子节点数量。
    /// </summary>
    public int LeafCount()
    {
        int count = 0;
        CountLeaves(Root, ref count);
        return count;
    }

    private void CountLeaves(BinaryTreeNode<T>? node, ref int count)
    {
        if (node == null) return;
        if (node.Left == null && node.Right == null)
        {
            count++;
            return;
        }
        CountLeaves(node.Left, ref count);
        CountLeaves(node.Right, ref count);
    }
}
