export class AVLTreeNode<T> {
  height = 1;
  left: AVLTreeNode<T> | null = null;
  right: AVLTreeNode<T> | null = null;

  constructor(public value: T) {}
}

export class AVLTree<T> {
  root: AVLTreeNode<T> | null = null;
  private _size = 0;
  private compare: (a: T, b: T) => number;

  constructor(compare?: (a: T, b: T) => number) {
    this.compare = compare ?? ((a, b) => (a as unknown as number) - (b as unknown as number));
  }

  insert(value: T): void {
    this.root = this._insert(this.root, value);
    this._size++;
  }

  delete(value: T): boolean {
    const before = this._size;
    this.root = this._delete(this.root, value);
    return this._size !== before;
  }

  contains(value: T): boolean {
    return this._search(this.root, value) !== null;
  }

  get size(): number {
    return this._size;
  }

  private height(node: AVLTreeNode<T> | null): number {
    return node ? node.height : 0;
  }

  private balanceFactor(node: AVLTreeNode<T>): number {
    return this.height(node.left) - this.height(node.right);
  }

  private updateHeight(node: AVLTreeNode<T>): void {
    node.height = 1 + Math.max(this.height(node.left), this.height(node.right));
  }

  private rotateRight(y: AVLTreeNode<T>): AVLTreeNode<T> {
    const x = y.left!;
    const T2 = x.right;
    x.right = y;
    y.left = T2;
    this.updateHeight(y);
    this.updateHeight(x);
    return x;
  }

  private rotateLeft(x: AVLTreeNode<T>): AVLTreeNode<T> {
    const y = x.right!;
    const T2 = y.left;
    y.left = x;
    x.right = T2;
    this.updateHeight(x);
    this.updateHeight(y);
    return y;
  }

  private balance(node: AVLTreeNode<T>): AVLTreeNode<T> {
    this.updateHeight(node);
    const bf = this.balanceFactor(node);
    // LL
    if (bf > 1 && this.balanceFactor(node.left!) >= 0) return this.rotateRight(node);
    // LR
    if (bf > 1 && this.balanceFactor(node.left!) < 0) {
      node.left = this.rotateLeft(node.left!);
      return this.rotateRight(node);
    }
    // RR
    if (bf < -1 && this.balanceFactor(node.right!) <= 0) return this.rotateLeft(node);
    // RL
    if (bf < -1 && this.balanceFactor(node.right!) > 0) {
      node.right = this.rotateRight(node.right!);
      return this.rotateLeft(node);
    }
    return node;
  }

  private _insert(node: AVLTreeNode<T> | null, value: T): AVLTreeNode<T> {
    if (!node) return new AVLTreeNode(value);
    const cmp = this.compare(value, node.value);
    if (cmp < 0) node.left = this._insert(node.left, value);
    else if (cmp > 0) node.right = this._insert(node.right, value);
    else {
      node.value = value;
      this._size--;
      return node;
    }
    return this.balance(node);
  }

  private _delete(node: AVLTreeNode<T> | null, value: T): AVLTreeNode<T> | null {
    if (!node) return null;
    const cmp = this.compare(value, node.value);
    if (cmp < 0) {
      node.left = this._delete(node.left, value);
    } else if (cmp > 0) {
      node.right = this._delete(node.right, value);
    } else {
      this._size--;
      if (!node.left || !node.right) {
        return node.left ?? node.right;
      }
      const min = this._min(node.right);
      node.value = min.value;
      node.right = this._delete(node.right, min.value);
    }
    return node ? this.balance(node) : null;
  }

  private _min(node: AVLTreeNode<T>): AVLTreeNode<T> {
    while (node.left) node = node.left;
    return node;
  }

  private _search(node: AVLTreeNode<T> | null, value: T): AVLTreeNode<T> | null {
    if (!node) return null;
    const cmp = this.compare(value, node.value);
    if (cmp === 0) return node;
    return cmp < 0 ? this._search(node.left, value) : this._search(node.right, value);
  }

  inorder(): T[] {
    const result: T[] = [];
    this._inorder(this.root, result);
    return result;
  }

  private _inorder(node: AVLTreeNode<T> | null, out: T[]): void {
    if (!node) return;
    this._inorder(node.left, out);
    out.push(node.value);
    this._inorder(node.right, out);
  }
}
