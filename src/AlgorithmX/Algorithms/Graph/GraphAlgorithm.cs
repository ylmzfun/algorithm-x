namespace AlgorithmX.Algorithms.Graph;

/// <summary>
/// 图论经典算法：最短路、最小生成树。
/// </summary>
public static class GraphAlgorithm
{
    // ═══════════════════════════════════════════
    // Dijkstra — 单源最短路（非负权）
    // ═══════════════════════════════════════════

    /// <summary>
    /// Dijkstra 算法。O((V+E) log V)
    /// </summary>
    /// <returns>从 start 到所有节点的最短距离。不可达为 -1。</returns>
    public static int[] Dijkstra(int n, int[][][] graph, int start)
    {
        // graph[u] = [[v1, w1], [v2, w2], ...]
        var dist = new int[n];
        Array.Fill(dist, int.MaxValue);
        dist[start] = 0;

        var pq = new PriorityQueue<int, int>();
        pq.Enqueue(start, 0);

        while (pq.Count > 0)
        {
            int u = pq.Dequeue();
            if (graph[u] == null) continue;

            foreach (var edge in graph[u])
            {
                int v = edge[0], w = edge[1];
                if (dist[u] + w < dist[v])
                {
                    dist[v] = dist[u] + w;
                    pq.Enqueue(v, dist[v]);
                }
            }
        }
        for (int i = 0; i < n; i++)
            if (dist[i] == int.MaxValue) dist[i] = -1;
        return dist;
    }

    // ═══════════════════════════════════════════
    // Bellman-Ford — 单源最短路（可处理负权边）
    // ═══════════════════════════════════════════

    /// <summary>
    /// Bellman-Ford 算法。O(V·E)。返回 (dist, hasNegativeCycle)。
    /// </summary>
    public static (int[] dist, bool hasNegativeCycle) BellmanFord(int n, int[][] edges, int start)
    {
        // edges = [[u, v, w], ...]
        var dist = new int[n];
        Array.Fill(dist, int.MaxValue);
        dist[start] = 0;

        for (int i = 0; i < n - 1; i++)
        {
            bool updated = false;
            foreach (var edge in edges)
            {
                int u = edge[0], v = edge[1], w = edge[2];
                if (dist[u] != int.MaxValue && dist[u] + w < dist[v])
                {
                    dist[v] = dist[u] + w;
                    updated = true;
                }
            }
            if (!updated) break;
        }

        // 检测负环
        bool hasNegativeCycle = false;
        foreach (var edge in edges)
        {
            int u = edge[0], v = edge[1], w = edge[2];
            if (dist[u] != int.MaxValue && dist[u] + w < dist[v])
            {
                hasNegativeCycle = true;
                break;
            }
        }
        return (dist, hasNegativeCycle);
    }

    // ═══════════════════════════════════════════
    // Floyd-Warshall — 全源最短路
    // ═══════════════════════════════════════════

    /// <summary>
    /// Floyd-Warshall 算法求全源最短路。O(V³)。
    /// 不可达记为 INF（int.MaxValue / 2 防止溢出）。
    /// </summary>
    public static int[,] FloydWarshall(int n, int[][] edges)
    {
        const int INF = int.MaxValue / 2;
        var dist = new int[n, n];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                dist[i, j] = i == j ? 0 : INF;

        foreach (var edge in edges)
        {
            int u = edge[0], v = edge[1], w = edge[2];
            dist[u, v] = Math.Min(dist[u, v], w);
        }

        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (dist[i, k] < INF && dist[k, j] < INF)
                        dist[i, j] = Math.Min(dist[i, j], dist[i, k] + dist[k, j]);

        return dist;
    }

    // ═══════════════════════════════════════════
    // Kruskal — 最小生成树
    // ═══════════════════════════════════════════

    /// <summary>
    /// Kruskal 算法求最小生成树边权和。O(E log E)。
    /// edges = [[u, v, w], ...]。
    /// </summary>
    public static int KruskalMst(int n, int[][] edges)
    {
        Array.Sort(edges, (a, b) => a[2].CompareTo(b[2]));
        var uf = new DataStructures.DisjointSet.UnionFind(n);
        int cost = 0;
        int edgesUsed = 0;

        foreach (var edge in edges)
        {
            int u = edge[0], v = edge[1], w = edge[2];
            if (uf.Union(u, v))
            {
                cost += w;
                edgesUsed++;
                if (edgesUsed == n - 1) break;
            }
        }
        return cost;
    }

    // ═══════════════════════════════════════════
    // Prim — 最小生成树
    // ═══════════════════════════════════════════

    /// <summary>
    /// Prim 算法求最小生成树边权和（邻接矩阵）。O(V²)。
    /// </summary>
    public static int PrimMst(int[][] graph)
    {
        // graph[i][j] = 边权，graph[i][j] = 0 表示不连通
        int n = graph.Length;
        var visited = new bool[n];
        var minEdge = new int[n];
        Array.Fill(minEdge, int.MaxValue);
        minEdge[0] = 0;

        int cost = 0;
        for (int i = 0; i < n; i++)
        {
            int u = -1;
            for (int j = 0; j < n; j++)
                if (!visited[j] && (u == -1 || minEdge[j] < minEdge[u]))
                    u = j;

            visited[u] = true;
            cost += minEdge[u];

            for (int v = 0; v < n; v++)
                if (graph[u][v] > 0 && !visited[v] && graph[u][v] < minEdge[v])
                    minEdge[v] = graph[u][v];
        }
        return cost;
    }
}
