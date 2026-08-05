"""
LeetCode 148: Sort List
https://leetcode.com/problems/sort-list/

Given the head of a linked list, return the list after sorting it in
ascending order. Follow up: Can you sort the linked list in O(n log n)
time and O(1) memory (i.e., constant space)?

Example:
  Input:  head = [4,2,1,3]
  Output: [1,2,3,4]

Approaches:
1. Merge sort (top-down recursive) — O(n log n) time, O(log n) space
2. Merge sort (bottom-up iterative) — O(n log n) time, O(1) space
"""

from __future__ import annotations
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional[ListNode] = None) -> None:
        self.val = val
        self.next = next


def _find_middle(head: ListNode) -> ListNode:
    """Find the node before the middle using slow/fast (first middle for even)."""
    slow: Optional[ListNode] = head
    fast: Optional[ListNode] = head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next  # type: ignore[assignment]
        fast = fast.next.next
    assert slow is not None
    return slow


def _merge(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    """Merge two sorted linked lists."""
    dummy = ListNode(0)
    tail = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next
    tail.next = l1 if l1 else l2
    return dummy.next


def sort_list_recursive(
    head: Optional[ListNode],
) -> Optional[ListNode]:
    """Top-down merge sort (recursive).

    Time:  O(n log n)
    Space: O(log n) recursion stack
    """
    if head is None or head.next is None:
        return head

    mid = _find_middle(head)
    right = mid.next
    mid.next = None

    left_sorted = sort_list_recursive(head)
    right_sorted = sort_list_recursive(right)
    return _merge(left_sorted, right_sorted)


def _split(head: ListNode, size: int) -> Optional[ListNode]:
    """Split `size` nodes from head; return the remaining list."""
    cur: Optional[ListNode] = head
    for _ in range(size - 1):
        if cur is None:
            break
        cur = cur.next
    if cur is None:
        return None
    rest = cur.next
    cur.next = None
    return rest


def _count(head: Optional[ListNode]) -> int:
    count = 0
    while head:
        count += 1
        head = head.next
    return count


def sort_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """Bottom-up merge sort (iterative, O(1) space).

    Time:  O(n log n)
    Space: O(1)
    """
    if head is None or head.next is None:
        return head

    n = _count(head)
    dummy = ListNode(0, head)

    step = 1
    while step < n:
        prev = dummy
        cur: Optional[ListNode] = dummy.next

        while cur is not None:
            # First half
            left = cur
            right = _split(left, step)

            # Second half
            cur = _split(right, step) if right else None

            # Merge left and right
            merged = _merge(left, right)
            prev.next = merged
            # Advance prev to the tail of merged
            while prev.next:
                prev = prev.next

        step *= 2

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
    for fn_name, fn in [("recursive", sort_list_recursive),
                         ("bottom-up", sort_list)]:
        # Test 1: standard
        head = build_list([4, 2, 1, 3])
        res = fn(head)
        print(f"{fn_name} Test 1:", "✓" if to_list(res) == [1, 2, 3, 4] else "✗")

        # Test 2: already sorted
        head = build_list([1, 2, 3, 4])
        res = fn(head)
        print(f"{fn_name} Test 2:", "✓" if to_list(res) == [1, 2, 3, 4] else "✗")

        # Test 3: single node
        head = build_list([5])
        res = fn(head)
        print(f"{fn_name} Test 3:", "✓" if to_list(res) == [5] else "✗")

        # Test 4: empty
        print(f"{fn_name} Test 4:", "✓" if fn(None) is None else "✗")
