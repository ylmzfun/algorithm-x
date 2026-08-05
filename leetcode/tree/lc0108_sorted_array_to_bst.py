"""
LeetCode 108: Convert Sorted Array to Binary Search Tree
https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/

Given an integer array nums where the elements are sorted in ascending order,
convert it to a height-balanced binary search tree.

Example:
  Input:  nums = [-10,-3,0,5,9]
  Output: [0,-3,9,-10,null,5]

Approaches:
1. Recursive — pick middle as root, recurse on left/right halves — O(n) time, O(log n) space
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


def sorted_array_to_bst(nums: list[int]) -> Optional[TreeNode]:
    """Recursive: pick middle element as root.

    Time:  O(n)
    Space: O(log n) for balanced recursion stack
    """

    def helper(left: int, right: int) -> Optional[TreeNode]:
        if left > right:
            return None
        mid = (left + right) // 2
        root = TreeNode(nums[mid])
        root.left = helper(left, mid - 1)
        root.right = helper(mid + 1, right)
        return root

    return helper(0, len(nums) - 1)


# ---------- Helpers ----------
def inorder(root: Optional[TreeNode]) -> list[int]:
    result: list[int] = []

    def dfs(n: Optional[TreeNode]) -> None:
        if n is None:
            return
        dfs(n.left)
        result.append(n.val)
        dfs(n.right)

    dfs(root)
    return result


# ---------- Tests ----------
if __name__ == "__main__":
    # Test 1: standard
    nums = [-10, -3, 0, 5, 9]
    tree = sorted_array_to_bst(nums)
    print("Test 1 inorder:", "✓" if inorder(tree) == sorted(nums) else "✗")

    # Test 2: single element
    tree = sorted_array_to_bst([1])
    print("Test 2:", "✓" if tree and tree.val == 1 else "✗")

    # Test 3: empty
    tree = sorted_array_to_bst([])
    print("Test 3:", "✓" if tree is None else "✗")

    # Test 4: two elements
    tree = sorted_array_to_bst([1, 3])
    print("Test 4 inorder:", "✓" if inorder(tree) == [1, 3] else "✗")
