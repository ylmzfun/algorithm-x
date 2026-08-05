"""
LeetCode 297: Serialize and Deserialize Binary Tree
https://leetcode.com/problems/serialize-and-deserialize-binary-tree/

Design an algorithm to serialize and deserialize a binary tree. There is no
restriction on how your serialization/deserialization algorithm should work.
You just need to ensure that a binary tree can be serialized to a string and
this string can be deserialized to the original tree structure.

Example:
  Input:  root = [1,2,3,null,null,4,5]
  Output: [1,2,3,null,null,4,5]

Approaches:
1. Preorder DFS with null markers — O(n) time, O(n) space
2. BFS (level order) with null markers — O(n) time, O(n) space
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


class Codec:
    """Serialization using preorder DFS with 'N' for null nodes."""

    def serialize(self, root: Optional[TreeNode]) -> str:
        """Encodes a tree to a single string.

        Time:  O(n)
        Space: O(n)
        """
        result: list[str] = []

        def dfs(node: Optional[TreeNode]) -> None:
            if node is None:
                result.append("N")
                return
            result.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(result)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        """Decodes your encoded data to tree.

        Time:  O(n)
        Space: O(n)
        """
        if not data:
            return None

        vals = data.split(",")
        self._idx = 0

        def dfs() -> Optional[TreeNode]:
            if self._idx >= len(vals) or vals[self._idx] == "N":
                self._idx += 1
                return None
            node = TreeNode(int(vals[self._idx]))
            self._idx += 1
            node.left = dfs()
            node.right = dfs()
            return node

        return dfs()


def serialize_bfs(root: Optional[TreeNode]) -> str:
    """Alternative: BFS serialization."""
    if root is None:
        return "N"
    result: list[str] = []
    q: deque[Optional[TreeNode]] = deque([root])
    while q:
        node = q.popleft()
        if node is None:
            result.append("N")
        else:
            result.append(str(node.val))
            q.append(node.left)
            q.append(node.right)
    return ",".join(result)


def deserialize_bfs(data: str) -> Optional[TreeNode]:
    """BFS deserialization."""
    if data == "N" or not data:
        return None
    vals = data.split(",")
    root = TreeNode(int(vals[0]))
    q: deque[TreeNode] = deque([root])
    i = 1
    while q and i < len(vals):
        node = q.popleft()
        # Left child
        if vals[i] != "N":
            node.left = TreeNode(int(vals[i]))
            q.append(node.left)
        i += 1
        if i >= len(vals):
            break
        # Right child
        if vals[i] != "N":
            node.right = TreeNode(int(vals[i]))
            q.append(node.right)
        i += 1
    return root


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
    codec = Codec()

    # Test 1: standard
    root = build_tree([1, 2, 3, None, None, 4, 5])
    data = codec.serialize(root)
    restored = codec.deserialize(data)
    print("Test 1:", "✓" if codec.serialize(restored) == data else "✗")

    # Test 2: single node
    root = build_tree([1])
    data = codec.serialize(root)
    restored = codec.deserialize(data)
    print("Test 2:", "✓" if codec.serialize(restored) == data else "✗")

    # Test 3: empty
    data = codec.serialize(None)
    restored = codec.deserialize(data)
    print("Test 3:", "✓" if restored is None else "✗")

    # Test 4: BFS codec
    root = build_tree([1, 2, 3, None, None, 4, 5])
    data = serialize_bfs(root)
    restored = deserialize_bfs(data)
    print("Test 4:", "✓" if serialize_bfs(restored) == data else "✗")
