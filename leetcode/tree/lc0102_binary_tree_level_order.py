"""
LeetCode 102: Binary Tree Level Order Traversal
https://leetcode.com/problems/binary-tree-level-order-traversal/

Given the root of a binary tree, return the level order traversal of its
nodes' values. (i.e., from left to right, level by level).

Example:
  Input:  root = [3,9,20,null,null,15,7]
  Output: [[3],[9,20],[15,7]]

Approaches:
1. BFS with queue — O(n) time, O(w) space (w = max width)
2. Recursive with level tracking — O(n) time, O(h) space
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


def level_order_bfs(root: Optional[TreeNode]) -> list[list[int]]:
    """BFS with queue — process level by level.

    Time:  O(n)
    Space: O(w) where w = max width
    """
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


def level_order(root: Optional[TreeNode]) -> list[list[int]]:
    """Recursive with depth tracking.

    Time:  O(n)
    Space: O(h)
    """
    result: list[list[int]] = []

    def dfs(node: Optional[TreeNode], depth: int) -> None:
        if node is None:
            return
        if depth == len(result):
            result.append([])
        result[depth].append(node.val)
        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)
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
    for fn_name, fn in [("bfs", level_order_bfs), ("dfs", level_order)]:
        # Test 1: standard
        root = build_tree([3, 9, 20, None, None, 15, 7])
        res = fn(root)
        print(f"{fn_name} Test 1:", "✓" if res == [[3], [9, 20], [15, 7]] else "✗")

        # Test 2: single node
        root = build_tree([1])
        print(f"{fn_name} Test 2:", "✓" if fn(root) == [[1]] else "✗")

        # Test 3: empty
        print(f"{fn_name} Test 3:", "✓" if fn(None) == [] else "✗")

        # Test 4: left-skewed
        root = build_tree([1, 2, None, 3])
        print(f"{fn_name} Test 4:", "✓" if fn(root) == [[1], [2], [3]] else "✗")
