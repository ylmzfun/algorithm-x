import { describe, it, expect } from 'vitest';
import { SeparateChainingHashTable } from '../src/data-structures/hash-table';

describe('SeparateChainingHashTable', () => {
  it('put and get', () => {
    const ht = new SeparateChainingHashTable<string, number>();
    ht.put('a', 1);
    ht.put('b', 2);
    expect(ht.get('a')).toBe(1);
    expect(ht.get('b')).toBe(2);
    expect(ht.get('c')).toBeUndefined();
  });

  it('put overwrites existing key', () => {
    const ht = new SeparateChainingHashTable<string, number>();
    ht.put('x', 1);
    ht.put('x', 99);
    expect(ht.get('x')).toBe(99);
    expect(ht.size).toBe(1);
  });

  it('remove key', () => {
    const ht = new SeparateChainingHashTable<string, number>();
    ht.put('a', 1);
    ht.put('b', 2);
    expect(ht.remove('a')).toBe(true);
    expect(ht.get('a')).toBeUndefined();
    expect(ht.size).toBe(1);
    expect(ht.remove('nonexistent')).toBe(false);
  });

  it('containsKey', () => {
    const ht = new SeparateChainingHashTable<string, number>();
    ht.put('hello', 42);
    expect(ht.containsKey('hello')).toBe(true);
    expect(ht.containsKey('world')).toBe(false);
  });

  it('auto-resize', () => {
    const ht = new SeparateChainingHashTable<number, number>(4);
    for (let i = 0; i < 100; i++) ht.put(i, i);
    expect(ht.size).toBe(100);
    for (let i = 0; i < 100; i++) expect(ht.get(i)).toBe(i);
  });
});
