"""
Stack Implementations
======================

Two stack implementations: array-based and linked-list-based.

A stack is a LIFO (Last-In, First-Out) data structure supporting:
- push: add element to top
- pop: remove and return top element
- peek: return top element without removing
- is_empty: check if empty
- size: number of elements

Time Complexities (both implementations):
    - push: O(1)
    - pop: O(1)
    - peek: O(1)
    - is_empty: O(1)
    - size: O(1)

Space Complexity: O(n) where n is the number of elements.
"""

from typing import Any, Optional, Iterator


class ArrayStack:
    """A stack implemented using a dynamic array (Python list).

    Simple, cache-friendly, and efficient. Python's list already supports
    amortized O(1) append/pop from the end.

    Examples:
        >>> s = ArrayStack()
        >>> s.push(1)
        >>> s.push(2)
        >>> s.peek()
        2
        >>> s.pop()
        2
        >>> s.size()
        1
    """

    def __init__(self) -> None:
        """Initialize an empty array-based stack."""
        self._data: list[Any] = []

    def push(self, item: Any) -> None:
        """Push `item` onto the top of the stack.

        Args:
            item: Element to add.

        Time Complexity: O(1) amortized
        """
        self._data.append(item)

    def pop(self) -> Any:
        """Remove and return the top element.

        Returns:
            The element at the top of the stack.

        Raises:
            IndexError: If the stack is empty.

        Time Complexity: O(1) amortized
        """
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self) -> Any:
        """Return the top element without removing it.

        Returns:
            The element at the top of the stack.

        Raises:
            IndexError: If the stack is empty.

        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._data[-1]

    def is_empty(self) -> bool:
        """Check if the stack is empty.

        Returns:
            True if no elements are stored.

        Time Complexity: O(1)
        """
        return len(self._data) == 0

    def size(self) -> int:
        """Return the number of elements.

        Returns:
            Count of elements in the stack.

        Time Complexity: O(1)
        """
        return len(self._data)

    def clear(self) -> None:
        """Remove all elements from the stack.

        Time Complexity: O(1)
        """
        self._data.clear()

    def __iter__(self) -> Iterator[Any]:
        """Yield elements from top to bottom."""
        return reversed(self._data)

    def __len__(self) -> int:
        """Support len()."""
        return self.size()

    def __str__(self) -> str:
        """Return string representation."""
        return str(self._data)

    def __repr__(self) -> str:
        """Return detailed representation."""
        return f"ArrayStack({self._data})"


class LinkedStack:
    """A stack implemented using a singly-linked list.

    The head of the linked list is the top of the stack.

    Examples:
        >>> s = LinkedStack()
        >>> s.push(1)
        >>> s.push(2)
        >>> s.peek()
        2
        >>> s.pop()
        2
        >>> s.size()
        1
    """

    class _Node:
        """Internal node for the linked list."""
        __slots__ = ("data", "next")

        def __init__(self, data: Any, next_node: Optional["LinkedStack._Node"] = None) -> None:
            self.data = data
            self.next = next_node

    def __init__(self) -> None:
        """Initialize an empty linked-list-based stack."""
        self._top: Optional[LinkedStack._Node] = None
        self._size: int = 0

    def push(self, item: Any) -> None:
        """Push `item` onto the top of the stack.

        Args:
            item: Element to add.

        Time Complexity: O(1)
        """
        new_node = self._Node(item, self._top)
        self._top = new_node
        self._size += 1

    def pop(self) -> Any:
        """Remove and return the top element.

        Returns:
            The element at the top of the stack.

        Raises:
            IndexError: If the stack is empty.

        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("pop from empty stack")
        data = self._top.data
        self._top = self._top.next
        self._size -= 1
        return data

    def peek(self) -> Any:
        """Return the top element without removing it.

        Returns:
            The element at the top of the stack.

        Raises:
            IndexError: If the stack is empty.

        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._top.data

    def is_empty(self) -> bool:
        """Check if the stack is empty.

        Returns:
            True if no elements.

        Time Complexity: O(1)
        """
        return self._top is None

    def size(self) -> int:
        """Return the number of elements.

        Returns:
            Count of elements.

        Time Complexity: O(1)
        """
        return self._size

    def clear(self) -> None:
        """Remove all elements.

        Time Complexity: O(1)
        """
        self._top = None
        self._size = 0

    def __iter__(self) -> Iterator[Any]:
        """Yield elements from top to bottom."""
        current = self._top
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
        items = list(self)
        return f"LinkedStack(size={self._size}, data={items})"


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

    def test_stack(stack_cls, name: str):
        print(f"\n{name}:")
        s = stack_cls()
        check("empty is_empty", s.is_empty() is True)
        check("empty size == 0", s.size() == 0)

        s.push(10)
        s.push(20)
        s.push(30)
        check("size after 3 pushes == 3", s.size() == 3)
        check("peek == 30", s.peek() == 30)
        check("pop == 30", s.pop() == 30)
        check("pop == 20", s.pop() == 20)
        check("size after 2 pops == 1", s.size() == 1)
        check("pop == 10", s.pop() == 10)
        check("empty after all pops", s.is_empty() is True)

        try:
            s.pop()
            check("pop empty raises IndexError", False)
        except IndexError:
            check("pop empty raises IndexError", True)

        try:
            s.peek()
            check("peek empty raises IndexError", False)
        except IndexError:
            check("peek empty raises IndexError", True)

        # Clear
        s.push(1)
        s.push(2)
        s.clear()
        check("clear makes empty", s.is_empty() is True)
        check("clear size == 0", s.size() == 0)

        # Iteration
        s.push(1)
        s.push(2)
        s.push(3)
        items = list(s)
        check("iteration top to bottom", items == [3, 2, 1])

        # len()
        check("len() == 3", len(s) == 3)

    test_stack(ArrayStack, "ArrayStack")
    test_stack(LinkedStack, "LinkedStack")

    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
