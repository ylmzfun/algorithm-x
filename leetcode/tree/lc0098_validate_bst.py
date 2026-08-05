"""
LeetCode 98: Validate Binary Search Tree
https://leetcode.com/problems/validate-binary-search-tree/

Given the root of a binary tree, determine if it is a valid binary search
tree (BST). A valid BST is defined as:
- The left subtree of a node contains only nodes with keys less than the
  node's key.
- The right subtree of a node contains only nodes with keys greater than
  the node's key.
- Both the left and right subtrees must also be binary search trees.

Example:
  Input:  root = [2,1,3]
  Output: True

Approaches:
1. Range check (recursive with min/max bounds) — O(n) time, O(h) space
2. Inorder traversal (check sorted order) — O(n) time, O(h) space
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


def is_valid_bst_range(root: Optional[TreeNode]) -> bool:
    """Recursive range check with min/max bounds.

    Time:  O(n)
    Space: O(h)
    """

    def validate(
        node: Optional[TreeNode],
        low: float = float("-inf"),
        high: float = float("inf"),
    ) -> bool:
        if node is None:
            return True
        if node.val <= low or node.val >= high:
            return False
        return validate(node.left, low, node.val) and validate(
            node.right, node.val, high
        )

    return validate(root)


def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """Inorder traversal: values must appear in strictly increasing order.

    Time:  O(n)
    Space: O(h)
    """
    prev: float = float("-inf")
    stack: list[TreeNode] = []
    cur: Optional[TreeNode] = root

    while cur is not None or stack:
        while cur is not None:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        if cur.val <= prev:
            return False
        prev = float(cur.val)
        cur = cur.right

    return True


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
    for fn_name, fn in [("range", is_valid_bst_range), ("inorder", is_valid_bst)]:
        # Test 1: valid BST
        root = build_tree([2, 1, 3])
        print(f"{fn_name} Test 1:", "✓" if fn(root) else "✗")

        # Test 2: invalid (right child < root)
        root = build_tree([5, 1, 4, None, None, 3, 6])
        print(f"{fn_name} Test 2:", "✓" if not fn(root) else "✗")

        # Test 3: equal values (invalid)
        root = build_tree([2, 2, 2])
        print(f"{fn_name} Test 3:", "✓" if not fn(root) else "✗")

        # Test 4: grandchild violates (not just direct child)
        root = build_tree([5, 4, 6, None, None, 3, 7])
        print(f"{fn_name} Test 4:", "✓" if not fn(root) else "✗")

        # Test 5: empty
        print(f"{fn_name} Test 5:", "✓" if fn(None) else "✗")
