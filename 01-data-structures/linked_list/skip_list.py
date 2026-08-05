"""
Skip List Implementation
=========================

A probabilistic data structure that provides O(log n) average-case
search, insertion, and deletion — similar to balanced trees but simpler
to implement.

The skip list consists of multiple levels of linked lists. Each element
appears at a level with probability p (typically 0.5), providing a
hierarchical structure that allows "express lanes" for fast search.

Time Complexities (average):
    - Search: O(log n)
    - Insert: O(log n)
    - Delete: O(log n)

Space Complexity: O(n) expected — each element appears in ~2 levels on average.
"""

import random
from typing import Any, List, Optional


class SkipNode:
    """A node in the skip list with data and multi-level forward pointers.

    Attributes:
        data: The value stored in this node.
        forward: List of forward pointers, one per level. forward[i] points
                 to the next node at level i.
    """

    def __init__(self, data: Any, level: int) -> None:
        """Initialize a skip list node.

        Args:
            data: Value to store (None for sentinel head only).
            level: Number of forward pointers (0-indexed, so level+1 total).
        """
        self.data: Any = data
        self.forward: List[Optional["SkipNode"]] = [None] * (level + 1)

    def __repr__(self) -> str:
        """Return string representation."""
        return f"SkipNode({self.data!r}, level={len(self.forward) - 1})"


