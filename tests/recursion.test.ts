import { describe, it, expect } from 'vitest';
import { permute, subsets, solveNQueens, combinationSum } from '../src/algorithms/recursion';

describe('permute', () => {
  it('returns all permutations', () => {
    expect(permute([1, 2, 3])).toEqual([
      [1, 2, 3],
      [1, 3, 2],
      [2, 1, 3],
      [2, 3, 1],
      [3, 1, 2],
      [3, 2, 1],
    ]);
  });
});

describe('subsets', () => {
  it('returns all subsets', () => {
    const result = subsets([1, 2]);
    expect(result.length).toBe(4);
    expect(result).toEqual(expect.arrayContaining([[], [1], [2], [1, 2]]));
  });
});

describe('solveNQueens', () => {
  it('solves 4-queens', () => {
    const solutions = solveNQueens(4);
    expect(solutions.length).toBe(2);
  });

  it('8-queens has 92 solutions', () => {
    expect(solveNQueens(8).length).toBe(92);
  });
});

describe('combinationSum', () => {
  it('finds combinations', () => {
    const result = combinationSum([2, 3, 6, 7], 7);
    expect(result).toEqual(expect.arrayContaining([[2, 2, 3], [7]]));
  });
});
