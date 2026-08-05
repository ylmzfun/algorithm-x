import { describe, it, expect } from 'vitest';
import { SinglyLinkedList, DoublyLinkedList } from '../src/data-structures/linked-list';

describe.each([
  ['SinglyLinkedList', () => new SinglyLinkedList<number>()],
  ['DoublyLinkedList', () => new DoublyLinkedList<number>()],
])('%s', (_, factory) => {
  it('starts empty', () => {
    const l = factory();
    expect(l.isEmpty()).toBe(true);
    expect(l.size).toBe(0);
    expect(l.toArray()).toEqual([]);
  });

  it('append adds items to the end', () => {
    const l = factory();
    l.append(1);
    l.append(2);
    l.append(3);
    expect(l.toArray()).toEqual([1, 2, 3]);
  });

  it('prepend adds items to the front', () => {
    const l = factory();
    l.prepend(1);
    l.prepend(2);
    expect(l.toArray()).toEqual([2, 1]);
  });

  it('delete removes the first matching item', () => {
    const l = factory();
    l.append(1);
    l.append(2);
    l.append(3);
    expect(l.delete(2)).toBe(true);
    expect(l.toArray()).toEqual([1, 3]);
    expect(l.size).toBe(2);
  });

  it('delete returns false when item not found', () => {
    const l = factory();
    l.append(1);
    expect(l.delete(99)).toBe(false);
    expect(l.size).toBe(1);
  });

  it('find returns item matching predicate', () => {
    const l = factory();
    l.append(10);
    l.append(20);
    l.append(30);
    expect(l.find((v) => v > 15)).toBe(20);
    expect(l.find((v) => v > 100)).toBeUndefined();
  });
});

describe('SinglyLinkedList.reverse', () => {
  it('reverses the list in place', () => {
    const l = new SinglyLinkedList<number>();
    l.append(1);
    l.append(2);
    l.append(3);
    l.reverse();
    expect(l.toArray()).toEqual([3, 2, 1]);
  });

  it('handles empty list', () => {
    const l = new SinglyLinkedList<number>();
    l.reverse();
    expect(l.toArray()).toEqual([]);
  });
});
