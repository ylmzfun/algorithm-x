import { UnionFind } from '../../data-structures/union-find';

// Prim
export function prim(edges: [number, number, number][], n: number): number {
  const adj: [number, number][][] = Array.from({ length: n }, () => []);
  for (const [u, v, w] of edges) {
    adj[u].push([v, w]);
    adj[v].push([u, w]);
  }

  const visited = new Array(n).fill(false);
  const minEdge = new Array(n).fill(Infinity);
  minEdge[0] = 0;
  let total = 0;

  for (let k = 0; k < n; k++) {
    let u = -1;
    let min = Infinity;
    for (let i = 0; i < n; i++) {
      if (!visited[i] && minEdge[i] < min) {
        min = minEdge[i];
        u = i;
      }
    }
    if (u === -1) break;
    visited[u] = true;
    total += minEdge[u];

    for (const [v, w] of adj[u]) {
      if (!visited[v] && w < minEdge[v]) {
        minEdge[v] = w;
      }
    }
  }
  return total;
}

// Kruskal
export function kruskal(edges: [number, number, number][], n: number): number {
  const sorted = [...edges].sort((a, b) => a[2] - b[2]);
  const uf = new UnionFind(n);
  let total = 0;
  let count = 0;

  for (const [u, v, w] of sorted) {
    if (!uf.connected(u, v)) {
      uf.union(u, v);
      total += w;
      count++;
      if (count === n - 1) break;
    }
  }
  return total;
}
