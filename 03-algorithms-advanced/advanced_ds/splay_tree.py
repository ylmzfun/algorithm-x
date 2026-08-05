"""
Splay Tree — a self-adjusting binary search tree.

After each operation (search, insert, delete), the accessed node is
"splayed" to the root.  This yields amortized O(log n) time for all
operations.

Supports:
- splay operation
- insert, delete, search
- split, merge
- In-order traversal
"""

from typing import List, Optional, Tuple


class SplayNode:
    """A node in the Splay Tree."""

    __slots__ = ("key", "left", "right", "parent")

    def __init__(self, key: int) -> None:
        self.key = key
        self.left: Optional["SplayNode"] = None
        self.right: Optional["SplayNode"] = None
        self.parent: Optional["SplayNode"] = None


class SplayTree:
    """
    Splay Tree: self-adjusting BST with amortized O(log n) per operation.
    """

    def __init__(self) -> None:
        """Create an empty Splay Tree."""
        self.root: Optional[SplayNode] = None

    # ------------------------------------------------------------------
    # Rotations
    # ------------------------------------------------------------------

    def _rotate_left(self, x: SplayNode) -> None:
        """Left rotation: x becomes left child of its right child."""
        y = x.right
        if y is None:
            return
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _rotate_right(self, x: SplayNode) -> None:
        """Right rotation: x becomes right child of its left child."""
        y = x.left
        if y is None:
            return
        x.left = y.right
        if y.right:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # ------------------------------------------------------------------
    # Splay
    # ------------------------------------------------------------------

    def splay(self, x: SplayNode) -> None:
        """
        Splay x to the root of the tree.

        Uses zig, zig-zig, and zig-zag cases.

        Args:
            x: The node to splay.

        Time: Amortized O(log n)
        """
        while x.parent is not None:
            p = x.parent
            g = p.parent

            if g is None:
                # Zig step
                if x == p.left:
                    self._rotate_right(p)
                else:
                    self._rotate_left(p)
            elif x == p.left and p == g.left:
                # Zig-zig (left-left)
                self._rotate_right(g)
                self._rotate_right(p)
            elif x == p.right and p == g.right:
                # Zig-zig (right-right)
                self._rotate_left(g)
                self._rotate_left(p)
            elif x == p.right and p == g.left:
                # Zig-zag (left-right)
                self._rotate_left(p)
                self._rotate_right(g)
            else:
                # Zig-zag (right-left)
                self._rotate_right(p)
                self._rotate_left(g)

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(self, key: int) -> bool:
        """
        Search for a key.  Splays the found node (or the last accessed
        node) to the root.

        Args:
            key: The key to search for.

        Returns:
            True if found, False otherwise.

        Time: Amortized O(log n)
        """
        node = self._find(key)
        if node:
            self.splay(node)
            return node.key == key
        return False

    def _find(self, key: int) -> Optional[SplayNode]:
        """Find a node by key, returning the last node on the search path."""
        cur = self.root
        prev = None
        while cur is not None:
            prev = cur
            if key == cur.key:
                return cur
            elif key < cur.key:
                cur = cur.left
            else:
                cur = cur.right
        return prev  # last accessed node

    # ------------------------------------------------------------------
    # Insert
    # ------------------------------------------------------------------

    def insert(self, key: int) -> None:
        """
        Insert a key into the tree.  The new node is splayed to the root.

        Args:
            key: The key to insert.  Duplicates are ignored.

        Time: Amortized O(log n)
        """
        if self.root is None:
            self.root = SplayNode(key)
            return

        # Splay the last accessed node
        node = self._find(key)
        if node and node.key == key:
            self.splay(node)
            return  # duplicate

        new_node = SplayNode(key)
        if node is None:
            self.root = new_node
            return

        self.splay(node)

        # Now the last accessed node is at the root
        if key < self.root.key:
            new_node.left = self.root.left
            new_node.right = self.root
            if self.root.left:
                self.root.left.parent = new_node
            self.root.left = None
            self.root.parent = new_node
        else:
            new_node.right = self.root.right
            new_node.left = self.root
            if self.root.right:
                self.root.right.parent = new_node
            self.root.right = None
            self.root.parent = new_node

        self.root = new_node

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    def delete(self, key: int) -> bool:
        """
        Delete a key from the tree.

        Args:
            key: The key to delete.

        Returns:
            True if deleted, False if not found.

        Time: Amortized O(log n)
        """
        if self.root is None:
            return False

        self.search(key)  # splay the node
        if self.root is None or self.root.key != key:
            return False

        # Root is the node to delete
        left = self.root.left
        right = self.root.right

        if left:
            left.parent = None
        if right:
            right.parent = None

        if left is None:
            self.root = right
        elif right is None:
            self.root = left
        else:
            # Splay the maximum in the left subtree
            self.root = left
            max_node = left
            while max_node.right:
                max_node = max_node.right
            self.splay(max_node)
            # Now left became root with no right child
            self.root.right = right
            right.parent = self.root

        return True

    # ------------------------------------------------------------------
    # Split
    # ------------------------------------------------------------------

    def split(self, key: int) -> Tuple[Optional["SplayNode"], Optional["SplayNode"]]:
        """
        Split the tree into two: left (keys ≤ key), right (keys > key).

        Splays the split point to the root.

        Args:
            key: The split key.

        Returns:
            (left_root, right_root).

        Time: Amortized O(log n)
        """
        if self.root is None:
            return None, None

        self.search(key)
        if self.root is None:
            return None, None

        if self.root.key <= key:
            right = self.root.right
            if right:
                right.parent = None
            self.root.right = None
            left = self.root
        else:
            left = self.root.left
            if left:
                left.parent = None
            self.root.left = None
            right = self.root

        return left, right

    # ------------------------------------------------------------------
    # Merge
    # ------------------------------------------------------------------

    def merge(self, left: Optional[SplayNode], right: Optional[SplayNode]) -> None:
        """
        Merge two trees where all keys in left ≤ all keys in right.

        Args:
            left: Root of left tree.
            right: Root of right tree.

        Time: Amortized O(log n)
        """
        if left is None:
            self.root = right
            return
        if right is None:
            self.root = left
            return

        # Find the maximum in left and splay to the root
        self.root = left
        max_node = left
        while max_node.right:
            max_node = max_node.right
        self.splay(max_node)
        # Now root has no right child
        self.root.right = right
        right.parent = self.root

    # ------------------------------------------------------------------
    # Traversal
    # ------------------------------------------------------------------

    def inorder(self) -> List[int]:
        """
        Return all keys in sorted (in-order) order.

        Returns:
            List of keys.

        Time: O(n)
        """
        result: List[int] = []

        def dfs(node: Optional[SplayNode]) -> None:
            if node:
                dfs(node.left)
                result.append(node.key)
                dfs(node.right)

        dfs(self.root)
        return result

    # ------------------------------------------------------------------
    # Min / Max
    # ------------------------------------------------------------------

    def minimum(self) -> Optional[int]:
        """Return the minimum key, or None if tree is empty."""
        if self.root is None:
            return None
        cur = self.root
        while cur.left:
            cur = cur.left
        self.splay(cur)
        return cur.key

    def maximum(self) -> Optional[int]:
        """Return the maximum key, or None if tree is empty."""
        if self.root is None:
            return None
        cur = self.root
        while cur.right:
            cur = cur.right
        self.splay(cur)
        return cur.key


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    import sys

    all_pass = True

    st = SplayTree()

    # Insert
    for v in [10, 5, 15, 3, 7, 12, 18]:
        st.insert(v)

    # Search
    if not st.search(7):
        print("FAIL search 7")
        all_pass = False
    if st.search(20):
        print("FAIL search 20")
        all_pass = False

    # Inorder
    if st.inorder() != [3, 5, 7, 10, 12, 15, 18]:
        print(f"FAIL inorder: {st.inorder()}")
        all_pass = False

    # Min / Max
    if st.minimum() != 3:
        print(f"FAIL min: {st.minimum()}")
        all_pass = False
    if st.maximum() != 18:
        print(f"FAIL max: {st.maximum()}")
        all_pass = False

    # Delete
    st.delete(7)
    if st.search(7):
        print("FAIL: 7 still present after delete")
        all_pass = False
    if st.inorder() != [3, 5, 10, 12, 15, 18]:
        print(f"FAIL inorder after delete 7: {st.inorder()}")
        all_pass = False

    st.delete(3)
    if st.search(3):
        print("FAIL: 3 still present after delete")
        all_pass = False

    st.delete(18)
    if st.search(18):
        print("FAIL: 18 still present after delete")
        all_pass = False

    if st.inorder() != [5, 10, 12, 15]:
        print(f"FAIL inorder after deletes: {st.inorder()}")
        all_pass = False

    # Split and Merge
    st2 = SplayTree()
    st2.insert(10)
    st2.insert(5)
    st2.insert(20)
    left, right = st2.split(10)
    # Reconstruct
    st3 = SplayTree()
    st3.merge(left, right)
    if st3.inorder() != [5, 10, 20]:
        print(f"FAIL split+merge: {st3.inorder()}")
        all_pass = False

    if all_pass:
        print("All Splay Tree tests PASSED")
    sys.exit(0 if all_pass else 1)
