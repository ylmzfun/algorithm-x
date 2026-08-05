"""
AVL Tree Implementation
========================

A self-balancing binary search tree where the height difference between
left and right subtrees (balance factor) is at most 1 for every node.

After insertion or deletion, rotations are applied to restore balance:
    - LL (Left-Left): Right rotation on unbalanced node.
    - RR (Right-Right): Left rotation on unbalanced node.
    - LR (Left-Right): Left rotation on left child, then right rotation.
    - RL (Right-Left): Right rotation on right child, then left rotation.

Time Complexities:
    - Search: O(log n) guaranteed
    - Insert: O(log n)
    - Delete: O(log n)

Space Complexity: O(n) for n nodes.
"""

from typing import Any, Optional, List


class AVLNode:
    """A node in an AVL tree with a height attribute.

    Attributes:
        data: Value stored in this node.
        left: Left child.
        right: Right child.
        height: Height of this subtree (leaf = 1).
    """

    def __init__(self, data: Any) -> None:
        """Initialize AVL node with height 1.

        Args:
            data: Value to store.
        """
        self.data: Any = data
        self.left: Optional["AVLNode"] = None
        self.right: Optional["AVLNode"] = None
        self.height: int = 1

    def __repr__(self) -> str:
        """Return string representation."""
        return f"AVLNode({self.data!r}, h={self.height})"


