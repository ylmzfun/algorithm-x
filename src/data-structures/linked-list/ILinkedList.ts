export interface LinkedList<T> {
  prepend(item: T): void;
  append(item: T): void;
  delete(item: T): boolean;
  find(predicate: (item: T) => boolean): T | undefined;
  get size(): number;
  isEmpty(): boolean;
  toArray(): T[];
}
