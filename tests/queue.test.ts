import { describe, it, expect } from 'vitest';
import { ArrayQueue, LinkedQueue } from '../src/data-structures/queue';

describe.each([
  ['ArrayQueue', () => new ArrayQueue<number>()],
  ['LinkedQueue', () => new LinkedQueue<number>()],
])('%s', (_, factory) => {
  it('starts empty', () => {
    const q = factory();
    expect(q.isEmpty()).toBe(true);
    expect(q.size).toBe(0);
    expect(q.dequeue()).toBeUndefined();
    expect(q.peek()).toBeUndefined();
  });

  it('enqueue / dequeue in FIFO order', () => {
    const q = factory();
    q.enqueue(1);
    q.enqueue(2);
    q.enqueue(3);
    expect(q.dequeue()).toBe(1);
    expect(q.dequeue()).toBe(2);
    q.enqueue(4);
    expect(q.dequeue()).toBe(3);
    expect(q.dequeue()).toBe(4);
    expect(q.isEmpty()).toBe(true);
  });

  it('peek returns front without removing', () => {
    const q = factory();
    q.enqueue(99);
    expect(q.peek()).toBe(99);
    expect(q.size).toBe(1);
  });
});
