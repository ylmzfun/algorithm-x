"""
LeetCode 111: Minimum Depth of Binary Tree
https://leetcode.com/problems/minimum-depth-of-binary-tree/

Given a binary tree, find its minimum depth. The minimum depth is the number
of nodes along the shortest path from the root node down to the nearest leaf
node. Note: A leaf is a node with no children.

Example:
  Input:  root = [3,9,20,null,null,15,7]
  Output: 2

Approaches:
1. Recursive DFS — O(n) time, O(h) space
2. BFS (early exit on first leaf) — O(n) worst, O(w) space
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


def min_depth_dfs(root: Optional[TreeNode]) -> int:
    """Recursive DFS.

    Time:  O(n)
    Space: O(h)
    """
    if root is None:
        return 0

    # If one child is None, depth is from the other child
    if root.left is None:
        return 1 + min_depth_dfs(root.right)
    if root.right is None:
        return 1 + min_depth_dfs(root.left)

    return 1 + min(min_depth_dfs(root.left), min_depth_dfs(root.right))


def min_depth(root: Optional[TreeNode]) -> int:
    """BFS with early exit on first leaf found.

    Time:  O(n) worst case
    Space: O(w)
    """
    if root is None:
        return 0

    q: deque[tuple[TreeNode, int]] = deque([(root, 1)])

    while q:
        node, depth = q.popleft()
        # Leaf check
        if node.left is None and node.right is None:
            return depth
        if node.left:
            q.append((node.left, depth + 1))
        if node.right:
            q.append((node.right, depth + 1))

    return 0  # unreachable


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
    for fn_name, fn in [("dfs", min_depth_dfs), ("bfs", min_depth)]:
        # Test 1: standard
        root = build_tree([3, 9, 20, None, None, 15, 7])
        print(f"{fn_name} Test 1:", "✓" if fn(root) == 2 else "✗")

        # Test 2: skewed
        root = build_tree([1, 2, None, 3])
        print(f"{fn_name} Test 2:", "✓" if fn(root) == 3 else "✗")

        # Test 3: single node
        root = build_tree([1])
        print(f"{fn_name} Test 3:", "✓" if fn(root) == 1 else "✗")

        # Test 4: empty
        print(f"{fn_name} Test 4:", "✓" if fn(None) == 0 else "✗")
