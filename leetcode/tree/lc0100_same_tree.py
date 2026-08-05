"""
LeetCode 100: Same Tree
https://leetcode.com/problems/same-tree/

Given the roots of two binary trees p and q, write a function to check if
they are the same or not. Two binary trees are considered the same if they
are structurally identical, and the nodes have the same value.

Example:
  Input:  p = [1,2,3], q = [1,2,3]
  Output: True

Approaches:
1. Recursive DFS — O(n) time, O(h) space
2. Iterative BFS/DFS — O(n) time, O(n) space
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


def is_same_tree_recursive(
    p: Optional[TreeNode], q: Optional[TreeNode]
) -> bool:
    """Recursive DFS comparison.

    Time:  O(n)
    Space: O(h)
    """
    if p is None and q is None:
        return True
    if p is None or q is None:
        return False
    if p.val != q.val:
        return False
    return is_same_tree_recursive(p.left, q.left) and is_same_tree_recursive(
        p.right, q.right
    )


def is_same_tree(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    """Iterative BFS using queue.

    Time:  O(n)
    Space: O(n)
    """
    dq: deque[tuple[Optional[TreeNode], Optional[TreeNode]]] = deque()
    dq.append((p, q))

    while dq:
        n1, n2 = dq.popleft()
        if n1 is None and n2 is None:
            continue
        if n1 is None or n2 is None:
            return False
        if n1.val != n2.val:
            return False
        dq.append((n1.left, n2.left))
        dq.append((n1.right, n2.right))

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
    for fn_name, fn in [("recursive", is_same_tree_recursive),
                         ("iterative", is_same_tree)]:
        # Test 1: same
        p = build_tree([1, 2, 3])
        q = build_tree([1, 2, 3])
        print(f"{fn_name} Test 1:", "✓" if fn(p, q) else "✗")

        # Test 2: different values
        p = build_tree([1, 2, 1])
        q = build_tree([1, 1, 2])
        print(f"{fn_name} Test 2:", "✓" if not fn(p, q) else "✗")

        # Test 3: different structures
        p = build_tree([1, 2])
        q = build_tree([1, None, 2])
        print(f"{fn_name} Test 3:", "✓" if not fn(p, q) else "✗")

        # Test 4: both empty
        print(f"{fn_name} Test 4:", "✓" if fn(None, None) else "✗")
