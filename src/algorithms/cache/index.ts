// LRU (Least Recently Used)
export class LRUCache<K, V> {
  private map = new Map<K, V>();
  private capacity: number;

  constructor(capacity: number) {
    this.capacity = capacity;
  }

  get(key: K): V | undefined {
    if (!this.map.has(key)) return undefined;
    const value = this.map.get(key)!;
    // JS Map 保证插入顺序 —— 移到末尾
    this.map.delete(key);
    this.map.set(key, value);
    return value;
  }

  put(key: K, value: V): void {
    if (this.map.has(key)) this.map.delete(key);
    else if (this.map.size >= this.capacity) {
      // 删除最旧的（第一个插入的）
      const oldest = this.map.keys().next().value;
      if (oldest !== undefined) this.map.delete(oldest);
    }
    this.map.set(key, value);
  }

  get size(): number {
    return this.map.size;
  }
}

// LFU (Least Frequently Used)
export class LFUCache<K, V> {
  private keyMap = new Map<K, { value: V; freq: number }>();
  private freqMap = new Map<number, Set<K>>();
  private capacity: number;
  private minFreq = 0;

  constructor(capacity: number) {
    this.capacity = capacity;
  }

  get(key: K): V | undefined {
    if (!this.keyMap.has(key)) return undefined;
    const entry = this.keyMap.get(key)!;
    this.updateFreq(key, entry.freq, entry.freq + 1);
    entry.freq++;
    return entry.value;
  }

  put(key: K, value: V): void {
    if (this.capacity === 0) return;

    if (this.keyMap.has(key)) {
      const entry = this.keyMap.get(key)!;
      entry.value = value;
      this.updateFreq(key, entry.freq, entry.freq + 1);
      entry.freq++;
      return;
    }

    if (this.keyMap.size >= this.capacity) {
      const minSet = this.freqMap.get(this.minFreq)!;
      const evict = minSet.values().next().value;
      if (evict !== undefined) {
        minSet.delete(evict);
        this.keyMap.delete(evict);
      }
    }

    this.keyMap.set(key, { value, freq: 1 });
    if (!this.freqMap.has(1)) this.freqMap.set(1, new Set());
    this.freqMap.get(1)!.add(key);
    this.minFreq = 1;
  }

  private updateFreq(key: K, oldFreq: number, newFreq: number) {
    this.freqMap.get(oldFreq)!.delete(key);
    if (this.freqMap.get(oldFreq)!.size === 0) {
      this.freqMap.delete(oldFreq);
      if (oldFreq === this.minFreq) this.minFreq++;
    }
    if (!this.freqMap.has(newFreq)) this.freqMap.set(newFreq, new Set());
    this.freqMap.get(newFreq)!.add(key);
  }

  get size(): number {
    return this.keyMap.size;
  }
}
