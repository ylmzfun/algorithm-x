import { Graph } from '../../data-structures/graph';

// BFS 遍历
export function bfs(graph: Graph, start: number): number[] {
  const visited = new Set<number>();
  const result: number[] = [];
  const queue = [start];
  visited.add(start);

  while (queue.length > 0) {
    const v = queue.shift()!;
    result.push(v);
    for (const nb of graph.getNeighbors(v)) {
      if (!visited.has(nb)) {
        visited.add(nb);
        queue.push(nb);
      }
    }
  }
  return result;
}

// DFS 遍历
export function dfs(graph: Graph, start: number): number[] {
  const visited = new Set<number>();
  const result: number[] = [];

  function explore(v: number) {
    visited.add(v);
    result.push(v);
    for (const nb of graph.getNeighbors(v)) {
      if (!visited.has(nb)) explore(nb);
    }
  }

  explore(start);
  return result;
}

// BFS 最短路径（无权图）
export function bfsShortestPath(graph: Graph, start: number): Map<number, number> {
  const dist = new Map<number, number>();
  dist.set(start, 0);
  const queue = [start];

  while (queue.length > 0) {
    const v = queue.shift()!;
    for (const nb of graph.getNeighbors(v)) {
      if (!dist.has(nb)) {
        dist.set(nb, dist.get(v)! + 1);
        queue.push(nb);
      }
    }
  }
  return dist;
}
