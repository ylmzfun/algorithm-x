"""
LeetCode 2: Add Two Numbers
https://leetcode.com/problems/add-two-numbers/

You are given two non-empty linked lists representing two non-negative integers.
The digits are stored in reverse order, and each of their nodes contains a single
digit. Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0
itself.

Example:
  Input:  l1 = [2,4,3], l2 = [5,6,4]
  Output: [7,0,8]
  Explanation: 342 + 465 = 807.

Approaches:
1. Iterative with carry — O(max(m,n)) time, O(max(m,n)) space
"""

from __future__ import annotations
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional[ListNode] = None) -> None:
        self.val = val
        self.next = next


def add_two_numbers(
    l1: Optional[ListNode], l2: Optional[ListNode]
) -> Optional[ListNode]:
    """Iterative approach with carry tracking.

    Time:  O(max(m, n))
    Space: O(max(m, n)) for result list
    """
    dummy = ListNode(0)
    curr = dummy
    carry = 0

    p1, p2 = l1, l2
    while p1 is not None or p2 is not None or carry != 0:
        val1 = p1.val if p1 else 0
        val2 = p2.val if p2 else 0
        total = val1 + val2 + carry
        carry = total // 10
        digit = total % 10

        curr.next = ListNode(digit)
        curr = curr.next

        if p1:
            p1 = p1.next
        if p2:
            p2 = p2.next

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
    # Test 1: basic
    l1 = build_list([2, 4, 3])
    l2 = build_list([5, 6, 4])
    res = add_two_numbers(l1, l2)
    print("Test 1:", "✓" if to_list(res) == [7, 0, 8] else "✗")

    # Test 2: different lengths
    l1 = build_list([9, 9, 9, 9])
    l2 = build_list([9, 9, 9, 9, 9, 9, 9])
    res = add_two_numbers(l1, l2)
    expected = [8, 9, 9, 9, 0, 0, 0, 1]
    print("Test 2:", "✓" if to_list(res) == expected else "✗")

    # Test 3: zeros
    l1 = build_list([0])
    l2 = build_list([0])
    res = add_two_numbers(l1, l2)
    print("Test 3:", "✓" if to_list(res) == [0] else "✗")

    # Test 4: single carry at end
    l1 = build_list([5])
    l2 = build_list([5])
    res = add_two_numbers(l1, l2)
    print("Test 4:", "✓" if to_list(res) == [0, 1] else "✗")
