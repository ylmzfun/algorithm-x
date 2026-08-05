import { describe, it, expect } from 'vitest';
import { UnionFind } from '../src/data-structures/union-find';

describe('UnionFind', () => {
  it('connects and finds', () => {
    const uf = new UnionFind(5);
    uf.union(0, 1);
    uf.union(1, 2);
    expect(uf.connected(0, 2)).toBe(true);
    expect(uf.connected(0, 3)).toBe(false);
    expect(uf.count).toBe(3);
  });

  it('path compression', () => {
    const uf = new UnionFind(10);
    for (let i = 1; i < 10; i++) uf.union(0, i);
    expect(uf.connected(0, 9)).toBe(true);
    expect(uf.count).toBe(1);
  });
});
