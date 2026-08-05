const MAX_LEVEL = 16;
const P = 0.5;

class SkipNode<T> {
  forward: Array<SkipNode<T> | null>;

  constructor(
    public value: T,
    level: number,
  ) {
    this.forward = new Array(level).fill(null);
  }
}

export class SkipList<T> {
  private head: SkipNode<T>;
  private level = 1;
  private _size = 0;
  private compare: (a: T, b: T) => number;

  constructor(compare?: (a: T, b: T) => number) {
    this.compare = compare ?? ((a, b) => (a as unknown as number) - (b as unknown as number));
    this.head = new SkipNode(null as unknown as T, MAX_LEVEL);
  }

  insert(value: T): void {
    const update: Array<SkipNode<T> | null> = new Array(MAX_LEVEL).fill(null);
    let cur: SkipNode<T> | null = this.head;
    for (let i = this.level - 1; i >= 0; i--) {
      while (cur!.forward[i] && this.compare(cur!.forward[i]!.value, value) < 0) {
        cur = cur!.forward[i];
      }
      update[i] = cur;
    }

    const newLevel = this.randomLevel();
    if (newLevel > this.level) {
      for (let i = this.level; i < newLevel; i++) update[i] = this.head;
      this.level = newLevel;
    }

    const node = new SkipNode(value, newLevel);
    for (let i = 0; i < newLevel; i++) {
      node.forward[i] = update[i]!.forward[i];
      update[i]!.forward[i] = node;
    }
    this._size++;
  }

  search(value: T): T | undefined {
    let cur: SkipNode<T> | null = this.head;
    for (let i = this.level - 1; i >= 0; i--) {
      while (cur!.forward[i] && this.compare(cur!.forward[i]!.value, value) < 0) {
        cur = cur!.forward[i];
      }
    }
    cur = cur!.forward[0];
    if (cur && this.compare(cur.value, value) === 0) return cur.value;
    return undefined;
  }

  delete(value: T): boolean {
    const update: Array<SkipNode<T> | null> = new Array(MAX_LEVEL).fill(null);
    let cur: SkipNode<T> | null = this.head;
    for (let i = this.level - 1; i >= 0; i--) {
      while (cur!.forward[i] && this.compare(cur!.forward[i]!.value, value) < 0) {
        cur = cur!.forward[i];
      }
      update[i] = cur;
    }
    cur = cur!.forward[0];
    if (!cur || this.compare(cur.value, value) !== 0) return false;

    for (let i = 0; i < this.level; i++) {
      if (update[i]!.forward[i] !== cur) break;
      update[i]!.forward[i] = cur.forward[i];
    }
    while (this.level > 1 && !this.head.forward[this.level - 1]) {
      this.level--;
    }
    this._size--;
    return true;
  }

  get size(): number {
    return this._size;
  }

  toArray(): T[] {
    const result: T[] = [];
    let cur = this.head.forward[0];
    while (cur) {
      result.push(cur.value);
      cur = cur.forward[0];
    }
    return result;
  }

  private randomLevel(): number {
    let lvl = 1;
    while (Math.random() < P && lvl < MAX_LEVEL) lvl++;
    return lvl;
  }
}
