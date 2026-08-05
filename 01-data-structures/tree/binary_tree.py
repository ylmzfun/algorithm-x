"""
Binary Tree Implementation
===========================

A general binary tree with basic operations and all four standard traversals
(pre-order, in-order, post-order, level-order). Both recursive and iterative
implementations provided.

TreeNode properties:
    - data: Value stored in the node
    - left: Left child (TreeNode or None)
    - right: Right child (TreeNode or None)

Operations:
    - Insert (level-order, first available position)
    - Search (BFS/DFS)
    - Delete (replace with deepest rightmost node)
    - Traversals: preorder, inorder, postorder, levelorder
    - Height, Size, Is Balanced

Time Complexities:
    - Search: O(n) — general binary tree (no ordering guarantee)
    - Insert: O(n) — level-order traversal to find empty spot
    - Delete: O(n)
    - Traversals: O(n)
    - Height: O(n)

Space Complexity: O(n) for n nodes
"""

from typing import Any, Optional, List, Iterator
from collections import deque


class TreeNode:
    """A node in a binary tree.

    Attributes:
        data: The value stored in this node.
        left: Left child node (None if absent).
        right: Right child node (None if absent).
    """

    def __init__(self, data: Any) -> None:
        """Initialize a tree node.

        Args:
            data: Value to store.
        """
        self.data: Any = data
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None

    def __repr__(self) -> str:
        """Return string representation."""
        return f"TreeNode({self.data!r})"


