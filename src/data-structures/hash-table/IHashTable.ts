export interface HashTable<K, V> {
  put(key: K, value: V): void;
  get(key: K): V | undefined;
  remove(key: K): boolean;
  containsKey(key: K): boolean;
  get size(): number;
}
