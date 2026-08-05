"""
Trie (Prefix Tree) Implementation
===================================

A trie is a tree-like data structure for efficient storage and retrieval
of strings, especially for prefix-based operations.

Each node stores:
    - children: Dict mapping characters to child nodes.
    - is_end: Whether this node marks the end of a word.
    - count: Number of words passing through this node (prefix count).

Operations:
    - insert(word): Add a word to the trie.
    - search(word): Check if a word exists.
    - starts_with(prefix): Check if any word starts with a prefix.
    - delete(word): Remove a word.
    - count_prefixes(prefix): Count words with a given prefix.

Time Complexities:
    - insert: O(L) where L = word length
    - search: O(L)
    - starts_with: O(L)
    - delete: O(L)
    - count_prefixes: O(P) where P = prefix length

Space Complexity: O(N * L) in worst case, where N = number of words,
L = average length (but much less with common prefixes).
"""

from typing import Any, Dict, Iterator, List, Optional


class TrieNode:
    """A node in the trie.

    Attributes:
        children: Dict mapping character → child TrieNode.
        is_end: True if this node is the end of a complete word.
        count: Number of words that pass through this node (prefix count).
    """

    def __init__(self) -> None:
        """Initialize an empty trie node."""
        self.children: Dict[str, "TrieNode"] = {}
        self.is_end: bool = False
        self.count: int = 0  # How many words pass through this node

    def __repr__(self) -> str:
        return f"TrieNode(children={list(self.children.keys())}, is_end={self.is_end})"


class Trie:
    """A prefix tree (trie) for storing and querying strings.

    Examples:
        >>> t = Trie()
        >>> t.insert("apple")
        >>> t.search("apple")
        True
        >>> t.search("app")
        False
        >>> t.starts_with("app")
        True
        >>> t.insert("app")
        >>> t.search("app")
        True
        >>> t.count_prefixes("app")
        2
        >>> t.delete("app")
        True
        >>> t.search("app")
        False
    """

    def __init__(self) -> None:
        """Initialize an empty trie with a root node."""
        self._root: TrieNode = TrieNode()
        self._word_count: int = 0

    def size(self) -> int:
        """Return number of unique words stored.

        Returns:
            Count of complete words.

        Time Complexity: O(1)
        """
        return self._word_count

    def is_empty(self) -> bool:
        """Check if trie is empty."""
        return self._word_count == 0

    def insert(self, word: str) -> None:
        """Insert `word` into the trie.

        Increments prefix counts along the path.

        Args:
            word: String to insert (case-sensitive).

        Time Complexity: O(L) where L = len(word)
        """
        node = self._root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.count += 1

        if not node.is_end:
            node.is_end = True
            self._word_count += 1

    def search(self, word: str) -> bool:
        """Check if `word` exists as a complete word in the trie.

        Args:
            word: String to search for.

        Returns:
            True if the exact word was inserted.

        Time Complexity: O(L)
        """
        node = self._find_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        """Check if any word in the trie starts with `prefix`.

        Args:
            prefix: Prefix string to check.

        Returns:
            True if at least one word has this prefix.

        Time Complexity: O(P) where P = len(prefix)
        """
        return self._find_node(prefix) is not None

    def count_prefixes(self, prefix: str) -> int:
        """Count how many words have `prefix` as their prefix.

        Args:
            prefix: Prefix to count.

        Returns:
            Number of words starting with `prefix`.

        Time Complexity: O(P)
        """
        node = self._find_node(prefix)
        return node.count if node else 0

    def delete(self, word: str) -> bool:
        """Remove `word` from the trie.

        Decrements prefix counts along the path. If a node becomes
        unused (count == 0 and no children), it's removed.

        Args:
            word: String to remove.

        Returns:
            True if the word was found and deleted, False otherwise.

        Time Complexity: O(L)
        """
        if not self.search(word):
            return False

        self._word_count -= 1
        self._delete(self._root, word, 0)
        return True

    def _delete(self, node: TrieNode, word: str, depth: int) -> bool:
        """Recursive delete helper.

        Returns True if parent should delete the child node.
        """
        if depth == len(word):
            # Reached the end node. Count was already decremented by parent.
            node.is_end = False
            return len(node.children) == 0 and node.count == 0

        ch = word[depth]
        child = node.children[ch]
        child.count -= 1

        should_delete = self._delete(child, word, depth + 1)

        if should_delete:
            del node.children[ch]
            return len(node.children) == 0 and not node.is_end and node.count == 0

        return False

    def _find_node(self, s: str) -> Optional[TrieNode]:
        """Traverse to the node for string `s`, or None if not present."""
        node = self._root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def get_all_words(self) -> List[str]:
        """Return all words stored in the trie.

        Returns:
            List of all words in lexicographic order (DFS).

        Time Complexity: O(N * L) where N = number of words.
        """
        result: List[str] = []

        def _collect(node: TrieNode, prefix: str) -> None:
            if node.is_end:
                result.append(prefix)
            for ch in sorted(node.children.keys()):
                _collect(node.children[ch], prefix + ch)

        _collect(self._root, "")
        return result

    def get_words_with_prefix(self, prefix: str) -> List[str]:
        """Return all words that start with `prefix`.

        Args:
            prefix: Prefix to filter by.

        Returns:
            List of matching words in lexicographic order.

        Time Complexity: O(P + K) where K = number of matching words.
        """
        node = self._find_node(prefix)
        if node is None:
            return []

        result: List[str] = []

        def _collect(n: TrieNode, curr: str) -> None:
            if n.is_end:
                result.append(curr)
            for ch in sorted(n.children.keys()):
                _collect(n.children[ch], curr + ch)

        _collect(node, prefix)
        return result

    def __contains__(self, word: str) -> bool:
        """Support `in` operator."""
        return self.search(word)

    def __len__(self) -> int:
        """Support len()."""
        return self._word_count

    def __iter__(self) -> Iterator[str]:
        """Yield all words."""
        yield from self.get_all_words()

    def __str__(self) -> str:
        return str(self.get_all_words())

    def __repr__(self) -> str:
        return f"Trie(words={self._word_count})"


