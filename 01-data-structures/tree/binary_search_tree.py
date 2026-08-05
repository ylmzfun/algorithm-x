"""
Binary Search Tree (BST) Implementation
=========================================

A binary search tree where for each node:
- All values in the left subtree are less than the node's value.
- All values in the right subtree are greater than the node's value.

Supports: insert, search, delete, min, max, successor, predecessor,
and range queries (inorder traversal within a range).

Time Complexities (average):
    - Search: O(log n)
    - Insert: O(log n)
    - Delete: O(log n)
    - Min/Max: O(log n)
    - Successor/Predecessor: O(log n)

Time Complexities (worst — unbalanced): O(n) for all operations.
Use AVL or Red-Black tree for guaranteed O(log n).

Space Complexity: O(n) for n nodes.
"""

from typing import Any, Optional, List, Iterator


class BSTNode:
    """A node in a binary search tree.

    Attributes:
        data: Value stored in this node.
        left: Left child (values < data).
        right: Right child (values > data).
    """

    def __init__(self, data: Any) -> None:
        """Initialize a BST node.

        Args:
            data: Value to store.
        """
        self.data: Any = data
        self.left: Optional["BSTNode"] = None
        self.right: Optional["BSTNode"] = None

    def __repr__(self) -> str:
        """Return string representation."""
        return f"BSTNode({self.data!r})"


