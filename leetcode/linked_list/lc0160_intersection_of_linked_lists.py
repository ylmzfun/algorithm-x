"""
LeetCode 160: Intersection of Two Linked Lists
https://leetcode.com/problems/intersection-of-two-linked-lists/

Given the heads of two singly linked-lists headA and headB, return the node
at which the two lists intersect. If the two linked lists have no intersection
at all, return None.

Example:
  Input:  intersectVal = 8, listA = [4,1,8,4,5], listB = [5,6,1,8,4,5],
          skipA = 2, skipB = 3
  Output: Intersected at '8'

Approaches:
1. Hash set — O(m+n) time, O(m) space
2. Two-pointer (浪漫相遇 / romantic meeting) — O(m+n) time, O(1) space
"""

from __future__ import annotations
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional[ListNode] = None) -> None:
        self.val = val
        self.next = next


def get_intersection_node_hash(
    headA: Optional[ListNode], headB: Optional[ListNode]
) -> Optional[ListNode]:
    """Hash-set approach.

    Time:  O(m + n)
    Space: O(m)
    """
    visited: set[int] = set()
    cur = headA
    while cur:
        visited.add(id(cur))
        cur = cur.next

    cur = headB
    while cur:
        if id(cur) in visited:
            return cur
        cur = cur.next

    return None


def get_intersection_node(
    headA: Optional[ListNode], headB: Optional[ListNode]
) -> Optional[ListNode]:
    """Two-pointer approach.

    Each pointer traverses both lists. If they intersect, they will meet.
    If they don't, both become None simultaneously.

    Time:  O(m + n)
    Space: O(1)
    """
    pa = headA
    pb = headB

    while pa != pb:
        pa = pa.next if pa else headB  # type: ignore[assignment]
        pb = pb.next if pb else headA  # type: ignore[assignment]

    return pa


# ---------- Helpers ----------
def build_intersecting_lists(
    listA: list[int],
    listB: list[int],
    intersect_vals: list[int],
    skipA: int,
    skipB: int,
) -> tuple[Optional[ListNode], Optional[ListNode]]:
    """Build two intersecting linked lists."""
    # Build common part
    common: Optional[ListNode] = None
    for v in reversed(intersect_vals):
        common = ListNode(v, common)

    # Build list A
    headA: Optional[ListNode] = common if skipA >= len(listA) else None
    for i in range(len(listA) - 1, -1, -1):
        headA = ListNode(listA[i], headA)
        if i == skipA:
            # Connect to common
            cur = headA
            while cur and cur.next:
                cur = cur.next
            if cur:
                cur.next = common

    # Build list B
    headB: Optional[ListNode] = common if skipB >= len(listB) else None
    for i in range(len(listB) - 1, -1, -1):
        headB = ListNode(listB[i], headB)
        if i == skipB:
            cur = headB
            while cur and cur.next:
                cur = cur.next
            if cur:
                cur.next = common

    return headA, headB


# ---------- Tests ----------
if __name__ == "__main__":
    for fn_name, fn in [("hash-set", get_intersection_node_hash),
                         ("two-pointer", get_intersection_node)]:
        # Test 1: intersection exists
        headA, headB = build_intersecting_lists(
            [4, 1], [5, 6, 1], [8, 4, 5], skipA=2, skipB=3
        )
        res = fn(headA, headB)
        print(f"{fn_name} Test 1:", "✓" if res and res.val == 8 else "✗")

        # Test 2: no intersection
        headA = build_intersecting_lists([2, 6, 4], [1, 5], [], skipA=3, skipB=2)[0]
        headB = build_intersecting_lists([2, 6, 4], [1, 5], [], skipA=3, skipB=2)[1]
        res = fn(headA, headB)
        print(f"{fn_name} Test 2:", "✓" if res is None else "✗")

        # Test 3: intersect at head
        headA, headB = build_intersecting_lists(
            [1], [], [2, 3], skipA=1, skipB=0
        )
        res = fn(headA, headB)
        print(f"{fn_name} Test 3:", "✓" if res and res.val == 2 else "✗")
