import { describe, it, expect } from 'vitest';
import { LRUCache, LFUCache } from '../src/algorithms/cache';

describe('LRUCache', () => {
  it('evicts least recently used', () => {
    const cache = new LRUCache<string, number>(2);
    cache.put('a', 1);
    cache.put('b', 2);
    expect(cache.get('a')).toBe(1); // a 变成最近使用
    cache.put('c', 3); // 淘汰 b
    expect(cache.get('b')).toBeUndefined();
    expect(cache.get('a')).toBe(1);
    expect(cache.get('c')).toBe(3);
  });

  it('overwrites existing key', () => {
    const cache = new LRUCache<string, number>(2);
    cache.put('a', 1);
    cache.put('a', 99);
    expect(cache.get('a')).toBe(99);
    expect(cache.size).toBe(1);
  });
});

describe('LFUCache', () => {
  it('evicts least frequently used', () => {
    const cache = new LFUCache<string, number>(2);
    cache.put('a', 1);
    cache.put('b', 2);
    cache.get('a'); // a: freq=2, b: freq=1
    cache.get('a');
    cache.put('c', 3); // 淘汰 b (freq=1)
    expect(cache.get('b')).toBeUndefined();
    expect(cache.get('a')).toBe(1);
    expect(cache.get('c')).toBe(3);
  });
});
