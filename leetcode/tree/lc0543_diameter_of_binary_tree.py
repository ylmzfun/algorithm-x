"""
LeetCode 543: Diameter of Binary Tree
https://leetcode.com/problems/diameter-of-binary-tree/

Given the root of a binary tree, return the length of the diameter of the
tree. The diameter of a binary tree is the length of the longest path between
any two nodes in a tree. This path may or may not pass through the root. The
length of a path between two nodes is represented by the number of edges
between them.

Example:
  Input:  root = [1,2,3,4,5]
  Output: 3 (path [4,2,1,3] or [5,2,1,3])

Approaches:
1. Post-order DFS with global max — O(n) time, O(h) space
   diameter = max(left_height + right_height, max_diameter so far)
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


def diameter_of_binary_tree(root: Optional[TreeNode]) -> int:
    """Post-order: compute height while tracking max diameter.

    Time:  O(n)
    Space: O(h)
    """
    max_diameter = 0

    def height(node: Optional[TreeNode]) -> int:
        nonlocal max_diameter
        if node is None:
            return 0

        left_h = height(node.left)
        right_h = height(node.right)

        # Diameter passing through this node
        max_diameter = max(max_diameter, left_h + right_h)

        # Return height for parent
        return 1 + max(left_h, right_h)

    height(root)
    return max_diameter


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
    root = build_tree([1, 2, 3, 4, 5])
    print("Test 1:", "✓" if diameter_of_binary_tree(root) == 3 else "✗")

    # Test 2: single node (diameter = 0 edges)
    root = build_tree([1])
    print("Test 2:", "✓" if diameter_of_binary_tree(root) == 0 else "✗")

    # Test 3: left-skewed
    root = build_tree([1, 2, None, 3])
    print("Test 3:", "✓" if diameter_of_binary_tree(root) == 2 else "✗")

    # Test 4: V-shaped
    root = build_tree([1, 2, 3])
    print("Test 4:", "✓" if diameter_of_binary_tree(root) == 2 else "✗")
