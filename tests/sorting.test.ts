import { describe, it, expect } from 'vitest';
import {
  bubbleSort,
  selectionSort,
  insertionSort,
  shellSort,
  mergeSort,
  quickSort,
  countingSort,
} from '../src/algorithms/sorting';

const sorts = [
  ['bubbleSort', bubbleSort],
  ['selectionSort', selectionSort],
  ['insertionSort', insertionSort],
  ['shellSort', shellSort],
  ['mergeSort', mergeSort],
  ['quickSort', quickSort],
  ['countingSort', countingSort],
] as const;

function verify(sort: (arr: number[]) => number[]) {
  it('sorts an empty array', () => {
    expect(sort([])).toEqual([]);
  });

  it('sorts a single element', () => {
    expect(sort([5])).toEqual([5]);
  });

  it('sorts a sorted array', () => {
    expect(sort([1, 2, 3, 4, 5])).toEqual([1, 2, 3, 4, 5]);
  });

  it('sorts a reversed array', () => {
    expect(sort([5, 4, 3, 2, 1])).toEqual([1, 2, 3, 4, 5]);
  });

  it('sorts with duplicates', () => {
    expect(sort([3, 1, 2, 1, 3, 2])).toEqual([1, 1, 2, 2, 3, 3]);
  });

  it('does not mutate the original array', () => {
    const original = [3, 1, 2];
    const sorted = sort(original);
    expect(sorted).toEqual([1, 2, 3]);
    expect(original).toEqual([3, 1, 2]);
  });
}

describe.each(sorts)('%s', (_, sort) => {
  verify(sort);
});
