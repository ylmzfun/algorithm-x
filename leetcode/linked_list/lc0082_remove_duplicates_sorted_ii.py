"""
LeetCode 82: Remove Duplicates from Sorted List II
https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/

Given the head of a sorted linked list, delete all nodes that have duplicate
numbers, leaving only distinct numbers from the original list. Return the
linked list sorted as well.

Example:
  Input:  head = [1,2,3,3,4,4,5]
  Output: [1,2,5]

Approaches:
1. Sentinel (dummy) + skip all duplicates — O(n) time, O(1) space
"""

from __future__ import annotations
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional[ListNode] = None) -> None:
        self.val = val
        self.next = next


def delete_duplicates(
    head: Optional[ListNode],
) -> Optional[ListNode]:
    """Use a sentinel node and skip all nodes with duplicate values.

    Time:  O(n)
    Space: O(1)
    """
    dummy = ListNode(0, head)
    prev = dummy

    while head is not None:
        # If current node has a duplicate
        if head.next is not None and head.val == head.next.val:
            # Skip all nodes with this value
            dup_val = head.val
            while head is not None and head.val == dup_val:
                head = head.next
            prev.next = head  # type: ignore[assignment]
        else:
            prev = prev.next  # type: ignore[assignment]
            head = head.next

    return dummy.next


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
    # Test 1: standard
    head = build_list([1, 2, 3, 3, 4, 4, 5])
    res = delete_duplicates(head)
    print("Test 1:", "✓" if to_list(res) == [1, 2, 5] else "✗")

    # Test 2: all duplicates
    head = build_list([1, 1, 1, 2, 2])
    res = delete_duplicates(head)
    print("Test 2:", "✓" if to_list(res) == [] else "✗")

    # Test 3: no duplicates
    head = build_list([1, 2, 3])
    res = delete_duplicates(head)
    print("Test 3:", "✓" if to_list(res) == [1, 2, 3] else "✗")

    # Test 4: head is duplicate
    head = build_list([1, 1, 2, 3])
    res = delete_duplicates(head)
    print("Test 4:", "✓" if to_list(res) == [2, 3] else "✗")
