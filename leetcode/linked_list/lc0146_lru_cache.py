"""
LeetCode 146: LRU Cache
https://leetcode.com/problems/lru-cache/

Design a data structure that follows the constraints of a Least Recently Used
(LRU) cache.

Implement the LRUCache class:
- LRUCache(capacity) — Initialize the LRU cache with positive size capacity.
- get(key) — Return the value of the key if the key exists, otherwise return -1.
- put(key, value) — Update the value of the key if the key exists. Otherwise,
  add the key-value pair to the cache. If the number of keys exceeds the
  capacity, evict the least recently used key.

The functions get and put must each run in O(1) average time complexity.

Approaches:
1. Hashmap + Doubly Linked List — O(1) for both operations
"""

from __future__ import annotations
from typing import Optional


class _DLLNode:
    """Doubly-linked list node for the LRU cache."""
    __slots__ = ("key", "val", "prev", "next")

    def __init__(
        self,
        key: int = 0,
        val: int = 0,
        prev: Optional[_DLLNode] = None,
        next: Optional[_DLLNode] = None,
    ) -> None:
        self.key = key
        self.val = val
        self.prev = prev
        self.next = next


class LRUCache:
    """LRU Cache with O(1) get and put.

    Uses a hashmap for O(1) lookup and a doubly-linked list to maintain
    access order. Head = most recently used, Tail = least recently used.

    Time:  O(1) for get and put
    Space: O(capacity)
    """

    def __init__(self, capacity: int) -> None:
        self._capacity = capacity
        self._cache: dict[int, _DLLNode] = {}
        # Dummy head and tail nodes
        self._head = _DLLNode()
        self._tail = _DLLNode()
        self._head.next = self._tail
        self._tail.prev = self._head

    def _add_to_head(self, node: _DLLNode) -> None:
        """Add node right after dummy head."""
        node.prev = self._head
        node.next = self._head.next
        assert self._head.next is not None
        self._head.next.prev = node
        self._head.next = node

    def _remove_node(self, node: _DLLNode) -> None:
        """Remove an existing node from the list."""
        assert node.prev is not None and node.next is not None
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_head(self, node: _DLLNode) -> None:
        """Move an existing node to right after head."""
        self._remove_node(node)
        self._add_to_head(node)

    def _pop_tail(self) -> _DLLNode:
        """Remove and return the tail node (before dummy tail)."""
        node = self._tail.prev
        assert node is not None and node is not self._head
        self._remove_node(node)
        return node

    def get(self, key: int) -> int:
        """Return value for key, or -1 if not present."""
        if key not in self._cache:
            return -1
        node = self._cache[key]
        self._move_to_head(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        """Insert or update key-value pair."""
        if key in self._cache:
            node = self._cache[key]
            node.val = value
            self._move_to_head(node)
        else:
            if len(self._cache) >= self._capacity:
                tail = self._pop_tail()
                del self._cache[tail.key]
            node = _DLLNode(key, value)
            self._cache[key] = node
            self._add_to_head(node)


# ---------- Tests ----------
if __name__ == "__main__":
    # Test 1: basic operations
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    v1 = cache.get(1)
    print("Test 1 get(1):", "✓" if v1 == 1 else "✗")
    cache.put(3, 3)  # evicts key 2
    v2 = cache.get(2)
    print("Test 1 get(2) evicted:", "✓" if v2 == -1 else "✗")
    cache.put(4, 4)  # evicts key 1
    v3 = cache.get(1)
    print("Test 1 get(1) evicted:", "✓" if v3 == -1 else "✗")
    v4 = cache.get(3)
    print("Test 1 get(3):", "✓" if v4 == 3 else "✗")
    v5 = cache.get(4)
    print("Test 1 get(4):", "✓" if v5 == 4 else "✗")

    # Test 2: update existing
    cache = LRUCache(2)
    cache.put(1, 10)
    cache.put(1, 100)
    v = cache.get(1)
    print("Test 2:", "✓" if v == 100 else "✗")

    # Test 3: single capacity
    cache = LRUCache(1)
    cache.put(2, 1)
    v = cache.get(2)
    print("Test 3 get(2):", "✓" if v == 1 else "✗")
    cache.put(3, 2)
    v = cache.get(2)
    print("Test 3 get(2) evicted:", "✓" if v == -1 else "✗")
    v = cache.get(3)
    print("Test 3 get(3):", "✓" if v == 2 else "✗")