class SkipList:
    """A sorted skip list implementation.

    Supports duplicate-free insertion, search, and deletion with O(log n)
    average time complexity.

    The maximum level is capped at 16 (supports ~65K elements at p=0.5).
    Probability factor p = 0.5 means each level has ~50% chance.

    Examples:
        >>> sl = SkipList()
        >>> sl.insert(3)
        >>> sl.insert(1)
        >>> sl.insert(2)
        >>> sl.search(2)
        True
        >>> sl.to_list()
        [1, 2, 3]
        >>> sl.delete(2)
        True
        >>> sl.size()
        2
    """

    _MAX_LEVEL = 16  # Supports ~2^16 elements
    _P = 0.5  # Probability factor

    def __init__(self) -> None:
        """Initialize an empty skip list with a sentinel head node."""
        self._head: SkipNode = SkipNode(None, self._MAX_LEVEL)
        self._level: int = 0  # Current highest level (0-indexed)
        self._size: int = 0

    def size(self) -> int:
        """Return number of elements.

        Returns:
            Count of stored elements.

        Time Complexity: O(1)
        """
        return self._size

    def is_empty(self) -> bool:
        """Check if the skip list is empty.

        Returns:
            True if no elements stored.

        Time Complexity: O(1)
        """
        return self._size == 0

    def _random_level(self) -> int:
        """Generate a random level for a new node.

        Level i is chosen with probability P^i * (1-P), capped at MAX_LEVEL.

        Returns:
            Integer level (0-indexed) for the new node.

        Time Complexity: O(1) expected
        """
        level = 0
        while random.random() < self._P and level < self._MAX_LEVEL:
            level += 1
        return level

    def search(self, data: Any) -> bool:
        """Check if `data` exists in the skip list.

        Args:
            data: Value to search for.

        Returns:
            True if found, False otherwise.

        Time Complexity: O(log n) average
        """
        current = self._head

        # Start from highest level and work down
        for i in range(self._level, -1, -1):
            while current.forward[i] is not None and current.forward[i].data < data:
                current = current.forward[i]  # type: ignore[assignment]

        # Move to next node at level 0
        current = current.forward[0]  # type: ignore[assignment]

        return current is not None and current.data == data

    def insert(self, data: Any) -> bool:
        """Insert `data` into the skip list if not already present.

        Args:
            data: Value to insert. Must support comparison operators.

        Returns:
            True if inserted, False if already present.

        Time Complexity: O(log n) average

        Examples:
            >>> sl = SkipList()
            >>> sl.insert(5)
            True
            >>> sl.insert(5)
            False
        """
        # `update[i]` = node whose forward[i] needs updating
        update: List[Optional[SkipNode]] = [None] * (self._MAX_LEVEL + 1)
        current = self._head

        # Find insertion position at each level
        for i in range(self._level, -1, -1):
            while current.forward[i] is not None and current.forward[i].data < data:
                current = current.forward[i]  # type: ignore[assignment]
            update[i] = current

        current = current.forward[0]  # type: ignore[assignment]

        # If data already exists, do not insert duplicate
        if current is not None and current.data == data:
            return False

        # Generate random level
        new_level = self._random_level()

        # If new node has higher level, update head pointers
        if new_level > self._level:
            for i in range(self._level + 1, new_level + 1):
                update[i] = self._head
            self._level = new_level

        # Create and link new node
        new_node = SkipNode(data, new_level)
        for i in range(new_level + 1):
            new_node.forward[i] = update[i].forward[i]  # type: ignore[union-attr]
            update[i].forward[i] = new_node  # type: ignore[union-attr]

        self._size += 1
        return True

    def delete(self, data: Any) -> bool:
        """Remove `data` from the skip list if present.

        Args:
            data: Value to remove.

        Returns:
            True if deleted, False if not found.

        Time Complexity: O(log n) average
        """
        update: List[Optional[SkipNode]] = [None] * (self._MAX_LEVEL + 1)
        current = self._head

        # Find node to delete
        for i in range(self._level, -1, -1):
            while current.forward[i] is not None and current.forward[i].data < data:
                current = current.forward[i]  # type: ignore[assignment]
            update[i] = current

        current = current.forward[0]  # type: ignore[assignment]

        # If not found
        if current is None or current.data != data:
            return False

        # Update forward pointers
        for i in range(self._level + 1):
            if update[i].forward[i] != current:  # type: ignore[union-attr]
                break
            update[i].forward[i] = current.forward[i]  # type: ignore[union-attr]

        # Update level if the deleted node was the only one at high levels
        while self._level > 0 and self._head.forward[self._level] is None:
            self._level -= 1

        self._size -= 1
        return True

    def to_list(self) -> List[Any]:
        """Return all elements as a sorted Python list.

        Returns:
            List of all stored values in ascending order.

        Time Complexity: O(n)
        """
        result: List[Any] = []
        current = self._head.forward[0]
        while current is not None:
            result.append(current.data)
            current = current.forward[0]
        return result

    def min(self) -> Optional[Any]:
        """Return the minimum element.

        Returns:
            Smallest value, or None if empty.

        Time Complexity: O(1)
        """
        node = self._head.forward[0]
        return node.data if node is not None else None

    def max(self) -> Optional[Any]:
        """Return the maximum element.

        Returns:
            Largest value, or None if empty.

        Time Complexity: O(log n) average
        """
        current = self._head
        for i in range(self._level, -1, -1):
            while current.forward[i] is not None:
                current = current.forward[i]  # type: ignore[assignment]
        return current.data if current is not self._head else None

    def __iter__(self):
        """Yield elements in ascending order."""
        current = self._head.forward[0]
        while current is not None:
            yield current.data
            current = current.forward[0]

    def __len__(self) -> int:
        """Support len()."""
        return self._size

    def __contains__(self, data: Any) -> bool:
        """Support `in` operator."""
        return self.search(data)

    def __str__(self) -> str:
        """Return string representation."""
        return str(self.to_list())

    def __repr__(self) -> str:
        """Return detailed representation."""
        return f"SkipList(size={self._size}, level={self._level}, data={self.to_list()})"


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

    # ── Creation ──────────────────────────────────────────────────────────────
    print("Creation:")
    sl = SkipList()
    check("empty size", sl.size() == 0)
    check("empty is_empty", sl.is_empty() is True)
    check("min on empty is None", sl.min() is None)
    check("max on empty is None", sl.max() is None)

    # ── Insert ────────────────────────────────────────────────────────────────
    print("\nInsert:")
    check("insert 3", sl.insert(3) is True)
    check("insert 1", sl.insert(1) is True)
    check("insert 2", sl.insert(2) is True)
    check("insert 5", sl.insert(5) is True)
    check("insert 4", sl.insert(4) is True)
    check("size after 5 inserts", sl.size() == 5)
    check("duplicate insert returns False", sl.insert(3) is False)
    check("size unchanged after duplicate", sl.size() == 5)

    # ── Search ────────────────────────────────────────────────────────────────
    print("\nSearch:")
    check("search(1) True", sl.search(1) is True)
    check("search(3) True", sl.search(3) is True)
    check("search(5) True", sl.search(5) is True)
    check("search(0) False", sl.search(0) is False)
    check("search(6) False", sl.search(6) is False)
    check("__contains__ via `in`", (3 in sl) is True)
    check("__contains__ via `in` False", (99 in sl) is False)

    # ── Sorted order ──────────────────────────────────────────────────────────
    print("\nSorted Order:")
    check("to_list is sorted", sl.to_list() == [1, 2, 3, 4, 5])
    check("min == 1", sl.min() == 1)
    check("max == 5", sl.max() == 5)

    # ── Delete ────────────────────────────────────────────────────────────────
    print("\nDelete:")
    check("delete(3) True", sl.delete(3) is True)
    check("after delete to_list", sl.to_list() == [1, 2, 4, 5])
    check("size after delete", sl.size() == 4)
    check("delete(3) again returns False", sl.delete(3) is False)
    check("delete(1) head", sl.delete(1) is True)
    check("after delete head", sl.to_list() == [2, 4, 5])
    check("delete(5) tail", sl.delete(5) is True)
    check("after delete tail", sl.to_list() == [2, 4])
    check("delete non-existent False", sl.delete(99) is False)

    # ── Clear and re-insert ───────────────────────────────────────────────────
    print("\nClear via sequential delete:")
    sl2 = SkipList()
    for x in [10, 5, 15, 3, 7, 12, 18]:
        sl2.insert(x)
    check("bulk insert sorted", sl2.to_list() == [3, 5, 7, 10, 12, 15, 18])

    for x in [3, 7, 12, 18]:
        sl2.delete(x)
    check("after partial deletes", sl2.to_list() == [5, 10, 15])

    for x in [5, 10, 15]:
        sl2.delete(x)
    check("empty after all deletes", sl2.is_empty())
    check("empty to_list", sl2.to_list() == [])

    # ── Larger scale test ─────────────────────────────────────────────────────
    print("\nLarge scale (100 elements):")
    sl3 = SkipList()
    nums = list(range(100))
    random.shuffle(nums)
    for n in nums:
        sl3.insert(n)
    check("size == 100", sl3.size() == 100)
    check("sorted output", sl3.to_list() == list(range(100)))
    check("min == 0", sl3.min() == 0)
    check("max == 99", sl3.max() == 99)

    # Delete evens
    for i in range(0, 100, 2):
        sl3.delete(i)
    check("after deleting evens, size == 50", sl3.size() == 50)
    check("only odds remain", all(x % 2 == 1 for x in sl3.to_list()))

    # ── Iteration ─────────────────────────────────────────────────────────────
    print("\nIteration:")
    iter_sl = SkipList()
    for x in [3, 1, 2]:
        iter_sl.insert(x)
    check("iteration sorted", list(iter_sl) == [1, 2, 3])

    # ── Summary ───────────────────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
