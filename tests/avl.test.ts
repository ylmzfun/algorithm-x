import { describe, it, expect } from 'vitest';
import { AVLTree } from '../src/data-structures/tree/AVLTree';

describe('AVLTree', () => {
  it('insert maintains balance (sorted order)', () => {
    const avl = new AVLTree<number>();
    const nums = [10, 20, 30, 40, 50, 25];
    nums.forEach((n) => avl.insert(n));
    expect(avl.inorder()).toEqual([10, 20, 25, 30, 40, 50]);
    expect(avl.size).toBe(6);
  });

  it('delete removes node and rebalances', () => {
    const avl = new AVLTree<number>();
    [9, 5, 10, 0, 6, 11, -1, 1, 2].forEach((n) => avl.insert(n));
    expect(avl.delete(10)).toBe(true);
    expect(avl.contains(10)).toBe(false);
    expect(avl.inorder()).toEqual([-1, 0, 1, 2, 5, 6, 9, 11]);
  });

  it('contains', () => {
    const avl = new AVLTree<number>();
    avl.insert(42);
    expect(avl.contains(42)).toBe(true);
    expect(avl.contains(99)).toBe(false);
  });
});
