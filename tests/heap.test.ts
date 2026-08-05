import { describe, it, expect } from 'vitest';
import { MaxHeap, MinHeap, heapSort } from '../src/data-structures/heap';

describe('MaxHeap', () => {
  it('extracts max', () => {
    const h = new MaxHeap();
    h.insert(3);
    h.insert(10);
    h.insert(5);
    expect(h.extract()).toBe(10);
    expect(h.extract()).toBe(5);
    expect(h.extract()).toBe(3);
    expect(h.extract()).toBeUndefined();
  });

  it('peek returns max without removing', () => {
    const h = new MaxHeap();
    h.insert(7);
    h.insert(1);
    expect(h.peek()).toBe(7);
    expect(h.size).toBe(2);
  });
});

describe('MinHeap', () => {
  it('extracts min', () => {
    const h = new MinHeap();
    h.insert(3);
    h.insert(1);
    h.insert(2);
    expect(h.extract()).toBe(1);
    expect(h.extract()).toBe(2);
    expect(h.extract()).toBe(3);
  });
});

describe('heapSort', () => {
  it('sorts using heap', () => {
    expect(heapSort([5, 2, 8, 1, 9])).toEqual([1, 2, 5, 8, 9]);
  });
});
