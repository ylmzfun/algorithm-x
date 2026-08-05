import { describe, it, expect } from 'vitest';
import {
  linearSearch,
  binarySearch,
  binarySearchRecursive,
} from '../src/algorithms/searching';

describe('linearSearch', () => {
  it('finds an existing element', () => {
    expect(linearSearch([10, 20, 30, 40], 30)).toBe(2);
  });

  it('returns -1 when not found', () => {
    expect(linearSearch([10, 20, 30], 99)).toBe(-1);
  });

  it('returns the first match when duplicated', () => {
    expect(linearSearch([1, 2, 1], 1)).toBe(0);
  });

  it('works with an empty array', () => {
    expect(linearSearch([], 5)).toBe(-1);
  });
});

describe('binarySearch', () => {
  const arr = [2, 5, 8, 12, 16, 23, 38, 56];

  it('finds an element', () => {
    expect(binarySearch(arr, 12)).toBe(3);
    expect(binarySearch(arr, 2)).toBe(0);
    expect(binarySearch(arr, 56)).toBe(7);
  });

  it('returns -1 when not found', () => {
    expect(binarySearch(arr, 99)).toBe(-1);
    expect(binarySearch(arr, 1)).toBe(-1);
  });

  it('works with a single-element array', () => {
    expect(binarySearch([5], 5)).toBe(0);
    expect(binarySearch([5], 3)).toBe(-1);
  });
});

describe('binarySearchRecursive', () => {
  const arr = [1, 3, 5, 7, 9];

  it('finds an element', () => {
    expect(binarySearchRecursive(arr, 5)).toBe(2);
    expect(binarySearchRecursive(arr, 9)).toBe(4);
  });

  it('returns -1 when not found', () => {
    expect(binarySearchRecursive(arr, 4)).toBe(-1);
  });
});
