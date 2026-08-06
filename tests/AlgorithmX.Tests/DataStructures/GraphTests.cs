namespace AlgorithmX.Tests.DataStructures;

public class GraphTests
{
    [Fact]
    public void AddVertex_ShouldAddIsolatedVertex()
    {
        var graph = new AlgorithmX.DataStructures.Graph.Graph<int>();
        graph.AddVertex(1);
        Assert.Equal(1, graph.VertexCount);
        Assert.Empty(graph.GetNeighbors(1));
    }

    [Fact]
    public void AddEdge_Undirected_ShouldAddBothDirections()
    {
        var graph = new AlgorithmX.DataStructures.Graph.Graph<int>();
        graph.AddEdge(1, 2);
        Assert.Contains(2, graph.GetNeighbors(1));
        Assert.Contains(1, graph.GetNeighbors(2));
        Assert.Equal(1, graph.EdgeCount); // 无向图只算一条
    }

    [Fact]
    public void AddEdge_Directed_ShouldAddOneDirection()
    {
        var graph = new AlgorithmX.DataStructures.Graph.Graph<int>(isDirected: true);
        graph.AddEdge(1, 2);
        Assert.Contains(2, graph.GetNeighbors(1));
        Assert.DoesNotContain(1, graph.GetNeighbors(2));
    }

    [Fact]
    public void Bfs_ShouldTraverseInBfsOrder()
    {
        //  1 -- 2 -- 4
        //  |    |
        //  3 -- 5
        var graph = new AlgorithmX.DataStructures.Graph.Graph<int>();
        graph.AddEdge(1, 2);
        graph.AddEdge(1, 3);
        graph.AddEdge(2, 4);
        graph.AddEdge(2, 5);
        graph.AddEdge(3, 5);

        var bfs = graph.Bfs(1).ToList();
        Assert.Equal(1, bfs[0]);
        Assert.Equal(new[] { 2, 3 }, bfs.GetRange(1, 2).OrderBy(x => x));
    }

    [Fact]
    public void Dfs_ShouldVisitAllReachableVertices()
    {
        var graph = new AlgorithmX.DataStructures.Graph.Graph<int>();
        graph.AddEdge(1, 2);
        graph.AddEdge(2, 3);
        graph.AddEdge(3, 4);

        var dfs = graph.Dfs(1).ToList();
        Assert.Equal(4, dfs.Count);
        Assert.Equal(new[] { 1, 2, 3, 4 }, dfs);
    }

    [Fact]
    public void ShortestPathLength_ShouldReturnCorrectDistance()
    {
        var graph = new AlgorithmX.DataStructures.Graph.Graph<int>();
        graph.AddEdge(1, 2);
        graph.AddEdge(2, 3);
        graph.AddEdge(3, 4);
        graph.AddEdge(1, 3);

        Assert.Equal(1, graph.ShortestPathLength(1, 3));
        Assert.Equal(2, graph.ShortestPathLength(1, 4));
        Assert.Equal(-1, graph.ShortestPathLength(1, 99));
    }

    [Fact]
    public void ConnectedComponents_ShouldCountCorrectly()
    {
        var graph = new AlgorithmX.DataStructures.Graph.Graph<int>();
        graph.AddEdge(1, 2);
        graph.AddEdge(3, 4);
        graph.AddEdge(5, 6);
        graph.AddEdge(5, 7);

        Assert.Equal(3, graph.ConnectedComponents());
    }

    [Fact]
    public void TopologicalSort_ShouldReturnValidOrder()
    {
        // DAG: 1 -> 2 -> 4, 1 -> 3 -> 4
        var graph = new AlgorithmX.DataStructures.Graph.Graph<int>(isDirected: true);
        graph.AddEdge(1, 2);
        graph.AddEdge(1, 3);
        graph.AddEdge(2, 4);
        graph.AddEdge(3, 4);

        var sorted = graph.TopologicalSort().ToList();
        Assert.Equal(4, sorted.Count);
        Assert.Equal(1, sorted[0]);
        Assert.Equal(4, sorted[^1]);
    }
}
