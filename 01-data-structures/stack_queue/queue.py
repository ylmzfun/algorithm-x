"""
Queue Implementations
======================

Three queue implementations: circular array queue, linked-list queue, and deque.

A queue is a FIFO (First-In, First-Out) data structure supporting:
- enqueue: add element to rear
- dequeue: remove and return front element
- peek/front: return front element without removing
- is_empty, size

ArrayQueue uses a circular buffer to achieve O(1) enqueue/dequeue.
LinkedQueue uses a linked list with head (front) and tail (rear) pointers.
Deque (double-ended queue) supports insert/remove from both ends.

Time Complexities (all implementations):
    - enqueue/push: O(1)
    - dequeue/pop: O(1)
    - peek: O(1)

Space Complexity: O(n)
"""

from typing import Any, Optional, Iterator


class ArrayQueue:
    """A queue implemented with a circular array (ring buffer).

    Uses a fixed-size array with front and rear pointers that wrap around.
    When full, resizes by doubling capacity.

    Examples:
        >>> q = ArrayQueue()
        >>> q.enqueue(1)
        >>> q.enqueue(2)
        >>> q.peek()
        1
        >>> q.dequeue()
        1
        >>> q.size()
        1
    """

    def __init__(self, initial_capacity: int = 8) -> None:
        """Initialize an empty circular queue.

        Args:
            initial_capacity: Initial size of the circular buffer (default 8).

        Raises:
            ValueError: If initial_capacity <= 0.
        """
        if initial_capacity <= 0:
            raise ValueError("initial_capacity must be positive")
        self._data: list[Optional[Any]] = [None] * initial_capacity
        self._front: int = 0  # Index of the front element
        self._rear: int = 0   # Index where the next element will be inserted
        self._size: int = 0
        self._capacity: int = initial_capacity

    def size(self) -> int:
        """Return number of elements.

        Returns:
            Count of elements.

        Time Complexity: O(1)
        """
        return self._size

    def is_empty(self) -> bool:
        """Check if queue is empty.

        Returns:
            True if no elements.

        Time Complexity: O(1)
        """
        return self._size == 0

    def is_full(self) -> bool:
        """Check if internal buffer is full.

        Returns:
            True if at capacity.

        Time Complexity: O(1)
        """
        return self._size == self._capacity

    def enqueue(self, item: Any) -> None:
        """Add `item` to the rear of the queue.

        Args:
            item: Element to add.

        Time Complexity: O(1) amortized (O(n) when resizing).
        """
        if self.is_full():
            self._resize(self._capacity * 2)
        self._data[self._rear] = item
        self._rear = (self._rear + 1) % self._capacity
        self._size += 1

    def dequeue(self) -> Any:
        """Remove and return the front element.

        Returns:
            The element at the front of the queue.

        Raises:
            IndexError: If queue is empty.

        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        item = self._data[self._front]
        self._data[self._front] = None  # Help garbage collection
        self._front = (self._front + 1) % self._capacity
        self._size -= 1

        # Shrink if load factor < 25%
        if self._size > 0 and self._size < self._capacity // 4:
            self._resize(max(8, self._capacity // 2))
        return item

    def peek(self) -> Any:
        """Return the front element without removing it.

        Returns:
            Front element.

        Raises:
            IndexError: If queue is empty.

        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self._data[self._front]

    def clear(self) -> None:
        """Remove all elements and reset to initial capacity.

        Time Complexity: O(capacity)
        """
        self._data = [None] * 8
        self._front = 0
        self._rear = 0
        self._size = 0
        self._capacity = 8

    def _resize(self, new_capacity: int) -> None:
        """Resize the circular buffer to `new_capacity`.

        Copies elements in order starting from front.

        Args:
            new_capacity: New buffer size (must be >= size).

        Time Complexity: O(n)
        """
        new_data: list[Optional[Any]] = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[(self._front + i) % self._capacity]
        self._data = new_data
        self._front = 0
        self._rear = self._size
        self._capacity = new_capacity

    def __iter__(self) -> Iterator[Any]:
        """Yield elements from front to rear."""
        for i in range(self._size):
            yield self._data[(self._front + i) % self._capacity]

    def __len__(self) -> int:
        """Support len()."""
        return self._size

    def __str__(self) -> str:
        """Return string representation."""
        return str(list(self))

    def __repr__(self) -> str:
        """Return detailed representation."""
        return f"ArrayQueue(size={self._size}, capacity={self._capacity}, data={list(self)})"


