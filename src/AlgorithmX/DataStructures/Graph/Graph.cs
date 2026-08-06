namespace AlgorithmX.DataStructures.Graph;

/// <summary>
/// 图的邻接表表示。
/// 支持有向图和无向图，带权或不带权。
/// </summary>
public class Graph<T> where T : notnull
{
    private readonly Dictionary<T, List<Edge<T>>> _adjacencyList;
    private readonly bool _isDirected;

    public Graph(bool isDirected = false)
    {
        _adjacencyList = new Dictionary<T, List<Edge<T>>>();
        _isDirected = isDirected;
    }

    public int VertexCount => _adjacencyList.Count;
    public int EdgeCount { get; private set; }
    public bool IsDirected => _isDirected;
    public IEnumerable<T> Vertices => _adjacencyList.Keys;

    /// <summary>
    /// 添加顶点。
    /// </summary>
    public void AddVertex(T vertex)
    {
        if (!_adjacencyList.ContainsKey(vertex))
            _adjacencyList[vertex] = new List<Edge<T>>();
    }

    /// <summary>
    /// 添加边（无权，权重默认 = 1）。
    /// </summary>
    public void AddEdge(T from, T to, double weight = 1.0)
    {
        AddVertex(from);
        AddVertex(to);
        _adjacencyList[from].Add(new Edge<T>(from, to, weight));
        EdgeCount++;

        if (!_isDirected)
        {
            _adjacencyList[to].Add(new Edge<T>(to, from, weight));
        }
    }

    /// <summary>
    /// 获取顶点的所有邻边。
    /// </summary>
    public IEnumerable<Edge<T>> GetEdges(T vertex)
    {
        return _adjacencyList.TryGetValue(vertex, out var edges)
            ? edges
            : Enumerable.Empty<Edge<T>>();
    }

    /// <summary>
    /// 获取顶点的所有邻居。
    /// </summary>
    public IEnumerable<T> GetNeighbors(T vertex)
    {
        return GetEdges(vertex).Select(e => e.To);
    }

    /// <summary>
    /// 广度优先搜索 (BFS)。返回遍历顺序。
    /// </summary>
    public IEnumerable<T> Bfs(T start)
    {
        if (!_adjacencyList.ContainsKey(start))
            throw new ArgumentException($"Vertex '{start}' not found.");

        var visited = new HashSet<T>();
        var queue = new Queue<T>();
        var result = new List<T>();

        visited.Add(start);
        queue.Enqueue(start);

        while (queue.Count > 0)
        {
            var current = queue.Dequeue();
            result.Add(current);

            foreach (var neighbor in GetNeighbors(current))
            {
                if (!visited.Contains(neighbor))
                {
                    visited.Add(neighbor);
                    queue.Enqueue(neighbor);
                }
            }
        }
        return result;
    }

    /// <summary>
    /// 深度优先搜索 (DFS)。返回遍历顺序。
    /// </summary>
    public IEnumerable<T> Dfs(T start)
    {
        if (!_adjacencyList.ContainsKey(start))
            throw new ArgumentException($"Vertex '{start}' not found.");

        var visited = new HashSet<T>();
        var result = new List<T>();
        DfsRecursive(start, visited, result);
        return result;
    }

    private void DfsRecursive(T current, HashSet<T> visited, List<T> result)
    {
        visited.Add(current);
        result.Add(current);

        foreach (var neighbor in GetNeighbors(current))
        {
            if (!visited.Contains(neighbor))
                DfsRecursive(neighbor, visited, result);
        }
    }

    /// <summary>
    /// 迭代 DFS（使用栈，模拟递归顺序）。
    /// </summary>
    public IEnumerable<T> DfsIterative(T start)
    {
        if (!_adjacencyList.ContainsKey(start))
            throw new ArgumentException($"Vertex '{start}' not found.");

        var visited = new HashSet<T>();
        var stack = new Stack<T>();
        var result = new List<T>();

        stack.Push(start);

        while (stack.Count > 0)
        {
            var current = stack.Pop();
            if (!visited.Add(current)) continue;

            result.Add(current);

            // 逆序入栈以保证与递归顺序一致
            foreach (var neighbor in GetNeighbors(current).Reverse())
            {
                if (!visited.Contains(neighbor))
                    stack.Push(neighbor);
            }
        }
        return result;
    }

    /// <summary>
    /// BFS 求无权图最短路径长度（边数）。返回 -1 表示不可达。
    /// </summary>
    public int ShortestPathLength(T start, T target)
    {
        if (!_adjacencyList.ContainsKey(start) || !_adjacencyList.ContainsKey(target))
            return -1;

        var visited = new HashSet<T>();
        var queue = new Queue<(T vertex, int distance)>();
        visited.Add(start);
        queue.Enqueue((start, 0));

        while (queue.Count > 0)
        {
            var (current, dist) = queue.Dequeue();
            if (EqualityComparer<T>.Default.Equals(current, target))
                return dist;

            foreach (var neighbor in GetNeighbors(current))
            {
                if (!visited.Contains(neighbor))
                {
                    visited.Add(neighbor);
                    queue.Enqueue((neighbor, dist + 1));
                }
            }
        }
        return -1;
    }

    /// <summary>
    /// 计算连通分量数量（仅无向图）。
    /// </summary>
    public int ConnectedComponents()
    {
        int components = 0;
        var visited = new HashSet<T>();

        foreach (var vertex in Vertices)
        {
            if (!visited.Contains(vertex))
            {
                components++;
                DfsRecursive(vertex, visited, new List<T>()); // 仅标记 visited
            }
        }
        return components;
    }

    /// <summary>
    /// 拓扑排序（Kahn 算法，仅适用于有向无环图 DAG）。返回空表示存在环。
    /// </summary>
    public IEnumerable<T> TopologicalSort()
    {
        if (!_isDirected)
            throw new InvalidOperationException("Topological sort requires a directed graph.");

        var inDegree = new Dictionary<T, int>();
        foreach (var v in Vertices)
            inDegree[v] = 0;
        foreach (var v in Vertices)
            foreach (var e in GetEdges(v))
                inDegree[e.To]++;

        var queue = new Queue<T>();
        foreach (var kv in inDegree)
            if (kv.Value == 0)
                queue.Enqueue(kv.Key);

        var sorted = new List<T>();
        while (queue.Count > 0)
        {
            var current = queue.Dequeue();
            sorted.Add(current);
            foreach (var neighbor in GetNeighbors(current))
            {
                inDegree[neighbor]--;
                if (inDegree[neighbor] == 0)
                    queue.Enqueue(neighbor);
            }
        }
        return sorted.Count == VertexCount ? sorted : Enumerable.Empty<T>();
    }
}

/// <summary>
/// 图的边。
/// </summary>
public class Edge<T>
{
    public T From { get; }
    public T To { get; }
    public double Weight { get; }

    public Edge(T from, T to, double weight = 1.0)
    {
        From = from;
        To = to;
        Weight = weight;
    }

    public override string ToString() => $"{From} --({Weight})--> {To}";
}
