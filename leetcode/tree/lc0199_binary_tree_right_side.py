"""
LeetCode 199: Binary Tree Right Side View
https://leetcode.com/problems/binary-tree-right-side-view/

Given the root of a binary tree, imagine yourself standing on the right side
of it, return the values of the nodes you can see ordered from top to bottom.

Example:
  Input:  root = [1,2,3,null,5,null,4]
  Output: [1,3,4]

Approaches:
1. BFS (level order, take rightmost) — O(n) time, O(w) space
2. DFS (preorder right-first, track depth) — O(n) time, O(h) space
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


def right_side_view_bfs(root: Optional[TreeNode]) -> list[int]:
    """BFS: take the last node at each level.

    Time:  O(n)
    Space: O(w)
    """
    if root is None:
        return []

    result: list[int] = []
    q: deque[TreeNode] = deque([root])

    while q:
        for i in range(len(q)):
            node = q.popleft()
            if i == 0:  # First rightmost (if we push right first)
                pass
            if node.right:  # Push right first so leftmost pops last
                q.append(node.right)
            if node.left:
                q.append(node.left)
        # After this level, the last popped node was the rightmost
        # Actually let's do standard: push left then right, take last
        pass

    # Cleaner version:
    if root is None:
        return []
    result = []
    q2: deque[TreeNode] = deque([root])
    while q2:
        size = len(q2)
        for i in range(size):
            node = q2.popleft()
            if i == size - 1:
                result.append(node.val)
            if node.left:
                q2.append(node.left)
            if node.right:
                q2.append(node.right)
    return result


def right_side_view(root: Optional[TreeNode]) -> list[int]:
    """DFS: preorder, right first, track first visit at each depth.

    Time:  O(n)
    Space: O(h)
    """
    result: list[int] = []

    def dfs(node: Optional[TreeNode], depth: int) -> None:
        if node is None:
            return
        if depth == len(result):
            result.append(node.val)
        dfs(node.right, depth + 1)
        dfs(node.left, depth + 1)

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
    for fn_name, fn in [("bfs", right_side_view_bfs), ("dfs", right_side_view)]:
        # Test 1: standard
        root = build_tree([1, 2, 3, None, 5, None, 4])
        print(f"{fn_name} Test 1:", "✓" if fn(root) == [1, 3, 4] else "✗")

        # Test 2: right-skewed
        root = build_tree([1, None, 2])
        print(f"{fn_name} Test 2:", "✓" if fn(root) == [1, 2] else "✗")

        # Test 3: empty
        print(f"{fn_name} Test 3:", "✓" if fn(None) == [] else "✗")

        # Test 4: single node
        root = build_tree([1])
        print(f"{fn_name} Test 4:", "✓" if fn(root) == [1] else "✗")
