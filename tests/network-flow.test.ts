import { describe, it, expect } from 'vitest';
import { fordFulkerson } from '../src/algorithms/graph/network-flow';

describe('fordFulkerson', () => {
  it('computes max flow', () => {
    const edges: [number, number, number][] = [
      [0, 1, 16],
      [0, 2, 13],
      [1, 2, 10],
      [1, 3, 12],
      [2, 1, 4],
      [2, 4, 14],
      [3, 2, 9],
      [3, 5, 20],
      [4, 3, 7],
      [4, 5, 4],
    ];
    expect(fordFulkerson(6, edges, 0, 5)).toBe(23);
  });
});