class LinkedQueue:
    """A queue implemented with a singly-linked list with tail pointer.

    Front of queue = head; rear = tail.

    Examples:
        >>> q = LinkedQueue()
        >>> q.enqueue(1)
        >>> q.enqueue(2)
        >>> q.peek()
        1
        >>> q.dequeue()
        1
        >>> q.size()
        1
    """

    class _Node:
        """Internal node for the linked list."""
        __slots__ = ("data", "next")

        def __init__(self, data: Any, next_node: Optional["LinkedQueue._Node"] = None) -> None:
            self.data = data
            self.next = next_node

    def __init__(self) -> None:
        """Initialize an empty linked queue."""
        self._front: Optional[LinkedQueue._Node] = None
        self._rear: Optional[LinkedQueue._Node] = None
        self._size: int = 0

    def size(self) -> int:
        """Return number of elements.

        Returns:
            Count of elements.

        Time Complexity: O(1)
        """
        return self._size

    def is_empty(self) -> bool:
        """Check if queue is empty.

        Returns:
            True if no elements.

        Time Complexity: O(1)
        """
        return self._front is None

    def enqueue(self, item: Any) -> None:
        """Add `item` to the rear of the queue.

        Args:
            item: Element to add.

        Time Complexity: O(1)
        """
        new_node = self._Node(item)
        if self._rear is None:
            self._front = self._rear = new_node
        else:
            self._rear.next = new_node
            self._rear = new_node
        self._size += 1

    def dequeue(self) -> Any:
        """Remove and return the front element.

        Returns:
            Front element.

        Raises:
            IndexError: If queue is empty.

        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        data = self._front.data
        self._front = self._front.next
        if self._front is None:
            self._rear = None
        self._size -= 1
        return data

    def peek(self) -> Any:
        """Return front element without removing.

        Returns:
            Front element.

        Raises:
            IndexError: If queue is empty.

        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self._front.data

    def clear(self) -> None:
        """Remove all elements.

        Time Complexity: O(1)
        """
        self._front = self._rear = None
        self._size = 0

    def __iter__(self) -> Iterator[Any]:
        """Yield elements from front to rear."""
        current = self._front
        while current is not None:
            yield current.data
            current = current.next

    def __len__(self) -> int:
        """Support len()."""
        return self._size

    def __str__(self) -> str:
        """Return string representation."""
        return " <- ".join(str(d) for d in self) if not self.is_empty() else "(empty)"

    def __repr__(self) -> str:
        """Return detailed representation."""
        return f"LinkedQueue(size={self._size}, data={list(self)})"


