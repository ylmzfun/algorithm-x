"""
LeetCode 144: Binary Tree Preorder Traversal
https://leetcode.com/problems/binary-tree-preorder-traversal/

Given the root of a binary tree, return the preorder traversal of its nodes'
values.

Example:
  Input:  root = [1,null,2,3]
  Output: [1,2,3]

Approaches:
1. Recursive — O(n) time, O(h) space
2. Iterative (stack) — O(n) time, O(h) space
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


def preorder_recursive(root: Optional[TreeNode]) -> list[int]:
    """Recursive preorder.

    Time:  O(n)
    Space: O(h)
    """
    result: list[int] = []

    def dfs(node: Optional[TreeNode]) -> None:
        if node is None:
            return
        result.append(node.val)
        dfs(node.left)
        dfs(node.right)

    dfs(root)
    return result


def preorder_traversal(root: Optional[TreeNode]) -> list[int]:
    """Iterative preorder using stack (push right first, then left).

    Time:  O(n)
    Space: O(h)
    """
    if root is None:
        return []

    result: list[int] = []
    stack: list[TreeNode] = [root]

    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right:  # Push right first so left pops first
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return result


# ---------- Helpers ----------
def build_tree(values: list[Optional[int]], idx: int = 0) -> Optional[TreeNode]:
    if idx >= len(values) or values[idx] is None:
        return None
    root = TreeNode(values[idx])  # type: ignore[arg-type]
    root.left = build_tree(values, 2 * idx + 1)
    root.right = build_tree(values, 2 * idx + 2)
    return root


# ---------- Tests ----------
if __name__ == "__main__":
    for fn_name, fn in [("recursive", preorder_recursive),
                         ("iterative", preorder_traversal)]:
        # Test 1: standard
        root = build_tree([1, None, 2, None, None, 3])
        print(f"{fn_name} Test 1:", "✓" if fn(root) == [1, 2, 3] else "✗")

        # Test 2: full tree
        root = build_tree([1, 2, 3, 4, 5])
        print(f"{fn_name} Test 2:", "✓" if fn(root) == [1, 2, 4, 5, 3] else "✗")

        # Test 3: empty
        print(f"{fn_name} Test 3:", "✓" if fn(None) == [] else "✗")

        # Test 4: single node
        root = build_tree([5])
        print(f"{fn_name} Test 4:", "✓" if fn(root) == [5] else "✗")
