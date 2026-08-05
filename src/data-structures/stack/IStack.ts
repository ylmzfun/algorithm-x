export interface Stack<T> {
  push(item: T): void;
  pop(): T | undefined;
  peek(): T | undefined;
  get size(): number;
  isEmpty(): boolean;
}
