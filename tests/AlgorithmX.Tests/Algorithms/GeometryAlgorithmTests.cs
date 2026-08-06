namespace AlgorithmX.Tests.Algorithms;

public class GeometryAlgorithmTests
{
    [Fact]
    public void Cross_ShouldHandleClockwiseAndCounterClockwise()
    {
        var p1 = new AlgorithmX.Algorithms.Geometry.Point(0, 0);
        var p2 = new AlgorithmX.Algorithms.Geometry.Point(1, 0);
        var p3 = new AlgorithmX.Algorithms.Geometry.Point(0, 1);
        Assert.True(AlgorithmX.Algorithms.Geometry.GeometryAlgorithm.Cross(p1, p2, p3) > 0); // 逆时针
    }

    [Fact]
    public void DistanceSquared_ShouldBeCorrect()
    {
        var a = new AlgorithmX.Algorithms.Geometry.Point(0, 0);
        var b = new AlgorithmX.Algorithms.Geometry.Point(3, 4);
        Assert.Equal(25, AlgorithmX.Algorithms.Geometry.GeometryAlgorithm.DistanceSquared(a, b));
    }

    [Fact]
    public void ConvexHull_ShouldReturnCorrectHull()
    {
        var points = new[]
        {
            new AlgorithmX.Algorithms.Geometry.Point(0, 0),
            new AlgorithmX.Algorithms.Geometry.Point(1, 1),
            new AlgorithmX.Algorithms.Geometry.Point(2, 2),
            new AlgorithmX.Algorithms.Geometry.Point(0, 2),
            new AlgorithmX.Algorithms.Geometry.Point(2, 0),
            new AlgorithmX.Algorithms.Geometry.Point(1, 0)
        };
        var hull = AlgorithmX.Algorithms.Geometry.GeometryAlgorithm.ConvexHull(points);
        Assert.Equal(4, hull.Count); // 正方形四个角
    }

    [Fact]
    public void PointToLineDistance_ShouldBeCorrect()
    {
        var p = new AlgorithmX.Algorithms.Geometry.Point(0, 1);
        var p1 = new AlgorithmX.Algorithms.Geometry.Point(0, 0);
        var p2 = new AlgorithmX.Algorithms.Geometry.Point(1, 0);
        Assert.Equal(1.0, AlgorithmX.Algorithms.Geometry.GeometryAlgorithm.PointToLineDistance(p, p1, p2), 10);
    }
}
