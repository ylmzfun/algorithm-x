import { describe, it, expect } from 'vitest';
import { BinarySearchTree } from '../src/data-structures/tree';

describe('BinarySearchTree', () => {
  it('insert and search', () => {
    const bst = new BinarySearchTree<number>();
    bst.insert(5);
    bst.insert(3);
    bst.insert(7);
    expect(bst.contains(5)).toBe(true);
    expect(bst.contains(3)).toBe(true);
    expect(bst.contains(7)).toBe(true);
    expect(bst.contains(99)).toBe(false);
    expect(bst.size).toBe(3);
  });

  it('insert overwrites duplicate', () => {
    const bst = new BinarySearchTree<number>();
    bst.insert(5);
    bst.insert(5);
    expect(bst.size).toBe(1);
  });

  it('delete leaf node', () => {
    const bst = new BinarySearchTree<number>();
    bst.insert(5);
    bst.insert(3);
    bst.insert(7);
    expect(bst.delete(3)).toBe(true);
    expect(bst.contains(3)).toBe(false);
    expect(bst.size).toBe(2);
  });

  it('delete node with one child', () => {
    const bst = new BinarySearchTree<number>();
    bst.insert(5);
    bst.insert(3);
    bst.insert(4);
    bst.delete(3);
    expect(bst.contains(4)).toBe(true);
  });

  it('delete node with two children', () => {
    const bst = new BinarySearchTree<number>();
    bst.insert(10);
    bst.insert(5);
    bst.insert(15);
    bst.insert(12);
    bst.insert(18);
    expect(bst.delete(15)).toBe(true);
    expect(bst.contains(15)).toBe(false);
    expect(bst.contains(12)).toBe(true);
    expect(bst.contains(18)).toBe(true);
  });

  it('inorder returns sorted order', () => {
    const bst = new BinarySearchTree<number>();
    [5, 3, 7, 1, 4, 6, 8].forEach((v) => bst.insert(v));
    expect(bst.inorder()).toEqual([1, 3, 4, 5, 6, 7, 8]);
  });

  it('preorder visits root first', () => {
    const bst = new BinarySearchTree<number>();
    [5, 3, 7].forEach((v) => bst.insert(v));
    expect(bst.preorder()).toEqual([5, 3, 7]);
  });

  it('postorder visits leaf first', () => {
    const bst = new BinarySearchTree<number>();
    [5, 3, 7].forEach((v) => bst.insert(v));
    expect(bst.postorder()).toEqual([3, 7, 5]);
  });

  it('levelOrder BFS', () => {
    const bst = new BinarySearchTree<number>();
    [5, 3, 7, 1, 4].forEach((v) => bst.insert(v));
    expect(bst.levelOrder()).toEqual([5, 3, 7, 1, 4]);
  });
});
