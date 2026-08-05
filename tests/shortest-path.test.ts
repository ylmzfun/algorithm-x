import { describe, it, expect } from 'vitest';
import { dijkstra, bellmanFord, floydWarshall } from '../src/algorithms/graph/shortest-path';

describe('dijkstra', () => {
  it('finds shortest paths from start', () => {
    const edges: [number, number, number][] = [
      [0, 1, 4],
      [0, 2, 1],
      [2, 1, 2],
      [1, 3, 1],
      [2, 3, 5],
    ];
    const dist = dijkstra(edges, 4, 0);
    expect(dist[0]).toBe(0);
    expect(dist[1]).toBe(3);
    expect(dist[2]).toBe(1);
    expect(dist[3]).toBe(4);
  });
});

describe('bellmanFord', () => {
  it('handles negative weights', () => {
    const edges: [number, number, number][] = [
      [0, 1, -1],
      [0, 2, 4],
      [1, 2, 3],
      [1, 3, 2],
      [1, 4, 2],
      [3, 2, 5],
      [3, 1, 1],
      [4, 3, -3],
    ];
    const { dist, hasNegativeCycle } = bellmanFord(edges, 5, 0);
    expect(hasNegativeCycle).toBe(false);
    expect(dist[3]).toBe(-2);
  });

  it('detects negative cycle', () => {
    const edges: [number, number, number][] = [
      [0, 1, 1],
      [1, 2, -1],
      [2, 0, -1],
    ];
    const { hasNegativeCycle } = bellmanFord(edges, 3, 0);
    expect(hasNegativeCycle).toBe(true);
  });
});

describe('floydWarshall', () => {
  it('all-pairs shortest path', () => {
    const edges: [number, number, number][] = [
      [0, 1, 3],
      [0, 2, 8],
      [1, 2, 2],
      [1, 3, 5],
      [2, 3, 1],
    ];
    const dp = floydWarshall(edges, 4);
    expect(dp[0][3]).toBe(6);
  });
});
