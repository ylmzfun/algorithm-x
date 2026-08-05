"""
LeetCode 61: Rotate List
https://leetcode.com/problems/rotate-list/

Given the head of a linked list, rotate the list to the right by k places.

Example:
  Input:  head = [1,2,3,4,5], k = 2
  Output: [4,5,1,2,3]

Approaches:
1. Close into a ring, then break — O(n) time, O(1) space
"""

from __future__ import annotations
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional[ListNode] = None) -> None:
        self.val = val
        self.next = next


def rotate_right(
    head: Optional[ListNode], k: int
) -> Optional[ListNode]:
    """Close list into a ring, find new tail, then break.

    Time:  O(n)
    Space: O(1)
    """
    if head is None or head.next is None or k == 0:
        return head

    # Count length and find tail
    length = 1
    tail = head
    while tail.next:
        tail = tail.next
        length += 1

    # Effective rotations needed
    k %= length
    if k == 0:
        return head

    # Close into ring
    tail.next = head

    # Find new tail: (length - k - 1) steps from head
    new_tail = head
    for _ in range(length - k - 1):
        new_tail = new_tail.next  # type: ignore[assignment]

    new_head = new_tail.next
    new_tail.next = None
    return new_head


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
    head = build_list([1, 2, 3, 4, 5])
    res = rotate_right(head, 2)
    print("Test 1:", "✓" if to_list(res) == [4, 5, 1, 2, 3] else "✗")

    # Test 2: k = length (no change)
    head = build_list([1, 2, 3])
    res = rotate_right(head, 3)
    print("Test 2:", "✓" if to_list(res) == [1, 2, 3] else "✗")

    # Test 3: k > length
    head = build_list([0, 1, 2])
    res = rotate_right(head, 4)
    print("Test 3:", "✓" if to_list(res) == [2, 0, 1] else "✗")

    # Test 4: single node
    head = build_list([1])
    res = rotate_right(head, 99)
    print("Test 4:", "✓" if to_list(res) == [1] else "✗")
