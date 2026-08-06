namespace AlgorithmX.Algorithms.Geometry;

/// <summary>
/// 二维点结构。
/// </summary>
public struct Point : IEquatable<Point>
{
    public long X { get; }
    public long Y { get; }

    public Point(long x, long y) { X = x; Y = y; }

    public static Point operator -(Point a, Point b) => new(a.X - b.X, a.Y - b.Y);
    public static Point operator +(Point a, Point b) => new(a.X + b.X, a.Y + b.Y);

    public bool Equals(Point other) => X == other.X && Y == other.Y;
    public override bool Equals(object? obj) => obj is Point p && Equals(p);
    public override int GetHashCode() => HashCode.Combine(X, Y);
    public override string ToString() => $"({X}, {Y})";
}

/// <summary>
/// 计算几何基础算法。
/// </summary>
public static class GeometryAlgorithm
{
    /// <summary>
    /// 向量叉积 — p1p2 × p1p3。
    /// > 0: p3 在 p1p2 左侧（逆时针）
    /// = 0: 三点共线
    /// &lt; 0: p3 在 p1p2 右侧（顺时针）
    /// </summary>
    public static long Cross(Point p1, Point p2, Point p3)
    {
        return (p2.X - p1.X) * (p3.Y - p1.Y) - (p2.Y - p1.Y) * (p3.X - p1.X);
    }

    /// <summary>
    /// 点积。
    /// </summary>
    public static long Dot(Point p1, Point p2, Point p3)
    {
        return (p2.X - p1.X) * (p3.X - p1.X) + (p2.Y - p1.Y) * (p3.Y - p1.Y);
    }

    /// <summary>
    /// 两点间欧几里得距离的平方。
    /// </summary>
    public static long DistanceSquared(Point a, Point b)
    {
        long dx = a.X - b.X, dy = a.Y - b.Y;
        return dx * dx + dy * dy;
    }

    /// <summary>
    /// 两点间欧几里得距离。
    /// </summary>
    public static double Distance(Point a, Point b) => Math.Sqrt(DistanceSquared(a, b));

    /// <summary>
    /// 点到直线的距离。直线由 p1, p2 确定。
    /// </summary>
    public static double PointToLineDistance(Point p, Point p1, Point p2)
    {
        return Math.Abs(Cross(p1, p2, p)) / Distance(p1, p2);
    }

    // ═══════════════════════════════════════════
    // 凸包 — Andrew (Monotone Chain) 算法
    // ═══════════════════════════════════════════

    /// <summary>
    /// Andrew 算法求二维凸包。O(n log n)。
    /// 返回凸包顶点（逆时针排列，不包含共线点）。
    /// </summary>
    public static IList<Point> ConvexHull(Point[] points)
    {
        if (points.Length <= 2) return new List<Point>(points);

        Array.Sort(points, (a, b) =>
        {
            int cmp = a.X.CompareTo(b.X);
            return cmp != 0 ? cmp : a.Y.CompareTo(b.Y);
        });

        var lower = new List<Point>();
        foreach (var p in points)
        {
            while (lower.Count >= 2 && Cross(lower[^2], lower[^1], p) <= 0)
                lower.RemoveAt(lower.Count - 1);
            lower.Add(p);
        }

        var upper = new List<Point>();
        for (int i = points.Length - 1; i >= 0; i--)
        {
            var p = points[i];
            while (upper.Count >= 2 && Cross(upper[^2], upper[^1], p) <= 0)
                upper.RemoveAt(upper.Count - 1);
            upper.Add(p);
        }

        lower.RemoveAt(lower.Count - 1);
        upper.RemoveAt(upper.Count - 1);
        lower.AddRange(upper);
        return lower;
    }
}
