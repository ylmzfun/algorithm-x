"""
LeetCode 230: Kth Smallest Element in a BST
https://leetcode.com/problems/kth-smallest-element-in-a-bst/

Given the root of a binary search tree, and an integer k, return the k-th
smallest value (1-indexed) of all the values of the nodes in the tree.

Example:
  Input:  root = [3,1,4,null,2], k = 1
  Output: 1

Approaches:
1. Inorder traversal (iterative) with early stop — O(h+k) time, O(h) space
2. Recursive inorder with counter — O(n) worst, O(h) space
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


def kth_smallest_recursive(root: Optional[TreeNode], k: int) -> int:
    """Recursive inorder with counter for early stop.

    Time:  O(n) worst, O(h+k) average
    Space: O(h)
    """
    result: list[int] = []
    count = 0

    def inorder(node: Optional[TreeNode]) -> None:
        nonlocal count
        if node is None or count >= k:
            return
        inorder(node.left)
        if count < k:
            result.append(node.val)
            count += 1
        inorder(node.right)

    inorder(root)
    return result[-1]


def kth_smallest(root: Optional[TreeNode], k: int) -> int:
    """Iterative inorder with early stop.

    Time:  O(h + k)
    Space: O(h)
    """
    stack: list[TreeNode] = []
    cur: Optional[TreeNode] = root

    while True:
        while cur is not None:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        k -= 1
        if k == 0:
            return cur.val
        cur = cur.right


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
    for fn_name, fn in [("recursive", kth_smallest_recursive),
                         ("iterative", kth_smallest)]:
        # Test 1: standard
        root = build_tree([3, 1, 4, None, 2])
        print(f"{fn_name} Test 1:", "✓" if fn(root, 1) == 1 else "✗")

        # Test 2: k=3
        root = build_tree([5, 3, 6, 2, 4, None, None, 1])
        print(f"{fn_name} Test 2:", "✓" if fn(root, 3) == 3 else "✗")

        # Test 3: k=1
        root = build_tree([2, 1, 3])
        print(f"{fn_name} Test 3:", "✓" if fn(root, 1) == 1 else "✗")

        # Test 4: single node
        root = build_tree([1])
        print(f"{fn_name} Test 4:", "✓" if fn(root, 1) == 1 else "✗")
