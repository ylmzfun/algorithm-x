import { describe, it, expect } from 'vitest';
import { SkipList } from '../src/data-structures/skip-list';

describe('SkipList', () => {
  it('insert and search', () => {
    const sl = new SkipList<number>();
    sl.insert(3);
    sl.insert(1);
    sl.insert(2);
    expect(sl.search(2)).toBe(2);
    expect(sl.search(5)).toBeUndefined();
    expect(sl.toArray()).toEqual([1, 2, 3]);
  });

  it('delete', () => {
    const sl = new SkipList<number>();
    sl.insert(5);
    sl.insert(3);
    sl.delete(3);
    expect(sl.search(3)).toBeUndefined();
    expect(sl.size).toBe(1);
  });
});
