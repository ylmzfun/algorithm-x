import { describe, it, expect } from 'vitest';
import { kahnTopologicalSort, dfsTopologicalSort } from '../src/algorithms/graph/topological-sort';

const edges: [number, number][] = [
  [5, 2],
  [5, 0],
  [4, 0],
  [4, 1],
  [2, 3],
  [3, 1],
];

describe.each([
  ['kahn', kahnTopologicalSort],
  ['dfs', dfsTopologicalSort],
])('%s', (_, fn) => {
  it('produces valid topological order', () => {
    const order = fn(6, edges);
    expect(order.length).toBe(6);
    const pos = new Map<number, number>();
    order.forEach((v, i) => pos.set(v, i));
    for (const [u, v] of edges) {
      expect(pos.get(u)!).toBeLessThan(pos.get(v)!);
    }
  });
});
