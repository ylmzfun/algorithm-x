"""
Doubly Linked List Implementation
==================================

A doubly-linked list where each node has both `next` and `prev` pointers.
This enables O(1) deletion given a node reference and efficient bidirectional
traversal.

Time Complexities:
    - Access by index: O(n)
    - Insert at head/tail: O(1)
    - Insert at index: O(n) (traversal) + O(1) (pointer updates)
    - Delete at head/tail: O(1)
    - Delete at index: O(n)
    - Search: O(n)
    - Reverse: O(n) — swap all prev/next pointers

Space Complexity: O(n) for n nodes (2 pointers per node vs. 1 for singly)
"""

from typing import Any, Optional, Iterator


class DoublyNode:
    """A node in a doubly-linked list with prev and next pointers.

    Attributes:
        data: The value stored in this node.
        prev: Reference to the previous node (None if head).
        next: Reference to the next node (None if tail).
    """

    def __init__(self, data: Any) -> None:
        """Initialize node with given data.

        Args:
            data: Value to store in this node.
        """
        self.data: Any = data
        self.prev: Optional["DoublyNode"] = None
        self.next: Optional["DoublyNode"] = None

    def __repr__(self) -> str:
        """Return string representation."""
        return f"DoublyNode({self.data!r})"


class DoublyLinkedList:
    """A doubly-linked list with head and tail sentinel-free pointers.

    Supports efficient insertions/deletions at both ends.

    Examples:
        >>> dll = DoublyLinkedList()
        >>> dll.append(1)
        >>> dll.append(2)
        >>> dll.prepend(0)
        >>> list(dll)
        [0, 1, 2]
        >>> dll.size()
        3
    """

    def __init__(self) -> None:
        """Initialize an empty doubly-linked list."""
        self._head: Optional[DoublyNode] = None
        self._tail: Optional[DoublyNode] = None
        self._size: int = 0

    def size(self) -> int:
        """Return the number of nodes.

        Returns:
            Count of nodes.

        Time Complexity: O(1)
        """
        return self._size

    def is_empty(self) -> bool:
        """Check if the list is empty.

        Returns:
            True if no nodes.

        Time Complexity: O(1)
        """
        return self._size == 0

    def head(self) -> Optional[DoublyNode]:
        """Return the head node.

        Returns:
            Head DoublyNode or None.

        Time Complexity: O(1)
        """
        return self._head

    def tail(self) -> Optional[DoublyNode]:
        """Return the tail node.

        Returns:
            Tail DoublyNode or None.

        Time Complexity: O(1)
        """
        return self._tail

    # ── Insertion ─────────────────────────────────────────────────────────────

    def prepend(self, data: Any) -> None:
        """Insert a new node at the head.

        Args:
            data: Value to store.

        Time Complexity: O(1)
        """
        new_node = DoublyNode(data)
        if self._head is None:
            self._head = self._tail = new_node
        else:
            new_node.next = self._head
            self._head.prev = new_node
            self._head = new_node
        self._size += 1

    def append(self, data: Any) -> None:
        """Insert a new node at the tail.

        Args:
            data: Value to store.

        Time Complexity: O(1)
        """
        new_node = DoublyNode(data)
        if self._tail is None:
            self._head = self._tail = new_node
        else:
            new_node.prev = self._tail
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1

    def insert_at(self, index: int, data: Any) -> None:
        """Insert a new node at the given 0-based index.

        Args:
            index: Position to insert (0 = head, size = tail).
            data: Value to store.

        Raises:
            IndexError: If index is out of bounds.

        Time Complexity: O(n) — traverses to index, O(1) pointer updates.
        """
        if not 0 <= index <= self._size:
            raise IndexError(f"Index {index} out of bounds for size {self._size}")

        if index == 0:
            self.prepend(data)
            return
        if index == self._size:
            self.append(data)
            return

        # Optimize: traverse from nearer end
        if index <= self._size // 2:
            current = self._head
            for _ in range(index):
                current = current.next  # type: ignore[union-attr]
        else:
            current = self._tail
            for _ in range(self._size - index):
                current = current.prev  # type: ignore[union-attr]

        new_node = DoublyNode(data)
        new_node.prev = current.prev  # type: ignore[union-attr]
        new_node.next = current
        current.prev.next = new_node  # type: ignore[union-attr]
        current.prev = new_node  # type: ignore[union-attr]
        self._size += 1

    # ── Deletion ──────────────────────────────────────────────────────────────

    def delete_at(self, index: int) -> Any:
        """Remove and return data at the given index.

        Args:
            index: 0-based position of node to remove.

        Returns:
            The data from the removed node.

        Raises:
            IndexError: If index out of bounds.

        Time Complexity: O(n) — traverses to index, O(1) pointer updates.
        """
        if not 0 <= index < self._size:
            raise IndexError(f"Index {index} out of bounds for size {self._size}")

        if index == 0:
            removed = self._head.data
            self._head = self._head.next
            if self._head is not None:
                self._head.prev = None
            else:
                self._tail = None
            self._size -= 1
            return removed

        if index == self._size - 1:
            removed = self._tail.data
            self._tail = self._tail.prev
            if self._tail is not None:
                self._tail.next = None
            else:
                self._head = None
            self._size -= 1
            return removed

        # Traverse from nearer end
        if index <= self._size // 2:
            current = self._head
            for _ in range(index):
                current = current.next  # type: ignore[union-attr]
        else:
            current = self._tail
            for _ in range(self._size - 1 - index):
                current = current.prev  # type: ignore[union-attr]

        removed = current.data  # type: ignore[union-attr]
        current.prev.next = current.next  # type: ignore[union-attr]
        current.next.prev = current.prev  # type: ignore[union-attr]
        self._size -= 1
        return removed  # type: ignore[return-value]

    def pop_front(self) -> Any:
        """Remove and return head data.

        Returns:
            Data from head node.

        Raises:
            IndexError: If empty.

        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("pop from empty list")
        return self.delete_at(0)

    def pop_back(self) -> Any:
        """Remove and return tail data.

        Returns:
            Data from tail node.

        Raises:
            IndexError: If empty.

        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("pop from empty list")
        return self.delete_at(self._size - 1)

    # ── Access / Search ───────────────────────────────────────────────────────

    def get(self, index: int) -> Any:
        """Return data at the given index.

        Args:
            index: 0-based position.

        Returns:
            Data stored at that index.

        Raises:
            IndexError: If out of bounds.

        Time Complexity: O(n)
        """
        return self._get_node_at(index).data

    def find(self, data: Any) -> int:
        """Return index of first node with `data`, or -1.

        Args:
            data: Value to search for.

        Returns:
            0-based index or -1 if not found.

        Time Complexity: O(n)
        """
        current = self._head
        index = 0
        while current is not None:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return -1

    def contains(self, data: Any) -> bool:
        """Check if data exists in list.

        Args:
            data: Value to search for.

        Returns:
            True if found.

        Time Complexity: O(n)
        """
        return self.find(data) != -1

    # ── Reverse ───────────────────────────────────────────────────────────────

    def reverse(self) -> None:
        """Reverse the list in-place by swapping prev/next of each node.

        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        current = self._head
        self._tail = self._head

        while current is not None:
            # Swap prev and next
            current.prev, current.next = current.next, current.prev
            # Move to the "next" node (which is now prev)
            self._head = current  # Keep track of new head
            current = current.prev  # prev was the old next

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _get_node_at(self, index: int) -> DoublyNode:
        """Return node at given index, traversing from nearer end.

        Args:
            index: 0-based position.

        Returns:
            The DoublyNode at that index.

        Raises:
            IndexError: If out of bounds.

        Time Complexity: O(n)
        """
        if not 0 <= index < self._size:
            raise IndexError(f"Index {index} out of bounds for size {self._size}")

        if index <= self._size // 2:
            current = self._head
            for _ in range(index):
                current = current.next  # type: ignore[union-attr]
        else:
            current = self._tail
            for _ in range(self._size - 1 - index):
                current = current.prev  # type: ignore[union-attr]
        return current  # type: ignore[return-value]

    def to_list(self) -> list[Any]:
        """Convert to Python list.

        Returns:
            List of all values in order.

        Time Complexity: O(n)
        """
        result: list[Any] = []
        current = self._head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def to_list_reverse(self) -> list[Any]:
        """Convert to Python list in reverse order.

        Returns:
            List of all values from tail to head.

        Time Complexity: O(n)
        """
        result: list[Any] = []
        current = self._tail
        while current is not None:
            result.append(current.data)
            current = current.prev
        return result

    # ── Dunder Methods ────────────────────────────────────────────────────────

    def __iter__(self) -> Iterator[Any]:
        """Yield data forward."""
        current = self._head
        while current is not None:
            yield current.data
            current = current.next

    def __reversed__(self) -> Iterator[Any]:
        """Yield data backward."""
        current = self._tail
        while current is not None:
            yield current.data
            current = current.prev

    def __len__(self) -> int:
        """Support len()."""
        return self._size

    def __getitem__(self, index: int) -> Any:
        """Support bracket indexing: dll[i]."""
        return self.get(index)

    def __str__(self) -> str:
        """Return string like '1 <-> 2 <-> 3'."""
        parts = [str(d) for d in self]
        return " <-> ".join(parts) if parts else "(empty)"

    def __repr__(self) -> str:
        """Return detailed representation."""
        return f"DoublyLinkedList(size={self._size}, data={self.to_list()})"


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
    dll = DoublyLinkedList()
    check("empty size", dll.size() == 0)
    check("empty is_empty", dll.is_empty() is True)
    check("empty head None", dll.head() is None)
    check("empty tail None", dll.tail() is None)

    # ── Append / Prepend ──────────────────────────────────────────────────────
    print("\nInsertion:")
    dll.append(10)
    dll.append(20)
    dll.prepend(5)
    dll.append(30)
    check("size after 4 inserts", dll.size() == 4)
    check("to_list forward", dll.to_list() == [5, 10, 20, 30])
    check("head == 5", dll.head().data == 5)
    check("tail == 30", dll.tail().data == 30)

    # Insert at middle
    dll.insert_at(2, 15)
    check("insert_at(2, 15)", dll.to_list() == [5, 10, 15, 20, 30])
    check("size after insert", dll.size() == 5)

    dll.insert_at(0, 0)
    check("insert_at head", dll.to_list() == [0, 5, 10, 15, 20, 30])

    dll.insert_at(dll.size(), 35)
    check("insert_at tail", dll.to_list() == [0, 5, 10, 15, 20, 30, 35])

    try:
        dll.insert_at(100, 0)
        check("insert_at oob", False)
    except IndexError:
        check("insert_at oob", True)

    # ── Get / Find ────────────────────────────────────────────────────────────
    print("\nAccess:")
    check("get(0) == 0", dll.get(0) == 0)
    check("get(3) == 15", dll.get(3) == 15)
    check("get(last) == 35", dll.get(dll.size() - 1) == 35)
    check("bracket dll[1] == 5", dll[1] == 5)
    check("find(15) == 3", dll.find(15) == 3)
    check("find(999) == -1", dll.find(999) == -1)
    check("contains(20)", dll.contains(20) is True)
    check("contains(999)", dll.contains(999) is False)

    try:
        dll.get(-1)
        check("get negative", False)
    except IndexError:
        check("get negative", True)

    # ── Delete ────────────────────────────────────────────────────────────────
    print("\nDeletion:")
    removed = dll.delete_at(3)  # Remove 15
    check("delete_at(3) == 15", removed == 15)
    check("after delete list", dll.to_list() == [0, 5, 10, 20, 30, 35])
    check("size after delete", dll.size() == 6)

    dll.delete_at(0)
    check("delete head", dll.to_list() == [5, 10, 20, 30, 35])

    dll.delete_at(dll.size() - 1)
    check("delete tail", dll.to_list() == [5, 10, 20, 30])

    try:
        dll.delete_at(100)
        check("delete_at oob", False)
    except IndexError:
        check("delete_at oob", True)

    # ── Pop ───────────────────────────────────────────────────────────────────
    print("\nPop:")
    pop_dll = DoublyLinkedList()
    pop_dll.append(1)
    pop_dll.append(2)
    check("pop_front == 1", pop_dll.pop_front() == 1)
    check("pop_back == 2", pop_dll.pop_back() == 2)
    check("empty after pops", pop_dll.is_empty())

    try:
        pop_dll.pop_front()
        check("pop on empty", False)
    except IndexError:
        check("pop on empty", True)

    # ── Reverse ───────────────────────────────────────────────────────────────
    print("\nReverse:")
    rev = DoublyLinkedList()
    for x in [1, 2, 3, 4, 5]:
        rev.append(x)
    rev.reverse()
    check("reversed forward", rev.to_list() == [5, 4, 3, 2, 1])
    check("reversed backward", rev.to_list_reverse() == [1, 2, 3, 4, 5])
    check("head == 5", rev.head().data == 5)
    check("tail == 1", rev.tail().data == 1)

    # Reverse empty
    empty_dll = DoublyLinkedList()
    empty_dll.reverse()
    check("reverse empty (no error)", empty_dll.is_empty())

    # ── Bidirectional traversal ───────────────────────────────────────────────
    print("\nBidirectional:")
    bi = DoublyLinkedList()
    for x in [1, 2, 3]:
        bi.append(x)
    forward = list(bi)
    backward = list(reversed(bi))
    check("forward iteration", forward == [1, 2, 3])
    check("backward iteration", backward == [3, 2, 1])
    check("prev from tail", bi.tail().prev.data == 2)
    check("next from head", bi.head().next.data == 2)

    # ── Iteration / String ────────────────────────────────────────────────────
    print("\nString/Iteration:")
    dll_str = DoublyLinkedList()
    for x in [10, 20, 30]:
        dll_str.append(x)
    check("list from iter", list(dll_str) == [10, 20, 30])
    check("str representation", "10 <-> 20 <-> 30" in str(dll_str))

    # ── Summary ───────────────────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
