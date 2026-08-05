"""
LeetCode 141: Linked List Cycle
https://leetcode.com/problems/linked-list-cycle/

Given head, the head of a linked list, determine if the linked list has a
cycle in it. Return True if there is a cycle, otherwise return False.

Approaches:
1. Hash set — O(n) time, O(n) space
2. Floyd's Tortoise and Hare — O(n) time, O(1) space
"""

from __future__ import annotations
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional[ListNode] = None) -> None:
        self.val = val
        self.next = next


def has_cycle_hash(head: Optional[ListNode]) -> bool:
    """Track visited nodes in a set.

    Time:  O(n)
    Space: O(n)
    """
    visited: set[int] = set()
    cur = head
    while cur:
        node_id = id(cur)
        if node_id in visited:
            return True
        visited.add(node_id)
        cur = cur.next
    return False


def has_cycle(head: Optional[ListNode]) -> bool:
    """Floyd's Tortoise and Hare algorithm.

    Time:  O(n)
    Space: O(1)
    """
    slow = head
    fast = head

    while fast is not None and fast.next is not None:
        slow = slow.next  # type: ignore[assignment]
        fast = fast.next.next
        if slow == fast:
            return True

    return False


# ---------- Helpers ----------
def build_list(values: list[int]) -> Optional[ListNode]:
    dummy = ListNode(0)
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


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
    for fn_name, fn in [("hash-set", has_cycle_hash), ("floyd", has_cycle)]:
        # Test 1: cycle at pos 1
        head = create_cycle_list([3, 2, 0, -4], 1)
        print(f"{fn_name} Test 1:", "✓" if fn(head) else "✗")

        # Test 2: no cycle
        head = build_list([1, 2, 3])
        print(f"{fn_name} Test 2:", "✓" if not fn(head) else "✗")

        # Test 3: single node with cycle
        head = create_cycle_list([1], 0)
        print(f"{fn_name} Test 3:", "✓" if fn(head) else "✗")

        # Test 4: empty
        print(f"{fn_name} Test 4:", "✓" if not fn(None) else "✗")
