"""
HashSet Implementation (Open Addressing / Linear Probing)
==========================================================

A hash set that stores unique elements using open addressing with
linear probing for collision resolution.

Features:
    - add(element): Insert an element.
    - remove(element): Delete an element.
    - contains(element): Check if element exists.
    - Automatic resize when load factor exceeds 0.7.

Uses a tombstone marker to handle deletions correctly during probing.

Time Complexities (average):
    - add: O(1)
    - remove: O(1)
    - contains: O(1)

Space Complexity: O(capacity)
"""

from typing import Any, Optional, Iterator


class HashSet:
    """A hash set using open addressing with linear probing.

    Slots can be: None (empty), _TOMBSTONE (deleted), or an actual element.

    Examples:
        >>> hs = HashSet()
        >>> hs.add(1)
        >>> hs.add(2)
        >>> hs.contains(1)
        True
        >>> hs.remove(1)
        True
        >>> hs.size()
        1
    """

    _DEFAULT_CAPACITY = 16
    _LOAD_FACTOR = 0.7

    # Sentinel for deleted slots
    class _Tombstone:
        """Marker for a deleted slot to preserve probe sequence."""
        def __repr__(self) -> str:
            return "<TOMBSTONE>"

    _TOMBSTONE = _Tombstone()

    def __init__(self, initial_capacity: int = _DEFAULT_CAPACITY) -> None:
        """Initialize hash set with given capacity.

        Args:
            initial_capacity: Number of slots (default 16).
        """
        if initial_capacity < 1:
            raise ValueError("initial_capacity must be >= 1")
        self._capacity: int = initial_capacity
        self._size: int = 0
        self._slots: list[Optional[Any]] = [None] * initial_capacity

    def size(self) -> int:
        """Return number of elements.

        Returns:
            Count of stored elements.

        Time Complexity: O(1)
        """
        return self._size

    def is_empty(self) -> bool:
        """Check if set is empty.

        Returns:
            True if no elements.

        Time Complexity: O(1)
        """
        return self._size == 0

    def _hash(self, element: Any) -> int:
        """Compute initial slot index.

        Args:
            element: Element to hash.

        Returns:
            Slot index.

        Time Complexity: O(1)
        """
        return abs(hash(element)) % self._capacity

    def _load_factor(self) -> float:
        """Return current load factor.

        Returns:
            Ratio of size to capacity.

        Time Complexity: O(1)
        """
        return self._size / self._capacity

    def _find_slot(self, element: Any) -> int:
        """Find the slot index where `element` is or should be.

        Uses linear probing: (hash + i) % capacity.

        Returns the index of the first matching element or the first
        empty slot (for insertion).

        Args:
            element: Element to find.

        Returns:
            Index of the slot containing the element, or the first empty
            slot if not found.

        Time Complexity: O(1) average, O(n) worst case.
        """
        idx = self._hash(element)
        first_tombstone: Optional[int] = None

        for i in range(self._capacity):
            probe_idx = (idx + i) % self._capacity
            slot = self._slots[probe_idx]

            if slot is self._TOMBSTONE:
                if first_tombstone is None:
                    first_tombstone = probe_idx
            elif slot is None:
                # Return first tombstone if found (reuse deleted slots),
                # otherwise this empty slot
                return first_tombstone if first_tombstone is not None else probe_idx
            elif slot == element:
                return probe_idx

        # Should not reach here if resize is called before full
        return first_tombstone if first_tombstone is not None else 0

    def add(self, element: Any) -> bool:
        """Add an element to the set.

        Args:
            element: Element to add.

        Returns:
            True if added, False if already present.

        Time Complexity: O(1) average, O(n) when resizing.
        """
        if self._load_factor() >= self._LOAD_FACTOR:
            self._resize(self._capacity * 2)

        idx = self._find_slot(element)
        slot = self._slots[idx]

        if slot is not None and slot is not self._TOMBSTONE and slot == element:
            return False  # Already present

        self._slots[idx] = element
        self._size += 1
        return True

    def remove(self, element: Any) -> bool:
        """Remove an element from the set.

        Args:
            element: Element to remove.

        Returns:
            True if removed, False if not present.

        Time Complexity: O(1) average.
        """
        idx = self._hash(element)

        for i in range(self._capacity):
            probe_idx = (idx + i) % self._capacity
            slot = self._slots[probe_idx]

            if slot is None:
                return False  # Element not found (hit empty slot)
            if slot is not self._TOMBSTONE and slot == element:
                self._slots[probe_idx] = self._TOMBSTONE
                self._size -= 1
                return True

        return False

    def contains(self, element: Any) -> bool:
        """Check if element exists in the set.

        Args:
            element: Element to check.

        Returns:
            True if present, False otherwise.

        Time Complexity: O(1) average.
        """
        idx = self._hash(element)

        for i in range(self._capacity):
            probe_idx = (idx + i) % self._capacity
            slot = self._slots[probe_idx]

            if slot is None:
                return False
            if slot is not self._TOMBSTONE and slot == element:
                return True

        return False

    def clear(self) -> None:
        """Remove all elements, reset to default capacity.

        Time Complexity: O(capacity)
        """
        self._capacity = self._DEFAULT_CAPACITY
        self._size = 0
        self._slots = [None] * self._capacity

    def _resize(self, new_capacity: int) -> None:
        """Resize the internal slot array and rehash all elements.

        Args:
            new_capacity: New number of slots.

        Time Complexity: O(n + new_capacity)
        """
        old_slots = self._slots
        self._capacity = new_capacity
        self._size = 0
        self._slots = [None] * new_capacity

        for element in old_slots:
            if element is not None and element is not self._TOMBSTONE:
                self.add(element)

    def __iter__(self) -> Iterator[Any]:
        """Yield all elements."""
        for slot in self._slots:
            if slot is not None and slot is not self._TOMBSTONE:
                yield slot

    def __contains__(self, element: Any) -> bool:
        """Support `in` operator."""
        return self.contains(element)

    def __len__(self) -> int:
        """Support len()."""
        return self._size

    def __str__(self) -> str:
        """Return string representation."""
        items = [str(x) for x in self]
        return "{" + ", ".join(items) + "}"

    def __repr__(self) -> str:
        """Return detailed representation."""
        return f"HashSet(size={self._size}, capacity={self._capacity})"


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

    # ── Basic operations ──────────────────────────────────────────────────────
    print("Basic operations:")
    hs = HashSet()
    check("empty size", hs.size() == 0)
    check("empty is_empty", hs.is_empty())

    check("add 1", hs.add(1) is True)
    check("add 2", hs.add(2) is True)
    check("add 3", hs.add(3) is True)
    check("size after 3 adds", hs.size() == 3)
    check("contains(1)", hs.contains(1))
    check("contains(2)", hs.contains(2))
    check("not contains(0)", not hs.contains(0))

    # ── Duplicate ─────────────────────────────────────────────────────────────
    print("\nDuplicate:")
    check("add duplicate 1 returns False", hs.add(1) is False)
    check("size unchanged", hs.size() == 3)

    # ── Remove ────────────────────────────────────────────────────────────────
    print("\nRemove:")
    check("remove(2) True", hs.remove(2) is True)
    check("size after remove", hs.size() == 2)
    check("removed not contains(2)", not hs.contains(2))
    check("remove absent returns False", hs.remove(99) is False)

    # ── Tombstone handling ───────────────────────────────────────────────────
    print("\nTombstone handling:")
    hs_tomb = HashSet(4)
    for i in range(5):
        hs_tomb.add(i)
    hs_tomb.remove(0)
    hs_tomb.remove(1)
    check("can still find 2", hs_tomb.contains(2))
    check("can still find 3", hs_tomb.contains(3))
    check("can still find 4", hs_tomb.contains(4))

    # ── Resize ────────────────────────────────────────────────────────────────
    print("\nResize:")
    hs_resize = HashSet(4)
    check("initial capacity", hs_resize._capacity == 4)
    for i in range(20):
        hs_resize.add(i)
    check("capacity increased", hs_resize._capacity > 4)
    check("size == 20", hs_resize.size() == 20)
    for i in range(20):
        check(f"contains({i}) after resize", hs_resize.contains(i))

    # ── __contains__ operator ─────────────────────────────────────────────────
    print("\nOperator:")
    hs_op = HashSet()
    hs_op.add("hello")
    check("'hello' in hs", "hello" in hs_op)
    check("'world' not in hs", "world" not in hs_op)

    # ── Iteration ─────────────────────────────────────────────────────────────
    print("\nIteration:")
    hs_iter = HashSet()
    for x in [10, 20, 30]:
        hs_iter.add(x)
    check("iteration gives all elements", set(hs_iter) == {10, 20, 30})
    check("len() == 3", len(hs_iter) == 3)

    # ── Clear ─────────────────────────────────────────────────────────────────
    print("\nClear:")
    hs_iter.add(40)
    hs_iter.clear()
    check("clear makes empty", hs_iter.is_empty())
    check("clear size == 0", hs_iter.size() == 0)

    # ── Summary ───────────────────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
