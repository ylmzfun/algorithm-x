"""
LRU Cache Implementation
=========================

Two implementations of the Least Recently Used (LRU) cache:

1. LRUCacheOrderedDict — Uses Python's collections.OrderedDict for simplicity.
2. LRUCache — Manual implementation using hash map + doubly-linked list.

An LRU cache evicts the least recently accessed item when at capacity.

Time Complexities (both implementations):
    - get(key): O(1)
    - put(key, value): O(1)

Space Complexity: O(capacity)
"""

from typing import Any, Optional, Dict
from collections import OrderedDict


# ─── LRU Cache using OrderedDict ─────────────────────────────────────────────


class LRUCacheOrderedDict:
    """LRU Cache using Python's OrderedDict.

    OrderedDict maintains insertion order; we move accessed keys to the end
    (most recently used). The first key is always the least recently used.

    Examples:
        >>> cache = LRUCacheOrderedDict(2)
        >>> cache.put(1, 1)
        >>> cache.put(2, 2)
        >>> cache.get(1)
        1
        >>> cache.put(3, 3)  # Evicts key 2
        >>> cache.get(2)
        -1
    """

    def __init__(self, capacity: int) -> None:
        """Initialize LRU cache with given capacity.

        Args:
            capacity: Maximum number of entries. Must be >= 1.

        Raises:
            ValueError: If capacity <= 0.
        """
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity: int = capacity
        self._cache: OrderedDict[Any, Any] = OrderedDict()

    def get(self, key: Any) -> int:
        """Return the value for `key`, or -1 if not present.

        Accessing a key marks it as most recently used.

        Args:
            key: Key to look up.

        Returns:
            Associated value, or -1 if key not in cache.

        Time Complexity: O(1)
        """
        if key not in self._cache:
            return -1
        # Move to end (most recently used)
        self._cache.move_to_end(key)
        return self._cache[key]

    def put(self, key: Any, value: Any) -> None:
        """Insert or update a key-value pair.

        If key exists, updates its value and marks it MRU.
        If at capacity, evicts the LRU key before inserting.

        Args:
            key: Key to insert/update.
            value: Value to associate.

        Time Complexity: O(1)
        """
        if key in self._cache:
            self._cache.move_to_end(key)
        else:
            if len(self._cache) >= self._capacity:
                # Pop the first item (least recently used)
                self._cache.popitem(last=False)
        self._cache[key] = value

    def size(self) -> int:
        """Return number of entries.

        Returns:
            Current count of cached items.

        Time Complexity: O(1)
        """
        return len(self._cache)


# ─── Manual LRU Cache (HashMap + DoublyLinkedList) ───────────────────────────


class _DoublyNode:
    """A node in the doubly-linked list for the manual LRU cache."""

    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: Any = None, value: Any = None) -> None:
        self.key = key
        self.value = value
        self.prev: Optional["_DoublyNode"] = None
        self.next: Optional["_DoublyNode"] = None


