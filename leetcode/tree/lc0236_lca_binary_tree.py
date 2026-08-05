"""
LeetCode 236: Lowest Common Ancestor of a Binary Tree
https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/

Given a binary tree, find the lowest common ancestor (LCA) of two given nodes
in the tree. The LCA is defined between two nodes p and q as the lowest node
in T that has both p and q as descendants (where we allow a node to be a
descendant of itself).

Example:
  Input:  root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
  Output: 3

Approaches:
1. Recursive DFS (post-order) — O(n) time, O(h) space
2. Iterative with parent map — O(n) time, O(n) space
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
    """Recursive post-order: if a node is p or q, return it; if left and right
    both return non-null, current node is LCA.

    Time:  O(n)
    Space: O(h)
    """

    def dfs(node: Optional[TreeNode]) -> Optional[TreeNode]:
        if node is None:
            return None
        if node == p or node == q:
            return node

        left = dfs(node.left)
        right = dfs(node.right)

        if left and right:
            return node
        return left if left else right

    result = dfs(root)
    assert result is not None
    return result


def lowest_common_ancestor(
    root: TreeNode, p: TreeNode, q: TreeNode
) -> TreeNode:
    """Iterative: build parent map via BFS, then trace ancestors of p.

    Time:  O(n)
    Space: O(n)
    """
    parent: dict[TreeNode, TreeNode] = {root: root}
    stack: list[TreeNode] = [root]

    # Build parent pointers until we find both p and q
    while p not in parent or q not in parent:
        node = stack.pop()
        if node.left:
            parent[node.left] = node
            stack.append(node.left)
        if node.right:
            parent[node.right] = node
            stack.append(node.right)

    # Trace ancestors of p
    ancestors: set[TreeNode] = set()
    cur: TreeNode = p
    while cur != parent[cur]:
        ancestors.add(cur)
        cur = parent[cur]
    ancestors.add(root)

    # Find first ancestor of q that's in p's ancestor set
    cur = q
    while cur not in ancestors:
        cur = parent[cur]
    return cur


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
        root = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
        assert root is not None
        p = find_node(root, 5)
        q = find_node(root, 1)
        assert p and q
        print(f"{fn_name} Test 1:", "✓" if fn(root, p, q).val == 3 else "✗")

        # Test 2: p is ancestor of q
        p = find_node(root, 5)
        q = find_node(root, 4)
        assert p and q
        print(f"{fn_name} Test 2:", "✓" if fn(root, p, q).val == 5 else "✗")

        # Test 3: same subtree
        p = find_node(root, 6)
        q = find_node(root, 4)
        assert p and q
        print(f"{fn_name} Test 3:", "✓" if fn(root, p, q).val == 5 else "✗")
