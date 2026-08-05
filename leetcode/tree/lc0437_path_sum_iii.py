"""
LeetCode 437: Path Sum III
https://leetcode.com/problems/path-sum-iii/

Given the root of a binary tree and an integer targetSum, return the number
of paths where the sum of the values along the path equals targetSum. The
path does not need to start or end at the root or a leaf, but it must go
downwards (i.e., traveling only from parent nodes to child nodes).

Example:
  Input:  root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8
  Output: 3

Approaches:
1. Prefix sum with hashmap — O(n) time, O(n) space
"""

from __future__ import annotations
from typing import Optional
from collections import defaultdict


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


def path_sum(root: Optional[TreeNode], target_sum: int) -> int:
    """Prefix sum approach: at each node, track cumulative sum from root.
    path_count = number of prefix sums equal to (current_sum - target_sum).

    Time:  O(n)
    Space: O(n)
    """
    prefix_sum_count: dict[int, int] = defaultdict(int)
    prefix_sum_count[0] = 1  # Empty path prefix

    def dfs(node: Optional[TreeNode], cur_sum: int) -> int:
        if node is None:
            return 0

        cur_sum += node.val
        count = prefix_sum_count.get(cur_sum - target_sum, 0)

        prefix_sum_count[cur_sum] += 1
        count += dfs(node.left, cur_sum)
        count += dfs(node.right, cur_sum)
        prefix_sum_count[cur_sum] -= 1  # Backtrack

        return count

    return dfs(root, 0)


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
    root = build_tree([10, 5, -3, 3, 2, None, 11, 3, -2, None, 1])
    print("Test 1:", "✓" if path_sum(root, 8) == 3 else "✗")

    # Test 2: single node equals target
    root = build_tree([5])
    print("Test 2:", "✓" if path_sum(root, 5) == 1 else "✗")

    # Test 3: no path
    root = build_tree([1, 2, 3])
    print("Test 3:", "✓" if path_sum(root, 10) == 0 else "✗")

    # Test 4: empty
    print("Test 4:", "✓" if path_sum(None, 0) == 0 else "✗")
