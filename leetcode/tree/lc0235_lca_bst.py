"""
LeetCode 235: Lowest Common Ancestor of a Binary Search Tree
https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/

Given a binary search tree (BST), find the lowest common ancestor (LCA) node
of two given nodes in the BST. The LCA is defined between two nodes p and q
as the lowest node in T that has both p and q as descendants (where we allow
a node to be a descendant of itself).

Example:
  Input:  root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8
  Output: 6

Approaches:
1. Iterative (use BST property — p < root < q → root is LCA) — O(h) time, O(1) space
2. Recursive — O(h) time, O(h) space
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


def lowest_common_ancestor_recursive(
    root: TreeNode, p: TreeNode, q: TreeNode
) -> TreeNode:
    """Recursive: use BST property.

    Time:  O(h)
    Space: O(h)
    """
    if p.val < root.val and q.val < root.val:
        assert root.left is not None
        return lowest_common_ancestor_recursive(root.left, p, q)
    if p.val > root.val and q.val > root.val:
        assert root.right is not None
        return lowest_common_ancestor_recursive(root.right, p, q)
    return root


def lowest_common_ancestor(
    root: TreeNode, p: TreeNode, q: TreeNode
) -> TreeNode:
    """Iterative: walk down based on BST ordering.

    Time:  O(h)
    Space: O(1)
    """
    cur: Optional[TreeNode] = root
    while cur:
        if p.val < cur.val and q.val < cur.val:
            cur = cur.left
        elif p.val > cur.val and q.val > cur.val:
            cur = cur.right
        else:
            return cur
    return root  # unreachable


# ---------- Helpers ----------
def build_tree(values: list[Optional[int]], idx: int = 0) -> Optional[TreeNode]:
    if idx >= len(values) or values[idx] is None:
        return None
    root = TreeNode(values[idx])  # type: ignore[arg-type]
    root.left = build_tree(values, 2 * idx + 1)
    root.right = build_tree(values, 2 * idx + 2)
    return root


def find_node(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    if root is None:
        return None
    if root.val == val:
        return root
    left = find_node(root.left, val)
    if left:
        return left
    return find_node(root.right, val)


# ---------- Tests ----------
if __name__ == "__main__":
    for fn_name, fn in [("recursive", lowest_common_ancestor_recursive),
                         ("iterative", lowest_common_ancestor)]:
        # Test 1: different subtrees
        root = build_tree([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])
        assert root is not None
        p = find_node(root, 2)
        q = find_node(root, 8)
        assert p and q
        print(f"{fn_name} Test 1:", "✓" if fn(root, p, q).val == 6 else "✗")

        # Test 2: same subtree
        p = find_node(root, 2)
        q = find_node(root, 4)
        assert p and q
        print(f"{fn_name} Test 2:", "✓" if fn(root, p, q).val == 2 else "✗")

        # Test 3: p is ancestor
        p = find_node(root, 2)
        q = find_node(root, 0)
        assert p and q
        print(f"{fn_name} Test 3:", "✓" if fn(root, p, q).val == 2 else "✗")
