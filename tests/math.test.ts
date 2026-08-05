import { describe, it, expect } from 'vitest';
import {
  generatePrimes,
  isPrime,
  gcd,
  lcm,
  combination,
  isPalindromeNumber,
} from '../src/algorithms/math';

describe('generatePrimes', () => {
  it('lists primes up to n', () => {
    expect(generatePrimes(10)).toEqual([2, 3, 5, 7]);
    expect(generatePrimes(20)).toEqual([2, 3, 5, 7, 11, 13, 17, 19]);
  });
});

describe('isPrime', () => {
  it('determines primality', () => {
    expect(isPrime(2)).toBe(true);
    expect(isPrime(17)).toBe(true);
    expect(isPrime(1)).toBe(false);
    expect(isPrime(25)).toBe(false);
  });
});

describe('gcd', () => {
  it('computes greatest common divisor', () => {
    expect(gcd(48, 18)).toBe(6);
    expect(gcd(7, 13)).toBe(1);
    expect(gcd(100, 10)).toBe(10);
  });
});

describe('lcm', () => {
  it('computes least common multiple', () => {
    expect(lcm(4, 6)).toBe(12);
    expect(lcm(7, 13)).toBe(91);
  });
});

describe('combination', () => {
  it('computes C(n, k)', () => {
    expect(combination(5, 2)).toBe(10);
    expect(combination(10, 3)).toBe(120);
    expect(combination(10, 0)).toBe(1);
    expect(combination(10, 10)).toBe(1);
  });
});

describe('isPalindromeNumber', () => {
  it('checks palindrome numbers', () => {
    expect(isPalindromeNumber(121)).toBe(true);
    expect(isPalindromeNumber(-121)).toBe(false);
    expect(isPalindromeNumber(10)).toBe(false);
  });
});
