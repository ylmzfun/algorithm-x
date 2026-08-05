"""
LeetCode 143: Reorder List
https://leetcode.com/problems/reorder-list/

You are given the head of a singly linked-list. The list can be represented as:
  L0 → L1 → … → Ln-1 → Ln
Reorder the list to be on the following form:
  L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …

You must do this in-place without altering the nodes' values.

Example:
  Input:  head = [1,2,3,4]
  Output: [1,4,2,3]

Approaches:
1. Find middle + reverse second half + merge — O(n) time, O(1) space
"""

from __future__ import annotations
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional[ListNode] = None) -> None:
        self.val = val
        self.next = next


def _find_middle(head: ListNode) -> ListNode:
    """Find the middle node (first middle for even length) using slow/fast."""
    slow: Optional[ListNode] = head
    fast: Optional[ListNode] = head
    while fast is not None and fast.next is not None and fast.next.next is not None:
        slow = slow.next  # type: ignore[assignment]
        fast = fast.next.next
    assert slow is not None
    return slow


def _reverse(head: Optional[ListNode]) -> Optional[ListNode]:
    """Reverse a linked list."""
    prev: Optional[ListNode] = None
    cur = head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev


def reorder_list(head: Optional[ListNode]) -> None:
    """Reorder in-place: find middle, reverse second half, merge.

    Time:  O(n)
    Space: O(1)
    """
    if head is None or head.next is None:
        return

    mid = _find_middle(head)
    second = mid.next
    mid.next = None  # Split

    second = _reverse(second)

    # Merge: interleave first and second
    first: Optional[ListNode] = head
    while second:
        tmp1 = first.next  # type: ignore[union-attr]
        tmp2 = second.next

        first.next = second  # type: ignore[union-attr]
        second.next = tmp1

        first = tmp1
        second = tmp2


# ---------- Helpers ----------
def build_list(values: list[int]) -> Optional[ListNode]:
    dummy = ListNode(0)
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_list(head: Optional[ListNode]) -> list[int]:
    result: list[int] = []
    while head:
        result.append(head.val)
        head = head.next
    return result


# ---------- Tests ----------
if __name__ == "__main__":
    # Test 1: even length
    head = build_list([1, 2, 3, 4])
    reorder_list(head)
    print("Test 1:", "✓" if to_list(head) == [1, 4, 2, 3] else "✗")

    # Test 2: odd length
    head = build_list([1, 2, 3, 4, 5])
    reorder_list(head)
    print("Test 2:", "✓" if to_list(head) == [1, 5, 2, 4, 3] else "✗")

    # Test 3: two nodes
    head = build_list([1, 2])
    reorder_list(head)
    print("Test 3:", "✓" if to_list(head) == [1, 2] else "✗")

    # Test 4: single node
    head = build_list([1])
    reorder_list(head)
    print("Test 4:", "✓" if to_list(head) == [1] else "✗")
