"""
LeetCode 226: Invert Binary Tree
https://leetcode.com/problems/invert-binary-tree/

Given the root of a binary tree, invert the tree, and return its root.

Example:
  Input:  root = [4,2,7,1,3,6,9]
  Output: [4,7,2,9,6,3,1]

Approaches:
1. Recursive DFS — O(n) time, O(h) space
2. Iterative BFS — O(n) time, O(w) space
"""

from __future__ import annotations
from typing import Optional
from collections import deque


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


def invert_tree_recursive(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """Recursive: swap left and right, then recurse.

    Time:  O(n)
    Space: O(h)
    """
    if root is None:
        return None

    root.left, root.right = root.right, root.left
    invert_tree_recursive(root.left)
    invert_tree_recursive(root.right)
    return root


def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """Iterative BFS.

    Time:  O(n)
    Space: O(w)
    """
    if root is None:
        return None

    q: deque[TreeNode] = deque([root])
    while q:
        node = q.popleft()
        node.left, node.right = node.right, node.left
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)

    return root


# ---------- Helpers ----------
def build_tree(values: list[Optional[int]], idx: int = 0) -> Optional[TreeNode]:
    if idx >= len(values) or values[idx] is None:
        return None
    root = TreeNode(values[idx])  # type: ignore[arg-type]
    root.left = build_tree(values, 2 * idx + 1)
    root.right = build_tree(values, 2 * idx + 2)
    return root


def level_order(root: Optional[TreeNode]) -> list[list[int]]:
    if root is None:
        return []
    result: list[list[int]] = []
    q: deque[TreeNode] = deque([root])
    while q:
        level: list[int] = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        result.append(level)
    return result


# ---------- Tests ----------
if __name__ == "__main__":
    for fn_name, fn in [("recursive", invert_tree_recursive),
                         ("iterative", invert_tree)]:
        # Test 1: standard
        root = build_tree([4, 2, 7, 1, 3, 6, 9])
        inv = fn(root)
        print(f"{fn_name} Test 1:", "✓"
              if level_order(inv) == [[4], [7, 2], [9, 6, 3, 1]] else "✗")

        # Test 2: single node
        root = build_tree([1])
        inv = fn(root)
        print(f"{fn_name} Test 2:", "✓"
              if inv and inv.val == 1 and inv.left is None and inv.right is None
              else "✗")

        # Test 3: empty
        print(f"{fn_name} Test 3:", "✓" if fn(None) is None else "✗")

        # Test 4: left-skewed
        root = build_tree([1, 2, None, 3])
        inv = fn(root)
        print(f"{fn_name} Test 4:", "✓"
              if level_order(inv) == [[1], [2], [3]] else "✗")
