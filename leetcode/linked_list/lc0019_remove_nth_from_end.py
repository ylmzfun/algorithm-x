"""
LeetCode 19: Remove Nth Node From End of List
https://leetcode.com/problems/remove-nth-node-from-end-of-list/

Given the head of a linked list, remove the n-th node from the end of the list
and return its head.

Example:
  Input:  head = [1,2,3,4,5], n = 2
  Output: [1,2,3,5]

Approaches:
1. Two-pass (count length then remove) — O(n) time, O(1) space
2. One-pass (two-pointer / fast-slow with dummy) — O(n) time, O(1) space
"""

from __future__ import annotations
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional[ListNode] = None) -> None:
        self.val = val
        self.next = next


def remove_nth_from_end_two_pass(
    head: Optional[ListNode], n: int
) -> Optional[ListNode]:
    """Count length first, then remove the (L - n)-th node from start."""
    dummy = ListNode(0, head)
    length = 0
    cur = head
    while cur:
        length += 1
        cur = cur.next

    cur = dummy
    for _ in range(length - n):
        assert cur is not None
        cur = cur.next
    assert cur is not None and cur.next is not None
    cur.next = cur.next.next
    return dummy.next


def remove_nth_from_end(
    head: Optional[ListNode], n: int
) -> Optional[ListNode]:
    """One-pass two-pointer approach (preferred).

    Use a dummy node and advance fast pointer n+1 steps ahead so that when
    fast reaches the end, slow is just before the target node.

    Time:  O(n)
    Space: O(1)
    """
    dummy = ListNode(0, head)
    slow: Optional[ListNode] = dummy
    fast: Optional[ListNode] = dummy

    # Advance fast by n+1 steps
    for _ in range(n + 1):
        if fast is None:
            break
        fast = fast.next

    while fast is not None:
        assert slow is not None
        slow = slow.next
        fast = fast.next

    assert slow is not None and slow.next is not None
    slow.next = slow.next.next
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
    for fn_name, fn in [("two-pass", remove_nth_from_end_two_pass),
                         ("one-pass", remove_nth_from_end)]:
        # Test 1
        head = build_list([1, 2, 3, 4, 5])
        res = fn(head, 2)
        print(f"{fn_name} Test 1:", "✓" if to_list(res) == [1, 2, 3, 5] else "✗")

        # Test 2: remove head
        head = build_list([1, 2])
        res = fn(head, 2)
        print(f"{fn_name} Test 2:", "✓" if to_list(res) == [2] else "✗")

        # Test 3: single node
        head = build_list([1])
        res = fn(head, 1)
        print(f"{fn_name} Test 3:", "✓" if to_list(res) == [] else "✗")

        # Test 4: remove last
        head = build_list([1, 2, 3])
        res = fn(head, 1)
        print(f"{fn_name} Test 4:", "✓" if to_list(res) == [1, 2] else "✗")
