"""
Disjoint Set Union (Union-Find) with path compression and union by rank.

Applications:
- Connected components in an undirected graph
- Cycle detection in an undirected graph
- Dynamic connectivity
"""

from typing import List, Optional


class UnionFind:
    """
    Disjoint Set Union with path compression and union by rank.

    Provides near-constant (inverse Ackermann) amortized time per operation.
    """

    def __init__(self, n: int) -> None:
        """
        Initialize n disjoint sets labeled 0 … n-1.

        Args:
            n: Number of elements.

        Time: O(n)
        """
        self.parent = list(range(n))
        self.rank = [0] * n
        self._count = n  # number of disjoint sets

    def find(self, x: int) -> int:
        """
        Find the root/representative of the set containing x.

        Applies path compression: all nodes along the path are linked
        directly to the root.

        Args:
            x: Element index.

        Returns:
            Root of the set containing x.

        Time: O(α(n)) amortized
        """
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # path halving
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> bool:
        """
        Merge the sets containing x and y (union by rank).

        Args:
            x, y: Element indices.

        Returns:
            True if a merge happened (they were in different sets),
            False if they were already in the same set.

        Time: O(α(n)) amortized
        """
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        # Union by rank: attach shorter tree under taller tree
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self._count -= 1
        return True

    def is_connected(self, x: int, y: int) -> bool:
        """
        Check whether x and y belong to the same set.

        Args:
            x, y: Element indices.

        Returns:
            True if x and y are in the same set.

        Time: O(α(n)) amortized
        """
        return self.find(x) == self.find(y)

    def count_sets(self) -> int:
        """
        Return the current number of disjoint sets.

        Returns:
            Number of disjoint sets.

        Time: O(1)
        """
        return self._count

    # ------------------------------------------------------------------
    # Applications
    # ------------------------------------------------------------------

    @staticmethod
    def connected_components(
        n: int, edges: List[tuple]
    ) -> List[List[int]]:
        """
        Find all connected components of an undirected graph using Union-Find.

        Args:
            n: Number of vertices (0 … n-1).
            edges: List of (u, v) pairs.

        Returns:
            List of connected components, each a list of vertices.

        Time: O((V + E) * α(V))
        """
        uf = UnionFind(n)
        for u, v in edges:
            uf.union(u, v)

        # Group vertices by root
        groups: dict = {}
        for v in range(n):
            root = uf.find(v)
            groups.setdefault(root, []).append(v)

        return list(groups.values())

    @staticmethod
    def has_cycle_undirected(
        n: int, edges: List[tuple]
    ) -> bool:
        """
        Detect a cycle in an undirected graph using Union-Find.

        Args:
            n: Number of vertices.
            edges: List of (u, v) edges.

        Returns:
            True if the undirected graph contains a cycle.

        Time: O(E * α(V))
        """
        uf = UnionFind(n)
        for u, v in edges:
            if not uf.union(u, v):
                return True  # already connected → cycle
        return False


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    import sys

    all_pass = True

    # --- Basic operations ---
    uf = UnionFind(5)
    if uf.count_sets() != 5:
        print("FAIL: initial count")
        all_pass = False

    uf.union(0, 1)
    uf.union(1, 2)
    if not uf.is_connected(0, 2):
        print("FAIL: 0 and 2 should be connected")
        all_pass = False
    if uf.is_connected(0, 3):
        print("FAIL: 0 and 3 should NOT be connected")
        all_pass = False
    if uf.count_sets() != 3:
        print(f"FAIL: count should be 3, got {uf.count_sets()}")
        all_pass = False

    # Union already connected
    merged = uf.union(0, 2)
    if merged:
        print("FAIL: should not merge already connected")
        all_pass = False

    # --- Connected components ---
    comps = UnionFind.connected_components(4, [(0, 1), (2, 3)])
    comps_sorted = sorted([sorted(c) for c in comps])
    if comps_sorted != [[0, 1], [2, 3]]:
        print(f"FAIL connected components: {comps_sorted}")
        all_pass = False

    # --- Cycle detection ---
    triangle = [(0, 1), (1, 2), (2, 0)]
    if not UnionFind.has_cycle_undirected(3, triangle):
        print("FAIL: triangle should have a cycle")
        all_pass = False

    tree = [(0, 1), (1, 2), (2, 3)]
    if UnionFind.has_cycle_undirected(4, tree):
        print("FAIL: tree should NOT have a cycle")
        all_pass = False

    if all_pass:
        print("All Union-Find tests PASSED")
    sys.exit(0 if all_pass else 1)
