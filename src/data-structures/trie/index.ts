class TrieNode {
  children: Map<string, TrieNode> = new Map();
  isEnd = false;
}

export class Trie {
  private root = new TrieNode();

  insert(word: string): void {
    let node = this.root;
    for (const ch of word) {
      if (!node.children.has(ch)) node.children.set(ch, new TrieNode());
      node = node.children.get(ch)!;
    }
    node.isEnd = true;
  }

  search(word: string): boolean {
    const node = this._find(word);
    return node !== null && node.isEnd;
  }

  startsWith(prefix: string): boolean {
    return this._find(prefix) !== null;
  }

  delete(word: string): boolean {
    return this._delete(this.root, word, 0);
  }

  private _delete(node: TrieNode, word: string, depth: number): boolean {
    if (depth === word.length) {
      if (!node.isEnd) return false;
      node.isEnd = false;
      return true;
    }
    const ch = word[depth];
    const child = node.children.get(ch);
    if (!child) return false;
    const found = this._delete(child, word, depth + 1);
    if (found && child.children.size === 0 && !child.isEnd) {
      node.children.delete(ch);
    }
    return found;
  }

  private _find(word: string): TrieNode | null {
    let node = this.root;
    for (const ch of word) {
      if (!node.children.has(ch)) return null;
      node = node.children.get(ch)!;
    }
    return node;
  }

  getAllWords(): string[] {
    const result: string[] = [];
    this._collect(this.root, '', result);
    return result;
  }

  private _collect(node: TrieNode, prefix: string, out: string[]): void {
    if (node.isEnd) out.push(prefix);
    for (const [ch, child] of node.children) {
      this._collect(child, prefix + ch, out);
    }
  }
}
