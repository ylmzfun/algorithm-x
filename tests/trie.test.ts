import { describe, it, expect } from 'vitest';
import { Trie } from '../src/data-structures/trie';

describe('Trie', () => {
  it('insert and search', () => {
    const t = new Trie();
    t.insert('hello');
    t.insert('world');
    expect(t.search('hello')).toBe(true);
    expect(t.search('world')).toBe(true);
    expect(t.search('hel')).toBe(false);
    expect(t.search('helloo')).toBe(false);
  });

  it('startsWith', () => {
    const t = new Trie();
    t.insert('apple');
    expect(t.startsWith('app')).toBe(true);
    expect(t.startsWith('apl')).toBe(false);
  });

  it('delete word', () => {
    const t = new Trie();
    t.insert('abc');
    t.insert('ab');
    expect(t.delete('abc')).toBe(true);
    expect(t.search('abc')).toBe(false);
    expect(t.search('ab')).toBe(true);
  });

  it('getAllWords', () => {
    const t = new Trie();
    t.insert('cat');
    t.insert('car');
    t.insert('card');
    expect(t.getAllWords().sort()).toEqual(['car', 'card', 'cat']);
  });
});
