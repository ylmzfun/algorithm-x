"""
Red-Black Tree Implementation (Simplified)
============================================

A simplified Red-Black tree — a self-balancing BST with the following
properties:
    1. Every node is either RED or BLACK.
    2. The root is always BLACK.
    3. No two adjacent RED nodes (RED node's children are BLACK).
    4. Every path from root to NIL has the same number of BLACK nodes.

This implementation focuses on INSERT with recoloring and rotations.
DELETE is noted as TODO (standard RB delete is covered in textbooks).

Time Complexities:
    - Insert: O(log n) guaranteed — at most 2 rotations per insert.

Space Complexity: O(n) for n nodes.

References:
    - CLRS Introduction to Algorithms, Chapter 13
"""

from enum import Enum
from typing import Any, Optional, List


class Color(Enum):
    """Red-Black tree node color."""
    RED = "RED"
    BLACK = "BLACK"


class RBNode:
    """A node in a Red-Black tree.

    Attributes:
        data: Value stored in this node.
        color: RED or BLACK.
        left: Left child.
        right: Right child.
        parent: Parent node (None for root).
    """

    def __init__(self, data: Any, color: Color = Color.RED) -> None:
        """Initialize RB node (new nodes are RED by default).

        Args:
            data: Value to store.
            color: Node color (default RED).
        """
        self.data: Any = data
        self.color: Color = color
        self.left: Optional["RBNode"] = None
        self.right: Optional["RBNode"] = None
        self.parent: Optional["RBNode"] = None

    def __repr__(self) -> str:
        """Return string representation."""
        return f"RBNode({self.data!r}, {self.color.value})"


