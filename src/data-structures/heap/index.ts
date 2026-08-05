export interface Heap<T> {
  insert(item: T): void;
  extract(): T | undefined;
  peek(): T | undefined;
  get size(): number;
  isEmpty(): boolean;
}

export class MaxHeap implements Heap<number> {
  private data: number[] = [];

  insert(item: number): void {
    this.data.push(item);
    this.siftUp(this.data.length - 1);
  }

  extract(): number | undefined {
    if (this.data.length === 0) return undefined;
    const top = this.data[0];
    const last = this.data.pop()!;
    if (this.data.length > 0) {
      this.data[0] = last;
      this.siftDown(0);
    }
    return top;
  }

  peek(): number | undefined {
    return this.data[0];
  }

  get size(): number {
    return this.data.length;
  }

  isEmpty(): boolean {
    return this.data.length === 0;
  }

  toArray(): number[] {
    return [...this.data];
  }

  private siftUp(i: number): void {
    while (i > 0) {
      const p = (i - 1) >> 1;
      if (this.data[p] >= this.data[i]) break;
      [this.data[p], this.data[i]] = [this.data[i], this.data[p]];
      i = p;
    }
  }

  private siftDown(i: number): void {
    const n = this.data.length;
    while (true) {
      let largest = i;
      const left = i * 2 + 1;
      const right = i * 2 + 2;
      if (left < n && this.data[left] > this.data[largest]) largest = left;
      if (right < n && this.data[right] > this.data[largest]) largest = right;
      if (largest === i) break;
      [this.data[i], this.data[largest]] = [this.data[largest], this.data[i]];
      i = largest;
    }
  }
}

export class MinHeap implements Heap<number> {
  private data: number[] = [];

  insert(item: number): void {
    this.data.push(item);
    this.siftUp(this.data.length - 1);
  }

  extract(): number | undefined {
    if (this.data.length === 0) return undefined;
    const top = this.data[0];
    const last = this.data.pop()!;
    if (this.data.length > 0) {
      this.data[0] = last;
      this.siftDown(0);
    }
    return top;
  }

  peek(): number | undefined {
    return this.data[0];
  }

  get size(): number {
    return this.data.length;
  }

  isEmpty(): boolean {
    return this.data.length === 0;
  }

  private siftUp(i: number): void {
    while (i > 0) {
      const p = (i - 1) >> 1;
      if (this.data[p] <= this.data[i]) break;
      [this.data[p], this.data[i]] = [this.data[i], this.data[p]];
      i = p;
    }
  }

  private siftDown(i: number): void {
    const n = this.data.length;
    while (true) {
      let smallest = i;
      const left = i * 2 + 1;
      const right = i * 2 + 2;
      if (left < n && this.data[left] < this.data[smallest]) smallest = left;
      if (right < n && this.data[right] < this.data[smallest]) smallest = right;
      if (smallest === i) break;
      [this.data[i], this.data[smallest]] = [this.data[smallest], this.data[i]];
      i = smallest;
    }
  }
}

export function heapSort(arr: number[]): number[] {
  const heap = new MinHeap();
  for (const v of arr) heap.insert(v);
  const result: number[] = [];
  while (!heap.isEmpty()) result.push(heap.extract()!);
  return result;
}
