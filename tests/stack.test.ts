import { describe, it, expect } from 'vitest';
import { ArrayStack, LinkedStack } from '../src/data-structures/stack';

describe.each([
  ['ArrayStack', () => new ArrayStack<number>()],
  ['LinkedStack', () => new LinkedStack<number>()],
])('%s', (_, factory) => {
  it('starts empty', () => {
    const s = factory();
    expect(s.isEmpty()).toBe(true);
    expect(s.size).toBe(0);
    expect(s.pop()).toBeUndefined();
    expect(s.peek()).toBeUndefined();
  });

  it('push / pop in LIFO order', () => {
    const s = factory();
    s.push(1);
    s.push(2);
    s.push(3);
    expect(s.size).toBe(3);
    expect(s.pop()).toBe(3);
    expect(s.pop()).toBe(2);
    expect(s.pop()).toBe(1);
    expect(s.isEmpty()).toBe(true);
  });

  it('peek returns top without removing', () => {
    const s = factory();
    s.push(42);
    expect(s.peek()).toBe(42);
    expect(s.size).toBe(1);
  });
});