class RedBlackTree:
    """A simplified Red-Black tree with insert and search.

    Uses a NIL sentinel (black) to represent leaves, simplifying
    boundary conditions.

    Examples:
        >>> rbt = RedBlackTree()
        >>> for x in [7, 3, 18, 10, 22, 8, 11, 26]:
        ...     rbt.insert(x)
        >>> rbt.search(10)
        True
        >>> rbt.search(99)
        False
        >>> rbt.inorder()[:3]
        [3, 7, 8]
    """

    def __init__(self) -> None:
        """Initialize an empty Red-Black tree with NIL sentinel."""
        self._NIL = RBNode(None, Color.BLACK)  # Sentinel for leaves
        self._root: RBNode = self._NIL
        self._size: int = 0

    def is_empty(self) -> bool:
        """Check if tree is empty."""
        return self._root is self._NIL

    def size(self) -> int:
        """Return number of nodes."""
        return self._size

    # ── Rotations ─────────────────────────────────────────────────────────────

    def _rotate_left(self, x: RBNode) -> None:
        """Left rotation on node x.

        Args:
            x: The node to rotate.

        Time Complexity: O(1)
        """
        y = x.right  # type: ignore[assignment]

        # y's left becomes x's right
        x.right = y.left  # type: ignore[union-attr]
        if y.left is not self._NIL:  # type: ignore[union-attr]
            y.left.parent = x  # type: ignore[union-attr]

        # Link y's parent
        y.parent = x.parent  # type: ignore[union-attr]

        if x.parent is None:
            self._root = y  # type: ignore[assignment]
        elif x == x.parent.left:
            x.parent.left = y  # type: ignore[union-attr]
        else:
            x.parent.right = y  # type: ignore[union-attr]

        # Put x on y's left
        y.left = x  # type: ignore[union-attr]
        x.parent = y  # type: ignore[union-attr]

    def _rotate_right(self, y: RBNode) -> None:
        """Right rotation on node y.

        Args:
            y: The node to rotate.

        Time Complexity: O(1)
        """
        x = y.left  # type: ignore[assignment]

        # x's right becomes y's left
        y.left = x.right  # type: ignore[union-attr]
        if x.right is not self._NIL:  # type: ignore[union-attr]
            x.right.parent = y  # type: ignore[union-attr]

        # Link x's parent
        x.parent = y.parent  # type: ignore[union-attr]

        if y.parent is None:
            self._root = x  # type: ignore[assignment]
        elif y == y.parent.right:
            y.parent.right = x  # type: ignore[union-attr]
        else:
            y.parent.left = x  # type: ignore[union-attr]

        # Put y on x's right
        x.right = y  # type: ignore[union-attr]
        y.parent = x  # type: ignore[union-attr]

    # ── Insert ────────────────────────────────────────────────────────────────

    def insert(self, data: Any) -> None:
        """Insert `data` into the Red-Black tree.

        After standard BST insertion, the node is colored RED, and
        the tree is fixed up to maintain RB properties.

        Args:
            data: Value to insert.

        Time Complexity: O(log n)
        """
        node = RBNode(data, Color.RED)
        node.left = self._NIL
        node.right = self._NIL

        y: Optional[RBNode] = None
        x = self._root

        # Standard BST insertion
        while x is not self._NIL:
            y = x
            if node.data < x.data:
                x = x.left  # type: ignore[assignment]
            elif node.data > x.data:
                x = x.right  # type: ignore[assignment]
            else:
                return  # Duplicate — do nothing

        node.parent = y

        if y is None:
            self._root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        self._size += 1

        # Fix Red-Black properties
        self._insert_fixup(node)

    def _insert_fixup(self, z: RBNode) -> None:
        """Fix Red-Black tree violations after insertion.

        While z's parent is RED (violation of property 3), we need to fix.
        Three cases based on uncle's color and position.

        Args:
            z: The newly inserted node.

        Time Complexity: O(log n) — at most 2 rotations.
        """
        while z.parent is not None and z.parent.color == Color.RED:
            if z.parent == z.parent.parent.left:  # type: ignore[union-attr]
                y = z.parent.parent.right  # type: ignore[union-attr] # Uncle

                # Case 1: Uncle is RED → recolor
                if y is not None and y.color == Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED  # type: ignore[union-attr]
                    z = z.parent.parent  # type: ignore[assignment]
                else:
                    # Case 2: z is right child → left rotate
                    if z == z.parent.right:
                        z = z.parent
                        self._rotate_left(z)
                    # Case 3: z is left child → right rotate
                    z.parent.color = Color.BLACK  # type: ignore[union-attr]
                    z.parent.parent.color = Color.RED  # type: ignore[union-attr]
                    self._rotate_right(z.parent.parent)  # type: ignore[arg-type]
            else:
                # Mirror: parent is right child
                y = z.parent.parent.left  # type: ignore[union-attr] # Uncle

                # Case 1: Uncle is RED
                if y is not None and y.color == Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED  # type: ignore[union-attr]
                    z = z.parent.parent  # type: ignore[assignment]
                else:
                    # Case 2: z is left child → right rotate
                    if z == z.parent.left:
                        z = z.parent
                        self._rotate_right(z)
                    # Case 3: z is right child → left rotate
                    z.parent.color = Color.BLACK  # type: ignore[union-attr]
                    z.parent.parent.color = Color.RED  # type: ignore[union-attr]
                    self._rotate_left(z.parent.parent)  # type: ignore[arg-type]

            if z == self._root:
                break

        # Property 2: Root is always BLACK
        self._root.color = Color.BLACK

    # ── Search ────────────────────────────────────────────────────────────────

    def search(self, data: Any) -> bool:
        """Check if `data` exists.

        Args:
            data: Value to find.

        Returns:
            True if found.

        Time Complexity: O(log n)
        """
        node = self._root
        while node is not self._NIL:
            if data == node.data:
                return True
            if data < node.data:
                node = node.left  # type: ignore[assignment]
            else:
                node = node.right  # type: ignore[assignment]
        return False

    # ── Min / Max ─────────────────────────────────────────────────────────────

    def min(self) -> Optional[Any]:
        """Return minimum value."""
        if self.is_empty():
            return None
        node = self._root
        while node.left is not self._NIL:
            node = node.left  # type: ignore[assignment]
        return node.data

    def max(self) -> Optional[Any]:
        """Return maximum value."""
        if self.is_empty():
            return None
        node = self._root
        while node.right is not self._NIL:
            node = node.right  # type: ignore[assignment]
        return node.data

    # ── Inorder Traversal ─────────────────────────────────────────────────────

    def inorder(self) -> List[Any]:
        """In-order traversal (sorted order).

        Returns:
            List of values in sorted order.

        Time Complexity: O(n)
        """
        result: List[Any] = []

        def _traverse(node: RBNode) -> None:
            if node is self._NIL:
                return
            _traverse(node.left)  # type: ignore[arg-type]
            result.append(node.data)
            _traverse(node.right)  # type: ignore[arg-type]

        _traverse(self._root)
        return result

    # ── Dunder ───────────────────────────────────────────────────────────────

    def __contains__(self, data: Any) -> bool:
        return self.search(data)

    def __len__(self) -> int:
        return self._size

    def __str__(self) -> str:
        return str(self.inorder())

    def __repr__(self) -> str:
        return f"RedBlackTree(size={self._size})"


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
    rbt = RedBlackTree()
    check("empty is_empty", rbt.is_empty())
    check("empty size == 0", rbt.size() == 0)

    # ── Insert ────────────────────────────────────────────────────────────────
    print("\nInsert:")
    for val in [7, 3, 18, 10, 22, 8, 11, 26]:
        rbt.insert(val)
    check("size after 8 inserts", rbt.size() == 8)
    check("inorder sorted", rbt.inorder() == [3, 7, 8, 10, 11, 18, 22, 26])
    check("root is BLACK", rbt._root.color == Color.BLACK)

    # Duplicate
    rbt.insert(10)
    check("duplicate not inserted", rbt.size() == 8)

    # ── Search ────────────────────────────────────────────────────────────────
    print("\nSearch:")
    check("search(7) True", rbt.search(7))
    check("search(26) True", rbt.search(26))
    check("search(8) True", rbt.search(8))
    check("search(99) False", not rbt.search(99))

    # ── Min / Max ─────────────────────────────────────────────────────────────
    print("\nMin/Max:")
    check("min == 3", rbt.min() == 3)
    check("max == 26", rbt.max() == 26)

    # ── RB Properties ─────────────────────────────────────────────────────────
    print("\nRB Properties verification:")

    def verify_rb_properties(tree: RedBlackTree) -> bool:
        """Verify Red-Black tree properties."""
        if tree.is_empty():
            return True

        # Property 2: root is BLACK
        if tree._root.color != Color.BLACK:
            return False

        def _verify(node: RBNode) -> tuple[bool, int]:
            """Returns (valid, black_height)."""
            if node is tree._NIL:
                return (True, 1)  # NIL counts as black

            # Property 3: No consecutive RED
            if node.color == Color.RED:
                if node.left is not tree._NIL and node.left.color == Color.RED:
                    return (False, 0)
                if node.right is not tree._NIL and node.right.color == Color.RED:
                    return (False, 0)

            left_valid, left_bh = _verify(node.left)  # type: ignore[arg-type]
            right_valid, right_bh = _verify(node.right)  # type: ignore[arg-type]

            if not (left_valid and right_valid):
                return (False, 0)

            # Property 4: Equal black height
            if left_bh != right_bh:
                return (False, 0)

            bh = left_bh + (1 if node.color == Color.BLACK else 0)
            return (True, bh)

        valid, _ = _verify(tree._root)
        return valid

    check("RB properties hold", verify_rb_properties(rbt))

    # ── Larger test ───────────────────────────────────────────────────────────
    print("\nLarger test (100 elements):")
    rbt_big = RedBlackTree()
    for i in range(100):
        rbt_big.insert(i)
    check("size == 100", rbt_big.size() == 100)
    check("inorder sorted", rbt_big.inorder() == list(range(100)))
    check("RB properties hold (big)", verify_rb_properties(rbt_big))
    check("all searchable", all(rbt_big.search(i) for i in range(100)))

    # ── Summary ───────────────────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
