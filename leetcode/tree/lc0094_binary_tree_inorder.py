"""
LeetCode 94: Binary Tree Inorder Traversal
https://leetcode.com/problems/binary-tree-inorder-traversal/

Given the root of a binary tree, return the inorder traversal of its nodes'
values.

Example:
  Input:  root = [1,null,2,3]
  Output: [1,3,2]

Approaches:
1. Recursive — O(n) time, O(h) space (call stack)
2. Iterative (stack) — O(n) time, O(h) space
3. Morris traversal (threaded binary tree) — O(n) time, O(1) space
"""

from __future__ import annotations
from typing import Optional


class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: Optional[TreeNode] = None,
        right: Optional[TreeNode] = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right


def inorder_recursive(root: Optional[TreeNode]) -> list[int]:
    """Recursive inorder.

    Time:  O(n)
    Space: O(h)
    """
    result: list[int] = []

    def dfs(node: Optional[TreeNode]) -> None:
        if node is None:
            return
        dfs(node.left)
        result.append(node.val)
        dfs(node.right)

    dfs(root)
    return result


def inorder_iterative(root: Optional[TreeNode]) -> list[int]:
    """Iterative inorder using explicit stack.

    Time:  O(n)
    Space: O(h)
    """
    result: list[int] = []
    stack: list[TreeNode] = []
    cur: Optional[TreeNode] = root

    while cur is not None or stack:
        # Go left as far as possible
        while cur is not None:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        result.append(cur.val)
        cur = cur.right

    return result


def inorder_traversal(root: Optional[TreeNode]) -> list[int]:
    """Morris traversal — O(1) space, threaded binary tree.

    Time:  O(n)
    Space: O(1)
    """
    result: list[int] = []
    cur: Optional[TreeNode] = root

    while cur is not None:
        if cur.left is None:
            result.append(cur.val)
            cur = cur.right
        else:
            # Find inorder predecessor
            pred = cur.left
            while pred.right is not None and pred.right != cur:
                pred = pred.right

            if pred.right is None:
                # Create thread
                pred.right = cur
                cur = cur.left
            else:
                # Remove thread
                pred.right = None
                result.append(cur.val)
                cur = cur.right

    return result


# ---------- Helpers ----------
def build_tree(values: list[Optional[int]], idx: int = 0) -> Optional[TreeNode]:
    """Build binary tree from level-order list (null for missing nodes)."""
    if idx >= len(values) or values[idx] is None:
        return None
    root = TreeNode(values[idx])  # type: ignore[arg-type]
    root.left = build_tree(values, 2 * idx + 1)
    root.right = build_tree(values, 2 * idx + 2)
    return root


# ---------- Tests ----------
if __name__ == "__main__":
    for fn_name, fn in [("recursive", inorder_recursive),
                         ("iterative", inorder_iterative),
                         ("morris", inorder_traversal)]:
        # Test 1: standard
        root = build_tree([1, None, 2, None, None, 3])
        res = fn(root)
        print(f"{fn_name} Test 1:", "✓" if res == [1, 3, 2] else "✗")

        # Test 2: full tree
        root = build_tree([4, 2, 5, 1, 3])
        res = fn(root)
        print(f"{fn_name} Test 2:", "✓" if res == [1, 2, 3, 4, 5] else "✗")

        # Test 3: empty
        print(f"{fn_name} Test 3:", "✓" if fn(None) == [] else "✗")

        # Test 4: single node
        root = build_tree([5])
        print(f"{fn_name} Test 4:", "✓" if fn(root) == [5] else "✗")
