import type { HashTable } from './IHashTable';

class Entry<K, V> {
  constructor(
    public key: K,
    public value: V,
    public next: Entry<K, V> | null = null,
  ) {}
}

export class SeparateChainingHashTable<K, V> implements HashTable<K, V> {
  private table: Array<Entry<K, V> | null>;
  private _size = 0;

  constructor(capacity = 16) {
    this.table = new Array(capacity).fill(null);
  }

  private hash(key: K): number {
    const str = String(key);
    let h = 0;
    for (let i = 0; i < str.length; i++) {
      h = (h * 31 + str.charCodeAt(i)) | 0;
    }
    return Math.abs(h) % this.table.length;
  }

  put(key: K, value: V): void {
    const idx = this.hash(key);
    let entry = this.table[idx];
    while (entry) {
      if (entry.key === key) {
        entry.value = value;
        return;
      }
      entry = entry.next;
    }
    this.table[idx] = new Entry(key, value, this.table[idx]);
    this._size++;
    if (this._size / this.table.length > 0.75) this.resize(this.table.length * 2);
  }

  get(key: K): V | undefined {
    const idx = this.hash(key);
    let entry = this.table[idx];
    while (entry) {
      if (entry.key === key) return entry.value;
      entry = entry.next;
    }
    return undefined;
  }

  remove(key: K): boolean {
    const idx = this.hash(key);
    let entry = this.table[idx];
    let prev: Entry<K, V> | null = null;
    while (entry) {
      if (entry.key === key) {
        if (prev) prev.next = entry.next;
        else this.table[idx] = entry.next;
        this._size--;
        return true;
      }
      prev = entry;
      entry = entry.next;
    }
    return false;
  }

  containsKey(key: K): boolean {
    return this.get(key) !== undefined;
  }

  get size(): number {
    return this._size;
  }

  private resize(newCapacity: number): void {
    const oldTable = this.table;
    this.table = new Array(newCapacity).fill(null);
    this._size = 0;
    for (const head of oldTable) {
      let entry = head;
      while (entry) {
        this.put(entry.key, entry.value);
        entry = entry.next;
      }
    }
  }
}
