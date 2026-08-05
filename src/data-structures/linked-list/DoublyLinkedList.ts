import type { LinkedList } from './ILinkedList';

class DoublyNode<T> {
  prev: DoublyNode<T> | null = null;
  next: DoublyNode<T> | null = null;
  constructor(public value: T) {}
}

export class DoublyLinkedList<T> implements LinkedList<T> {
  private head: DoublyNode<T> | null = null;
  private tail: DoublyNode<T> | null = null;
  private _size = 0;

  prepend(item: T): void {
    const node = new DoublyNode(item);
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

  append(item: T): void {
    const node = new DoublyNode(item);
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

  delete(item: T): boolean {
    let cur = this.head;
    while (cur) {
      if (cur.value === item) {
        if (cur.prev) cur.prev.next = cur.next;
        else this.head = cur.next;
        if (cur.next) cur.next.prev = cur.prev;
        else this.tail = cur.prev;
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
