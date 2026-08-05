"""
LeetCode 112: Path Sum
https://leetcode.com/problems/path-sum/

Given the root of a binary tree and an integer targetSum, return True if the
tree has a root-to-leaf path such that adding up all the values along the
path equals targetSum. A leaf is a node with no children.

Example:
  Input:  root = [5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum = 22
  Output: True (5→4→11→2)

Approaches:
1. Recursive DFS — O(n) time, O(h) space
2. Iterative DFS with stack — O(n) time, O(h) space
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


def has_path_sum_recursive(
    root: Optional[TreeNode], target_sum: int
) -> bool:
    """Recursive DFS.

    Time:  O(n)
    Space: O(h)
    """
    if root is None:
        return False

    target_sum -= root.val
    # Leaf check
    if root.left is None and root.right is None:
        return target_sum == 0

    return has_path_sum_recursive(root.left, target_sum) or has_path_sum_recursive(
        root.right, target_sum
    )


def has_path_sum(root: Optional[TreeNode], target_sum: int) -> bool:
    """Iterative DFS using stack.

    Time:  O(n)
    Space: O(h)
    """
    if root is None:
        return False

    stack: list[tuple[TreeNode, int]] = [(root, target_sum)]

    while stack:
        node, remaining = stack.pop()
        if node.left is None and node.right is None and node.val == remaining:
            return True
        if node.right:
            stack.append((node.right, remaining - node.val))
        if node.left:
            stack.append((node.left, remaining - node.val))

    return False


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
    for fn_name, fn in [("recursive", has_path_sum_recursive),
                         ("iterative", has_path_sum)]:
        # Test 1: path exists
        root = build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])
        print(f"{fn_name} Test 1:", "✓" if fn(root, 22) else "✗")

        # Test 2: path does not exist
        root = build_tree([1, 2, 3])
        print(f"{fn_name} Test 2:", "✓" if not fn(root, 5) else "✗")

        # Test 3: empty tree
        print(f"{fn_name} Test 3:", "✓" if not fn(None, 0) else "✗")

        # Test 4: single node == target
        root = build_tree([1])
        print(f"{fn_name} Test 4:", "✓" if fn(root, 1) else "✗")
