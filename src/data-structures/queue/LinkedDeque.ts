import type { Deque } from './IDeque';

class ListNode<T> {
  prev: ListNode<T> | null = null;
  next: ListNode<T> | null = null;
  constructor(public value: T) {}
}

export class LinkedDeque<T> implements Deque<T> {
  private head: ListNode<T> | null = null;
  private tail: ListNode<T> | null = null;
  private _size = 0;

  addFirst(item: T): void {
    const node = new ListNode(item);
    if (!this.head) {
      this.head = node;
      this.tail = node;
    } else {
      node.next = this.head;
      this.head.prev = node;
      this.head = node;
    }
    this._size++;
  }

  addLast(item: T): void {
    const node = new ListNode(item);
    if (!this.tail) {
      this.head = node;
      this.tail = node;
    } else {
      node.prev = this.tail;
      this.tail.next = node;
      this.tail = node;
    }
    this._size++;
  }

  removeFirst(): T | undefined {
    if (!this.head) return undefined;
    const value = this.head.value;
    if (this.head === this.tail) {
      this.head = null;
      this.tail = null;
    } else {
      this.head = this.head.next;
      this.head!.prev = null;
    }
    this._size--;
    return value;
  }

  removeLast(): T | undefined {
    if (!this.tail) return undefined;
    const value = this.tail.value;
    if (this.head === this.tail) {
      this.head = null;
      this.tail = null;
    } else {
      this.tail = this.tail.prev;
      this.tail!.next = null;
    }
    this._size--;
    return value;
  }

  peekFirst(): T | undefined {
    return this.head?.value;
  }

  peekLast(): T | undefined {
    return this.tail?.value;
  }

  get size(): number {
    return this._size;
  }

  isEmpty(): boolean {
    return this._size === 0;
  }
}
