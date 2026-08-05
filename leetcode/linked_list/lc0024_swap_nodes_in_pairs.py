"""
LeetCode 24: Swap Nodes in Pairs
https://leetcode.com/problems/swap-nodes-in-pairs/

Given a linked list, swap every two adjacent nodes and return its head.
You must solve the problem without modifying the values in the list's nodes
(i.e., only nodes themselves may be changed.)

Example:
  Input:  head = [1,2,3,4]
  Output: [2,1,4,3]

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


def swap_pairs_iterative(
    head: Optional[ListNode],
) -> Optional[ListNode]:
    """Iterative approach with a dummy node.

    Time:  O(n)
    Space: O(1)
    """
    dummy = ListNode(0, head)
    prev = dummy

    while prev.next is not None and prev.next.next is not None:
        first = prev.next
        second = first.next

        # Swap
        first.next = second.next
        second.next = first
        prev.next = second

        prev = first

    return dummy.next


def swap_pairs(
    head: Optional[ListNode],
) -> Optional[ListNode]:
    """Recursive approach.

    Time:  O(n)
    Space: O(n)
    """
    if head is None or head.next is None:
        return head

    second = head.next
    head.next = swap_pairs(second.next)
    second.next = head
    return second


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
    for fn_name, fn in [("iterative", swap_pairs_iterative),
                         ("recursive", swap_pairs)]:
        # Test 1: even length
        head = build_list([1, 2, 3, 4])
        res = fn(head)
        print(f"{fn_name} Test 1:", "✓" if to_list(res) == [2, 1, 4, 3] else "✗")

        # Test 2: odd length
        head = build_list([1, 2, 3])
        res = fn(head)
        print(f"{fn_name} Test 2:", "✓" if to_list(res) == [2, 1, 3] else "✗")

        # Test 3: single node
        head = build_list([1])
        res = fn(head)
        print(f"{fn_name} Test 3:", "✓" if to_list(res) == [1] else "✗")

        # Test 4: empty
        res = fn(None)
        print(f"{fn_name} Test 4:", "✓" if res is None else "✗")
