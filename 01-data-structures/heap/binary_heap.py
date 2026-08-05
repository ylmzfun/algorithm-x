"""
Binary Heap Implementation (MinHeap and MaxHeap)
==================================================

A binary heap is a complete binary tree stored in an array where each node
satisfies the heap property:
    - MinHeap: parent <= children (smallest at root)
    - MaxHeap: parent >= children (largest at root)

Operations:
    - push (sift up): O(log n)
    - pop (sift down): O(log n)
    - peek: O(1)
    - heapify (build from array): O(n)
    - heapsort: O(n log n)

Array representation:
    - Parent of i: (i - 1) // 2
    - Left child of i: 2*i + 1
    - Right child of i: 2*i + 2

Space Complexity: O(n) for n elements.
"""

from typing import Any, List, Optional, Iterator


class MinHeap:
    """A binary min-heap: the smallest element is always at the root.

    Examples:
        >>> heap = MinHeap()
        >>> heap.push(5)
        >>> heap.push(3)
        >>> heap.push(7)
        >>> heap.peek()
        3
        >>> heap.pop()
        3
        >>> heap.size()
        2
        >>> heap.pop()
        5
        >>> heap.pop()
        7
    """

    def __init__(self, items: Optional[List[Any]] = None) -> None:
        """Initialize min-heap, optionally from a list of items.

        If `items` is provided, heapify is called in O(n) time.

        Args:
            items: Optional initial list to heapify.
        """
        self._data: List[Any] = []
        if items:
            self._data = items[:]
            self._heapify()

    def size(self) -> int:
        """Return number of elements."""
        return len(self._data)

    def is_empty(self) -> bool:
        """Check if heap is empty."""
        return len(self._data) == 0

    def peek(self) -> Any:
        """Return the minimum element without removing it.

        Returns:
            Smallest element.

        Raises:
            IndexError: If heap is empty.

        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("peek from empty heap")
        return self._data[0]

    def push(self, item: Any) -> None:
        """Insert `item` and sift up to maintain heap property.

        Args:
            item: Element to add.

        Time Complexity: O(log n)
        """
        self._data.append(item)
        self._sift_up(len(self._data) - 1)

    def pop(self) -> Any:
        """Remove and return the minimum element.

        Returns:
            Smallest element.

        Raises:
            IndexError: If heap is empty.

        Time Complexity: O(log n)
        """
        if self.is_empty():
            raise IndexError("pop from empty heap")

        if len(self._data) == 1:
            return self._data.pop()

        root = self._data[0]
        # Move last element to root and sift down
        self._data[0] = self._data.pop()
        self._sift_down(0)
        return root

    def replace(self, item: Any) -> Any:
        """Pop root and push new item (more efficient than pop + push).

        Args:
            item: New element to insert.

        Returns:
            Previous minimum element.

        Raises:
            IndexError: If heap is empty.

        Time Complexity: O(log n)
        """
        if self.is_empty():
            raise IndexError("replace on empty heap")
        root = self._data[0]
        self._data[0] = item
        self._sift_down(0)
        return root

    # ── Sift operations ──────────────────────────────────────────────────────

    def _sift_up(self, idx: int) -> None:
        """Move element at `idx` up while it's smaller than its parent.

        Args:
            idx: Index of element to sift up.
        """
        parent = (idx - 1) // 2
        while idx > 0 and self._data[idx] < self._data[parent]:
            self._data[idx], self._data[parent] = self._data[parent], self._data[idx]
            idx = parent
            parent = (idx - 1) // 2

    def _sift_down(self, idx: int) -> None:
        """Move element at `idx` down while it's larger than its children.

        Args:
            idx: Index of element to sift down.
        """
        n = len(self._data)
        while True:
            smallest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2

            if left < n and self._data[left] < self._data[smallest]:
                smallest = left
            if right < n and self._data[right] < self._data[smallest]:
                smallest = right

            if smallest == idx:
                break

            self._data[idx], self._data[smallest] = self._data[smallest], self._data[idx]
            idx = smallest

    def _heapify(self) -> None:
        """Transform the internal array into a valid heap in O(n) time.

        Starts from the last non-leaf node and sifts down.
        """
        n = len(self._data)
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(i)

    # ── Static heapsort ──────────────────────────────────────────────────────

    @staticmethod
    def heapsort(items: List[Any]) -> List[Any]:
        """Sort `items` in ascending order using heapsort.

        Builds a min-heap and extracts elements one by one.

        Args:
            items: List to sort.

        Returns:
            New sorted list.

        Time Complexity: O(n log n)
        Space Complexity: O(n) for the result.
        """
        heap = MinHeap(items)
        result: List[Any] = []
        while not heap.is_empty():
            result.append(heap.pop())
        return result

    # ── Dunder ───────────────────────────────────────────────────────────────

    def __iter__(self) -> Iterator[Any]:
        """Yield elements (heap order not guaranteed for arbitrary iteration)."""
        yield from self._data

    def __len__(self) -> int:
        return len(self._data)

    def __str__(self) -> str:
        return str(self._data)

    def __repr__(self) -> str:
        return f"MinHeap({self._data})"


class MaxHeap:
    """A binary max-heap: the largest element is always at the root.

    Implemented by wrapping a MinHeap with negated values.

    Examples:
        >>> heap = MaxHeap()
        >>> heap.push(5)
        >>> heap.push(3)
        >>> heap.push(7)
        >>> heap.peek()
        7
        >>> heap.pop()
        7
        >>> heap.size()
        2
    """

    def __init__(self, items: Optional[List[Any]] = None) -> None:
        """Initialize max-heap, optionally from a list.

        Args:
            items: Optional initial list to heapify.
        """
        self._data: List[Any] = []
        if items:
            self._data = items[:]
            self._heapify()

    def size(self) -> int:
        """Return number of elements."""
        return len(self._data)

    def is_empty(self) -> bool:
        """Check if heap is empty."""
        return len(self._data) == 0

    def peek(self) -> Any:
        """Return the maximum element.

        Returns:
            Largest element.

        Raises:
            IndexError: If heap is empty.

        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("peek from empty heap")
        return self._data[0]

    def push(self, item: Any) -> None:
        """Insert `item` and sift up.

        Args:
            item: Element to add.

        Time Complexity: O(log n)
        """
        self._data.append(item)
        self._sift_up(len(self._data) - 1)

    def pop(self) -> Any:
        """Remove and return the maximum element.

        Returns:
            Largest element.

        Raises:
            IndexError: If heap is empty.

        Time Complexity: O(log n)
        """
        if self.is_empty():
            raise IndexError("pop from empty heap")
        if len(self._data) == 1:
            return self._data.pop()
        root = self._data[0]
        self._data[0] = self._data.pop()
        self._sift_down(0)
        return root

    def _sift_up(self, idx: int) -> None:
        """Move element up while larger than parent."""
        parent = (idx - 1) // 2
        while idx > 0 and self._data[idx] > self._data[parent]:
            self._data[idx], self._data[parent] = self._data[parent], self._data[idx]
            idx = parent
            parent = (idx - 1) // 2

    def _sift_down(self, idx: int) -> None:
        """Move element down while smaller than children."""
        n = len(self._data)
        while True:
            largest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2
            if left < n and self._data[left] > self._data[largest]:
                largest = left
            if right < n and self._data[right] > self._data[largest]:
                largest = right
            if largest == idx:
                break
            self._data[idx], self._data[largest] = self._data[largest], self._data[idx]
            idx = largest

    def _heapify(self) -> None:
        """Build heap from array in O(n)."""
        n = len(self._data)
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(i)

    @staticmethod
    def heapsort(items: List[Any]) -> List[Any]:
        """Sort in descending order using max-heap.

        Args:
            items: List to sort.

        Returns:
            New list sorted in descending order.

        Time Complexity: O(n log n)
        """
        heap = MaxHeap(items)
        result: List[Any] = []
        while not heap.is_empty():
            result.append(heap.pop())
        return result

    def __len__(self) -> int:
        return len(self._data)

    def __str__(self) -> str:
        return str(self._data)

    def __repr__(self) -> str:
        return f"MaxHeap({self._data})"


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

    # ── MinHeap ───────────────────────────────────────────────────────────────
    print("MinHeap:")
    mh = MinHeap()
    check("empty size", mh.size() == 0)
    check("empty is_empty", mh.is_empty())

    try:
        mh.peek()
        check("peek empty raises", False)
    except IndexError:
        check("peek empty raises", True)

    mh.push(5)
    mh.push(3)
    mh.push(7)
    mh.push(1)
    mh.push(9)
    check("size after 5 pushes", mh.size() == 5)
    check("peek == 1", mh.peek() == 1)
    check("pop == 1", mh.pop() == 1)
    check("pop == 3", mh.pop() == 3)
    check("pop == 5", mh.pop() == 5)
    check("pop == 7", mh.pop() == 7)
    check("pop == 9", mh.pop() == 9)
    check("empty after all pops", mh.is_empty())

    # Replace
    mh.push(10)
    mh.push(20)
    check("replace: pop 10, push 15", mh.replace(15) == 10)
    check("peek now 15", mh.peek() == 15)

    # Heapify
    print("\nHeapify:")
    heap2 = MinHeap([7, 2, 9, 1, 5])
    check("heapify size", heap2.size() == 5)
    check("heapify peek == 1", heap2.peek() == 1)
    check("heapify pop order", [heap2.pop() for _ in range(5)] == [1, 2, 5, 7, 9])

    # Heapsort
    print("\nHeapsort:")
    sorted_arr = MinHeap.heapsort([3, 1, 4, 1, 5, 9, 2, 6])
    check("heapsort ascending", sorted_arr == [1, 1, 2, 3, 4, 5, 6, 9])

    # ── MaxHeap ───────────────────────────────────────────────────────────────
    print("\nMaxHeap:")
    mxh = MaxHeap()
    mxh.push(5)
    mxh.push(3)
    mxh.push(7)
    mxh.push(1)
    check("max peek == 7", mxh.peek() == 7)
    check("max pop == 7", mxh.pop() == 7)
    check("max pop == 5", mxh.pop() == 5)

    # Max heapify
    mxh2 = MaxHeap([7, 2, 9, 1, 5])
    check("max heapify peek == 9", mxh2.peek() == 9)

    # Max heapsort
    sorted_desc = MaxHeap.heapsort([3, 1, 4, 1, 5])
    check("heapsort descending", sorted_desc == [5, 4, 3, 1, 1])

    try:
        MaxHeap().pop()
        check("pop empty raises", False)
    except IndexError:
        check("pop empty raises", True)

    # ── Summary ───────────────────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
