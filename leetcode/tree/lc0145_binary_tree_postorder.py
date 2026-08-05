"""
LeetCode 145: Binary Tree Postorder Traversal
https://leetcode.com/problems/binary-tree-postorder-traversal/

Given the root of a binary tree, return the postorder traversal of its nodes'
values.

Example:
  Input:  root = [1,null,2,3]
  Output: [3,2,1]

Approaches:
1. Recursive — O(n) time, O(h) space
2. Iterative (two-stack or reverse preorder) — O(n) time, O(h) space
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


def postorder_recursive(root: Optional[TreeNode]) -> list[int]:
    """Recursive postorder.

    Time:  O(n)
    Space: O(h)
    """
    result: list[int] = []

    def dfs(node: Optional[TreeNode]) -> None:
        if node is None:
            return
        dfs(node.left)
        dfs(node.right)
        result.append(node.val)

    dfs(root)
    return result


def postorder_traversal(root: Optional[TreeNode]) -> list[int]:
    """Iterative: reverse of (root→right→left) preorder.

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
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)

    # Reverse: preorder (root→right→left) becomes postorder (left→right→root)
    result.reverse()
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
    for fn_name, fn in [("recursive", postorder_recursive),
                         ("iterative", postorder_traversal)]:
        # Test 1: standard
        root = build_tree([1, None, 2, None, None, 3])
        print(f"{fn_name} Test 1:", "✓" if fn(root) == [3, 2, 1] else "✗")

        # Test 2: full tree
        root = build_tree([1, 2, 3, 4, 5])
        print(f"{fn_name} Test 2:", "✓" if fn(root) == [4, 5, 2, 3, 1] else "✗")

        # Test 3: empty
        print(f"{fn_name} Test 3:", "✓" if fn(None) == [] else "✗")

        # Test 4: single node
        root = build_tree([5])
        print(f"{fn_name} Test 4:", "✓" if fn(root) == [5] else "✗")
