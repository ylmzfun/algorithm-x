"""
LeetCode 105: Construct Binary Tree from Preorder and Inorder Traversal
https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/

Given two integer arrays preorder and inorder where preorder is the preorder
traversal of a binary tree and inorder is the inorder traversal of the same
tree, construct and return the binary tree.

Example:
  Input:  preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
  Output: [3,9,20,null,null,15,7]

Approaches:
1. Recursive with hashmap index lookup — O(n) time, O(n) space
2. Iterative with stack — O(n) time, O(n) space
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


def build_tree_recursive(
    preorder: list[int], inorder: list[int]
) -> Optional[TreeNode]:
    """Recursive with inorder index map for O(1) lookups.

    preorder[0] is root; find its position in inorder to split left/right subtrees.

    Time:  O(n)
    Space: O(n) for hashmap + recursion stack
    """
    inorder_idx = {val: i for i, val in enumerate(inorder)}
    pre_idx = 0

    def helper(left: int, right: int) -> Optional[TreeNode]:
        nonlocal pre_idx
        if left > right:
            return None

        root_val = preorder[pre_idx]
        pre_idx += 1
        root = TreeNode(root_val)

        in_idx = inorder_idx[root_val]
        root.left = helper(left, in_idx - 1)
        root.right = helper(in_idx + 1, right)
        return root

    return helper(0, len(inorder) - 1)


def build_tree(
    preorder: list[int], inorder: list[int]
) -> Optional[TreeNode]:
    """Iterative approach using a stack.

    Time:  O(n)
    Space: O(n)
    """
    if not preorder:
        return None

    root = TreeNode(preorder[0])
    stack: list[TreeNode] = [root]
    inorder_idx = 0

    for i in range(1, len(preorder)):
        node = stack[-1]
        if node.val != inorder[inorder_idx]:
            node.left = TreeNode(preorder[i])
            stack.append(node.left)
        else:
            while stack and stack[-1].val == inorder[inorder_idx]:
                node = stack.pop()
                inorder_idx += 1
            node.right = TreeNode(preorder[i])
            stack.append(node.right)

    return root


# ---------- Helpers ----------
def preorder_traversal(root: Optional[TreeNode]) -> list[int]:
    result: list[int] = []

    def dfs(node: Optional[TreeNode]) -> None:
        if node is None:
            return
        result.append(node.val)
        dfs(node.left)
        dfs(node.right)

    dfs(root)
    return result


def inorder_traversal(root: Optional[TreeNode]) -> list[int]:
    result: list[int] = []

    def dfs(node: Optional[TreeNode]) -> None:
        if node is None:
            return
        dfs(node.left)
        result.append(node.val)
        dfs(node.right)

    dfs(root)
    return result


# ---------- Tests ----------
if __name__ == "__main__":
    for fn_name, fn in [("recursive", build_tree_recursive),
                         ("iterative", build_tree)]:
        # Test 1: standard
        preorder = [3, 9, 20, 15, 7]
        inorder = [9, 3, 15, 20, 7]
        tree = fn(preorder, inorder)
        print(
            f"{fn_name} Test 1:",
            "✓"
            if preorder_traversal(tree) == preorder
            and inorder_traversal(tree) == inorder
            else "✗",
        )

        # Test 2: single node
        tree = fn([1], [1])
        print(
            f"{fn_name} Test 2:",
            "✓"
            if tree and tree.val == 1 and tree.left is None and tree.right is None
            else "✗",
        )

        # Test 3: left-skewed
        preorder = [3, 2, 1]
        inorder = [1, 2, 3]
        tree = fn(preorder, inorder)
        print(
            f"{fn_name} Test 3:",
            "✓"
            if preorder_traversal(tree) == preorder
            else "✗",
        )
