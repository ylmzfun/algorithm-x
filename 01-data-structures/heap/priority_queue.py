"""
Priority Queue Implementation
===============================

A priority queue built on a binary heap where elements are associated with
priorities. Lower priority values are served first (min-priority queue by
default). Supports push, pop, peek, and update_priority.

Time Complexities:
    - push: O(log n)
    - pop: O(log n)
    - peek: O(1)
    - update_priority: O(n) — search + O(log n) — sift

Space Complexity: O(n) for n elements.
"""

from typing import Any, Generic, List, Optional, Tuple, TypeVar

T = TypeVar("T")


class PriorityQueue(Generic[T]):
    """A min-priority queue storing (priority, item) pairs.

    Items with the same priority are served in FIFO order (stable).

    Examples:
        >>> pq = PriorityQueue[str]()
        >>> pq.push("task1", priority=3)
        >>> pq.push("task2", priority=1)
        >>> pq.push("task3", priority=2)
        >>> pq.peek()
        ('task2', 1)
        >>> pq.pop()
        ('task2', 1)
        >>> pq.pop()
        ('task3', 2)
        >>> pq.size()
        1
    """

    def __init__(self) -> None:
        """Initialize an empty priority queue."""
        self._heap: List[Tuple[int, int, T]] = []  # (priority, counter, item)
        self._counter: int = 0  # Tie-breaker for stability

    def size(self) -> int:
        """Return number of elements."""
        return len(self._heap)

    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return len(self._heap) == 0

    def push(self, item: T, priority: int) -> None:
        """Insert `item` with given `priority`.

        Lower priority numbers are served first. Tie-breaker uses
        insertion order for stability.

        Args:
            item: Element to insert.
            priority: Priority value (lower = higher priority).

        Time Complexity: O(log n)
        """
        entry = (priority, self._counter, item)
        self._counter += 1
        self._heap.append(entry)
        self._sift_up(len(self._heap) - 1)

    def pop(self) -> Tuple[T, int]:
        """Remove and return the (item, priority) with highest priority.

        Returns:
            Tuple of (item, priority) for the highest-priority element.

        Raises:
            IndexError: If queue is empty.

        Time Complexity: O(log n)
        """
        if self.is_empty():
            raise IndexError("pop from empty priority queue")

        if len(self._heap) == 1:
            priority, _, item = self._heap.pop()
            return (item, priority)

        root = self._heap[0]
        self._heap[0] = self._heap.pop()
        self._sift_down(0)
        return (root[2], root[0])

    def peek(self) -> Tuple[T, int]:
        """Return the highest-priority (item, priority) without removing.

        Returns:
            Tuple of (item, priority).

        Raises:
            IndexError: If queue is empty.

        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("peek from empty priority queue")
        priority, _, item = self._heap[0]
        return (item, priority)

    def update_priority(self, item: T, new_priority: int) -> bool:
        """Update the priority of an existing item.

        Searches for `item` (O(n)), removes it, and re-inserts with
        the new priority. If multiple copies of the same item exist,
        only the first found (closest to root) is updated.

        Args:
            item: Element whose priority to update.
            new_priority: New priority value.

        Returns:
            True if the item was found and updated, False otherwise.

        Time Complexity: O(n) — linear search through heap array.
        """
        idx = -1
        for i, (_, _, val) in enumerate(self._heap):
            if val == item:
                idx = i
                break

        if idx == -1:
            return False

        # Remove and re-insert
        old_entry = self._heap[idx]
        self._heap[idx] = self._heap[-1]
        self._heap.pop()

        if idx < len(self._heap):
            # Sift to fix
            parent = (idx - 1) // 2
            if idx > 0 and self._heap[idx] < self._heap[parent]:
                self._sift_up(idx)
            else:
                self._sift_down(idx)

        # Insert with new priority
        self.push(item, new_priority)
        return True

    # ── Sift operations ──────────────────────────────────────────────────────

    def _sift_up(self, idx: int) -> None:
        """Move element up while it has higher priority (smaller tuple)."""
        parent = (idx - 1) // 2
        while idx > 0 and self._heap[idx] < self._heap[parent]:
            self._heap[idx], self._heap[parent] = self._heap[parent], self._heap[idx]
            idx = parent
            parent = (idx - 1) // 2

    def _sift_down(self, idx: int) -> None:
        """Move element down while it has lower priority (larger tuple)."""
        n = len(self._heap)
        while True:
            smallest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2

            if left < n and self._heap[left] < self._heap[smallest]:
                smallest = left
            if right < n and self._heap[right] < self._heap[smallest]:
                smallest = right

            if smallest == idx:
                break

            self._heap[idx], self._heap[smallest] = self._heap[smallest], self._heap[idx]
            idx = smallest

    def __len__(self) -> int:
        return len(self._heap)

    def __str__(self) -> str:
        items = [(item, pri) for pri, _, item in sorted(self._heap)]
        return str(items)

    def __repr__(self) -> str:
        return f"PriorityQueue(size={len(self)})"


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
    pq = PriorityQueue[str]()
    check("empty size", pq.size() == 0)
    check("empty is_empty", pq.is_empty())

    pq.push("task1", 3)
    pq.push("task2", 1)
    pq.push("task3", 2)
    check("size after 3 pushes", pq.size() == 3)
    check("peek returns task2 pri=1", pq.peek() == ("task2", 1))
    check("pop returns task2", pq.pop() == ("task2", 1))
    check("pop returns task3", pq.pop() == ("task3", 2))
    check("pop returns task1", pq.pop() == ("task1", 3))
    check("empty after pops", pq.is_empty())

    try:
        pq.pop()
        check("pop empty raises", False)
    except IndexError:
        check("pop empty raises", True)

    try:
        pq.peek()
        check("peek empty raises", False)
    except IndexError:
        check("peek empty raises", True)

    # ── Same priority (FIFO) ─────────────────────────────────────────────────
    print("\nSame priority (FIFO):")
    pq2 = PriorityQueue[str]()
    pq2.push("A", 1)
    pq2.push("B", 1)
    pq2.push("C", 1)
    check("FIFO: A first", pq2.pop() == ("A", 1))
    check("FIFO: B second", pq2.pop() == ("B", 1))
    check("FIFO: C third", pq2.pop() == ("C", 1))

    # ── Update priority ──────────────────────────────────────────────────────
    print("\nUpdate priority:")
    pq3 = PriorityQueue[str]()
    pq3.push("X", 5)
    pq3.push("Y", 3)
    pq3.push("Z", 4)
    check("update Y to 1", pq3.update_priority("Y", 1))
    check("after update peek is Y", pq3.peek() == ("Y", 1))
    check("update non-existent", not pq3.update_priority("W", 0))

    # ── Mixed types ──────────────────────────────────────────────────────────
    print("\nMixed types:")
    pq_int = PriorityQueue[int]()
    pq_int.push(42, 0)
    pq_int.push(7, -10)
    check("negative priority works", pq_int.peek() == (7, -10))

    # ── Summary ───────────────────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
