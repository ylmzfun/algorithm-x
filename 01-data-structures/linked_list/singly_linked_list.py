"""
Singly Linked List Implementation
==================================

A singly-linked list where each node points to the next node. Supports
common operations including insertion, deletion, reversal, cycle detection,
and merging.

Time Complexities:
    - Access by index: O(n)
    - Insert at head: O(1)
    - Insert at tail: O(1) with tail pointer
    - Insert at index: O(n)
    - Delete at index: O(n)
    - Search: O(n)
    - Reverse: O(n)
    - Cycle detection: O(n)
    - Find middle: O(n)

Space Complexity: O(n) for n nodes
"""

from typing import Any, Optional, Iterator


class Node:
    """A single node in a singly-linked list.

    Attributes:
        data: The value stored in this node.
        next: Reference to the next node (None if tail).
    """

    def __init__(self, data: Any) -> None:
        """Initialize node with given data.

        Args:
            data: Value to store in this node.
        """
        self.data: Any = data
        self.next: Optional["Node"] = None

    def __repr__(self) -> str:
        """Return string representation of the node."""
        return f"Node({self.data!r})"


class SinglyLinkedList:
    """A singly-linked list with head and tail pointers.

    Supports efficient head and tail insertions, index-based operations,
    and standard linked list algorithms.

    Examples:
        >>> ll = SinglyLinkedList()
        >>> ll.append(1)
        >>> ll.append(2)
        >>> ll.prepend(0)
        >>> list(ll)
        [0, 1, 2]
        >>> ll.size()
        3
    """

    def __init__(self) -> None:
        """Initialize an empty singly-linked list."""
        self._head: Optional[Node] = None
        self._tail: Optional[Node] = None
        self._size: int = 0

    def size(self) -> int:
        """Return the number of nodes.

        Returns:
            Count of nodes in the list.

        Time Complexity: O(1)
        """
        return self._size

    def is_empty(self) -> bool:
        """Check if the list is empty.

        Returns:
            True if no nodes, False otherwise.

        Time Complexity: O(1)
        """
        return self._size == 0

    def head(self) -> Optional[Node]:
        """Return the head node (without removing it).

        Returns:
            The head Node, or None if empty.

        Time Complexity: O(1)
        """
        return self._head

    def tail(self) -> Optional[Node]:
        """Return the tail node.

        Returns:
            The tail Node, or None if empty.

        Time Complexity: O(1)
        """
        return self._tail

    # ── Insertion ─────────────────────────────────────────────────────────────

    def prepend(self, data: Any) -> None:
        """Insert a new node with `data` at the head of the list.

        Args:
            data: Value to store.

        Time Complexity: O(1)
        """
        new_node = Node(data)
        new_node.next = self._head
        self._head = new_node
        if self._tail is None:
            self._tail = new_node
        self._size += 1

    def append(self, data: Any) -> None:
        """Insert a new node with `data` at the tail of the list.

        Args:
            data: Value to store.

        Time Complexity: O(1) — uses tail pointer.
        """
        new_node = Node(data)
        if self._tail is None:
            self._head = self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1

    def insert_at(self, index: int, data: Any) -> None:
        """Insert a new node at the specified 0-based index.

        Args:
            index: Position to insert (0 = head, size = tail/append).
            data: Value to store.

        Raises:
            IndexError: If index is out of bounds.

        Time Complexity: O(n) — traverses to index.
        """
        if not 0 <= index <= self._size:
            raise IndexError(f"Index {index} out of bounds for size {self._size}")

        if index == 0:
            self.prepend(data)
            return
        if index == self._size:
            self.append(data)
            return

        new_node = Node(data)
        prev = self._get_node_at(index - 1)
        new_node.next = prev.next
        prev.next = new_node
        self._size += 1

    # ── Deletion ──────────────────────────────────────────────────────────────

    def delete_at(self, index: int) -> Any:
        """Remove and return the node's data at the given index.

        Args:
            index: Position of the node to remove (0-based).

        Returns:
            The data that was stored in the removed node.

        Raises:
            IndexError: If index is out of bounds.

        Time Complexity: O(n) — traverses to index.
        """
        if not 0 <= index < self._size:
            raise IndexError(f"Index {index} out of bounds for size {self._size}")

        if index == 0:
            removed = self._head.data
            self._head = self._head.next
            if self._head is None:
                self._tail = None
            self._size -= 1
            return removed

        prev = self._get_node_at(index - 1)
        removed = prev.next.data
        prev.next = prev.next.next
        if prev.next is None:
            self._tail = prev
        self._size -= 1
        return removed

    def pop_front(self) -> Any:
        """Remove and return the head node's data.

        Returns:
            Data from the head node.

        Raises:
            IndexError: If the list is empty.

        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("pop from empty list")
        return self.delete_at(0)

    def pop_back(self) -> Any:
        """Remove and return the tail node's data.

        Returns:
            Data from the tail node.

        Raises:
            IndexError: If the list is empty.

        Time Complexity: O(n) — must find second-to-last node.
        """
        if self.is_empty():
            raise IndexError("pop from empty list")
        return self.delete_at(self._size - 1)

    # ── Access / Search ───────────────────────────────────────────────────────

    def get(self, index: int) -> Any:
        """Return the data at the given index.

        Args:
            index: 0-based position.

        Returns:
            The data stored at that index.

        Raises:
            IndexError: If index is out of bounds.

        Time Complexity: O(n)
        """
        return self._get_node_at(index).data

    def find(self, data: Any) -> int:
        """Return the index of the first node containing `data`.

        Args:
            data: Value to search for.

        Returns:
            The 0-based index of the first match, or -1 if not found.

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
        """Check if `data` exists in the list.

        Args:
            data: Value to search for.

        Returns:
            True if found, False otherwise.

        Time Complexity: O(n)
        """
        return self.find(data) != -1

    # ── Reverse ───────────────────────────────────────────────────────────────

    def reverse(self) -> None:
        """Reverse the list in-place (iterative).

        Swaps head and tail, then reverses all next pointers.

        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        prev: Optional[Node] = None
        current = self._head
        self._tail = self._head  # Old head becomes new tail

        while current is not None:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node

        self._head = prev

    def reverse_recursive(self) -> None:
        """Reverse the list in-place (recursive).

        Time Complexity: O(n)
        Space Complexity: O(n) — recursion stack.
        """
        if self._head is None:
            return

        self._tail = self._head

        def _reverse(node: Node) -> Node:
            """Recursively reverse from `node` onward. Returns new head."""
            if node.next is None:
                return node
            new_head = _reverse(node.next)
            node.next.next = node
            node.next = None
            return new_head

        self._head = _reverse(self._head)

    # ── Algorithms ────────────────────────────────────────────────────────────

    def detect_cycle(self) -> Optional[Node]:
        """Detect if the list has a cycle using Floyd's tortoise-and-hare.

        Returns:
            The node where the cycle begins, or None if acyclic.

        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        if self._head is None:
            return None

        slow = self._head
        fast = self._head

        # Phase 1: Detect if cycle exists
        while fast is not None and fast.next is not None:
            slow = slow.next  # type: ignore[assignment]
            fast = fast.next.next
            if slow == fast:
                break
        else:
            return None  # No cycle

        # Phase 2: Find cycle start
        slow = self._head
        while slow != fast:
            slow = slow.next  # type: ignore[assignment]
            fast = fast.next  # type: ignore[union-attr]

        return slow

    def has_cycle(self) -> bool:
        """Check if the list contains a cycle.

        Returns:
            True if a cycle exists.

        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        return self.detect_cycle() is not None

    def find_middle(self) -> Optional[Node]:
        """Return the middle node using slow-fast pointer technique.

        If even number of nodes, returns the second middle node.

        Returns:
            The middle Node, or None if empty.

        Time Complexity: O(n)
        Space Complexity: O(1)

        Examples:
            >>> ll = SinglyLinkedList()
            >>> for x in [1, 2, 3, 4, 5]: ll.append(x)
            >>> ll.find_middle().data
            3
        """
        if self._head is None:
            return None

        slow = self._head
        fast = self._head

        while fast is not None and fast.next is not None:
            slow = slow.next  # type: ignore[assignment]
            fast = fast.next.next

        return slow

    @staticmethod
    def merge_sorted(l1: "SinglyLinkedList", l2: "SinglyLinkedList") -> "SinglyLinkedList":
        """Merge two sorted linked lists into one sorted list (in-place).

        Args:
            l1: First sorted singly-linked list.
            l2: Second sorted singly-linked list.

        Returns:
            A new sorted SinglyLinkedList containing all nodes from l1 and l2.
            Note: l1 and l2 are modified (nodes are reused).

        Time Complexity: O(n + m) where n, m are sizes of l1, l2.
        Space Complexity: O(1) — in-place merging.

        Examples:
            >>> l1 = SinglyLinkedList()
            >>> for x in [1, 3, 5]: l1.append(x)
            >>> l2 = SinglyLinkedList()
            >>> for x in [2, 4, 6]: l2.append(x)
            >>> merged = SinglyLinkedList.merge_sorted(l1, l2)
            >>> list(merged)
            [1, 2, 3, 4, 5, 6]
        """
        result = SinglyLinkedList()
        dummy = Node(0)  # Dummy head
        current = dummy

        p1 = l1._head
        p2 = l2._head

        while p1 is not None and p2 is not None:
            if p1.data <= p2.data:
                current.next = p1
                p1 = p1.next
            else:
                current.next = p2
                p2 = p2.next
            current = current.next

        # Attach remaining nodes
        if p1 is not None:
            current.next = p1
        if p2 is not None:
            current.next = p2

        result._head = dummy.next
        # Compute tail and size
        node = result._head
        count = 0
        last = None
        while node is not None:
            count += 1
            last = node
            node = node.next
        result._tail = last
        result._size = count

        return result

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _get_node_at(self, index: int) -> Node:
        """Return the node at the given index.

        Args:
            index: 0-based position.

        Returns:
            The Node at that index.

        Raises:
            IndexError: If index is out of bounds.

        Time Complexity: O(n)
        """
        if not 0 <= index < self._size:
            raise IndexError(f"Index {index} out of bounds for size {self._size}")

        current = self._head
        for _ in range(index):
            current = current.next  # type: ignore[union-attr]
        return current  # type: ignore[return-value]

    def to_list(self) -> list[Any]:
        """Convert the linked list to a Python list.

        Returns:
            A list of all node data values in order.

        Time Complexity: O(n)
        """
        result: list[Any] = []
        current = self._head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    # ── Dunder Methods ────────────────────────────────────────────────────────

    def __iter__(self) -> Iterator[Any]:
        """Yield data from each node in order."""
        current = self._head
        while current is not None:
            yield current.data
            current = current.next

    def __len__(self) -> int:
        """Support len()."""
        return self._size

    def __getitem__(self, index: int) -> Any:
        """Support bracket indexing: ll[i]."""
        return self.get(index)

    def __str__(self) -> str:
        """Return string like '1 -> 2 -> 3'."""
        parts = [str(d) for d in self]
        return " -> ".join(parts) if parts else "(empty)"

    def __repr__(self) -> str:
        """Return detailed representation."""
        return f"SinglyLinkedList(size={self._size}, data={self.to_list()})"


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
    ll = SinglyLinkedList()
    check("empty size", ll.size() == 0)
    check("empty is_empty", ll.is_empty() is True)
    check("empty head is None", ll.head() is None)
    check("empty tail is None", ll.tail() is None)

    # ── Append / Prepend ──────────────────────────────────────────────────────
    print("\nInsertion:")
    ll.append(10)
    ll.append(20)
    ll.append(30)
    check("size after 3 appends", ll.size() == 3)
    check("head == 10", ll.head().data == 10)
    check("tail == 30", ll.tail().data == 30)

    ll.prepend(0)
    check("head after prepend == 0", ll.head().data == 0)
    check("size after prepend", ll.size() == 4)

    ll.insert_at(2, 15)
    check("insert_at(2,15)", ll.get(2) == 15)
    check("size after insert", ll.size() == 5)
    check("to_list", ll.to_list() == [0, 10, 15, 20, 30])

    try:
        ll.insert_at(100, 0)
        check("insert_at out of bounds", False)
    except IndexError:
        check("insert_at out of bounds", True)

    # ── Get / Find ────────────────────────────────────────────────────────────
    print("\nAccess:")
    check("get(0) == 0", ll.get(0) == 0)
    check("get(4) == 30", ll.get(4) == 30)
    check("bracket access ll[1] == 10", ll[1] == 10)
    check("find(15) == 2", ll.find(15) == 2)
    check("find(999) == -1", ll.find(999) == -1)
    check("contains(20)", ll.contains(20) is True)
    check("contains(999)", ll.contains(999) is False)

    try:
        ll.get(100)
        check("get out of bounds", False)
    except IndexError:
        check("get out of bounds", True)

    # ── Delete ────────────────────────────────────────────────────────────────
    print("\nDeletion:")
    removed = ll.delete_at(2)
    check("delete_at(2) == 15", removed == 15)
    check("size after delete", ll.size() == 4)
    check("after delete list", ll.to_list() == [0, 10, 20, 30])

    ll.delete_at(0)
    check("delete head", ll.to_list() == [10, 20, 30])
    check("new head == 10", ll.head().data == 10)

    ll.delete_at(ll.size() - 1)
    check("delete tail", ll.to_list() == [10, 20])
    check("new tail == 20", ll.tail().data == 20)

    try:
        ll.delete_at(100)
        check("delete_at out of bounds", False)
    except IndexError:
        check("delete_at out of bounds", True)

    # ── Pop ───────────────────────────────────────────────────────────────────
    print("\nPop:")
    pop_ll = SinglyLinkedList()
    pop_ll.append(1)
    pop_ll.append(2)
    check("pop_front == 1", pop_ll.pop_front() == 1)
    check("pop_back == 2", pop_ll.pop_back() == 2)
    check("empty after pops", pop_ll.is_empty())

    try:
        pop_ll.pop_front()
        check("pop on empty", False)
    except IndexError:
        check("pop on empty", True)

    # ── Iterative Reverse ─────────────────────────────────────────────────────
    print("\nIterative Reverse:")
    rev_ll = SinglyLinkedList()
    for x in [1, 2, 3, 4, 5]:
        rev_ll.append(x)
    rev_ll.reverse()
    check("reversed list", rev_ll.to_list() == [5, 4, 3, 2, 1])
    check("head == 5", rev_ll.head().data == 5)
    check("tail == 1", rev_ll.tail().data == 1)

    # Single element reverse
    single = SinglyLinkedList()
    single.append(42)
    single.reverse()
    check("single element reverse", single.to_list() == [42])

    # Empty reverse
    empty_ll = SinglyLinkedList()
    empty_ll.reverse()
    check("empty reverse (no error)", empty_ll.is_empty())

    # ── Recursive Reverse ─────────────────────────────────────────────────────
    print("\nRecursive Reverse:")
    rev2 = SinglyLinkedList()
    for x in [1, 2, 3]:
        rev2.append(x)
    rev2.reverse_recursive()
    check("recursive reverse", rev2.to_list() == [3, 2, 1])

    # ── Find Middle ───────────────────────────────────────────────────────────
    print("\nFind Middle:")
    odd_ll = SinglyLinkedList()
    for x in [1, 2, 3, 4, 5]:
        odd_ll.append(x)
    check("odd length middle", odd_ll.find_middle().data == 3)

    even_ll = SinglyLinkedList()
    for x in [1, 2, 3, 4]:
        even_ll.append(x)
    check("even length middle (2nd)", even_ll.find_middle().data == 3)

    single_mid = SinglyLinkedList()
    single_mid.append(99)
    check("single element middle", single_mid.find_middle().data == 99)

    check("empty middle None", SinglyLinkedList().find_middle() is None)

    # ── Cycle Detection ───────────────────────────────────────────────────────
    print("\nCycle Detection:")
    cycle_ll = SinglyLinkedList()
    for x in [1, 2, 3, 4]:
        cycle_ll.append(x)
    check("no cycle", cycle_ll.has_cycle() is False)

    # Create a cycle: 4 -> 2
    cycle_ll.tail().next = cycle_ll.head().next
    check("has cycle", cycle_ll.has_cycle() is True)
    cycle_node = cycle_ll.detect_cycle()
    check("cycle start == 2", cycle_node is not None and cycle_node.data == 2)

    # ── Merge Two Sorted ──────────────────────────────────────────────────────
    print("\nMerge Sorted:")
    l1 = SinglyLinkedList()
    for x in [1, 3, 5]:
        l1.append(x)
    l2 = SinglyLinkedList()
    for x in [2, 4, 6]:
        l2.append(x)
    merged = SinglyLinkedList.merge_sorted(l1, l2)
    check("merge sorted", merged.to_list() == [1, 2, 3, 4, 5, 6])
    check("merge size", merged.size() == 6)
    check("merge tail", merged.tail().data == 6)

    # Merge with empty
    empty = SinglyLinkedList()
    merged2 = SinglyLinkedList.merge_sorted(empty, empty)
    check("merge two empties", merged2.is_empty())

    # ── Iteration ─────────────────────────────────────────────────────────────
    print("\nIteration:")
    iter_ll = SinglyLinkedList()
    for x in [10, 20, 30]:
        iter_ll.append(x)
    check("list from iterator", list(iter_ll) == [10, 20, 30])
    check("str representation", str(iter_ll) == "10 -> 20 -> 30")

    # ── Summary ───────────────────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
