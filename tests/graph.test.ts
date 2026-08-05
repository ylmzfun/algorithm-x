import { describe, it, expect } from 'vitest';
import { Graph } from '../src/data-structures/graph';

describe('Graph (undirected)', () => {
  it('addVertex and addEdge', () => {
    const g = new Graph();
    g.addEdge(1, 2);
    g.addEdge(2, 3);
    expect(g.getVertices()).toContain(1);
    expect(g.getVertices()).toContain(2);
    expect(g.getVertices()).toContain(3);
    expect(g.getNeighbors(2)).toEqual(expect.arrayContaining([1, 3]));
    expect(g.vertexCount).toBe(3);
    expect(g.edgeCount).toBe(2);
  });
});

describe('Graph (directed)', () => {
  it('edge is one-way', () => {
    const g = new Graph(true);
    g.addEdge(1, 2);
    expect(g.getNeighbors(1)).toEqual([2]);
    expect(g.getNeighbors(2)).toEqual([]);
  });
});