class Deque:
    """A double-ended queue (deque) implemented with a doubly-linked list.

    Supports O(1) insertion and removal from both ends.

    Examples:
        >>> dq = Deque()
        >>> dq.push_front(1)
        >>> dq.push_back(2)
        >>> dq.push_front(0)
        >>> dq.peek_front()
        0
        >>> dq.peek_back()
        2
        >>> dq.pop_front()
        0
        >>> dq.pop_back()
        2
        >>> dq.size()
        1
    """

    class _Node:
        """Internal node for the doubly-linked list."""
        __slots__ = ("data", "prev", "next")

        def __init__(self, data: Any) -> None:
            self.data = data
            self.prev: Optional["Deque._Node"] = None
            self.next: Optional["Deque._Node"] = None

    def __init__(self) -> None:
        """Initialize an empty deque."""
        self._front: Optional[Deque._Node] = None
        self._back: Optional[Deque._Node] = None
        self._size: int = 0

    def size(self) -> int:
        """Return number of elements.

        Returns:
            Count of elements.

        Time Complexity: O(1)
        """
        return self._size

    def is_empty(self) -> bool:
        """Check if empty.

        Returns:
            True if no elements.

        Time Complexity: O(1)
        """
        return self._size == 0

    def push_front(self, item: Any) -> None:
        """Add `item` to the front.

        Args:
            item: Element to add.

        Time Complexity: O(1)
        """
        new_node = self._Node(item)
        if self._front is None:
            self._front = self._back = new_node
        else:
            new_node.next = self._front
            self._front.prev = new_node
            self._front = new_node
        self._size += 1

    def push_back(self, item: Any) -> None:
        """Add `item` to the back.

        Args:
            item: Element to add.

        Time Complexity: O(1)
        """
        new_node = self._Node(item)
        if self._back is None:
            self._front = self._back = new_node
        else:
            new_node.prev = self._back
            self._back.next = new_node
            self._back = new_node
        self._size += 1

    def pop_front(self) -> Any:
        """Remove and return the front element.

        Returns:
            Front element.

        Raises:
            IndexError: If deque is empty.

        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("pop_front from empty deque")
        data = self._front.data
        self._front = self._front.next
        if self._front is None:
            self._back = None
        else:
            self._front.prev = None
        self._size -= 1
        return data

    def pop_back(self) -> Any:
        """Remove and return the back element.

        Returns:
            Back element.

        Raises:
            IndexError: If deque is empty.

        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("pop_back from empty deque")
        data = self._back.data
        self._back = self._back.prev
        if self._back is None:
            self._front = None
        else:
            self._back.next = None
        self._size -= 1
        return data

    def peek_front(self) -> Any:
        """Return front element without removing.

        Returns:
            Front element.

        Raises:
            IndexError: If deque is empty.

        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("peek_front from empty deque")
        return self._front.data

    def peek_back(self) -> Any:
        """Return back element without removing.

        Returns:
            Back element.

        Raises:
            IndexError: If deque is empty.

        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("peek_back from empty deque")
        return self._back.data

    def clear(self) -> None:
        """Remove all elements.

        Time Complexity: O(1)
        """
        self._front = self._back = None
        self._size = 0

    def __iter__(self) -> Iterator[Any]:
        """Yield elements from front to back."""
        current = self._front
        while current is not None:
            yield current.data
            current = current.next

    def __len__(self) -> int:
        """Support len()."""
        return self._size

    def __str__(self) -> str:
        """Return string representation."""
        return str(list(self))

    def __repr__(self) -> str:
        """Return detailed representation."""
        return f"Deque(size={self._size}, data={list(self)})"


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

    # ── ArrayQueue ────────────────────────────────────────────────────────────
    print("ArrayQueue:")
    aq = ArrayQueue(4)
    check("initial size == 0", aq.size() == 0)
    check("is_empty", aq.is_empty())

    for i in range(5):
        aq.enqueue(i)
    check("size after 5 enqueues", aq.size() == 5)
    check("capacity grew >= 8", aq._capacity >= 8)
    check("peek == 0", aq.peek() == 0)
    check("dequeue == 0", aq.dequeue() == 0)
    check("dequeue == 1", aq.dequeue() == 1)
    check("size after 2 dequeues", aq.size() == 3)
    check("peek now 2", aq.peek() == 2)

    try:
        ArrayQueue(0)
        check("capacity 0 raises", False)
    except ValueError:
        check("capacity 0 raises", True)

    try:
        empty = ArrayQueue()
        empty.dequeue()
        check("dequeue empty raises", False)
    except IndexError:
        check("dequeue empty raises", True)

    # Test wrap-around
    wrap = ArrayQueue(4)
    wrap.enqueue(1)
    wrap.enqueue(2)
    wrap.dequeue()
    wrap.enqueue(3)
    wrap.enqueue(4)
    wrap.enqueue(5)
    check("wrap-around iteration", list(wrap) == [2, 3, 4, 5])

    wrap.clear()
    check("clear makes empty", wrap.is_empty())

    # ── LinkedQueue ───────────────────────────────────────────────────────────
    print("\nLinkedQueue:")
    lq = LinkedQueue()
    check("initial is_empty", lq.is_empty())

    lq.enqueue(10)
    lq.enqueue(20)
    lq.enqueue(30)
    check("size after 3 enqueues", lq.size() == 3)
    check("peek == 10", lq.peek() == 10)
    check("dequeue == 10", lq.dequeue() == 10)
    check("dequeue == 20", lq.dequeue() == 20)
    check("dequeue == 30", lq.dequeue() == 30)
    check("empty after all", lq.is_empty())

    try:
        lq.dequeue()
        check("dequeue empty raises", False)
    except IndexError:
        check("dequeue empty raises", True)

    lq.enqueue(1)
    lq.enqueue(2)
    lq.clear()
    check("clear makes empty", lq.is_empty())

    # Iteration
    for x in [1, 2, 3]:
        lq.enqueue(x)
    check("iteration", list(lq) == [1, 2, 3])

    # ── Deque ─────────────────────────────────────────────────────────────────
    print("\nDeque:")
    dq = Deque()
    check("initial is_empty", dq.is_empty())

    dq.push_front(2)
    dq.push_front(1)
    dq.push_back(3)
    dq.push_back(4)
    check("size == 4", dq.size() == 4)
    check("peek_front == 1", dq.peek_front() == 1)
    check("peek_back == 4", dq.peek_back() == 4)
    check("iteration", list(dq) == [1, 2, 3, 4])

    check("pop_front == 1", dq.pop_front() == 1)
    check("pop_back == 4", dq.pop_back() == 4)
    check("after pops", list(dq) == [2, 3])
    check("pop_front == 2", dq.pop_front() == 2)
    check("pop_back == 3", dq.pop_back() == 3)
    check("empty after all", dq.is_empty())

    try:
        dq.pop_front()
        check("pop_front empty raises", False)
    except IndexError:
        check("pop_front empty raises", True)

    try:
        dq.peek_front()
        check("peek_front empty raises", False)
    except IndexError:
        check("peek_front empty raises", True)

    # Mixed operations
    dq.push_back(1)
    dq.push_front(0)
    dq.push_back(2)
    check("mixed push order", list(dq) == [0, 1, 2])

    # ── Summary ───────────────────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
