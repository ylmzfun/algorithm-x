"""
LeetCode 101: Symmetric Tree
https://leetcode.com/problems/symmetric-tree/

Given the root of a binary tree, check whether it is a mirror of itself
(i.e., symmetric around its center).

Example:
  Input:  root = [1,2,2,3,4,4,3]
  Output: True

Approaches:
1. Recursive mirror comparison — O(n) time, O(h) space
2. Iterative BFS — O(n) time, O(n) space
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


def is_symmetric_recursive(root: Optional[TreeNode]) -> bool:
    """Recursive mirror check.

    Time:  O(n)
    Space: O(h)
    """

    def is_mirror(
        t1: Optional[TreeNode], t2: Optional[TreeNode]
    ) -> bool:
        if t1 is None and t2 is None:
            return True
        if t1 is None or t2 is None:
            return False
        return (
            t1.val == t2.val
            and is_mirror(t1.left, t2.right)
            and is_mirror(t1.right, t2.left)
        )

    return is_mirror(root, root)


def is_symmetric(root: Optional[TreeNode]) -> bool:
    """Iterative BFS — compare nodes in pairs.

    Time:  O(n)
    Space: O(n)
    """
    if root is None:
        return True

    q: deque[Optional[TreeNode]] = deque()
    q.append(root.left)
    q.append(root.right)

    while q:
        t1 = q.popleft()
        t2 = q.popleft()
        if t1 is None and t2 is None:
            continue
        if t1 is None or t2 is None:
            return False
        if t1.val != t2.val:
            return False
        q.append(t1.left)
        q.append(t2.right)
        q.append(t1.right)
        q.append(t2.left)

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
    for fn_name, fn in [("recursive", is_symmetric_recursive),
                         ("iterative", is_symmetric)]:
        # Test 1: symmetric
        root = build_tree([1, 2, 2, 3, 4, 4, 3])
        print(f"{fn_name} Test 1:", "✓" if fn(root) else "✗")

        # Test 2: not symmetric
        root = build_tree([1, 2, 2, None, 3, None, 3])
        print(f"{fn_name} Test 2:", "✓" if not fn(root) else "✗")

        # Test 3: single node
        root = build_tree([1])
        print(f"{fn_name} Test 3:", "✓" if fn(root) else "✗")

        # Test 4: empty
        print(f"{fn_name} Test 4:", "✓" if fn(None) else "✗")
