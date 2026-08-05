import { describe, it, expect } from 'vitest';
import { bfs, dfs, bfsShortestPath } from '../src/algorithms/graph/traversal';
import { Graph } from '../src/data-structures/graph';

function buildGraph(): Graph {
  const g = new Graph();
  g.addEdge(0, 1);
  g.addEdge(0, 2);
  g.addEdge(1, 3);
  g.addEdge(2, 3);
  g.addEdge(2, 4);
  return g;
}

describe('bfs', () => {
  it('traverses level by level', () => {
    const result = bfs(buildGraph(), 0);
    expect(result[0]).toBe(0);
    expect(result.slice(1, 3)).toEqual(expect.arrayContaining([1, 2]));
    expect(result.slice(3)).toEqual(expect.arrayContaining([3, 4]));
  });
});

describe('dfs', () => {
  it('traverses depth first', () => {
    const result = dfs(buildGraph(), 0);
    expect(result[0]).toBe(0);
    expect(result).toContain(4);
  });
});

describe('bfsShortestPath', () => {
  it('finds shortest distances', () => {
    const dist = bfsShortestPath(buildGraph(), 0);
    expect(dist.get(0)).toBe(0);
    expect(dist.get(1)).toBe(1);
    expect(dist.get(3)).toBe(2);
    expect(dist.get(4)).toBe(2);
  });
});
