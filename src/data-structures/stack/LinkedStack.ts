import type { Stack } from './IStack';

class ListNode<T> {
  constructor(
    public value: T,
    public next: ListNode<T> | null = null,
  ) {}
}

export class LinkedStack<T> implements Stack<T> {
  private top: ListNode<T> | null = null;
  private _size = 0;

  push(item: T): void {
    this.top = new ListNode(item, this.top);
    this._size++;
  }

  pop(): T | undefined {
    if (!this.top) return undefined;
    const value = this.top.value;
    this.top = this.top.next;
    this._size--;
    return value;
  }

  peek(): T | undefined {
    return this.top?.value;
  }

  get size(): number {
    return this._size;
  }

  isEmpty(): boolean {
    return this._size === 0;
  }
}
