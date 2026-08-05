"""
LeetCode 104: Maximum Depth of Binary Tree
https://leetcode.com/problems/maximum-depth-of-binary-tree/

Given the root of a binary tree, return its maximum depth. A binary tree's
maximum depth is the number of nodes along the longest path from the root
node down to the farthest leaf node.

Example:
  Input:  root = [3,9,20,null,null,15,7]
  Output: 3

Approaches:
1. Recursive DFS — O(n) time, O(h) space
2. Iterative BFS (level count) — O(n) time, O(w) space
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


def max_depth_recursive(root: Optional[TreeNode]) -> int:
    """Recursive DFS.

    Time:  O(n)
    Space: O(h)
    """
    if root is None:
        return 0
    return 1 + max(max_depth_recursive(root.left), max_depth_recursive(root.right))


def max_depth(root: Optional[TreeNode]) -> int:
    """Iterative BFS counting levels.

    Time:  O(n)
    Space: O(w)
    """
    if root is None:
        return 0

    depth = 0
    q: deque[TreeNode] = deque([root])

    while q:
        depth += 1
        for _ in range(len(q)):
            node = q.popleft()
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)

    return depth


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
    for fn_name, fn in [("recursive", max_depth_recursive), ("iterative", max_depth)]:
        # Test 1: standard
        root = build_tree([3, 9, 20, None, None, 15, 7])
        print(f"{fn_name} Test 1:", "✓" if fn(root) == 3 else "✗")

        # Test 2: single node
        root = build_tree([1])
        print(f"{fn_name} Test 2:", "✓" if fn(root) == 1 else "✗")

        # Test 3: empty
        print(f"{fn_name} Test 3:", "✓" if fn(None) == 0 else "✗")

        # Test 4: skewed
        root = build_tree([1, 2, None, 3])
        print(f"{fn_name} Test 4:", "✓" if fn(root) == 3 else "✗")
