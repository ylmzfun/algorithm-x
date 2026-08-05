// Ford-Fulkerson 最大流
export function fordFulkerson(
  n: number,
  edges: [number, number, number][], // [from, to, capacity]
  source: number,
  sink: number,
): number {
  // 残差图
  const capacity: number[][] = Array.from({ length: n }, () => new Array(n).fill(0));
  for (const [u, v, c] of edges) capacity[u][v] = c;

  const residual = capacity.map((row) => [...row]);
  let maxFlow = 0;

  function bfs(): number[] | null {
    const parent = new Array(n).fill(-1);
    const queue = [source];
    parent[source] = source;

    while (queue.length > 0) {
      const u = queue.shift()!;
      for (let v = 0; v < n; v++) {
        if (parent[v] === -1 && residual[u][v] > 0) {
          parent[v] = u;
          if (v === sink) return parent;
          queue.push(v);
        }
      }
    }
    return null;
  }

  let parent = bfs();
  while (parent) {
    // 找瓶颈容量
    let flow = Infinity;
    for (let v = sink; v !== source; v = parent[v]) {
      const u = parent[v];
      flow = Math.min(flow, residual[u][v]);
    }
    // 更新残差图
    for (let v = sink; v !== source; v = parent[v]) {
      const u = parent[v];
      residual[u][v] -= flow;
      residual[v][u] += flow;
    }
    maxFlow += flow;
    parent = bfs();
  }

  return maxFlow;
}
