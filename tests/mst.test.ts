import { describe, it, expect } from 'vitest';
import { prim, kruskal } from '../src/algorithms/graph/mst';

const edges: [number, number, number][] = [
  [0, 1, 4],
  [0, 2, 3],
  [1, 2, 1],
  [1, 3, 2],
  [2, 3, 4],
];

describe('prim', () => {
  it('finds MST total weight', () => {
    expect(prim(edges, 4)).toBe(6);
  });
});

describe('kruskal', () => {
  it('finds MST total weight', () => {
    expect(kruskal(edges, 4)).toBe(6);
  });
});
