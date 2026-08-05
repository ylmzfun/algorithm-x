import type { LinkedList } from './ILinkedList';

class SinglyNode<T> {
  constructor(
    public value: T,
    public next: SinglyNode<T> | null = null,
  ) {}
}

export class SinglyLinkedList<T> implements LinkedList<T> {
  private head: SinglyNode<T> | null = null;
  private _size = 0;

  prepend(item: T): void {
    this.head = new SinglyNode(item, this.head);
    this._size++;
  }

  append(item: T): void {
    const node = new SinglyNode(item);
    if (!this.head) {
      this.head = node;
    } else {
      let cur = this.head;
      while (cur.next) cur = cur.next;
      cur.next = node;
    }
    this._size++;
  }

  delete(item: T): boolean {
    if (!this.head) return false;
    if (this.head.value === item) {
      this.head = this.head.next;
      this._size--;
      return true;
    }
    let cur: SinglyNode<T> | null = this.head;
    while (cur.next) {
      if (cur.next.value === item) {
        cur.next = cur.next.next;
        this._size--;
        return true;
      }
      cur = cur.next;
    }
    return false;
  }

  find(predicate: (item: T) => boolean): T | undefined {
    let cur = this.head;
    while (cur) {
      if (predicate(cur.value)) return cur.value;
      cur = cur.next;
    }
    return undefined;
  }

  reverse(): this {
    let prev: SinglyNode<T> | null = null;
    let cur = this.head;
    while (cur) {
      const next: SinglyNode<T> | null = cur.next;
      cur.next = prev;
      prev = cur;
      cur = next;
    }
    this.head = prev;
    return this;
  }

  toArray(): T[] {
    const result: T[] = [];
    let cur = this.head;
    while (cur) {
      result.push(cur.value);
      cur = cur.next;
    }
    return result;
  }

  get size(): number {
    return this._size;
  }

  isEmpty(): boolean {
    return this._size === 0;
  }
}
