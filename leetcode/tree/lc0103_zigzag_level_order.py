"""
LeetCode 103: Binary Tree Zigzag Level Order Traversal
https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/

Given the root of a binary tree, return the zigzag level order traversal of
its nodes' values. (i.e., from left to right, then right to left for the
next level and alternate between).

Example:
  Input:  root = [3,9,20,null,null,15,7]
  Output: [[3],[20,9],[15,7]]

Approaches:
1. BFS with direction flag — O(n) time, O(w) space
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


def zigzag_level_order(root: Optional[TreeNode]) -> list[list[int]]:
    """BFS with a boolean flag for direction.

    Time:  O(n)
    Space: O(w)
    """
    if root is None:
        return []

    result: list[list[int]] = []
    q: deque[TreeNode] = deque([root])
    left_to_right = True

    while q:
        level: deque[int] = deque()
        for _ in range(len(q)):
            node = q.popleft()
            if left_to_right:
                level.append(node.val)
            else:
                level.appendleft(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        result.append(list(level))
        left_to_right = not left_to_right

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
    # Test 1: standard
    root = build_tree([3, 9, 20, None, None, 15, 7])
    res = zigzag_level_order(root)
    print("Test 1:", "✓" if res == [[3], [20, 9], [15, 7]] else "✗")

    # Test 2: single node
    root = build_tree([1])
    print("Test 2:", "✓" if zigzag_level_order(root) == [[1]] else "✗")

    # Test 3: empty
    print("Test 3:", "✓" if zigzag_level_order(None) == [] else "✗")

    # Test 4: full tree
    root = build_tree([1, 2, 3, 4, 5, 6, 7])
    print("Test 4:", "✓" if zigzag_level_order(root) == [[1], [3, 2], [4, 5, 6, 7]] else "✗")
