"""
LeetCode 124: Binary Tree Maximum Path Sum
https://leetcode.com/problems/binary-tree-maximum-path-sum/

A path in a binary tree is a sequence of nodes where each pair of adjacent
nodes in the sequence has an edge connecting them. A node can only appear in
the sequence at most once. Note that the path does not need to pass through
the root.

The path sum of a path is the sum of the node's values in the path.
Given the root of a binary tree, return the maximum path sum of any non-empty
path.

Example:
  Input:  root = [1,2,3]
  Output: 6 (path 2→1→3)

Approaches:
1. Post-order DFS with global max — O(n) time, O(h) space
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


def max_path_sum(root: Optional[TreeNode]) -> int:
    """Post-order DFS: at each node, compute the max single-path contribution
    and update the global max for paths that split at this node.

    Time:  O(n)
    Space: O(h)
    """
    max_sum = float("-inf")

    def max_gain(node: Optional[TreeNode]) -> int:
        nonlocal max_sum
        if node is None:
            return 0

        # Max gain from left/right subtrees (ignore negative gains)
        left_gain = max(max_gain(node.left), 0)
        right_gain = max(max_gain(node.right), 0)

        # Path that goes through this node (may split)
        price_newpath = node.val + left_gain + right_gain
        max_sum = max(max_sum, price_newpath)

        # Return max single-branch path for parent
        return node.val + max(left_gain, right_gain)

    max_gain(root)
    return int(max_sum)


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
    root = build_tree([1, 2, 3])
    print("Test 1:", "✓" if max_path_sum(root) == 6 else "✗")

    # Test 2: path through negative node
    root = build_tree([-10, 9, 20, None, None, 15, 7])
    print("Test 2:", "✓" if max_path_sum(root) == 42 else "✗")

    # Test 3: single negative node
    root = build_tree([-3])
    print("Test 3:", "✓" if max_path_sum(root) == -3 else "✗")

    # Test 4: all positive
    root = build_tree([2, 1, 3])
    print("Test 4:", "✓" if max_path_sum(root) == 6 else "✗")
