export class TreeNode<T> {
  constructor(
    public value: T,
    public left: TreeNode<T> | null = null,
    public right: TreeNode<T> | null = null,
  ) {}
}

export class BinarySearchTree<T> {
  root: TreeNode<T> | null = null;
  private _size = 0;
  private compare: (a: T, b: T) => number;

  constructor(compare?: (a: T, b: T) => number) {
    this.compare = compare ?? ((a, b) => (a as unknown as number) - (b as unknown as number));
  }

  insert(value: T): void {
    const inserted = { count: 0 };
    this.root = this._insert(this.root, value, inserted);
    this._size += inserted.count;
  }

  private _insert(node: TreeNode<T> | null, value: T, inserted: { count: number }): TreeNode<T> {
    if (!node) {
      inserted.count = 1;
      return new TreeNode(value);
    }
    const cmp = this.compare(value, node.value);
    if (cmp < 0) node.left = this._insert(node.left, value, inserted);
    else if (cmp > 0) node.right = this._insert(node.right, value, inserted);
    else node.value = value; // duplicate: overwrite, count stays 0
    return node;
  }

  search(value: T): TreeNode<T> | null {
    let node = this.root;
    while (node) {
      const cmp = this.compare(value, node.value);
      if (cmp === 0) return node;
      node = cmp < 0 ? node.left : node.right;
    }
    return null;
  }

  contains(value: T): boolean {
    return this.search(value) !== null;
  }

  delete(value: T): boolean {
    if (!this.root) return false;
    const before = this._size;
    this.root = this._delete(this.root, value);
    return this._size !== before;
  }

  private _delete(node: TreeNode<T> | null, value: T): TreeNode<T> | null {
    if (!node) return null;
    const cmp = this.compare(value, node.value);
    if (cmp < 0) {
      node.left = this._delete(node.left, value);
    } else if (cmp > 0) {
      node.right = this._delete(node.right, value);
    } else {
      this._size--;
      if (!node.left) return node.right;
      if (!node.right) return node.left;
      const min = this._minNode(node.right);
      node.value = min.value;
      node.right = this._deleteMin(node.right);
    }
    return node;
  }

  private _minNode(node: TreeNode<T>): TreeNode<T> {
    while (node.left) node = node.left;
    return node;
  }

  private _deleteMin(node: TreeNode<T>): TreeNode<T> | null {
    if (!node.left) return node.right;
    node.left = this._deleteMin(node.left);
    return node;
  }

  get size(): number {
    return this._size;
  }

  // 遍历
  inorder(): T[] {
    const result: T[] = [];
    this._inorder(this.root, result);
    return result;
  }

  private _inorder(node: TreeNode<T> | null, out: T[]): void {
    if (!node) return;
    this._inorder(node.left, out);
    out.push(node.value);
    this._inorder(node.right, out);
  }

  preorder(): T[] {
    const result: T[] = [];
    this._preorder(this.root, result);
    return result;
  }

  private _preorder(node: TreeNode<T> | null, out: T[]): void {
    if (!node) return;
    out.push(node.value);
    this._preorder(node.left, out);
    this._preorder(node.right, out);
  }

  postorder(): T[] {
    const result: T[] = [];
    this._postorder(this.root, result);
    return result;
  }

  private _postorder(node: TreeNode<T> | null, out: T[]): void {
    if (!node) return;
    this._postorder(node.left, out);
    this._postorder(node.right, out);
    out.push(node.value);
  }

  levelOrder(): T[] {
    if (!this.root) return [];
    const result: T[] = [];
    const q = [this.root];
    while (q.length > 0) {
      const node = q.shift()!;
      result.push(node.value);
      if (node.left) q.push(node.left);
      if (node.right) q.push(node.right);
    }
    return result;
  }
}
