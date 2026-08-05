import { describe, it, expect } from 'vitest';
import { activitySelection, huffmanEncode, canJump } from '../src/algorithms/greedy';

describe('activitySelection', () => {
  it('selects max non-overlapping activities', () => {
    const s = [1, 3, 0, 5, 8, 5];
    const f = [2, 4, 6, 7, 9, 9];
    const result = activitySelection(s, f);
    expect(result.length).toBe(4);
  });
});

describe('huffmanEncode', () => {
  it('builds prefix-free codes', () => {
    const freq = new Map([
      ['a', 5],
      ['b', 9],
      ['c', 12],
      ['d', 13],
      ['e', 16],
      ['f', 45],
    ]);
    const codes = huffmanEncode(freq);
    expect(codes.size).toBe(6);
    // 高频字符应有更短的编码
    expect(codes.get('f')!.length).toBeLessThanOrEqual(codes.get('a')!.length);
  });
});

describe('canJump', () => {
  it('determines if end is reachable', () => {
    expect(canJump([2, 3, 1, 1, 4])).toBe(true);
    expect(canJump([3, 2, 1, 0, 4])).toBe(false);
  });
});
