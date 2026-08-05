"""
LeetCode 110: Balanced Binary Tree
https://leetcode.com/problems/balanced-binary-tree/

Given a binary tree, determine if it is height-balanced. A height-balanced
binary tree is a binary tree in which the depth of the two subtrees of every
node never differs by more than one.

Example:
  Input:  root = [3,9,20,null,null,15,7]
  Output: True

Approaches:
1. Bottom-up DFS (post-order) return height — O(n) time, O(h) space
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


def is_balanced(root: Optional[TreeNode]) -> bool:
    """Bottom-up: return height if balanced, -1 if not.

    Time:  O(n)
    Space: O(h)
    """

    def height(node: Optional[TreeNode]) -> int:
        if node is None:
            return 0

        left_h = height(node.left)
        if left_h == -1:
            return -1

        right_h = height(node.right)
        if right_h == -1:
            return -1

        if abs(left_h - right_h) > 1:
            return -1

        return 1 + max(left_h, right_h)

    return height(root) != -1


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
    # Test 1: balanced
    root = build_tree([3, 9, 20, None, None, 15, 7])
    print("Test 1:", "✓" if is_balanced(root) else "✗")

    # Test 2: unbalanced
    root = build_tree([1, 2, 2, 3, 3, None, None, 4, 4])
    print("Test 2:", "✓" if not is_balanced(root) else "✗")

    # Test 3: single node
    root = build_tree([1])
    print("Test 3:", "✓" if is_balanced(root) else "✗")

    # Test 4: empty
    print("Test 4:", "✓" if is_balanced(None) else "✗")
