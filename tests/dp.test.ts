import { describe, it, expect } from 'vitest';
import {
  knapsack01,
  lcs,
  lis,
  editDistance,
  climbStairs,
  coinChange,
} from '../src/algorithms/dynamic-programming';

describe('knapsack01', () => {
  it('maximizes value within capacity', () => {
    expect(knapsack01([2, 3, 4, 5], [3, 4, 5, 6], 8)).toBe(10);
  });
});

describe('lcs', () => {
  it('finds longest common subsequence', () => {
    expect(lcs('abcde', 'ace')).toBe('ace');
    expect(lcs('abc', 'def')).toBe('');
  });
});

describe('lis', () => {
  it('finds longest increasing subsequence', () => {
    const result = lis([10, 9, 2, 5, 3, 7, 101, 18]);
    expect(result.length).toBe(4);
    // verify strictly increasing
    for (let i = 1; i < result.length; i++) {
      expect(result[i]).toBeGreaterThan(result[i - 1]);
    }
  });
});

describe('editDistance', () => {
  it('computes edit distance', () => {
    expect(editDistance('horse', 'ros')).toBe(3);
    expect(editDistance('intention', 'execution')).toBe(5);
  });
});

describe('climbStairs', () => {
  it('counts ways', () => {
    expect(climbStairs(3)).toBe(3);
    expect(climbStairs(5)).toBe(8);
  });
});

describe('coinChange', () => {
  it('finds minimum coins', () => {
    expect(coinChange([1, 2, 5], 11)).toBe(3);
    expect(coinChange([2], 3)).toBe(-1);
  });
});
