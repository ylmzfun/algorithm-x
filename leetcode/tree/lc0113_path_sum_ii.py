"""
LeetCode 113: Path Sum II
https://leetcode.com/problems/path-sum-ii/

Given the root of a binary tree and an integer targetSum, return all
root-to-leaf paths where the sum of the node values in the path equals
targetSum. Each path should be returned as a list of the node values, not
node references.

Example:
  Input:  root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
  Output: [[5,4,11,2],[5,8,4,5]]

Approaches:
1. Backtracking DFS — O(n) time, O(h) space + output
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


def path_sum(root: Optional[TreeNode], target_sum: int) -> list[list[int]]:
    """Backtracking DFS.

    Time:  O(n)
    Space: O(h) stack + O(n·h) for output paths
    """
    result: list[list[int]] = []
    path: list[int] = []

    def backtrack(node: Optional[TreeNode], remaining: int) -> None:
        if node is None:
            return

        path.append(node.val)

        if node.left is None and node.right is None and node.val == remaining:
            result.append(list(path))
        else:
            backtrack(node.left, remaining - node.val)
            backtrack(node.right, remaining - node.val)

        path.pop()  # backtrack

    backtrack(root, target_sum)
    return result


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
    # Test 1: multiple paths
    root = build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1])
    res = path_sum(root, 22)
    expected = [[5, 4, 11, 2], [5, 8, 4, 5]]
    print("Test 1:", "✓" if sorted([tuple(p) for p in res]) == sorted([tuple(p) for p in expected]) else "✗")

    # Test 2: no path
    root = build_tree([1, 2, 3])
    print("Test 2:", "✓" if path_sum(root, 5) == [] else "✗")

    # Test 3: single path
    root = build_tree([1, 2])
    print("Test 3:", "✓" if path_sum(root, 3) == [[1, 2]] else "✗")

    # Test 4: empty
    print("Test 4:", "✓" if path_sum(None, 0) == [] else "✗")
