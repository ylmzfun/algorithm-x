"""
LeetCode 23: Merge k Sorted Lists
https://leetcode.com/problems/merge-k-sorted-lists/

You are given an array of k linked-lists, each linked-list is sorted in
ascending order. Merge all the linked-lists into one sorted linked-list
and return it.

Example:
  Input:  lists = [[1,4,5],[1,3,4],[2,6]]
  Output: [1,1,2,3,4,4,5,6]

Approaches:
1. Min-heap (priority queue) — O(N log k) time, O(k) space
2. Divide and conquer (pairwise merge) — O(N log k) time, O(log k) space
"""

from __future__ import annotations
from typing import Optional
import heapq


class ListNode:
    def __init__(self, val: int = 0, next: Optional[ListNode] = None) -> None:
        self.val = val
        self.next = next

    # Make ListNode comparable for heap (needs __lt__)
    def __lt__(self, other: ListNode) -> bool:
        return self.val < other.val


def merge_k_lists_heap(
    lists: list[Optional[ListNode]],
) -> Optional[ListNode]:
    """Min-heap approach.

    Push the head of every list into a min-heap. Repeatedly pop the smallest
    node, append it to result, and push its next node back.

    Time:  O(N log k) where N = total nodes, k = number of lists
    Space: O(k) for the heap
    """
    heap: list[ListNode] = []
    # Push all non-empty list heads; use index as tiebreaker
    for i, head in enumerate(lists):
        if head is not None:
            heapq.heappush(heap, (head.val, i, head))

    dummy = ListNode(0)
    tail = dummy

    while heap:
        _val, i, node = heapq.heappop(heap)
        tail.next = node
        tail = tail.next
        if node.next is not None:
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next


def _merge_two(
    l1: Optional[ListNode], l2: Optional[ListNode]
) -> Optional[ListNode]:
    """Merge two sorted linked lists (helper for divide-conquer)."""
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


def merge_k_lists(
    lists: list[Optional[ListNode]],
) -> Optional[ListNode]:
    """Divide and conquer: pairwise merge like merge-sort.

    Time:  O(N log k)
    Space: O(log k) for recursion stack
    """
    if not lists:
        return None

    interval = 1
    n = len(lists)
    while interval < n:
        for i in range(0, n - interval, interval * 2):
            lists[i] = _merge_two(lists[i], lists[i + interval])
        interval *= 2
    return lists[0]


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
    for fn_name, fn in [("heap", merge_k_lists_heap),
                         ("divide-conquer", merge_k_lists)]:
        # Test 1: standard
        lists = [build_list([1, 4, 5]), build_list([1, 3, 4]),
                 build_list([2, 6])]
        res = fn(lists)
        print(f"{fn_name} Test 1:", "✓" if to_list(res) == [1, 1, 2, 3, 4, 4, 5, 6] else "✗")

        # Test 2: empty lists
        res = fn([])
        print(f"{fn_name} Test 2:", "✓" if res is None else "✗")

        # Test 3: all empty
        res = fn([None, None])
        print(f"{fn_name} Test 3:", "✓" if res is None else "✗")

        # Test 4: single list
        lists = [build_list([1, 2, 3])]
        res = fn(lists)
        print(f"{fn_name} Test 4:", "✓" if to_list(res) == [1, 2, 3] else "✗")
