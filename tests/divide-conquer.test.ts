import { describe, it, expect } from 'vitest';
import { karatsuba, fastPow, maxSubArray, countInversions } from '../src/algorithms/divide-conquer';

describe('karatsuba', () => {
  it('multiplies correctly', () => {
    expect(karatsuba(12, 34)).toBe(408);
    expect(karatsuba(1234, 5678)).toBe(1234 * 5678);
  });
});

describe('fastPow', () => {
  it('computes power', () => {
    expect(fastPow(2, 10)).toBe(1024);
    expect(fastPow(3, 5)).toBe(243);
    expect(fastPow(5, 0)).toBe(1);
  });
});

describe('maxSubArray', () => {
  it('finds maximum subarray sum', () => {
    expect(maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4])).toBe(6);
  });
});

describe('countInversions', () => {
  it('counts inversions', () => {
    expect(countInversions([2, 4, 1, 3, 5])).toBe(3);
    expect(countInversions([1, 2, 3, 4, 5])).toBe(0);
    expect(countInversions([5, 4, 3, 2, 1])).toBe(10);
  });
});
