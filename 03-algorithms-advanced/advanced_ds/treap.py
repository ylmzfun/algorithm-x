"""
Treap — a randomized binary search tree.

Combines BST (by key) with max-heap (by random priority), yielding
expected O(log n) height and O(log n) for all operations.

Supports:
- insert, delete, search
- split (by key), merge
- kth smallest element, order of a key
- In-order traversal
"""

import random
from typing import List, Optional, Tuple


class TreapNode:
    """A node in the Treap."""

    __slots__ = ("key", "priority", "size", "left", "right")

    def __init__(self, key: int) -> None:
        self.key = key
        self.priority = random.random()
        self.size = 1
        self.left: Optional["TreapNode"] = None
        self.right: Optional["TreapNode"] = None


class Treap:
    """
    Treap (Tree + Heap): a randomized BST.

    All operations have expected O(log n) time.
    """

    def __init__(self) -> None:
        """Create an empty Treap."""
        self.root: Optional[TreapNode] = None

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _size(node: Optional[TreapNode]) -> int:
        return node.size if node else 0

    @staticmethod
    def _update(node: TreapNode) -> None:
        """Recalculate size after children change."""
        node.size = 1 + Treap._size(node.left) + Treap._size(node.right)

    # ------------------------------------------------------------------
    # Split: splits tree into (≤ key, > key)
    # ------------------------------------------------------------------

    def _split(
        self, node: Optional[TreapNode], key: int
    ) -> Tuple[Optional[TreapNode], Optional[TreapNode]]:
        """
        Split the subtree rooted at `node` into two treaps:
          left:  all elements with key ≤ key
          right: all elements with key > key

        Args:
            node: Root of the subtree.
            key: Split key.

        Returns:
            (left_root, right_root).

        Time: O(log n) expected
        """
        if node is None:
            return None, None

        if node.key <= key:
            left, right = self._split(node.right, key)
            node.right = left
            self._update(node)
            return node, right
        else:
            left, right = self._split(node.left, key)
            node.left = right
            self._update(node)
            return left, node

    # ------------------------------------------------------------------
    # Merge: combines two treaps (all keys in left ≤ all keys in right)
    # ------------------------------------------------------------------

    def _merge(
        self, left: Optional[TreapNode], right: Optional[TreapNode]
    ) -> Optional[TreapNode]:
        """
        Merge two treaps where all keys in `left` ≤ all keys in `right`.

        Args:
            left: First treap (smaller keys).
            right: Second treap (larger keys).

        Returns:
            Root of the merged treap.

        Time: O(log n) expected
        """
        if left is None:
            return right
        if right is None:
            return left

        if left.priority > right.priority:
            left.right = self._merge(left.right, right)
            self._update(left)
            return left
        else:
            right.left = self._merge(left, right.left)
            self._update(right)
            return right

    # ------------------------------------------------------------------
    # Insert
    # ------------------------------------------------------------------

    def insert(self, key: int) -> None:
        """
        Insert a key into the Treap.  Duplicates are allowed.

        Args:
            key: The key to insert.

        Time: O(log n) expected
        """
        if self.search(key):
            # Duplicate — allow it by inserting to the right of equal keys
            pass
        left, right = self._split(self.root, key)
        new_node = TreapNode(key)
        self.root = self._merge(self._merge(left, new_node), right)

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    def delete(self, key: int) -> bool:
        """
        Delete one occurrence of key from the Treap.

        Args:
            key: The key to delete.

        Returns:
            True if the key was found and deleted, False otherwise.

        Time: O(log n) expected
        """
        if not self.search(key):
            return False
        left, mid = self._split(self.root, key - 1)
        mid, right = self._split(mid, key)
        # mid now contains all nodes with key == key (for duplicates)
        # Delete the root of mid (one occurrence)
        if mid is not None:
            mid = self._merge(mid.left, mid.right)
        self.root = self._merge(self._merge(left, mid), right)
        return True

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(self, key: int) -> bool:
        """
        Check whether the given key exists in the Treap.

        Args:
            key: The key to search for.

        Returns:
            True if the key is present, False otherwise.

        Time: O(log n) expected
        """
        return self._search(self.root, key)

    def _search(self, node: Optional[TreapNode], key: int) -> bool:
        if node is None:
            return False
        if node.key == key:
            return True
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    # ------------------------------------------------------------------
    # kth smallest element
    # ------------------------------------------------------------------

    def kth(self, k: int) -> Optional[int]:
        """
        Return the k-th smallest element (1-indexed).

        Args:
            k: 1-based rank.

        Returns:
            The k-th smallest key, or None if k is out of range.

        Time: O(log n) expected
        """
        if k < 1 or k > self._size(self.root):
            return None
        return self._kth(self.root, k)

    def _kth(self, node: Optional[TreapNode], k: int) -> Optional[int]:
        if node is None:
            return None
        left_size = self._size(node.left)
        if k <= left_size:
            return self._kth(node.left, k)
        elif k == left_size + 1:
            return node.key
        else:
            return self._kth(node.right, k - left_size - 1)

    # ------------------------------------------------------------------
    # Order of key (number of elements strictly less than key)
    # ------------------------------------------------------------------

    def order_of_key(self, key: int) -> int:
        """
        Return the number of elements strictly less than the given key.

        Args:
            key: The key.

        Returns:
            Count of elements < key.

        Time: O(log n) expected
        """
        return self._order_of_key(self.root, key)

    def _order_of_key(self, node: Optional[TreapNode], key: int) -> int:
        if node is None:
            return 0
        if key <= node.key:
            return self._order_of_key(node.left, key)
        else:
            return self._size(node.left) + 1 + self._order_of_key(node.right, key)

    # ------------------------------------------------------------------
    # Size
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        """Return the number of elements in the Treap."""
        return self._size(self.root)

    # ------------------------------------------------------------------
    # In-order traversal
    # ------------------------------------------------------------------

    def inorder(self) -> List[int]:
        """
        Return all keys in sorted order.

        Returns:
            List of keys in ascending order.

        Time: O(n)
        """
        result: List[int] = []

        def dfs(node: Optional[TreapNode]) -> None:
            if node:
                dfs(node.left)
                result.append(node.key)
                dfs(node.right)

        dfs(self.root)
        return result


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    import sys

    all_pass = True

    treap = Treap()

    # Insert
    for v in [5, 2, 8, 1, 3, 7, 9]:
        treap.insert(v)

    if len(treap) != 7:
        print(f"FAIL size: {len(treap)}")
        all_pass = False

    # Search
    if not treap.search(5):
        print("FAIL search 5")
        all_pass = False
    if treap.search(10):
        print("FAIL search 10")
        all_pass = False

    # Inorder
    if treap.inorder() != [1, 2, 3, 5, 7, 8, 9]:
        print(f"FAIL inorder: {treap.inorder()}")
        all_pass = False

    # kth
    if treap.kth(1) != 1:
        print(f"FAIL kth 1: {treap.kth(1)}")
        all_pass = False
    if treap.kth(4) != 5:
        print(f"FAIL kth 4: {treap.kth(4)}")
        all_pass = False
    if treap.kth(7) != 9:
        print(f"FAIL kth 7: {treap.kth(7)}")
        all_pass = False
    if treap.kth(0) is not None:
        print(f"FAIL kth 0: {treap.kth(0)}")
        all_pass = False
    if treap.kth(8) is not None:
        print(f"FAIL kth 8: {treap.kth(8)}")
        all_pass = False

    # order_of_key
    if treap.order_of_key(1) != 0:
        print(f"FAIL order 1: {treap.order_of_key(1)}")
        all_pass = False
    if treap.order_of_key(5) != 3:
        print(f"FAIL order 5: {treap.order_of_key(5)}")
        all_pass = False
    if treap.order_of_key(9) != 6:
        print(f"FAIL order 9: {treap.order_of_key(9)}")
        all_pass = False
    if treap.order_of_key(10) != 7:
        print(f"FAIL order 10: {treap.order_of_key(10)}")
        all_pass = False

    # Delete
    deleted = treap.delete(3)
    if not deleted or treap.search(3):
        print("FAIL delete 3")
        all_pass = False
    if len(treap) != 6:
        print(f"FAIL size after delete: {len(treap)}")
        all_pass = False

    deleted2 = treap.delete(10)
    if deleted2:
        print("FAIL delete nonexistent")
        all_pass = False

    # Duplicate insert
    treap.insert(5)
    if len(treap) != 7:
        print(f"FAIL size after dup: {len(treap)}")
        all_pass = False

    if all_pass:
        print("All Treap tests PASSED")
    sys.exit(0 if all_pass else 1)
