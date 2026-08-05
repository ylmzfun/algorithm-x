"""
LeetCode 142: Linked List Cycle II
https://leetcode.com/problems/linked-list-cycle-ii/

Given the head of a linked list, return the node where the cycle begins.
If there is no cycle, return None.

Example:
  Input:  head = [3,2,0,-4], pos = 1
  Output: node with val = 2

Approaches:
1. Hash set — O(n) time, O(n) space
2. Floyd's algorithm: detect cycle then find entry — O(n) time, O(1) space

Floyd's cycle detection (two phases):
  Phase 1: slow moves 1 step, fast moves 2 steps — they meet inside the cycle.
  Phase 2: reset one pointer to head; both move 1 step until they meet;
            the meeting point is the cycle entry.
"""

from __future__ import annotations
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional[ListNode] = None) -> None:
        self.val = val
        self.next = next


def detect_cycle_hash(head: Optional[ListNode]) -> Optional[ListNode]:
    """Hash-set approach.

    Time:  O(n)
    Space: O(n)
    """
    visited: set[int] = set()
    cur = head
    while cur:
        if id(cur) in visited:
            return cur
        visited.add(id(cur))
        cur = cur.next
    return None


def detect_cycle(head: Optional[ListNode]) -> Optional[ListNode]:
    """Floyd's algorithm to find cycle entry.

    Time:  O(n)
    Space: O(1)
    """
    slow = head
    fast = head

    # Phase 1: detect meeting point
    while fast is not None and fast.next is not None:
        slow = slow.next  # type: ignore[assignment]
        fast = fast.next.next
        if slow == fast:
            # Phase 2: find cycle entry
            slow2 = head
            while slow2 != slow:
                slow2 = slow2.next  # type: ignore[assignment]
                slow = slow.next  # type: ignore[assignment]
            return slow

    return None


# ---------- Helpers ----------
def create_cycle_list(
    values: list[int], pos: int
) -> Optional[ListNode]:
    """Create a linked list with a cycle at the given position (-1 = no cycle)."""
    if not values:
        return None
    dummy = ListNode(0)
    cur = dummy
    nodes: list[ListNode] = []
    for v in values:
        node = ListNode(v)
        nodes.append(node)
        cur.next = node
        cur = cur.next
    if pos >= 0:
        nodes[-1].next = nodes[pos]
    return dummy.next


# ---------- Tests ----------
if __name__ == "__main__":
    for fn_name, fn in [("hash-set", detect_cycle_hash), ("floyd", detect_cycle)]:
        # Test 1: cycle at pos 1
        head = create_cycle_list([3, 2, 0, -4], 1)
        res = fn(head)
        print(f"{fn_name} Test 1:", "✓" if res and res.val == 2 else "✗")

        # Test 2: no cycle
        head = create_cycle_list([1, 2, 3], -1)
        res = fn(head)
        print(f"{fn_name} Test 2:", "✓" if res is None else "✗")

        # Test 3: cycle at head (pos 0)
        head = create_cycle_list([1, 2], 0)
        res = fn(head)
        print(f"{fn_name} Test 3:", "✓" if res and res.val == 1 else "✗")

        # Test 4: empty
        print(f"{fn_name} Test 4:", "✓" if fn(None) is None else "✗")
