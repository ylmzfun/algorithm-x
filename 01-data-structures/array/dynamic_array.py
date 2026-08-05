"""
Dynamic Array Implementation
=============================

A resizable array (similar to Python's list) that automatically grows and shrinks
based on the number of elements stored.

Time Complexities:
    - Access (get/set): O(1)
    - Append (amortized): O(1)
    - Insert/Delete at index: O(n)
    - Search: O(n)

Space Complexity: O(n)

The array doubles in capacity when full and halves when utilization drops below 25%.
This ensures amortized O(1) for append operations while avoiding excessive resizing.
"""

from typing import Any, Optional, Iterator


class DynamicArray:
    """A dynamic array that automatically resizes based on load factor.

    Attributes:
        _data: Internal fixed-size list for storing elements.
        _size: Number of elements currently stored.
        _capacity: Current maximum capacity before resize is needed.

    Examples:
        >>> arr = DynamicArray()
        >>> arr.append(1)
        >>> arr.append(2)
        >>> arr.size()
        2
        >>> arr.get(0)
        1
    """

    def __init__(self, initial_capacity: int = 8) -> None:
        """Initialize dynamic array with a given initial capacity.

        Args:
            initial_capacity: Starting capacity (default 8). Must be positive.

        Raises:
            ValueError: If initial_capacity <= 0.
        """
        if initial_capacity <= 0:
            raise ValueError("initial_capacity must be positive")
        self._data: list[Optional[Any]] = [None] * initial_capacity
        self._size: int = 0
        self._capacity: int = initial_capacity

    def size(self) -> int:
        """Return the number of elements in the array.

        Returns:
            The count of elements currently stored.

        Time Complexity: O(1)
        """
        return self._size

    def capacity(self) -> int:
        """Return the current maximum capacity before resize.

        Returns:
            The internal array capacity.

        Time Complexity: O(1)
        """
        return self._capacity

    def is_empty(self) -> bool:
        """Check if the array is empty.

        Returns:
            True if no elements are stored, False otherwise.

        Time Complexity: O(1)
        """
        return self._size == 0

    def get(self, index: int) -> Any:
        """Return the element at the given index.

        Args:
            index: Zero-based position to retrieve.

        Returns:
            The element stored at `index`.

        Raises:
            IndexError: If index is out of bounds.

        Time Complexity: O(1)
        """
        if not 0 <= index < self._size:
            raise IndexError(f"Index {index} out of bounds for size {self._size}")
        return self._data[index]

    def set(self, index: int, value: Any) -> None:
        """Set the element at the given index to `value`.

        Args:
            index: Zero-based position to update.
            value: New value to store.

        Raises:
            IndexError: If index is out of bounds.

        Time Complexity: O(1)
        """
        if not 0 <= index < self._size:
            raise IndexError(f"Index {index} out of bounds for size {self._size}")
        self._data[index] = value

    def append(self, value: Any) -> None:
        """Add an element to the end of the array.

        If the array is full, capacity is doubled before insertion.

        Args:
            value: Element to append.

        Time Complexity: O(1) amortized, O(n) when resizing.
        """
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        self._data[self._size] = value
        self._size += 1

    def insert(self, index: int, value: Any) -> None:
        """Insert an element at the specified index, shifting elements right.

        Args:
            index: Position to insert at. Can be equal to size (append).
            value: Element to insert.

        Raises:
            IndexError: If index is out of bounds.

        Time Complexity: O(n) — shifts elements after index.
        """
        if not 0 <= index <= self._size:
            raise IndexError(f"Index {index} out of bounds for size {self._size}")

        if self._size == self._capacity:
            self._resize(self._capacity * 2)

        # Shift elements to the right
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        self._data[index] = value
        self._size += 1

    def delete(self, index: int) -> Any:
        """Remove and return the element at the specified index.

        After removal, if the load factor drops below 25%, the array is halved
        (minimum capacity of 8 is maintained).

        Args:
            index: Position of element to remove.

        Returns:
            The removed element.

        Raises:
            IndexError: If index is out of bounds.

        Time Complexity: O(n) — shifts elements after index.
        """
        if not 0 <= index < self._size:
            raise IndexError(f"Index {index} out of bounds for size {self._size}")

        removed = self._data[index]

        # Shift elements to the left
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]

        self._data[self._size - 1] = None  # Help garbage collection
        self._size -= 1

        # Shrink if load factor < 25% and capacity > initial minimum
        if self._size > 0 and self._size < self._capacity // 4:
            new_capacity = max(8, self._capacity // 2)
            if new_capacity != self._capacity:
                self._resize(new_capacity)

        return removed

    def pop(self) -> Any:
        """Remove and return the last element.

        Returns:
            The last element.

        Raises:
            IndexError: If the array is empty.

        Time Complexity: O(1) amortized.
        """
        if self._size == 0:
            raise IndexError("pop from empty DynamicArray")
        return self.delete(self._size - 1)

    def index_of(self, value: Any) -> int:
        """Return the index of the first occurrence of `value`.

        Args:
            value: Element to search for.

        Returns:
            The zero-based index of the first match, or -1 if not found.

        Time Complexity: O(n)
        """
        for i in range(self._size):
            if self._data[i] == value:
                return i
        return -1

    def contains(self, value: Any) -> bool:
        """Check if `value` exists in the array.

        Args:
            value: Element to search for.

        Returns:
            True if found, False otherwise.

        Time Complexity: O(n)
        """
        return self.index_of(value) != -1

    def clear(self) -> None:
        """Remove all elements from the array, resetting to initial capacity.

        Time Complexity: O(capacity)
        """
        self._data = [None] * 8
        self._size = 0
        self._capacity = 8

    def _resize(self, new_capacity: int) -> None:
        """Resize the internal array to `new_capacity`.

        Creates a new array of the given size and copies all elements over.

        Args:
            new_capacity: The new capacity (must be >= size).

        Time Complexity: O(n) where n is the current size.
        """
        new_data: list[Optional[Any]] = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity

    def __iter__(self) -> Iterator[Any]:
        """Yield elements in order.

        Yields:
            Each element from index 0 to size-1.
        """
        for i in range(self._size):
            yield self._data[i]

    def __getitem__(self, index: int) -> Any:
        """Support bracket indexing: arr[i]."""
        return self.get(index)

    def __setitem__(self, index: int, value: Any) -> None:
        """Support bracket assignment: arr[i] = value."""
        self.set(index, value)

    def __len__(self) -> int:
        """Support len(arr)."""
        return self._size

    def __str__(self) -> str:
        """Return string representation of the array."""
        elements = [str(self._data[i]) for i in range(self._size)]
        return "[" + ", ".join(elements) + "]"

    def __repr__(self) -> str:
        """Return detailed string representation."""
        return f"DynamicArray(size={self._size}, capacity={self._capacity}, data={self})"


# ─── Tests ────────────────────────────────────────────────────────────────────


def _run_tests() -> None:
    """Run all tests for DynamicArray and report results."""
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
    arr = DynamicArray()

    check("empty array has size 0", arr.size() == 0)
    check("empty array is_empty()", arr.is_empty() is True)
    check("default capacity is 8", arr.capacity() == 8)

    # ── Append ─────────────────────────────────────────────────────────────────
    print("\nAppend operations:")
    for i in range(10):
        arr.append(i)
    check("size after 10 appends", arr.size() == 10)
    check("capacity doubled (>=16)", arr.capacity() >= 16)
    check("get(0) == 0", arr.get(0) == 0)
    check("get(9) == 9", arr.get(9) == 9)
    check("bracket access arr[5] == 5", arr[5] == 5)

    # ── Insert ─────────────────────────────────────────────────────────────────
    print("\nInsert operations:")
    arr.insert(0, 100)
    check("insert at beginning: arr[0] == 100", arr[0] == 100)
    check("size after insert", arr.size() == 11)

    mid = arr.size() // 2
    arr.insert(mid, 200)
    check("insert at middle", arr[mid] == 200)
    check("size after mid insert", arr.size() == 12)

    arr.insert(arr.size(), 300)
    check("insert at end (like append)", arr[arr.size() - 1] == 300)

    try:
        arr.insert(-1, 0)
        check("insert at negative index raises IndexError", False)
    except IndexError:
        check("insert at negative index raises IndexError", True)

    try:
        arr.insert(arr.size() + 1, 0)
        check("insert past end raises IndexError", False)
    except IndexError:
        check("insert past end raises IndexError", True)

    # ── Delete ─────────────────────────────────────────────────────────────────
    print("\nDelete operations:")
    removed = arr.delete(0)
    check("delete at 0 returns 100", removed == 100)
    check("arr[0] now 0", arr[0] == 0)
    check("size decreased", arr.size() == 12)

    removed = arr.delete(arr.size() - 1)
    check("delete last returns 300", removed == 300)
    check("size after last delete", arr.size() == 11)

    try:
        arr.delete(100)
        check("delete out of bounds raises IndexError", False)
    except IndexError:
        check("delete out of bounds raises IndexError", True)

    # ── Pop ────────────────────────────────────────────────────────────────────
    print("\nPop operations:")
    last = arr.pop()
    check("pop returns last element (9)", last == 9)
    check("size after pop", arr.size() == 10)

    try:
        empty_arr = DynamicArray()
        empty_arr.pop()
        check("pop on empty raises IndexError", False)
    except IndexError:
        check("pop on empty raises IndexError", True)

    # ── Set / index_of / contains ─────────────────────────────────────────────
    print("\nSearch/update operations:")
    arr.set(0, 999)
    check("set(0, 999)", arr[0] == 999)
    check("index_of(999) == 0", arr.index_of(999) == 0)
    check("index_of(9999) == -1 (not found)", arr.index_of(9999) == -1)
    check("contains(999)", arr.contains(999) is True)
    check("contains(9999)", arr.contains(9999) is False)

    # ── Shrink behavior ───────────────────────────────────────────────────────
    print("\nShrink behavior:")
    shrink_arr = DynamicArray(4)
    for i in range(100):
        shrink_arr.append(i)
    big_capacity = shrink_arr.capacity()
    check("capacity grew >= 128", big_capacity >= 128)

    for _ in range(95):
        shrink_arr.pop()
    check("size after popping 95", shrink_arr.size() == 5)
    check("capacity shrunk (load factor < 25%)", shrink_arr.capacity() < big_capacity)

    # ── Clear ──────────────────────────────────────────────────────────────────
    print("\nClear operations:")
    arr.clear()
    check("clear resets size to 0", arr.size() == 0)
    check("clear resets capacity to 8", arr.capacity() == 8)
    check("clear makes is_empty true", arr.is_empty() is True)

    # ── Iteration ──────────────────────────────────────────────────────────────
    print("\nIteration:")
    iter_arr = DynamicArray()
    for i in range(5):
        iter_arr.append(i * 10)
    values = list(iter_arr)
    check("iteration yields all elements", values == [0, 10, 20, 30, 40])
    check("len() works", len(iter_arr) == 5)

    # ── String representation ─────────────────────────────────────────────────
    print("\nString representation:")
    check("str() shows elements", "10" in str(iter_arr))
    check("repr() shows size and capacity", "size=5" in repr(iter_arr))

    # ── Negative tests ────────────────────────────────────────────────────────
    print("\nEdge cases:")
    try:
        DynamicArray(0)
        check("initial_capacity=0 raises ValueError", False)
    except ValueError:
        check("initial_capacity=0 raises ValueError", True)

    try:
        DynamicArray(-1)
        check("initial_capacity<0 raises ValueError", False)
    except ValueError:
        check("initial_capacity<0 raises ValueError", True)

    try:
        iter_arr.get(-1)
        check("negative index get raises IndexError", False)
    except IndexError:
        check("negative index get raises IndexError", True)

    try:
        iter_arr.get(iter_arr.size())
        check("index==size get raises IndexError", False)
    except IndexError:
        check("index==size get raises IndexError", True)

    # ── Summary ────────────────────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
