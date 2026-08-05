import type { Queue } from './IQueue';

export class ArrayQueue<T> implements Queue<T> {
  private items: T[] = [];
  private head = 0;
  private tail = 0;

  enqueue(item: T): void {
    this.items[this.tail] = item;
    this.tail++;
  }

  dequeue(): T | undefined {
    if (this.head === this.tail) return undefined;
    const value = this.items[this.head];
    this.head++;
    // 空间收缩：当空闲过多时搬运到前面
    if (this.head > 100 && this.head * 2 > this.tail) {
      this.items = this.items.slice(this.head, this.tail);
      this.tail -= this.head;
      this.head = 0;
    }
    return value;
  }

  peek(): T | undefined {
    if (this.head === this.tail) return undefined;
    return this.items[this.head];
  }

  get size(): number {
    return this.tail - this.head;
  }

  isEmpty(): boolean {
    return this.head === this.tail;
  }
}