class AVLTree:
    """An AVL (Adelson-Velsky and Landis) self-balancing binary search tree.

    Examples:
        >>> avl = AVLTree()
        >>> for x in [10, 20, 30, 40, 50]:
        ...     avl.insert(x)
        >>> avl.search(30)
        True
        >>> avl.inorder()
        [10, 20, 30, 40, 50]
        >>> avl.delete(30)
        True
        >>> avl.size()
        4
    """

    def __init__(self) -> None:
        """Initialize an empty AVL tree."""
        self._root: Optional[AVLNode] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        """Check if tree is empty."""
        return self._root is None

    def size(self) -> int:
        """Return number of nodes."""
        return self._size

    def root(self) -> Optional[AVLNode]:
        """Return root node."""
        return self._root

    # ── Height utility ────────────────────────────────────────────────────────

    @staticmethod
    def _height(node: Optional[AVLNode]) -> int:
        """Return height of node, 0 if None."""
        return node.height if node else 0

    @staticmethod
    def _balance_factor(node: AVLNode) -> int:
        """Return balance factor: left_height - right_height."""
        return AVLTree._height(node.left) - AVLTree._height(node.right)

    @staticmethod
    def _update_height(node: AVLNode) -> None:
        """Recalculate node.height from children."""
        node.height = 1 + max(AVLTree._height(node.left),
                               AVLTree._height(node.right))

    # ── Rotations ─────────────────────────────────────────────────────────────

    @staticmethod
    def _rotate_right(y: AVLNode) -> AVLNode:
        """Perform a right rotation on `y`.

        Returns the new root of the subtree (x).

        Args:
            y: The unbalanced node (root of subtree).

        Returns:
            New subtree root.

        Time Complexity: O(1)

        Diagram:
              y           x
             / \         / \
            x   C  →   A   y
           / \             / \
          A   B           B   C
        """
        x = y.left  # type: ignore[assignment]
        T2 = x.right  # type: ignore[union-attr]

        # Rotation
        x.right = y  # type: ignore[union-attr]
        y.left = T2

        # Update heights
        AVLTree._update_height(y)
        AVLTree._update_height(x)  # type: ignore[arg-type]

        return x  # type: ignore[return-value]

    @staticmethod
    def _rotate_left(x: AVLNode) -> AVLNode:
        """Perform a left rotation on `x`.

        Returns the new root of the subtree (y).

        Args:
            x: The unbalanced node (root of subtree).

        Returns:
            New subtree root.

        Time Complexity: O(1)

        Diagram:
            x               y
           / \             / \
          A   y     →     x   C
             / \         / \
            B   C       A   B
        """
        y = x.right  # type: ignore[assignment]
        T2 = y.left  # type: ignore[union-attr]

        # Rotation
        y.left = x  # type: ignore[union-attr]
        x.right = T2

        # Update heights
        AVLTree._update_height(x)
        AVLTree._update_height(y)  # type: ignore[arg-type]

        return y  # type: ignore[return-value]

    # ── Insert ────────────────────────────────────────────────────────────────

    def insert(self, data: Any) -> None:
        """Insert `data` into the AVL tree.

        If `data` already exists, does nothing.

        Args:
            data: Value to insert.

        Time Complexity: O(log n)
        """
        self._root = self._insert(self._root, data)

    def _insert(self, node: Optional[AVLNode], data: Any) -> AVLNode:
        """Recursive insert with rebalancing."""
        # Standard BST insert
        if node is None:
            self._size += 1
            return AVLNode(data)

        if data < node.data:
            node.left = self._insert(node.left, data)
        elif data > node.data:
            node.right = self._insert(node.right, data)
        else:
            return node  # Duplicate, do nothing

        # Update height
        self._update_height(node)

        # Get balance factor
        balance = self._balance_factor(node)

        # ── LL Case: left-left ────────────────────────────────────────────
        if balance > 1 and data < node.left.data:  # type: ignore[union-attr]
            return self._rotate_right(node)

        # ── RR Case: right-right ──────────────────────────────────────────
        if balance < -1 and data > node.right.data:  # type: ignore[union-attr]
            return self._rotate_left(node)

        # ── LR Case: left-right ───────────────────────────────────────────
        if balance > 1 and data > node.left.data:  # type: ignore[union-attr]
            node.left = self._rotate_left(node.left)  # type: ignore[arg-type]
            return self._rotate_right(node)

        # ── RL Case: right-left ───────────────────────────────────────────
        if balance < -1 and data < node.right.data:  # type: ignore[union-attr]
            node.right = self._rotate_right(node.right)  # type: ignore[arg-type]
            return self._rotate_left(node)

        return node

    # ── Delete ────────────────────────────────────────────────────────────────

    def delete(self, data: Any) -> bool:
        """Remove `data` from the AVL tree.

        Args:
            data: Value to delete.

        Returns:
            True if deleted, False if not found.

        Time Complexity: O(log n)
        """
        prev_size = self._size
        self._root = self._delete(self._root, data)
        return self._size < prev_size

    def _delete(self, node: Optional[AVLNode], data: Any) -> Optional[AVLNode]:
        """Recursive delete with rebalancing."""
        if node is None:
            return None

        if data < node.data:
            node.left = self._delete(node.left, data)
        elif data > node.data:
            node.right = self._delete(node.right, data)
        else:
            # Found — perform deletion
            self._size -= 1

            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            # Two children: replace with inorder successor
            succ = self._min_node(node.right)
            node.data = succ.data
            node.right = self._delete(node.right, succ.data)
            self._size += 1  # Adjust for the successor handle
            self._size -= 1

        if node is None:
            return None

        # Update height and rebalance
        self._update_height(node)
        balance = self._balance_factor(node)

        # LL
        if balance > 1 and self._balance_factor(node.left) >= 0:  # type: ignore[arg-type]
            return self._rotate_right(node)
        # LR
        if balance > 1 and self._balance_factor(node.left) < 0:  # type: ignore[arg-type]
            node.left = self._rotate_left(node.left)  # type: ignore[arg-type]
            return self._rotate_right(node)
        # RR
        if balance < -1 and self._balance_factor(node.right) <= 0:  # type: ignore[arg-type]
            return self._rotate_left(node)
        # RL
        if balance < -1 and self._balance_factor(node.right) > 0:  # type: ignore[arg-type]
            node.right = self._rotate_right(node.right)  # type: ignore[arg-type]
            return self._rotate_left(node)

        return node

    # ── Search ────────────────────────────────────────────────────────────────

    def search(self, data: Any) -> bool:
        """Check if `data` exists in the AVL tree.

        Args:
            data: Value to find.

        Returns:
            True if found.

        Time Complexity: O(log n)
        """
        return self._search(self._root, data)

    def _search(self, node: Optional[AVLNode], data: Any) -> bool:
        if node is None:
            return False
        if node.data == data:
            return True
        if data < node.data:
            return self._search(node.left, data)
        return self._search(node.right, data)

    # ── Min / Max ─────────────────────────────────────────────────────────────

    def _min_node(self, node: AVLNode) -> AVLNode:
        """Return minimum node in subtree."""
        while node.left is not None:
            node = node.left
        return node

    def min(self) -> Optional[Any]:
        """Return minimum value."""
        if self._root is None:
            return None
        return self._min_node(self._root).data

    def max(self) -> Optional[Any]:
        """Return maximum value."""
        if self._root is None:
            return None
        node = self._root
        while node.right is not None:
            node = node.right
        return node.data

    # ── Traversals ────────────────────────────────────────────────────────────

    def inorder(self) -> List[Any]:
        """In-order traversal (sorted order).

        Returns:
            List of values in sorted order.

        Time Complexity: O(n)
        """
        result: List[Any] = []

        def _traverse(node: Optional[AVLNode]) -> None:
            if node is None:
                return
            _traverse(node.left)
            result.append(node.data)
            _traverse(node.right)

        _traverse(self._root)
        return result

    # ── Height ───────────────────────────────────────────────────────────────

    def height(self) -> int:
        """Return tree height (0-based, empty = -1)."""
        return self._height(self._root) - 1 if self._root else -1

    # ── Dunder ───────────────────────────────────────────────────────────────

    def __contains__(self, data: Any) -> bool:
        return self.search(data)

    def __len__(self) -> int:
        return self._size

    def __str__(self) -> str:
        return str(self.inorder())

    def __repr__(self) -> str:
        return f"AVLTree(size={self._size}, height={self.height()})"


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
    avl = AVLTree()
    check("empty is_empty", avl.is_empty())
    check("empty size == 0", avl.size() == 0)
    check("empty height == -1", avl.height() == -1)

    # ── Insert (triggers rotations) ───────────────────────────────────────────
    print("\nInsert (balancing):")
    # Insert in sorted order (worst case for plain BST, AVL stays balanced)
    for val in [10, 20, 30, 40, 50, 25]:
        avl.insert(val)
    check("size == 6", avl.size() == 6)
    check("inorder sorted", avl.inorder() == [10, 20, 25, 30, 40, 50])
    check("height is O(log n)", avl.height() <= 3)  # log2(6) ≈ 2.6 → h ≤ 3

    # ── LL Rotation ───────────────────────────────────────────────────────────
    print("\nLL Rotation (30, 20, 10):")
    avl_ll = AVLTree()
    avl_ll.insert(30)
    avl_ll.insert(20)
    avl_ll.insert(10)
    check("LL: inorder sorted", avl_ll.inorder() == [10, 20, 30])
    check("LL: balanced height == 1", avl_ll.height() == 1)

    # ── RR Rotation ───────────────────────────────────────────────────────────
    print("\nRR Rotation (10, 20, 30):")
    avl_rr = AVLTree()
    avl_rr.insert(10)
    avl_rr.insert(20)
    avl_rr.insert(30)
    check("RR: inorder sorted", avl_rr.inorder() == [10, 20, 30])
    check("RR: balanced height == 1", avl_rr.height() == 1)

    # ── LR Rotation ───────────────────────────────────────────────────────────
    print("\nLR Rotation (30, 10, 20):")
    avl_lr = AVLTree()
    avl_lr.insert(30)
    avl_lr.insert(10)
    avl_lr.insert(20)
    check("LR: inorder sorted", avl_lr.inorder() == [10, 20, 30])
    check("LR: balanced height == 1", avl_lr.height() == 1)

    # ── RL Rotation ───────────────────────────────────────────────────────────
    print("\nRL Rotation (10, 30, 20):")
    avl_rl = AVLTree()
    avl_rl.insert(10)
    avl_rl.insert(30)
    avl_rl.insert(20)
    check("RL: inorder sorted", avl_rl.inorder() == [10, 20, 30])
    check("RL: balanced height == 1", avl_rl.height() == 1)

    # ── Search ────────────────────────────────────────────────────────────────
    print("\nSearch:")
    check("search(25) True", avl.search(25))
    check("search(50) True", avl.search(50))
    check("search(15) False", not avl.search(15))

    # ── Min / Max ─────────────────────────────────────────────────────────────
    print("\nMin/Max:")
    check("min == 10", avl.min() == 10)
    check("max == 50", avl.max() == 50)

    # ── Delete ────────────────────────────────────────────────────────────────
    print("\nDelete:")
    # Delete leaf
    check("delete(25) True", avl.delete(25))
    check("25 removed", not avl.search(25))
    check("size after delete(25)", avl.size() == 5)

    # Delete non-existent
    check("delete(99) False", avl.delete(99) is False)

    # Delete root-ish node — ensure tree stays balanced
    avl.delete(30)
    check("after delete(30) inorder valid", avl.inorder() == [10, 20, 40, 50])
    check("height still balanced", avl.height() <= 3)

    # Delete remaining
    for val in [10, 20, 40, 50]:
        avl.delete(val)
    check("empty after all deletes", avl.is_empty())

    # ── Large scale ───────────────────────────────────────────────────────────
    print("\nLarge scale (100 elements):")
    avl_big = AVLTree()
    for i in range(100):
        avl_big.insert(i)
    check("size == 100", avl_big.size() == 100)
    check("inorder is sorted 0..99", avl_big.inorder() == list(range(100)))
    check("height <= 2*log2(100) ≈ 14", avl_big.height() <= 14)
    check("all searchable", all(avl_big.search(i) for i in range(100)))

    # ── Summary ───────────────────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
