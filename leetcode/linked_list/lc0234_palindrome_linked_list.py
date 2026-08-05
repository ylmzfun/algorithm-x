"""
LeetCode 234: Palindrome Linked List
https://leetcode.com/problems/palindrome-linked-list/

Given the head of a singly linked list, return True if it is a palindrome
or False otherwise.

Example:
  Input:  head = [1,2,2,1]
  Output: True

Approaches:
1. Copy to array + two-pointer — O(n) time, O(n) space
2. Reverse second half in-place — O(n) time, O(1) space
"""

from __future__ import annotations
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional[ListNode] = None) -> None:
        self.val = val
        self.next = next


def is_palindrome_array(head: Optional[ListNode]) -> bool:
    """Convert to list and use two pointers.

    Time:  O(n)
    Space: O(n)
    """
    vals: list[int] = []
    cur = head
    while cur:
        vals.append(cur.val)
        cur = cur.next

    left, right = 0, len(vals) - 1
    while left < right:
        if vals[left] != vals[right]:
            return False
        left += 1
        right -= 1
    return True


def _find_middle(head: ListNode) -> ListNode:
    """Find the middle (first middle for even length)."""
    slow: Optional[ListNode] = head
    fast: Optional[ListNode] = head
    while fast.next is not None and fast.next.next is not None:
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


def is_palindrome(head: Optional[ListNode]) -> bool:
    """Reverse second half in-place and compare.

    Time:  O(n)
    Space: O(1)
    """
    if head is None or head.next is None:
        return True

    mid = _find_middle(head)
    second = _reverse(mid.next)

    # Compare
    p1: Optional[ListNode] = head
    p2 = second
    result = True
    while p2:
        assert p1 is not None
        if p1.val != p2.val:
            result = False
            break
        p1 = p1.next
        p2 = p2.next

    # Restore (optional, for good practice)
    mid.next = _reverse(second)
    return result


# ---------- Helpers ----------
def build_list(values: list[int]) -> Optional[ListNode]:
    dummy = ListNode(0)
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


# ---------- Tests ----------
if __name__ == "__main__":
    for fn_name, fn in [("array", is_palindrome_array),
                         ("in-place", is_palindrome)]:
        # Test 1: palindrome even
        head = build_list([1, 2, 2, 1])
        print(f"{fn_name} Test 1:", "✓" if fn(head) else "✗")

        # Test 2: palindrome odd
        head = build_list([1, 2, 3, 2, 1])
        print(f"{fn_name} Test 2:", "✓" if fn(head) else "✗")

        # Test 3: not palindrome
        head = build_list([1, 2, 3])
        print(f"{fn_name} Test 3:", "✓" if not fn(head) else "✗")

        # Test 4: single node
        head = build_list([1])
        print(f"{fn_name} Test 4:", "✓" if fn(head) else "✗")
