namespace AlgorithmX.Tests.Algorithms;

public class GraphAlgorithmTests
{
    [Fact]
    public void Dijkstra_ShouldFindShortestPaths()
    {
        // 图: 0--(1)-->1, 0--(4)-->2, 1--(2)-->2, 1--(5)-->3, 2--(1)-->3
        int n = 4;
        var graph = new int[n][][];
        graph[0] = new[] { new[] { 1, 1 }, new[] { 2, 4 } };
        graph[1] = new[] { new[] { 2, 2 }, new[] { 3, 5 } };
        graph[2] = new[] { new[] { 3, 1 } };
        graph[3] = Array.Empty<int[]>();

        var dist = AlgorithmX.Algorithms.Graph.GraphAlgorithm.Dijkstra(n, graph, 0);
        Assert.Equal(new[] { 0, 1, 3, 4 }, dist);
    }

    [Fact]
    public void BellmanFord_ShouldDetectNegativeCycle()
    {
        int n = 3;
        int[][] edges = { new[] { 0, 1, -1 }, new[] { 1, 2, -2 }, new[] { 2, 0, -3 } };
        var (dist, hasNegCycle) = AlgorithmX.Algorithms.Graph.GraphAlgorithm.BellmanFord(n, edges, 0);
        Assert.True(hasNegCycle);
    }

    [Fact]
    public void FloydWarshall_ShouldFindAllPairsShortest()
    {
        int n = 3;
        int[][] edges = { new[] { 0, 1, 3 }, new[] { 1, 2, 1 }, new[] { 0, 2, 8 } };
        var dist = AlgorithmX.Algorithms.Graph.GraphAlgorithm.FloydWarshall(n, edges);
        Assert.Equal(4, dist[0, 2]); // 0 -> 1 -> 2 = 3+1 = 4
    }

    [Fact]
    public void KruskalMst_ShouldFindMinCost()
    {
        int n = 4;
        int[][] edges =
        {
            new[] { 0, 1, 1 }, new[] { 0, 2, 3 }, new[] { 1, 2, 2 },
            new[] { 1, 3, 4 }, new[] { 2, 3, 1 }
        };
        Assert.Equal(4, AlgorithmX.Algorithms.Graph.GraphAlgorithm.KruskalMst(n, edges));
    }

    [Fact]
    public void PrimMst_ShouldFindMinCost()
    {
        int[][] graph =
        {
            new[] { 0, 2, 0, 6, 0 },
            new[] { 2, 0, 3, 8, 5 },
            new[] { 0, 3, 0, 0, 7 },
            new[] { 6, 8, 0, 0, 9 },
            new[] { 0, 5, 7, 9, 0 }
        };
        Assert.Equal(16, AlgorithmX.Algorithms.Graph.GraphAlgorithm.PrimMst(graph));
    }
}