# ─── Tests ────────────────────────────────────────────────────────────────────


def _run_tests() -> None:
    """Run all tests and report results."""
    import sys

    passed = 0
    failed = 0

    def check(description: str, condition: bool) -> None:
        nonlocal passed, failed
        if condition:
            passed += 1
            print(f"  ✓ {description}")
        else:
            failed += 1
            print(f"  ✗ {description}", file=sys.stderr)

    # ── Basic operations ──────────────────────────────────────────────────────
    print("Basic operations:")
    t = Trie()
    check("empty size", t.size() == 0)
    check("empty is_empty", t.is_empty())

    t.insert("apple")
    t.insert("app")
    t.insert("application")
    t.insert("banana")
    t.insert("band")
    check("size after inserts", t.size() == 5)

    # ── Search ────────────────────────────────────────────────────────────────
    print("\nSearch:")
    check("search 'apple'", t.search("apple"))
    check("search 'app'", t.search("app"))
    check("search 'application'", t.search("application"))
    check("search 'banana'", t.search("banana"))
    check("not search 'ap'", not t.search("ap"))
    check("not search 'appl'", not t.search("appl"))
    check("not search 'bandana'", not t.search("bandana"))

    # ── Starts with ──────────────────────────────────────────────────────────
    print("\nStarts with:")
    check("starts_with 'app'", t.starts_with("app"))
    check("starts_with 'ban'", t.starts_with("ban"))
    check("starts_with 'ba'", t.starts_with("ba"))
    check("not starts_with 'cat'", not t.starts_with("cat"))
    check("not starts_with 'xyz'", not t.starts_with("xyz"))

    # ── Count prefixes ───────────────────────────────────────────────────────
    print("\nCount prefixes:")
    check("count 'app' == 3", t.count_prefixes("app") == 3)
    check("count 'appl' == 2", t.count_prefixes("appl") == 2)
    check("count 'b' == 2", t.count_prefixes("b") == 2)
    check("count 'ban' == 2", t.count_prefixes("ban") == 2)
    check("count 'xyz' == 0", t.count_prefixes("xyz") == 0)

    # ── Delete ────────────────────────────────────────────────────────────────
    print("\nDelete:")
    check("delete 'app' True", t.delete("app"))
    check("search 'app' False after delete", not t.search("app"))
    check("search 'apple' still True", t.search("apple"))
    check("count_prefixes 'app' == 2", t.count_prefixes("app") == 2)
    check("size after delete", t.size() == 4)
    check("delete non-existent False", not t.delete("xyz"))

    # ── Get all words ────────────────────────────────────────────────────────
    print("\nGet all words:")
    words = t.get_all_words()
    check("all words sorted", words == ["apple", "application", "banana", "band"])

    # Prefix search
    check("prefix 'ban'", t.get_words_with_prefix("ban") == ["banana", "band"])
    check("prefix 'apple'", t.get_words_with_prefix("apple") == ["apple"])
    check("prefix 'xyz'", t.get_words_with_prefix("xyz") == [])

    # ── Iteration / contains ─────────────────────────────────────────────────
    print("\nIteration/contains:")
    check("'apple' in t", "apple" in t)
    check("'app' not in t", "app" not in t)
    check("len(t) == 4", len(t) == 4)
    all_words = list(iter(t))
    check("iterator gives 4 words", len(all_words) == 4)

    # ── Edge cases ───────────────────────────────────────────────────────────
    print("\nEdge cases:")
    t2 = Trie()
    t2.insert("")
    check("empty string search", t2.search(""))
    check("empty string starts_with", t2.starts_with(""))
    check("size with empty string", t2.size() == 1)

    # ── Summary ───────────────────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
