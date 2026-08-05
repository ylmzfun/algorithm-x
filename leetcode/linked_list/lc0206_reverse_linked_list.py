"""
LeetCode 206: Reverse Linked List
https://leetcode.com/problems/reverse-linked-list/

Given the head of a singly linked list, reverse the list, and return the
reversed list.

Example:
  Input:  head = [1,2,3,4,5]
  Output: [5,4,3,2,1]

Approaches:
1. Iterative — O(n) time, O(1) space
2. Recursive — O(n) time, O(n) space (call stack)
"""

from __future__ import annotations
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional[ListNode] = None) -> None:
        self.val = val
        self.next = next


def reverse_list_iterative(
    head: Optional[ListNode],
) -> Optional[ListNode]:
    """Iterative approach with three pointers.

    Time:  O(n)
    Space: O(1)
    """
    prev: Optional[ListNode] = None
    cur = head

    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt

    return prev


def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """Recursive approach.

    Time:  O(n)
    Space: O(n) recursion stack
    """
    if head is None or head.next is None:
        return head

    new_head = reverse_list(head.next)
    head.next.next = head
    head.next = None
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
    for fn_name, fn in [("iterative", reverse_list_iterative),
                         ("recursive", reverse_list)]:
        # Test 1: standard
        head = build_list([1, 2, 3, 4, 5])
        res = fn(head)
        print(f"{fn_name} Test 1:", "✓" if to_list(res) == [5, 4, 3, 2, 1] else "✗")

        # Test 2: two nodes
        head = build_list([1, 2])
        res = fn(head)
        print(f"{fn_name} Test 2:", "✓" if to_list(res) == [2, 1] else "✗")

        # Test 3: single node
        head = build_list([1])
        res = fn(head)
        print(f"{fn_name} Test 3:", "✓" if to_list(res) == [1] else "✗")

        # Test 4: empty
        print(f"{fn_name} Test 4:", "✓" if fn(None) is None else "✗")
