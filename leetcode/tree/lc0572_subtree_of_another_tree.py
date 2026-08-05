"""
LeetCode 572: Subtree of Another Tree
https://leetcode.com/problems/subtree-of-another-tree/

Given the roots of two binary trees root and subRoot, return True if there
is a subtree of root with the same structure and node values of subRoot and
False otherwise. A subtree of a binary tree tree is a tree that consists of
a node in tree and all of this node's descendants. The tree tree could also
be considered as a subtree of itself.

Example:
  Input:  root = [3,4,5,1,2], subRoot = [4,1,2]
  Output: True

Approaches:
1. Check every node (DFS + same-tree check) — O(m·n) time, O(h) space
2. Serialize + string matching — O(m+n) time, O(m+n) space
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


def _is_same_tree(
    p: Optional[TreeNode], q: Optional[TreeNode]
) -> bool:
    """Check if two trees are identical."""
    if p is None and q is None:
        return True
    if p is None or q is None:
        return False
    if p.val != q.val:
        return False
    return _is_same_tree(p.left, q.left) and _is_same_tree(p.right, q.right)


def is_subtree_dfs(
    root: Optional[TreeNode], sub_root: Optional[TreeNode]
) -> bool:
    """DFS: at each node, check if subtree starting here matches subRoot.

    Time:  O(m · n) worst case
    Space: O(h)
    """
    if root is None:
        return sub_root is None
    if _is_same_tree(root, sub_root):
        return True
    return is_subtree_dfs(root.left, sub_root) or is_subtree_dfs(
        root.right, sub_root
    )


def is_subtree(
    root: Optional[TreeNode], sub_root: Optional[TreeNode]
) -> bool:
    """Serialize both trees and check if subRoot's serialization is a
    substring of root's serialization.

    Time:  O(m + n)
    Space: O(m + n)
    """

    def serialize(node: Optional[TreeNode]) -> str:
        """Serialize with special markers for null and value boundaries."""
        if node is None:
            return "#"  # null marker
        return f"^{node.val}${serialize(node.left)}{serialize(node.right)}"

    root_str = serialize(root)
    sub_str = serialize(sub_root)
    return sub_str in root_str


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
    for fn_name, fn in [("dfs", is_subtree_dfs),
                         ("serialize", is_subtree)]:
        # Test 1: subtree exists
        root = build_tree([3, 4, 5, 1, 2])
        sub = build_tree([4, 1, 2])
        print(f"{fn_name} Test 1:", "✓" if fn(root, sub) else "✗")

        # Test 2: not a subtree (partial match)
        root = build_tree([3, 4, 5, 1, 2, None, None, None, None, 0])
        sub = build_tree([4, 1, 2])
        print(f"{fn_name} Test 2:", "✓" if not fn(root, sub) else "✗")

        # Test 3: root == subRoot
        root = build_tree([1, 2, 3])
        sub = build_tree([1, 2, 3])
        print(f"{fn_name} Test 3:", "✓" if fn(root, sub) else "✗")

        # Test 4: empty subRoot (should always be true)
        root = build_tree([1, 2, 3])
        print(f"{fn_name} Test 4:", "✓" if fn(root, None) else "✗")
