import { describe, it, expect } from 'vitest';
import { kmpSearch, rabinKarp, longestPalindrome } from '../src/algorithms/string';

describe('kmpSearch', () => {
  it('finds all occurrences', () => {
    expect(kmpSearch('ababcabc', 'abc')).toEqual([2, 5]);
    expect(kmpSearch('aaaa', 'aa')).toEqual([0, 1, 2]);
    expect(kmpSearch('hello', 'xx')).toEqual([]);
  });
});

describe('rabinKarp', () => {
  it('finds all occurrences', () => {
    expect(rabinKarp('ababcabc', 'abc')).toEqual([2, 5]);
  });
});

describe('longestPalindrome', () => {
  it('finds longest palindromic substring', () => {
    expect(longestPalindrome('babad')).toBe('bab');
    expect(longestPalindrome('cbbd')).toBe('bb');
  });
});
