"""
LeetCode 337: House Robber III

The thief has found himself a new place for his thievery again.
There is only one entrance to this area, called root.

Besides the root, each house has one and only one parent house.
After a tour, the smart thief realized that all houses in this place
form a binary tree. It will automatically contact the police if two
directly-linked houses were broken into on the same night.

Given the root of the binary tree, return the maximum amount of money
the thief can rob without alerting the police.

Constraints:
- The number of nodes in the tree is in the range [1, 10^4].
- 0 <= Node.val <= 10^4
"""

from typing import Optional, Tuple


class TreeNode:
    def __init__(self, val: int = 0, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    # ── Tree DP (Post-order with State) O(n) time, O(h) space ────────────
    def rob(self, root: Optional[TreeNode]) -> int:
        """
        For each node, return (rob_this, skip_this):
        - rob_this: max profit if we rob this node
        - skip_this: max profit if we skip this node
        """
        def dfs(node: Optional[TreeNode]) -> Tuple[int, int]:
            if not node:
                return (0, 0)

            left_rob, left_skip = dfs(node.left)
            right_rob, right_skip = dfs(node.right)

            # If we rob this node, we must skip children
            rob_this = node.val + left_skip + right_skip

            # If we skip this node, we can choose max for each child
            skip_this = max(left_rob, left_skip) + max(right_rob, right_skip)

            return (rob_this, skip_this)

        rob_root, skip_root = dfs(root)
        return max(rob_root, skip_root)


# ── Helpers for testing ─────────────────────────────────────────────────────
def build_tree(values, idx=0):
    """Build binary tree from list (level order). None = no node."""
    if idx >= len(values) or values[idx] is None:
        return None
    root = TreeNode(values[idx])
    root.left = build_tree(values, 2 * idx + 1)
    root.right = build_tree(values, 2 * idx + 2)
    return root


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([3, 2, 3, None, 3, None, 1], 7),
        ([3, 4, 5, 1, 3, None, 1], 9),
        ([1], 1),
        ([2, 1, 3, None, 4], 7),
        ([4, 1, None, 2, None, None, None, 3], 7),
    ]

    for values, expected in tests:
        root = build_tree(values)
        result = sol.rob(root)
        status = "✓" if result == expected else "✗"
        print(f"{values} → {result} (expected {expected}) {status}")