class BinaryTree:
    """A general binary tree (not necessarily a search tree).

    Supports insertion at the first available position (level-order),
    and all standard traversals.

    Examples:
        >>> bt = BinaryTree()
        >>> bt.insert(1)
        >>> bt.insert(2)
        >>> bt.insert(3)
        >>> bt.inorder()
        [2, 1, 3]
        >>> bt.height()
        1
        >>> bt.size()
        3
    """

    def __init__(self) -> None:
        """Initialize an empty binary tree."""
        self._root: Optional[TreeNode] = None

    def root(self) -> Optional[TreeNode]:
        """Return the root node.

        Returns:
            Root TreeNode or None if empty.

        Time Complexity: O(1)
        """
        return self._root

    def is_empty(self) -> bool:
        """Check if tree is empty.

        Returns:
            True if no nodes.

        Time Complexity: O(1)
        """
        return self._root is None

    # ── Insert ────────────────────────────────────────────────────────────────

    def insert(self, data: Any) -> None:
        """Insert a node at the first available position (level-order).

        This ensures the tree remains a complete binary tree. Uses BFS
        to find the first node with a missing child.

        Args:
            data: Value to insert.

        Time Complexity: O(n) — BFS traversal.
        """
        new_node = TreeNode(data)

        if self._root is None:
            self._root = new_node
            return

        queue = deque([self._root])
        while queue:
            current = queue.popleft()
            if current.left is None:
                current.left = new_node
                return
            queue.append(current.left)
            if current.right is None:
                current.right = new_node
                return
            queue.append(current.right)

    # ── Search ────────────────────────────────────────────────────────────────

    def search(self, data: Any) -> bool:
        """Check if `data` exists in the tree using BFS.

        Args:
            data: Value to search for.

        Returns:
            True if found, False otherwise.

        Time Complexity: O(n)
        """
        if self._root is None:
            return False

        queue = deque([self._root])
        while queue:
            current = queue.popleft()
            if current.data == data:
                return True
            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)
        return False

    def search_dfs(self, data: Any) -> bool:
        """Check if `data` exists using DFS (preorder).

        Args:
            data: Value to search for.

        Returns:
            True if found.

        Time Complexity: O(n)
        """

        def _dfs(node: Optional[TreeNode]) -> bool:
            if node is None:
                return False
            if node.data == data:
                return True
            return _dfs(node.left) or _dfs(node.right)

        return _dfs(self._root)

    # ── Delete ────────────────────────────────────────────────────────────────

    def delete(self, data: Any) -> bool:
        """Delete the first node containing `data`.

        Finds the node to delete, then replaces it with the deepest,
        rightmost node (to keep the tree compact), and deletes that node.

        Args:
            data: Value of node to delete.

        Returns:
            True if deleted, False if not found.

        Time Complexity: O(n)
        """
        if self._root is None:
            return False

        # BFS to find target and track the deepest rightmost node
        target: Optional[TreeNode] = None
        last: Optional[TreeNode] = None  # Deepest rightmost
        last_parent: Optional[TreeNode] = None

        queue = deque([(self._root, None)])  # (node, parent)
        while queue:
            current, parent = queue.popleft()
            last = current
            last_parent = parent

            if current.data == data and target is None:
                target = current

            if current.left:
                queue.append((current.left, current))
            if current.right:
                queue.append((current.right, current))

        if target is None:
            return False

        # Replace target's data with last node's data
        target.data = last.data  # type: ignore[union-attr]

        # Delete the last node
        if last_parent is None:
            # Last node is root (single node tree)
            self._root = None
        elif last_parent.left == last:
            last_parent.left = None
        else:
            last_parent.right = None

        return True

    # ── Height ───────────────────────────────────────────────────────────────

    def height(self) -> int:
        """Return the height of the tree (root = 0, empty = -1).

        Height is the number of edges on the longest path from root to leaf.

        Returns:
            Tree height (-1 for empty tree).

        Time Complexity: O(n)
        """
        return self._height(self._root)

    def _height(self, node: Optional[TreeNode]) -> int:
        """Recursive height helper."""
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

    # ── Size ─────────────────────────────────────────────────────────────────

    def size(self) -> int:
        """Return the number of nodes in the tree.

        Returns:
            Total node count.

        Time Complexity: O(n)
        """
        return self._size(self._root)

    def _size(self, node: Optional[TreeNode]) -> int:
        """Recursive size helper."""
        if node is None:
            return 0
        return 1 + self._size(node.left) + self._size(node.right)

    # ── Is Balanced ──────────────────────────────────────────────────────────

    def is_balanced(self) -> bool:
        """Check if the tree is height-balanced.

        A tree is balanced if for every node, the height difference between
        left and right subtrees is at most 1.

        Returns:
            True if balanced.

        Time Complexity: O(n)
        """

        def _check(node: Optional[TreeNode]) -> int:
            """Return height if balanced, -1 if unbalanced."""
            if node is None:
                return 0
            left_h = _check(node.left)
            if left_h == -1:
                return -1
            right_h = _check(node.right)
            if right_h == -1:
                return -1
            if abs(left_h - right_h) > 1:
                return -1
            return 1 + max(left_h, right_h)

        return _check(self._root) != -1

    # ── Traversals (Recursive) ────────────────────────────────────────────────

    def preorder(self) -> List[Any]:
        """Pre-order traversal: root → left → right (recursive).

        Returns:
            List of values in pre-order.

        Time Complexity: O(n)
        """
        result: List[Any] = []

        def _traverse(node: Optional[TreeNode]) -> None:
            if node is None:
                return
            result.append(node.data)
            _traverse(node.left)
            _traverse(node.right)

        _traverse(self._root)
        return result

    def inorder(self) -> List[Any]:
        """In-order traversal: left → root → right (recursive).

        Returns:
            List of values in in-order.

        Time Complexity: O(n)
        """
        result: List[Any] = []

        def _traverse(node: Optional[TreeNode]) -> None:
            if node is None:
                return
            _traverse(node.left)
            result.append(node.data)
            _traverse(node.right)

        _traverse(self._root)
        return result

    def postorder(self) -> List[Any]:
        """Post-order traversal: left → right → root (recursive).

        Returns:
            List of values in post-order.

        Time Complexity: O(n)
        """
        result: List[Any] = []

        def _traverse(node: Optional[TreeNode]) -> None:
            if node is None:
                return
            _traverse(node.left)
            _traverse(node.right)
            result.append(node.data)

        _traverse(self._root)
        return result

    # ── Traversals (Iterative) ────────────────────────────────────────────────

    def preorder_iterative(self) -> List[Any]:
        """Pre-order traversal: root → left → right (iterative).

        Uses a stack: push right first, then left (so left is processed next).

        Returns:
            List of values in pre-order.

        Time Complexity: O(n)
        Space Complexity: O(h) where h is height.
        """
        result: List[Any] = []
        if self._root is None:
            return result

        stack = [self._root]
        while stack:
            node = stack.pop()
            result.append(node.data)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

        return result

    def inorder_iterative(self) -> List[Any]:
        """In-order traversal: left → root → right (iterative).

        Uses a stack to simulate recursion. Traverses as far left as possible,
        then visits the node, then moves right.

        Returns:
            List of values in in-order.

        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        result: List[Any] = []
        stack: List[TreeNode] = []
        current = self._root

        while stack or current is not None:
            # Go as far left as possible
            while current is not None:
                stack.append(current)
                current = current.left
            # Visit node
            current = stack.pop()
            result.append(current.data)
            # Move right
            current = current.right

        return result

    def postorder_iterative(self) -> List[Any]:
        """Post-order traversal: left → right → root (iterative).

        Uses two stacks: process in modified pre-order (root→right→left)
        onto stack2, then pop stack2 for post-order.

        Returns:
            List of values in post-order.

        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        result: List[Any] = []
        if self._root is None:
            return result

        stack1 = [self._root]
        stack2: List[TreeNode] = []

        while stack1:
            node = stack1.pop()
            stack2.append(node)
            if node.left:
                stack1.append(node.left)
            if node.right:
                stack1.append(node.right)

        while stack2:
            result.append(stack2.pop().data)

        return result

    def levelorder(self) -> List[Any]:
        """Level-order (BFS) traversal.

        Returns:
            List of values level by level.

        Time Complexity: O(n)
        """
        result: List[Any] = []
        if self._root is None:
            return result

        queue = deque([self._root])
        while queue:
            node = queue.popleft()
            result.append(node.data)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        return result

    def levelorder_by_level(self) -> List[List[Any]]:
        """Level-order traversal grouped by level.

        Returns:
            List of lists, each inner list contains values at that level.

        Time Complexity: O(n)
        """
        result: List[List[Any]] = []
        if self._root is None:
            return result

        queue = deque([self._root])
        while queue:
            level_size = len(queue)
            level: List[Any] = []
            for _ in range(level_size):
                node = queue.popleft()
                level.append(node.data)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.append(level)

        return result

    def __contains__(self, data: Any) -> bool:
        """Support `in` operator."""
        return self.search(data)

    def __len__(self) -> int:
        """Support len()."""
        return self.size()

    def __str__(self) -> str:
        """Return level-order representation."""
        return str(self.levelorder())

    def __repr__(self) -> str:
        """Return detailed representation."""
        return f"BinaryTree(size={self.size()}, height={self.height()})"


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
    bt = BinaryTree()
    check("empty is_empty", bt.is_empty())
    check("empty height == -1", bt.height() == -1)
    check("empty size == 0", bt.size() == 0)
    check("empty search False", not bt.search(1))
    check("empty root None", bt.root() is None)

    # ── Insert ────────────────────────────────────────────────────────────────
    print("\nInsert:")
    bt.insert(1)
    bt.insert(2)
    bt.insert(3)
    bt.insert(4)
    bt.insert(5)
    check("size after 5 inserts", bt.size() == 5)
    check("height after inserts", bt.height() == 2)  # 3-level complete tree
    check("search(3)", bt.search(3))
    check("search(5)", bt.search(5))
    check("search(6) False", not bt.search(6))
    check("search_dfs(4)", bt.search_dfs(4))
    check("search_dfs(10) False", not bt.search_dfs(10))

    # ── Traversals (Recursive) ────────────────────────────────────────────────
    print("\nRecursive Traversals:")
    # Tree:     1
    #         /   \
    #        2     3
    #       / \
    #      4   5
    check("preorder", bt.preorder() == [1, 2, 4, 5, 3])
    check("inorder", bt.inorder() == [4, 2, 5, 1, 3])
    check("postorder", bt.postorder() == [4, 5, 2, 3, 1])
    check("levelorder", bt.levelorder() == [1, 2, 3, 4, 5])
    check("levelorder_by_level", bt.levelorder_by_level() == [[1], [2, 3], [4, 5]])

    # ── Traversals (Iterative) ────────────────────────────────────────────────
    print("\nIterative Traversals:")
    check("preorder_iter", bt.preorder_iterative() == [1, 2, 4, 5, 3])
    check("inorder_iter", bt.inorder_iterative() == [4, 2, 5, 1, 3])
    check("postorder_iter", bt.postorder_iterative() == [4, 5, 2, 3, 1])

    # ── Empty tree traversals ─────────────────────────────────────────────────
    print("\nEmpty tree traversals:")
    empty = BinaryTree()
    check("empty preorder", empty.preorder() == [])
    check("empty inorder", empty.inorder() == [])
    check("empty postorder", empty.postorder() == [])
    check("empty levelorder", empty.levelorder() == [])

    # ── Delete ────────────────────────────────────────────────────────────────
    print("\nDelete:")
    bt2 = BinaryTree()
    for x in [1, 2, 3, 4, 5]:
        bt2.insert(x)
    check("delete(3) True", bt2.delete(3))
    check("size after delete", bt2.size() == 4)
    check("search(3) False after delete", not bt2.search(3))

    # Delete root
    bt3 = BinaryTree()
    for x in [10, 20, 30]:
        bt3.insert(x)
    check("delete root(10)", bt3.delete(10))
    check("root data changed", bt3.root().data != 10)
    check("size after root delete", bt3.size() == 2)

    # Delete non-existent
    check("delete non-existent False", bt3.delete(999) is False)

    # ── Is Balanced ───────────────────────────────────────────────────────────
    print("\nIs Balanced:")
    balanced = BinaryTree()
    for x in [1, 2, 3, 4, 5]:
        balanced.insert(x)
    check("complete tree is balanced", balanced.is_balanced())

    # Create unbalanced tree manually
    unbalanced = BinaryTree()
    unbalanced._root = TreeNode(1)
    unbalanced._root.right = TreeNode(2)
    unbalanced._root.right.right = TreeNode(3)
    check("right-skewed is NOT balanced", not unbalanced.is_balanced())

    single = BinaryTree()
    single.insert(1)
    check("single node balanced", single.is_balanced())

    # ── dunder methods ────────────────────────────────────────────────────────
    print("\nDunder methods:")
    check("__len__", len(bt) == 5)
    check("__contains__", 4 in bt)
    check("__contains__ not", 99 not in bt)

    # ── Summary ───────────────────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