class LRUCache:
    """Manual LRU Cache using hash map + doubly-linked list.

    The linked list maintains access order:
    - Head.next = most recently used (MRU)
    - Tail.prev = least recently used (LRU)

    Sentinels (head and tail) simplify boundary operations.

    Examples:
        >>> cache = LRUCache(2)
        >>> cache.put(1, 1)
        >>> cache.put(2, 2)
        >>> cache.get(1)
        1
        >>> cache.put(3, 3)  # Evicts key 2
        >>> cache.get(2)
        -1
        >>> cache.get(3)
        3
        >>> cache.get(1)
        1
    """

    def __init__(self, capacity: int) -> None:
        """Initialize LRU cache.

        Args:
            capacity: Maximum number of entries. Must be >= 1.

        Raises:
            ValueError: If capacity <= 0.
        """
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        self._capacity: int = capacity
        self._cache: Dict[Any, _DoublyNode] = {}

        # Sentinel nodes: head <-> ... <-> tail
        self._head = _DoublyNode()  # MRU sentinel
        self._tail = _DoublyNode()  # LRU sentinel
        self._head.next = self._tail
        self._tail.prev = self._head

    def _add_node(self, node: _DoublyNode) -> None:
        """Add node right after head (making it the new MRU).

        Args:
            node: Node to add.

        Time Complexity: O(1)
        """
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node  # type: ignore[union-attr]
        self._head.next = node

    def _remove_node(self, node: _DoublyNode) -> None:
        """Remove `node` from the linked list.

        Args:
            node: Node to remove.

        Time Complexity: O(1)
        """
        prev = node.prev
        nxt = node.next
        prev.next = nxt  # type: ignore[union-attr]
        nxt.prev = prev  # type: ignore[union-attr]

    def _move_to_front(self, node: _DoublyNode) -> None:
        """Move existing node to the MRU position (right after head).

        Args:
            node: Node to promote.

        Time Complexity: O(1)
        """
        self._remove_node(node)
        self._add_node(node)

    def _pop_tail(self) -> _DoublyNode:
        """Remove and return the LRU node (right before tail).

        Returns:
            The evicted node.

        Time Complexity: O(1)
        """
        lru = self._tail.prev
        self._remove_node(lru)  # type: ignore[arg-type]
        return lru  # type: ignore[return-value]

    def get(self, key: Any) -> int:
        """Return the value for `key`, or -1 if not present.

        Accessing a key promotes it to MRU.

        Args:
            key: Key to look up.

        Returns:
            Associated value, or -1.

        Time Complexity: O(1)
        """
        node = self._cache.get(key)
        if node is None:
            return -1
        self._move_to_front(node)
        return node.value

    def put(self, key: Any, value: Any) -> None:
        """Insert or update a key-value pair.

        If at capacity, evicts the LRU entry.

        Args:
            key: Key to insert/update.
            value: Value to associate.

        Time Complexity: O(1)
        """
        node = self._cache.get(key)

        if node is not None:
            # Update existing
            node.value = value
            self._move_to_front(node)
        else:
            if len(self._cache) >= self._capacity:
                # Evict LRU
                lru = self._pop_tail()
                del self._cache[lru.key]
            # Insert new
            new_node = _DoublyNode(key, value)
            self._cache[key] = new_node
            self._add_node(new_node)

    def size(self) -> int:
        """Return number of entries.

        Returns:
            Current count.

        Time Complexity: O(1)
        """
        return len(self._cache)


# ─── Tests ────────────────────────────────────────────────────────────────────


def _run_tests() -> None:
    """Run all tests and report results."""
    import sys

    passed = 0
    failed = 0

    def check(description: str, condition: bool) -> None:
        nonlocal passed, failed
        if condition:
            passed += 1
            print(f"  ✓ {description}")
        else:
            failed += 1
            print(f"  ✗ {description}", file=sys.stderr)

    def test_lru(cache_cls, name: str):
        print(f"\n{name}:")
        cache = cache_cls(2)

        # Basic put/get
        cache.put(1, 1)
        cache.put(2, 2)
        check("get(1) == 1", cache.get(1) == 1)

        # Eviction
        cache.put(3, 3)
        check("get(2) == -1 (evicted)", cache.get(2) == -1)
        check("get(1) == 1 (still present)", cache.get(1) == 1)
        check("get(3) == 3", cache.get(3) == 3)

        # Update
        cache.put(1, 10)
        check("update value", cache.get(1) == 10)

        # LRU order: 1 is MRU after get, then put
        cache.put(4, 4)  # Evicts 3 (LRU after get(1))
        check("get(3) evicted by 4", cache.get(3) == -1)
        check("get(1) still present", cache.get(1) == 10)
        check("get(4) present", cache.get(4) == 4)

        # Get missing
        check("get missing == -1", cache.get(99) == -1)

        # Size
        check("size == 2", cache.size() == 2)

        # Capacity 1
        small = cache_cls(1)
        small.put(1, 1)
        small.put(2, 2)
        check("capacity 1 evicts 1", small.get(1) == -1)
        check("capacity 1 has 2", small.get(2) == 2)

    test_lru(LRUCacheOrderedDict, "LRUCacheOrderedDict")
    test_lru(LRUCache, "LRUCache (Manual)")

    # Test capacity validation
    try:
        LRUCache(0)
        check("capacity 0 raises", False)
    except ValueError:
        check("capacity 0 raises", True)

    try:
        LRUCacheOrderedDict(-1)
        check("capacity -1 raises", False)
    except ValueError:
        check("capacity -1 raises", True)

    # Additional scenario from LeetCode
    print("\nAdditional scenario:")
    cache = LRUCache(2)
    cache.put(1, 0)
    cache.put(2, 2)
    check("get(1)", cache.get(1) == 0)
    cache.put(3, 3)
    check("eviction", cache.get(2) == -1)
    cache.put(4, 4)
    check("eviction 2", cache.get(1) == -1)
    check("get(3)", cache.get(3) == 3)
    check("get(4)", cache.get(4) == 4)

    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
