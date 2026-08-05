"""
LeetCode 25: Reverse Nodes in k-Group
https://leetcode.com/problems/reverse-nodes-in-k-group/

Given the head of a linked list, reverse the nodes of the list k at a time,
and return the modified list. k is a positive integer and is less than or
equal to the length of the linked list. If the number of nodes is not a
multiple of k then left-out nodes, in the end, should remain as is.

Example:
  Input:  head = [1,2,3,4,5], k = 2
  Output: [2,1,4,3,5]

Approaches:
1. Iterative with group reversal — O(n) time, O(1) space
"""

from __future__ import annotations
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional[ListNode] = None) -> None:
        self.val = val
        self.next = next


def _reverse_list(head: ListNode, k: int) -> ListNode:
    """Reverse exactly k nodes, return new head and reconnect tail."""
    prev: Optional[ListNode] = None
    curr: Optional[ListNode] = head
    for _ in range(k):
        assert curr is not None
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    # head is now the tail of the reversed segment; connect to remaining
    head.next = curr
    assert prev is not None
    return prev


def reverse_k_group(
    head: Optional[ListNode], k: int
) -> Optional[ListNode]:
    """Reverse nodes in groups of k.

    Time:  O(n) — each node visited twice (once for counting, once for reversing)
    Space: O(1)
    """
    if head is None or k == 1:
        return head

    # Count total nodes
    count = 0
    cur: Optional[ListNode] = head
    while cur:
        count += 1
        cur = cur.next

    dummy = ListNode(0, head)
    prev_group_end = dummy

    while count >= k:
        start = prev_group_end.next
        assert start is not None
        new_head = _reverse_list(start, k)
        prev_group_end.next = new_head
        prev_group_end = start  # start is now tail of reversed segment
        count -= k

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
    # Test 1: k=2, even groups
    head = build_list([1, 2, 3, 4, 5])
    res = reverse_k_group(head, 2)
    print("Test 1:", "✓" if to_list(res) == [2, 1, 4, 3, 5] else "✗")

    # Test 2: k=3, exact multiple
    head = build_list([1, 2, 3, 4, 5, 6])
    res = reverse_k_group(head, 3)
    print("Test 2:", "✓" if to_list(res) == [3, 2, 1, 6, 5, 4] else "✗")

    # Test 3: k=1 (no change)
    head = build_list([1, 2, 3])
    res = reverse_k_group(head, 1)
    print("Test 3:", "✓" if to_list(res) == [1, 2, 3] else "✗")

    # Test 4: k larger than list
    head = build_list([1, 2])
    res = reverse_k_group(head, 5)
    print("Test 4:", "✓" if to_list(res) == [1, 2] else "✗")
