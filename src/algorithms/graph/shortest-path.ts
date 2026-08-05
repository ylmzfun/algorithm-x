// Dijkstra
export function dijkstra(
  graph: [number, number, number][], // [from, to, weight]
  n: number,
  start: number,
): number[] {
  const adj: [number, number][][] = Array.from({ length: n }, () => []);
  for (const [u, v, w] of graph) adj[u].push([v, w]);

  const dist = new Array(n).fill(Infinity);
  dist[start] = 0;
  const visited = new Array(n).fill(false);

  for (let k = 0; k < n; k++) {
    // pick min unvisited
    let u = -1;
    let min = Infinity;
    for (let i = 0; i < n; i++) {
      if (!visited[i] && dist[i] < min) {
        min = dist[i];
        u = i;
      }
    }
    if (u === -1) break;
    visited[u] = true;
    for (const [v, w] of adj[u]) {
      if (!visited[v] && dist[u] + w < dist[v]) {
        dist[v] = dist[u] + w;
      }
    }
  }
  return dist;
}

// Bellman-Ford（含负权检测）
export function bellmanFord(
  edges: [number, number, number][], // [from, to, weight]
  n: number,
  start: number,
): { dist: number[]; hasNegativeCycle: boolean } {
  const dist = new Array(n).fill(Infinity);
  dist[start] = 0;

  for (let i = 0; i < n - 1; i++) {
    let updated = false;
    for (const [u, v, w] of edges) {
      if (dist[u] !== Infinity && dist[u] + w < dist[v]) {
        dist[v] = dist[u] + w;
        updated = true;
      }
    }
    if (!updated) break;
  }

  // 检测负权环
  let hasNegativeCycle = false;
  for (const [u, v, w] of edges) {
    if (dist[u] !== Infinity && dist[u] + w < dist[v]) {
      hasNegativeCycle = true;
      break;
    }
  }

  return { dist, hasNegativeCycle };
}

// Floyd-Warshall
export function floydWarshall(
  edges: [number, number, number][],
  n: number,
): number[][] {
  const dp: number[][] = Array.from({ length: n }, (_, i) =>
    Array.from({ length: n }, (_, j) => (i === j ? 0 : Infinity)),
  );
  for (const [u, v, w] of edges) dp[u][v] = Math.min(dp[u][v], w);

  for (let k = 0; k < n; k++) {
    for (let i = 0; i < n; i++) {
      for (let j = 0; j < n; j++) {
        if (dp[i][k] !== Infinity && dp[k][j] !== Infinity) {
          dp[i][j] = Math.min(dp[i][j], dp[i][k] + dp[k][j]);
        }
      }
    }
  }
  return dp;
}
