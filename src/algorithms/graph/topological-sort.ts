// Kahn 算法
export function kahnTopologicalSort(n: number, edges: [number, number][]): number[] {
  const adj: number[][] = Array.from({ length: n }, () => []);
  const inDegree = new Array(n).fill(0);
  for (const [u, v] of edges) {
    adj[u].push(v);
    inDegree[v]++;
  }

  const queue: number[] = [];
  for (let i = 0; i < n; i++) {
    if (inDegree[i] === 0) queue.push(i);
  }

  const result: number[] = [];
  while (queue.length > 0) {
    const u = queue.shift()!;
    result.push(u);
    for (const v of adj[u]) {
      if (--inDegree[v] === 0) queue.push(v);
    }
  }
  return result.length === n ? result : []; // 有环返回空
}

// DFS 拓扑排序
export function dfsTopologicalSort(n: number, edges: [number, number][]): number[] {
  const adj: number[][] = Array.from({ length: n }, () => []);
  for (const [u, v] of edges) adj[u].push(v);

  const visited = new Array(n).fill(0); // 0=未访问, 1=访问中, 2=已完成
  const result: number[] = [];
  let hasCycle = false;

  function dfs(v: number) {
    visited[v] = 1;
    for (const nb of adj[v]) {
      if (visited[nb] === 0) dfs(nb);
      else if (visited[nb] === 1) hasCycle = true;
    }
    visited[v] = 2;
    result.push(v);
  }

  for (let i = 0; i < n; i++) {
    if (visited[i] === 0) dfs(i);
  }

  return hasCycle ? [] : result.reverse();
}