class BinarySearchTree:
    """A binary search tree with standard BST operations.

    Examples:
        >>> bst = BinarySearchTree()
        >>> bst.insert(5)
        >>> bst.insert(3)
        >>> bst.insert(7)
        >>> bst.search(3)
        True
        >>> bst.min()
        3
        >>> bst.max()
        7
        >>> list(bst.range_query(2, 6))
        [3, 5]
    """

    def __init__(self) -> None:
        """Initialize an empty BST."""
        self._root: Optional[BSTNode] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        """Check if tree is empty."""
        return self._root is None

    def size(self) -> int:
        """Return number of nodes."""
        return self._size

    def root(self) -> Optional[BSTNode]:
        """Return root node."""
        return self._root

    # ── Search ────────────────────────────────────────────────────────────────

    def search(self, data: Any) -> bool:
        """Check if `data` exists in the BST.

        Args:
            data: Value to find.

        Returns:
            True if found.

        Time Complexity: O(h) where h is tree height.
        """
        return self._search(self._root, data) is not None

    def _search(self, node: Optional[BSTNode], data: Any) -> Optional[BSTNode]:
        """Recursive search helper. Returns node if found, else None."""
        if node is None or node.data == data:
            return node
        if data < node.data:
            return self._search(node.left, data)
        return self._search(node.right, data)

    # ── Insert ────────────────────────────────────────────────────────────────

    def insert(self, data: Any) -> None:
        """Insert `data` into the BST.

        If `data` already exists, does nothing (no duplicates).

        Args:
            data: Value to insert.

        Time Complexity: O(h)
        """
        self._root = self._insert(self._root, data)

    def _insert(self, node: Optional[BSTNode], data: Any) -> BSTNode:
        """Recursive insert helper."""
        if node is None:
            self._size += 1
            return BSTNode(data)
        if data < node.data:
            node.left = self._insert(node.left, data)
        elif data > node.data:
            node.right = self._insert(node.right, data)
        # data == node.data: do nothing (no duplicates)
        return node

    # ── Delete ────────────────────────────────────────────────────────────────

    def delete(self, data: Any) -> bool:
        """Remove `data` from the BST.

        Three cases:
        1. Node has no children → simply remove.
        2. Node has one child → replace with child.
        3. Node has two children → replace with inorder successor.

        Args:
            data: Value to delete.

        Returns:
            True if deleted, False if not found.

        Time Complexity: O(h)
        """
        prev_size = self._size
        self._root = self._delete(self._root, data)
        return self._size < prev_size

    def _delete(self, node: Optional[BSTNode], data: Any) -> Optional[BSTNode]:
        """Recursive delete helper."""
        if node is None:
            return None

        if data < node.data:
            node.left = self._delete(node.left, data)
        elif data > node.data:
            node.right = self._delete(node.right, data)
        else:
            # Found the node

            # Case 1 & 2: 0 or 1 child
            if node.left is None:
                self._size -= 1
                return node.right
            if node.right is None:
                self._size -= 1
                return node.left

            # Case 3: Two children — replace with inorder successor
            successor = self._min_node(node.right)
            node.data = successor.data
            # Delete the successor (which has at most 1 child).
            # The recursive call will handle size decrement.
            node.right = self._delete(node.right, successor.data)

        return node

    # ── Min / Max ─────────────────────────────────────────────────────────────

    def min(self) -> Optional[Any]:
        """Return the minimum value in the BST.

        Returns:
            Smallest value, or None if empty.

        Time Complexity: O(h)
        """
        node = self._min_node(self._root)
        return node.data if node else None

    def _min_node(self, node: Optional[BSTNode]) -> Optional[BSTNode]:
        """Return the node with minimum value in the subtree."""
        if node is None:
            return None
        while node.left is not None:
            node = node.left
        return node

    def max(self) -> Optional[Any]:
        """Return the maximum value in the BST.

        Returns:
            Largest value, or None if empty.

        Time Complexity: O(h)
        """
        node = self._max_node(self._root)
        return node.data if node else None

    def _max_node(self, node: Optional[BSTNode]) -> Optional[BSTNode]:
        """Return the node with maximum value in the subtree."""
        if node is None:
            return None
        while node.right is not None:
            node = node.right
        return node

    # ── Successor / Predecessor ───────────────────────────────────────────────

    def successor(self, data: Any) -> Optional[Any]:
        """Return the inorder successor of `data` (next larger value).

        Args:
            data: Value whose successor to find.

        Returns:
            Successor value, or None if `data` is the maximum or not found.

        Time Complexity: O(h)
        """
        node = self._search(self._root, data)
        if node is None:
            return None

        # Case 1: Node has right subtree → successor is min of right
        if node.right is not None:
            return self._min_node(node.right).data

        # Case 2: No right subtree → go up to find first ancestor
        # where node is in the left subtree
        succ: Optional[BSTNode] = None
        current = self._root
        while current is not None:
            if data < current.data:
                succ = current
                current = current.left
            elif data > current.data:
                current = current.right
            else:
                break

        return succ.data if succ else None

    def predecessor(self, data: Any) -> Optional[Any]:
        """Return the inorder predecessor of `data` (next smaller value).

        Args:
            data: Value whose predecessor to find.

        Returns:
            Predecessor value, or None if `data` is minimum or not found.

        Time Complexity: O(h)
        """
        node = self._search(self._root, data)
        if node is None:
            return None

        # Case 1: Node has left subtree → predecessor is max of left
        if node.left is not None:
            return self._max_node(node.left).data

        # Case 2: No left subtree → go up to find first ancestor
        # where node is in the right subtree
        pred: Optional[BSTNode] = None
        current = self._root
        while current is not None:
            if data > current.data:
                pred = current
                current = current.right
            elif data < current.data:
                current = current.left
            else:
                break

        return pred.data if pred else None

    # ── Range Query ───────────────────────────────────────────────────────────

    def range_query(self, low: Any, high: Any) -> Iterator[Any]:
        """Yield all values in the range [low, high] in sorted order.

        Uses an optimized inorder traversal that prunes subtrees.

        Args:
            low: Lower bound (inclusive).
            high: Upper bound (inclusive).

        Yields:
            Values within [low, high] in ascending order.

        Time Complexity: O(k + h) where k = number of values in range,
                         h = tree height.
        """

        def _range(node: Optional[BSTNode]) -> Iterator[Any]:
            if node is None:
                return
            if node.data > low:
                yield from _range(node.left)
            if low <= node.data <= high:
                yield node.data
            if node.data < high:
                yield from _range(node.right)

        yield from _range(self._root)

    # ── Traversals ────────────────────────────────────────────────────────────

    def inorder(self) -> List[Any]:
        """In-order traversal (sorted order for BST).

        Returns:
            List of values in sorted order.

        Time Complexity: O(n)
        """
        result: List[Any] = []

        def _traverse(node: Optional[BSTNode]) -> None:
            if node is None:
                return
            _traverse(node.left)
            result.append(node.data)
            _traverse(node.right)

        _traverse(self._root)
        return result

    # ── Dunder ───────────────────────────────────────────────────────────────

    def __contains__(self, data: Any) -> bool:
        """Support `in` operator."""
        return self.search(data)

    def __len__(self) -> int:
        """Support len()."""
        return self._size

    def __iter__(self) -> Iterator[Any]:
        """Yield values in sorted order."""
        yield from self.inorder()

    def __str__(self) -> str:
        """Return string representation."""
        return str(self.inorder())

    def __repr__(self) -> str:
        """Return detailed representation."""
        return f"BinarySearchTree(size={self._size})"


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

    # ── Creation ──────────────────────────────────────────────────────────────
    print("Creation:")
    bst = BinarySearchTree()
    check("empty is_empty", bst.is_empty())
    check("empty size == 0", bst.size() == 0)

    # ── Insert ────────────────────────────────────────────────────────────────
    print("\nInsert:")
    for val in [5, 3, 7, 2, 4, 6, 8]:
        bst.insert(val)
    check("size after 7 inserts", bst.size() == 7)
    check("inorder sorted", bst.inorder() == [2, 3, 4, 5, 6, 7, 8])

    # Duplicate
    bst.insert(5)
    check("duplicate not added", bst.size() == 7)

    # ── Search ────────────────────────────────────────────────────────────────
    print("\nSearch:")
    check("search(5) True", bst.search(5))
    check("search(2) True", bst.search(2))
    check("search(8) True", bst.search(8))
    check("search(10) False", not bst.search(10))
    check("search(0) False", not bst.search(0))

    # ── Min / Max ─────────────────────────────────────────────────────────────
    print("\nMin/Max:")
    check("min == 2", bst.min() == 2)
    check("max == 8", bst.max() == 8)

    empty_bst = BinarySearchTree()
    check("empty min None", empty_bst.min() is None)
    check("empty max None", empty_bst.max() is None)

    # ── Successor / Predecessor ───────────────────────────────────────────────
    print("\nSuccessor/Predecessor:")
    check("successor(2) == 3", bst.successor(2) == 3)
    check("successor(4) == 5", bst.successor(4) == 5)
    check("successor(7) == 8", bst.successor(7) == 8)
    check("successor(8) None", bst.successor(8) is None)
    check("predecessor(3) == 2", bst.predecessor(3) == 2)
    check("predecessor(5) == 4", bst.predecessor(5) == 4)
    check("predecessor(8) == 7", bst.predecessor(8) == 7)
    check("predecessor(2) None", bst.predecessor(2) is None)

    # ── Range Query ───────────────────────────────────────────────────────────
    print("\nRange Query:")
    check("range [4,6]", list(bst.range_query(4, 6)) == [4, 5, 6])
    check("range [2,2]", list(bst.range_query(2, 2)) == [2])
    check("range [0,100]", list(bst.range_query(0, 100)) == [2, 3, 4, 5, 6, 7, 8])
    check("range [9,10] empty", list(bst.range_query(9, 10)) == [])

    # ── Delete ────────────────────────────────────────────────────────────────
    print("\nDelete:")
    # Delete leaf (2)
    check("delete(2) True", bst.delete(2))
    check("2 removed", not bst.search(2))
    check("size after delete(2)", bst.size() == 6)

    # Delete node with one child — 3 now has only right child 4
    # Actually after removing 2, 3 has 4 as left child... Let me recheck
    # Tree was: [5, 3, 7, 2, 4, 6, 8]. After deleting 2: [3,4,5,6,7,8]
    # Delete 3 (has right child 4)
    check("delete(3) True", bst.delete(3))
    check("3 removed", not bst.search(3))
    check("4 still present", bst.search(4))
    check("size after delete(3)", bst.size() == 5)

    # Delete node with two children (5)
    check("delete(5) True", bst.delete(5))
    check("5 removed", not bst.search(5))
    check("size after delete(5)", bst.size() == 4)
    check("tree still valid", bst.inorder() == [4, 6, 7, 8])

    # Delete non-existent
    check("delete(99) False", bst.delete(99) is False)

    # ── Iteration ─────────────────────────────────────────────────────────────
    print("\nIteration:")
    check("iterator gives sorted", list(iter(bst)) == [4, 6, 7, 8])

    # ── Summary ───────────────────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
