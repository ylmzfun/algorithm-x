import { describe, it, expect } from 'vitest';
import { LinkedDeque } from '../src/data-structures/queue';

describe('LinkedDeque', () => {
  it('addFirst / removeFirst in LIFO order', () => {
    const d = new LinkedDeque<number>();
    d.addFirst(1);
    d.addFirst(2);
    d.addFirst(3);
    expect(d.removeFirst()).toBe(3);
    expect(d.removeFirst()).toBe(2);
    expect(d.removeFirst()).toBe(1);
  });

  it('addLast / removeFirst in FIFO order', () => {
    const d = new LinkedDeque<number>();
    d.addLast(1);
    d.addLast(2);
    d.addLast(3);
    expect(d.removeFirst()).toBe(1);
    expect(d.removeFirst()).toBe(2);
    expect(d.removeFirst()).toBe(3);
  });

  it('removeLast returns from the back', () => {
    const d = new LinkedDeque<number>();
    d.addLast(1);
    d.addLast(2);
    d.addLast(3);
    expect(d.removeLast()).toBe(3);
    expect(d.removeLast()).toBe(2);
    expect(d.removeLast()).toBe(1);
  });

  it('peekFirst / peekLast without removing', () => {
    const d = new LinkedDeque<number>();
    d.addLast(10);
    d.addLast(20);
    expect(d.peekFirst()).toBe(10);
    expect(d.peekLast()).toBe(20);
    expect(d.size).toBe(2);
  });

  it('starts empty', () => {
    const d = new LinkedDeque<number>();
    expect(d.isEmpty()).toBe(true);
    expect(d.removeFirst()).toBeUndefined();
    expect(d.removeLast()).toBeUndefined();
  });
});
