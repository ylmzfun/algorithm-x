type Point = [number, number];

// 线段相交检测
export function segmentsIntersect(
  a: Point, b: Point, c: Point, d: Point,
): boolean {
  function cross(o: Point, p: Point, q: Point): number {
    return (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0]);
  }

  const d1 = cross(a, b, c);
  const d2 = cross(a, b, d);
  const d3 = cross(c, d, a);
  const d4 = cross(c, d, b);

  if (d1 === 0 && d2 === 0 && d3 === 0 && d4 === 0) {
    // 共线，检查投影重叠
    return (
      Math.min(a[0], b[0]) <= Math.max(c[0], d[0]) &&
      Math.min(c[0], d[0]) <= Math.max(a[0], b[0]) &&
      Math.min(a[1], b[1]) <= Math.max(c[1], d[1]) &&
      Math.min(c[1], d[1]) <= Math.max(a[1], b[1])
    );
  }

  return d1 * d2 <= 0 && d3 * d4 <= 0;
}

// Graham 扫描凸包
export function convexHull(points: Point[]): Point[] {
  if (points.length <= 3) return points;

  // 找最左下点
  let pivot = points[0];
  for (const p of points) {
    if (p[1] < pivot[1] || (p[1] === pivot[1] && p[0] < pivot[0])) pivot = p;
  }

  function cross(o: Point, a: Point, b: Point): number {
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
  }

  function dist(o: Point, p: Point): number {
    return (p[0] - o[0]) ** 2 + (p[1] - o[1]) ** 2;
  }

  // 极角排序
  const sorted = points
    .filter((p) => p !== pivot)
    .sort((a, b) => {
      const c = cross(pivot, a, b);
      if (c !== 0) return -c; // 逆时针
      return dist(pivot, a) - dist(pivot, b);
    });

  // Graham 扫描
  const hull: Point[] = [pivot, sorted[0]];
  for (let i = 1; i < sorted.length; i++) {
    while (
      hull.length >= 2 &&
      cross(hull[hull.length - 2], hull[hull.length - 1], sorted[i]) <= 0
    ) {
      hull.pop();
    }
    hull.push(sorted[i]);
  }
  return hull;
}

// 点到线段的最短距离
export function pointToSegmentDist(p: Point, a: Point, b: Point): number {
  const abx = b[0] - a[0];
  const aby = b[1] - a[1];
  const apx = p[0] - a[0];
  const apy = p[1] - a[1];
  const lenSq = abx * abx + aby * aby;
  if (lenSq === 0) return Math.hypot(apx, apy);

  let t = (apx * abx + apy * aby) / lenSq;
  t = Math.max(0, Math.min(1, t));
  const dx = apx - t * abx;
  const dy = apy - t * aby;
  return Math.hypot(dx, dy);
}

// 多边形面积
export function polygonArea(vertices: Point[]): number {
  let area = 0;
  const n = vertices.length;
  for (let i = 0; i < n; i++) {
    const j = (i + 1) % n;
    area += vertices[i][0] * vertices[j][1];
    area -= vertices[j][0] * vertices[i][1];
  }
  return Math.abs(area) / 2;
}

// 点在多边形内部判断（射线法）
export function pointInPolygon(p: Point, polygon: Point[]): boolean {
  let inside = false;
  const n = polygon.length;
  for (let i = 0, j = n - 1; i < n; j = i++) {
    const xi = polygon[i][0], yi = polygon[i][1];
    const xj = polygon[j][0], yj = polygon[j][1];
    if (
      yi > p[1] !== yj > p[1] &&
      p[0] < ((xj - xi) * (p[1] - yi)) / (yj - yi) + xi
    ) {
      inside = !inside;
    }
  }
  return inside;
}
