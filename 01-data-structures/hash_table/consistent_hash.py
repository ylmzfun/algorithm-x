"""
Consistent Hashing Implementation
===================================

A simple consistent hashing ring implementation. Consistent hashing maps
keys to nodes (servers) in a way that minimizes redistribution when nodes
are added or removed.

The ring is a sorted circular space (0 to 2^32 - 1). Each node is placed
at multiple positions (virtual nodes) to improve load distribution.

Features:
    - add_node: Add a server with virtual replicas.
    - remove_node: Remove a server and all its replicas.
    - get_node: Find the responsible node for a given key.

Time Complexities:
    - add_node: O(v * log(n)) where v = virtual nodes, n = total positions
    - remove_node: O(v * log(n))
    - get_node: O(log n) — binary search on sorted ring

Space Complexity: O(n * v) where n = number of nodes
"""

import hashlib
import bisect
from typing import Any, Dict, List, Optional, Set


class ConsistentHash:
    """A consistent hashing ring with virtual nodes.

    Maps keys to nodes using MD5-based hashing. Each physical node gets
    `virtual_nodes` replicas distributed around the ring for balanced load.

    Examples:
        >>> ch = ConsistentHash(virtual_nodes=3)
        >>> ch.add_node("server1")
        >>> ch.add_node("server2")
        >>> ch.get_node("key1")
        'server1'
        >>> ch.remove_node("server1")
        >>> ch.get_node("key1")
        'server2'
    """

    def __init__(self, virtual_nodes: int = 100) -> None:
        """Initialize consistent hash ring.

        Args:
            virtual_nodes: Number of virtual replicas per physical node.
                           Higher values improve balance (default 100).
        """
        if virtual_nodes < 1:
            raise ValueError("virtual_nodes must be >= 1")
        self._virtual_nodes: int = virtual_nodes
        self._ring: Dict[int, str] = {}        # hash → node name
        self._sorted_keys: List[int] = []       # Sorted hash values
        self._nodes: Set[str] = set()           # Registered physical nodes

    def _hash(self, key: str) -> int:
        """Compute a 32-bit integer hash of `key` using MD5.

        Args:
            key: String to hash.

        Returns:
            Integer in range [0, 2^32).

        Time Complexity: O(len(key))
        """
        md5 = hashlib.md5(key.encode('utf-8')).hexdigest()
        return int(md5, 16) % (2 ** 32)

    def add_node(self, node: str) -> None:
        """Add a physical node to the ring.

        Creates `virtual_nodes` replicas at different hash positions
        by appending an index suffix: "node#0", "node#1", ...

        Args:
            node: Identifier for the physical node (e.g., "server1").

        Time Complexity: O(v * log(v*n)) where v = virtual_nodes, n = existing nodes.
        """
        if node in self._nodes:
            return  # Already present

        self._nodes.add(node)

        for i in range(self._virtual_nodes):
            virtual_key = f"{node}#{i}"
            hash_val = self._hash(virtual_key)
            self._ring[hash_val] = node
            bisect.insort(self._sorted_keys, hash_val)

    def remove_node(self, node: str) -> None:
        """Remove a physical node and all its virtual replicas.

        Args:
            node: Node identifier to remove.

        Time Complexity: O(v * log(v*n))
        """
        if node not in self._nodes:
            return

        self._nodes.discard(node)

        for i in range(self._virtual_nodes):
            virtual_key = f"{node}#{i}"
            hash_val = self._hash(virtual_key)
            if hash_val in self._ring:
                del self._ring[hash_val]
                idx = bisect.bisect_left(self._sorted_keys, hash_val)
                if idx < len(self._sorted_keys) and self._sorted_keys[idx] == hash_val:
                    self._sorted_keys.pop(idx)

    def get_node(self, key: str) -> Optional[str]:
        """Find the responsible node for `key`.

        Walks clockwise around the ring from the key's hash position
        until a node is found. If no node exists, returns None.

        Args:
            key: The key to look up.

        Returns:
            Node identifier responsible for `key`, or None if ring is empty.

        Time Complexity: O(log n) — binary search on sorted ring.
        """
        if not self._sorted_keys:
            return None

        hash_val = self._hash(key)
        # Find the first node with hash >= hash_val (clockwise walk)
        idx = bisect.bisect_left(self._sorted_keys, hash_val)

        # Wrap around if we go past the end
        if idx == len(self._sorted_keys):
            idx = 0

        return self._ring[self._sorted_keys[idx]]

    def get_nodes(self) -> Set[str]:
        """Return the set of registered physical nodes.

        Returns:
            Set of node identifiers.

        Time Complexity: O(m) where m = number of physical nodes.
        """
        return self._nodes.copy()

    def size(self) -> int:
        """Return number of physical nodes.

        Returns:
            Count of registered nodes.

        Time Complexity: O(1)
        """
        return len(self._nodes)

    def is_empty(self) -> bool:
        """Check if ring has any nodes.

        Returns:
            True if no nodes registered.

        Time Complexity: O(1)
        """
        return len(self._nodes) == 0


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
    ch = ConsistentHash(virtual_nodes=20)
    check("initial empty", ch.is_empty())
    check("size == 0", ch.size() == 0)
    check("get_node on empty returns None", ch.get_node("test") is None)

    ch.add_node("server1")
    ch.add_node("server2")
    ch.add_node("server3")
    check("size after 3 adds", ch.size() == 3)
    check("not empty", not ch.is_empty())

    # ── Deterministic mapping ─────────────────────────────────────────────────
    print("\nDeterministic mapping:")
    # Same key should always map to same node
    node1 = ch.get_node("mykey")
    node2 = ch.get_node("mykey")
    check("same key same node", node1 == node2)
    check("returns a valid node", node1 in {"server1", "server2", "server3"})

    # ── All keys map somewhere ────────────────────────────────────────────────
    print("\nAll keys map:")
    keys = ["alpha", "beta", "gamma", "delta", "epsilon"]
    for key in keys:
        node = ch.get_node(key)
        check(f"key '{key}' maps to a node", node in {"server1", "server2", "server3"})

    # ── Remove and re-add ─────────────────────────────────────────────────────
    print("\nRemove and re-add:")
    ch.remove_node("server1")
    check("size after remove", ch.size() == 2)
    check("nodes set", ch.get_nodes() == {"server2", "server3"})

    # Keys that mapped to server1 should now map to server2 or server3
    for key in keys:
        node = ch.get_node(key)
        check(f"key '{key}' maps after removal", node in {"server2", "server3"})

    ch.add_node("server1")
    check("size after re-add", ch.size() == 3)

    # ── Remove non-existent ───────────────────────────────────────────────────
    print("\nRemove non-existent:")
    ch.remove_node("nonexistent")
    check("size unchanged after removing non-existent", ch.size() == 3)

    # ── Duplicate add ─────────────────────────────────────────────────────────
    print("\nDuplicate add:")
    ch.add_node("server1")
    check("size unchanged after duplicate add", ch.size() == 3)

    # ── Distribution check ────────────────────────────────────────────────────
    print("\nDistribution check (100 keys, 3 nodes, 150 vnodes):")
    ch2 = ConsistentHash(virtual_nodes=150)
    ch2.add_node("A")
    ch2.add_node("B")
    ch2.add_node("C")

    counts: Dict[str, int] = {"A": 0, "B": 0, "C": 0}
    for i in range(300):
        node = ch2.get_node(f"item_{i}")
        counts[node] += 1  # type: ignore[index]

    # Each node should get roughly 1/3 of keys (not strict, just sanity)
    for node_name, count in counts.items():
        check(f"node {node_name} has {count} items (>0)", count > 0)

    # ─── Summary ──────────────────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
