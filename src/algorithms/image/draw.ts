// Flood Fill (DFS)
export function floodFill(
  img: number[][],
  sr: number,
  sc: number,
  newColor: number,
): number[][] {
  const h = img.length;
  const w = img[0].length;
  const targetColor = img[sr][sc];
  if (targetColor === newColor) return img;

  const result = img.map((row) => [...row]);

  function fill(r: number, c: number) {
    if (r < 0 || r >= h || c < 0 || c >= w) return;
    if (result[r][c] !== targetColor) return;
    result[r][c] = newColor;
    fill(r - 1, c);
    fill(r + 1, c);
    fill(r, c - 1);
    fill(r, c + 1);
  }

  fill(sr, sc);
  return result;
}

// Bresenham 直线 —— 返回直线经过的像素点
export function bresenhamLine(
  x0: number,
  y0: number,
  x1: number,
  y1: number,
): [number, number][] {
  const points: [number, number][] = [];
  const dx = Math.abs(x1 - x0);
  const dy = -Math.abs(y1 - y0);
  const sx = x0 < x1 ? 1 : -1;
  const sy = y0 < y1 ? 1 : -1;
  let err = dx + dy;

  let x = x0;
  let y = y0;

  while (true) {
    points.push([x, y]);
    if (x === x1 && y === y1) break;
    const e2 = 2 * err;
    if (e2 >= dy) {
      if (x === x1) break;
      err += dy;
      x += sx;
    }
    if (e2 <= dx) {
      if (y === y1) break;
      err += dx;
      y += sy;
    }
  }
  return points;
}

// 三次 Bezier 曲线 —— 采样 t ∈ [0, 1]，返回采样点
export function bezierCurve(
  p0: [number, number],
  p1: [number, number],
  p2: [number, number],
  p3: [number, number],
  segments = 50,
): [number, number][] {
  const points: [number, number][] = [];
  for (let i = 0; i <= segments; i++) {
    const t = i / segments;
    const mt = 1 - t;
    const x = mt ** 3 * p0[0] + 3 * mt ** 2 * t * p1[0] + 3 * mt * t ** 2 * p2[0] + t ** 3 * p3[0];
    const y = mt ** 3 * p0[1] + 3 * mt ** 2 * t * p1[1] + 3 * mt * t ** 2 * p2[1] + t ** 3 * p3[1];
    points.push([Math.round(x), Math.round(y)]);
  }
  return points;
}
