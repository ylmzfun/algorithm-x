import { describe, it, expect } from 'vitest';
import {
  isPowerOfTwo,
  countSetBits,
  reverseBits,
  singleNumber,
  BloomFilter,
} from '../src/algorithms/bit';

describe('isPowerOfTwo', () => {
  it('detects powers of two', () => {
    expect(isPowerOfTwo(1)).toBe(true);
    expect(isPowerOfTwo(2)).toBe(true);
    expect(isPowerOfTwo(128)).toBe(true);
    expect(isPowerOfTwo(3)).toBe(false);
    expect(isPowerOfTwo(0)).toBe(false);
  });
});

describe('countSetBits', () => {
  it('counts 1 bits', () => {
    expect(countSetBits(7)).toBe(3); // 111
    expect(countSetBits(0)).toBe(0);
    expect(countSetBits(16)).toBe(1); // 10000
  });
});

describe('reverseBits', () => {
  it('reverses 32-bit integer', () => {
    // 0b...0001 → 0b1000...0000
    expect(reverseBits(1)).toBe(0x80000000);
  });
});

describe('singleNumber', () => {
  it('finds the unique element', () => {
    expect(singleNumber([2, 2, 1])).toBe(1);
    expect(singleNumber([4, 1, 2, 1, 2])).toBe(4);
  });
});

describe('BloomFilter', () => {
  it('may contain added items', () => {
    const bf = new BloomFilter(64);
    bf.add('hello');
    bf.add('world');
    expect(bf.contains('hello')).toBe(true);
    expect(bf.contains('world')).toBe(true);
  });

  it('does not contain items never added (probabilistic)', () => {
    const bf = new BloomFilter(256, 5);
    bf.add('one');
    // Very unlikely false positive with small dataset
    expect(bf.contains('never_added')).toBe(false);
  });
});
