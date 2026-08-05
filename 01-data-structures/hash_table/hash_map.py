"""
HashMap Implementation (Separate Chaining)
===========================================

A hash map (dictionary) that maps keys to values. Uses separate chaining
with linked lists to handle collisions.

Features:
    - put(key, value): Insert or update a key-value pair.
    - get(key): Retrieve the value for a key.
    - remove(key): Delete a key-value pair.
    - contains_key(key): Check if a key exists.
    - Automatic resize when load factor exceeds 0.75.

Time Complexities (average):
    - put: O(1)
    - get: O(1)
    - remove: O(1)
    - contains_key: O(1)

Space Complexity: O(n + capacity)
"""

from typing import Any, Optional, Iterator, Tuple


class HashMap:
    """A hash map using separate chaining for collision resolution.

    Each bucket is a list of (key, value) pairs (simulated linked list
    for simplicity, using Python lists for clarity).

    Examples:
        >>> hm = HashMap()
        >>> hm.put("a", 1)
        >>> hm.put("b", 2)
        >>> hm.get("a")
        1
        >>> hm.contains_key("b")
        True
        >>> hm.remove("a")
        1
        >>> hm.size()
        1
    """

    _DEFAULT_CAPACITY = 16
    _LOAD_FACTOR = 0.75

    def __init__(self, initial_capacity: int = _DEFAULT_CAPACITY) -> None:
        """Initialize hash map with given initial capacity.

        Args:
            initial_capacity: Number of buckets (default 16).
        """
        if initial_capacity < 1:
            raise ValueError("initial_capacity must be >= 1")
        self._capacity: int = initial_capacity
        self._size: int = 0
        # Each bucket is a list of (key, value) tuples
        self._buckets: list[list[Tuple[Any, Any]]] = [[] for _ in range(initial_capacity)]

    def size(self) -> int:
        """Return number of key-value pairs.

        Returns:
            Count of entries.

        Time Complexity: O(1)
        """
        return self._size

    def is_empty(self) -> bool:
        """Check if map is empty.

        Returns:
            True if no entries.

        Time Complexity: O(1)
        """
        return self._size == 0

    def _hash(self, key: Any) -> int:
        """Compute bucket index for `key`.

        Uses Python's built-in hash() and modulo capacity.

        Args:
            key: Key to hash.

        Returns:
            Bucket index in range [0, capacity).

        Time Complexity: O(1) (depends on key's hash implementation)
        """
        return abs(hash(key)) % self._capacity

    def _load_factor(self) -> float:
        """Return current load factor.

        Returns:
            Ratio of size to capacity.

        Time Complexity: O(1)
        """
        return self._size / self._capacity

    def put(self, key: Any, value: Any) -> None:
        """Insert or update a key-value pair.

        If key already exists, its value is updated. If the load factor
        exceeds 0.75 after insertion, the table is resized.

        Args:
            key: Key to insert.
            value: Value associated with the key.

        Time Complexity: O(1) average, O(n) when resizing.
        """
        if self._load_factor() >= self._LOAD_FACTOR:
            self._resize(self._capacity * 2)

        index = self._hash(key)
        bucket = self._buckets[index]

        # Check if key already exists — update
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        # New key — append
        bucket.append((key, value))
        self._size += 1

    def get(self, key: Any, default: Any = None) -> Any:
        """Retrieve the value for `key`.

        Args:
            key: Key to look up.
            default: Value to return if key not found (default None).

        Returns:
            Associated value, or `default` if key not present.

        Time Complexity: O(1) average.
        """
        index = self._hash(key)
        for k, v in self._buckets[index]:
            if k == key:
                return v
        return default

    def remove(self, key: Any) -> Any:
        """Remove a key-value pair.

        Args:
            key: Key to remove.

        Returns:
            The value that was associated with the key.

        Raises:
            KeyError: If key is not present.

        Time Complexity: O(1) average.
        """
        index = self._hash(key)
        bucket = self._buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self._size -= 1
                return v
        raise KeyError(f"Key '{key}' not found")

    def contains_key(self, key: Any) -> bool:
        """Check if `key` exists in the map.

        Args:
            key: Key to check.

        Returns:
            True if key present, False otherwise.

        Time Complexity: O(1) average.
        """
        index = self._hash(key)
        for k, _ in self._buckets[index]:
            if k == key:
                return True
        return False

    def keys(self) -> Iterator[Any]:
        """Yield all keys.

        Yields:
            Each key in the map (order not guaranteed).

        Time Complexity: O(n + capacity)
        """
        for bucket in self._buckets:
            for k, _ in bucket:
                yield k

    def values(self) -> Iterator[Any]:
        """Yield all values.

        Yields:
            Each value in the map.

        Time Complexity: O(n + capacity)
        """
        for bucket in self._buckets:
            for _, v in bucket:
                yield v

    def items(self) -> Iterator[Tuple[Any, Any]]:
        """Yield all (key, value) pairs.

        Yields:
            Each key-value pair.

        Time Complexity: O(n + capacity)
        """
        for bucket in self._buckets:
            for pair in bucket:
                yield pair

    def clear(self) -> None:
        """Remove all entries, resetting to default capacity.

        Time Complexity: O(capacity)
        """
        self._capacity = self._DEFAULT_CAPACITY
        self._size = 0
        self._buckets = [[] for _ in range(self._capacity)]

    def _resize(self, new_capacity: int) -> None:
        """Resize the internal bucket array.

        Rehashes all existing entries into a new bucket array.

        Args:
            new_capacity: New number of buckets.

        Time Complexity: O(n + new_capacity)
        """
        old_buckets = self._buckets
        self._capacity = new_capacity
        self._size = 0
        self._buckets = [[] for _ in range(new_capacity)]

        # Re-insert all entries
        for bucket in old_buckets:
            for k, v in bucket:
                index = self._hash(k)
                self._buckets[index].append((k, v))
                self._size += 1

    def __getitem__(self, key: Any) -> Any:
        """Support bracket access: hm[key]."""
        value = self.get(key, _SENTINEL := object())
        if value is _SENTINEL:
            raise KeyError(key)
        return value

    def __setitem__(self, key: Any, value: Any) -> None:
        """Support bracket assignment: hm[key] = value."""
        self.put(key, value)

    def __delitem__(self, key: Any) -> None:
        """Support del hm[key]."""
        self.remove(key)

    def __contains__(self, key: Any) -> bool:
        """Support `in` operator."""
        return self.contains_key(key)

    def __len__(self) -> int:
        """Support len()."""
        return self._size

    def __iter__(self) -> Iterator[Any]:
        """Yield keys."""
        return self.keys()

    def __str__(self) -> str:
        """Return string representation."""
        pairs = [f"{k!r}: {v!r}" for k, v in self.items()]
        return "{" + ", ".join(pairs) + "}"

    def __repr__(self) -> str:
        """Return detailed representation."""
        return f"HashMap(size={self._size}, capacity={self._capacity})"


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
    hm = HashMap()
    check("empty size", hm.size() == 0)
    check("empty is_empty", hm.is_empty())

    hm.put("a", 1)
    hm.put("b", 2)
    hm.put("c", 3)
    check("size after 3 puts", hm.size() == 3)
    check("get('a') == 1", hm.get("a") == 1)
    check("get('b') == 2", hm.get("b") == 2)
    check("get('c') == 3", hm.get("c") == 3)
    check("get missing returns default", hm.get("z") is None)
    check("get missing with default", hm.get("z", -1) == -1)
    check("contains_key('a')", hm.contains_key("a"))
    check("not contains_key('z')", not hm.contains_key("z"))

    # ── Update ────────────────────────────────────────────────────────────────
    print("\nUpdate:")
    hm.put("a", 100)
    check("update 'a' to 100", hm.get("a") == 100)
    check("size unchanged after update", hm.size() == 3)

    # ── Remove ────────────────────────────────────────────────────────────────
    print("\nRemove:")
    removed = hm.remove("a")
    check("remove returns old value", removed == 100)
    check("size after remove", hm.size() == 2)
    check("removed key not found", not hm.contains_key("a"))

    try:
        hm.remove("nonexistent")
        check("remove missing raises", False)
    except KeyError:
        check("remove missing raises", True)

    # ── Bucket collisions ─────────────────────────────────────────────────────
    print("\nCollision handling:")
    hm_collision = HashMap(4)
    for i in range(20):
        hm_collision.put(f"key{i}", i)
    check("size with collisions", hm_collision.size() == 20)
    for i in range(20):
        check(f"get key{i}", hm_collision.get(f"key{i}") == i)

    # ── Resize ────────────────────────────────────────────────────────────────
    print("\nResize:")
    hm_resize = HashMap(4)
    check("initial capacity", hm_resize._capacity == 4)
    for i in range(10):
        hm_resize.put(i, i)
    check("capacity increased", hm_resize._capacity > 4)
    check("all entries preserved", hm_resize.size() == 10)
    for i in range(10):
        check(f"get({i}) after resize", hm_resize.get(i) == i)

    # ── Duplicate handling ───────────────────────────────────────────────────
    print("\nDuplicate handling:")
    hm_dup = HashMap()
    hm_dup.put("key", 1)
    hm_dup.put("key", 2)
    check("duplicate key updates value", hm_dup.get("key") == 2)
    check("size still 1", hm_dup.size() == 1)

    # ── Iteration ─────────────────────────────────────────────────────────────
    print("\nIteration:")
    hm_iter = HashMap()
    hm_iter.put("x", 10)
    hm_iter.put("y", 20)
    all_keys = list(hm_iter.keys())
    all_values = list(hm_iter.values())
    check("keys contains 'x','y'", set(all_keys) == {"x", "y"})
    check("values contains 10,20", set(all_values) == {10, 20})

    # ── Dunder methods ────────────────────────────────────────────────────────
    print("\nDunder methods:")
    hm_dunder = HashMap()
    hm_dunder["key"] = 42
    check("__setitem__ / __getitem__", hm_dunder["key"] == 42)
    check("__contains__", "key" in hm_dunder)
    check("__len__", len(hm_dunder) == 1)
    del hm_dunder["key"]
    check("__delitem__", not hm_dunder.contains_key("key"))
    try:
        _ = hm_dunder["missing"]
        check("__getitem__ missing raises", False)
    except KeyError:
        check("__getitem__ missing raises", True)

    # ── Clear ─────────────────────────────────────────────────────────────────
    print("\nClear:")
    hm_clear = HashMap()
    hm_clear.put("a", 1)
    hm_clear.put("b", 2)
    hm_clear.clear()
    check("clear makes empty", hm_clear.is_empty())
    check("clear resets size", hm_clear.size() == 0)

    # ── Summary ───────────────────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
