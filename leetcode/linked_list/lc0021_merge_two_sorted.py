"""
LeetCode 21: Merge Two Sorted Lists
https://leetcode.com/problems/merge-two-sorted-lists/

Merge two sorted linked lists and return it as a sorted list. The list should
be made by splicing together the nodes of the first two lists.

Example:
  Input:  l1 = [1,2,4], l2 = [1,3,4]
  Output: [1,1,2,3,4,4]

Approaches:
1. Iterative with dummy head — O(m+n) time, O(1) space
2. Recursive — O(m+n) time, O(m+n) space (call stack)
"""

from __future__ import annotations
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional[ListNode] = None) -> None:
        self.val = val
        self.next = next


def merge_two_lists_iterative(
    l1: Optional[ListNode], l2: Optional[ListNode]
) -> Optional[ListNode]:
    """Iterative merge using a dummy head node.

    Time:  O(m + n)
    Space: O(1)
    """
    dummy = ListNode(0)
    tail = dummy

    while l1 is not None and l2 is not None:
        if l1.val <= l2.val:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next

    tail.next = l1 if l1 is not None else l2
    return dummy.next


def merge_two_lists(
    l1: Optional[ListNode], l2: Optional[ListNode]
) -> Optional[ListNode]:
    """Recursive merge.

    Time:  O(m + n)
    Space: O(m + n) due to recursion stack
    """
    if l1 is None:
        return l2
    if l2 is None:
        return l1

    if l1.val <= l2.val:
        l1.next = merge_two_lists(l1.next, l2)
        return l1
    else:
        l2.next = merge_two_lists(l1, l2.next)
        return l2


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
    for fn_name, fn in [("iterative", merge_two_lists_iterative),
                         ("recursive", merge_two_lists)]:
        # Test 1: interleaving
        l1 = build_list([1, 2, 4])
        l2 = build_list([1, 3, 4])
        res = fn(l1, l2)
        print(f"{fn_name} Test 1:", "✓" if to_list(res) == [1, 1, 2, 3, 4, 4] else "✗")

        # Test 2: one empty
        l1 = build_list([])
        l2 = build_list([0])
        res = fn(l1, l2)
        print(f"{fn_name} Test 2:", "✓" if to_list(res) == [0] else "✗")

        # Test 3: disjoint ranges
        l1 = build_list([1, 2])
        l2 = build_list([5, 6])
        res = fn(l1, l2)
        print(f"{fn_name} Test 3:", "✓" if to_list(res) == [1, 2, 5, 6] else "✗")

        # Test 4: both empty
        res = fn(None, None)
        print(f"{fn_name} Test 4:", "✓" if res is None else "✗")
