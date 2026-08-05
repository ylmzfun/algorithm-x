"""
LeetCode 83: Remove Duplicates from Sorted List
https://leetcode.com/problems/remove-duplicates-from-sorted-list/

Given the head of a sorted linked list, delete all duplicates such that each
element appears only once. Return the linked list sorted as well.

Example:
  Input:  head = [1,1,2,3,3]
  Output: [1,2,3]

Approaches:
1. Single pass — O(n) time, O(1) space
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
    """Single pass: skip next nodes with same value.

    Time:  O(n)
    Space: O(1)
    """
    cur = head
    while cur is not None and cur.next is not None:
        if cur.val == cur.next.val:
            cur.next = cur.next.next
        else:
            cur = cur.next
    return head


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
    head = build_list([1, 1, 2, 3, 3])
    res = delete_duplicates(head)
    print("Test 1:", "✓" if to_list(res) == [1, 2, 3] else "✗")

    # Test 2: all same
    head = build_list([1, 1, 1])
    res = delete_duplicates(head)
    print("Test 2:", "✓" if to_list(res) == [1] else "✗")

    # Test 3: no duplicates
    head = build_list([1, 2, 3])
    res = delete_duplicates(head)
    print("Test 3:", "✓" if to_list(res) == [1, 2, 3] else "✗")

    # Test 4: empty
    res = delete_duplicates(None)
    print("Test 4:", "✓" if res is None else "✗")
