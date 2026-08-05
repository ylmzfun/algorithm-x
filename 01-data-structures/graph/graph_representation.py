"""
Graph Representation
=====================

A graph implementation supporting both adjacency matrix and adjacency list
representations. The graph can be directed or undirected and supports
basic operations plus BFS/DFS traversals.

Operations:
    - add_edge, remove_edge: Modify edges
    - has_edge: Check edge existence
    - neighbors: Return adjacent vertices
    - bfs: Breadth-first search
    - dfs: Depth-first search (iterative + recursive)

Time Complexities:
    - Adjacency List:
        - add_edge: O(1)
        - remove_edge: O(degree)
        - has_edge: O(degree)
        - neighbors: O(degree)
    - Adjacency Matrix:
        - add_edge: O(1)
        - remove_edge: O(1)
        - has_edge: O(1)
        - neighbors: O(V)

Space Complexity:
    - Adjacency List: O(V + E)
    - Adjacency Matrix: O(V²)
"""

from typing import Any, Dict, List, Optional, Set, Iterator
from collections import deque


class Graph:
    """A graph supporting both adjacency list and adjacency matrix.

    The adjacency list is the primary representation. The adjacency matrix
    is lazily built when needed.

    Vertices are stored as integers 0..V-1 for efficient matrix operations,
    but a label mapping allows arbitrary vertex labels.

    Examples:
        >>> g = Graph(directed=False)
        >>> g.add_edge(0, 1)
        >>> g.add_edge(1, 2)
        >>> g.has_edge(0, 1)
        True
        >>> list(g.neighbors(1))
        [0, 2]
        >>> g.bfs(0)
        [0, 1, 2]
    """

    def __init__(self, directed: bool = False) -> None:
        """Initialize an empty graph.

        Args:
            directed: If True, edges are one-way (default False).
        """
        self._directed = directed
        self._adj_list: Dict[int, List[int]] = {}  # vertex → [neighbors]
        self._adj_matrix: Optional[List[List[int]]] = None  # Lazily built
        self._vertices: Set[int] = set()
        self._edge_count: int = 0

    def is_directed(self) -> bool:
        """Return True if graph is directed."""
        return self._directed

    def vertex_count(self) -> int:
        """Return number of vertices."""
        return len(self._vertices)

    def edge_count(self) -> int:
        """Return number of edges."""
        return self._edge_count

    def vertices(self) -> Set[int]:
        """Return set of all vertex IDs."""
        return self._vertices.copy()

    # ── Edge Operations ──────────────────────────────────────────────────────

    def add_edge(self, u: int, v: int) -> None:
        """Add an edge between vertices u and v.

        Automatically registers vertices if not already present.

        Args:
            u: Source vertex.
            v: Destination vertex.

        Time Complexity: O(1)
        """
        self._vertices.add(u)
        self._vertices.add(v)

        # Adjacency list
        if u not in self._adj_list:
            self._adj_list[u] = []
        if v not in self._adj_list:
            self._adj_list[v] = []

        if v not in self._adj_list[u]:
            self._adj_list[u].append(v)
            self._edge_count += 1

        if not self._directed and u != v:
            if u not in self._adj_list[v]:
                self._adj_list[v].append(u)

        # Invalidate matrix cache
        self._adj_matrix = None

    def remove_edge(self, u: int, v: int) -> None:
        """Remove edge between u and v.

        Args:
            u: Source vertex.
            v: Destination vertex.

        Raises:
            ValueError: If either vertex doesn't exist.

        Time Complexity: O(degree)
        """
        if u not in self._adj_list:
            raise ValueError(f"Vertex {u} not in graph")
        if v not in self._adj_list:
            raise ValueError(f"Vertex {v} not in graph")

        if v in self._adj_list[u]:
            self._adj_list[u].remove(v)
            self._edge_count -= 1

        if not self._directed and u in self._adj_list[v]:
            self._adj_list[v].remove(u)

        self._adj_matrix = None

    def has_edge(self, u: int, v: int) -> bool:
        """Check if edge (u, v) exists.

        Args:
            u: Source vertex.
            v: Destination vertex.

        Returns:
            True if edge exists.

        Time Complexity: O(degree) with list, O(1) with matrix.
        """
        if u not in self._adj_list:
            return False
        if self._adj_matrix is not None:
            n = len(self._vertices_sorted)
            ui = self._vertex_to_index[u]
            vi = self._vertex_to_index[v]
            return self._adj_matrix[ui][vi] == 1
        return v in self._adj_list[u]

    def neighbors(self, u: int) -> List[int]:
        """Return list of neighbors of vertex u.

        Args:
            u: Vertex ID.

        Returns:
            List of adjacent vertices (order is insertion order).

        Raises:
            ValueError: If vertex not in graph.

        Time Complexity: O(degree)
        """
        if u not in self._adj_list:
            raise ValueError(f"Vertex {u} not in graph")
        return self._adj_list[u].copy()

    def degree(self, u: int) -> int:
        """Return degree of vertex u.

        For directed graphs, returns out-degree.

        Args:
            u: Vertex ID.

        Returns:
            Number of edges from u.

        Time Complexity: O(1)
        """
        if u not in self._adj_list:
            raise ValueError(f"Vertex {u} not in graph")
        return len(self._adj_list[u])

    # ── Adjacency Matrix ─────────────────────────────────────────────────────

    def get_adjacency_matrix(self) -> List[List[int]]:
        """Return the adjacency matrix (builds if needed).

        Returns:
            V×V matrix where matrix[i][j] = 1 if edge exists, 0 otherwise.

        Time Complexity: O(V²) on first call, O(1) afterwards.
        """
        if self._adj_matrix is not None:
            return self._adj_matrix

        sorted_verts = sorted(self._vertices)
        n = len(sorted_verts)
        self._vertices_sorted = sorted_verts
        self._vertex_to_index = {v: i for i, v in enumerate(sorted_verts)}

        matrix = [[0] * n for _ in range(n)]
        for u, neighbors_list in self._adj_list.items():
            ui = self._vertex_to_index[u]
            for v in neighbors_list:
                vi = self._vertex_to_index[v]
                matrix[ui][vi] = 1

        self._adj_matrix = matrix
        return matrix

    # ── BFS ──────────────────────────────────────────────────────────────────

    def bfs(self, start: int) -> List[int]:
        """Breadth-first search from `start`.

        Returns vertices in BFS visit order.

        Args:
            start: Starting vertex.

        Returns:
            List of vertex IDs in BFS order.

        Raises:
            ValueError: If start not in graph.

        Time Complexity: O(V + E)
        """
        if start not in self._adj_list:
            raise ValueError(f"Start vertex {start} not in graph")

        visited: Set[int] = {start}
        result: List[int] = [start]
        queue = deque([start])

        while queue:
            u = queue.popleft()
            for v in self._adj_list.get(u, []):
                if v not in visited:
                    visited.add(v)
                    result.append(v)
                    queue.append(v)

        return result

    def bfs_distance(self, start: int) -> Dict[int, int]:
        """Return shortest-path distances from `start` to all reachable vertices.

        Args:
            start: Starting vertex.

        Returns:
            Dict mapping vertex → distance (number of edges from start).

        Time Complexity: O(V + E)
        """
        if start not in self._adj_list:
            raise ValueError(f"Start vertex {start} not in graph")

        dist: Dict[int, int] = {start: 0}
        queue = deque([start])

        while queue:
            u = queue.popleft()
            for v in self._adj_list.get(u, []):
                if v not in dist:
                    dist[v] = dist[u] + 1
                    queue.append(v)

        return dist

    # ── DFS ──────────────────────────────────────────────────────────────────

    def dfs(self, start: int) -> List[int]:
        """Depth-first search (iterative) from `start`.

        Args:
            start: Starting vertex.

        Returns:
            List of vertex IDs in DFS visit order.

        Time Complexity: O(V + E)
        Space Complexity: O(V)
        """
        if start not in self._adj_list:
            raise ValueError(f"Start vertex {start} not in graph")

        visited: Set[int] = set()
        result: List[int] = []
        stack = [start]

        while stack:
            u = stack.pop()
            if u not in visited:
                visited.add(u)
                result.append(u)
                # Push neighbors in reverse order to maintain the same order
                # as recursive DFS (optional — just for consistency)
                for v in reversed(self._adj_list.get(u, [])):
                    if v not in visited:
                        stack.append(v)

        return result

    def dfs_recursive(self, start: int) -> List[int]:
        """Depth-first search (recursive) from `start`.

        Args:
            start: Starting vertex.

        Returns:
            List of vertex IDs in DFS visit order.

        Time Complexity: O(V + E)
        Space Complexity: O(V) — recursion stack.
        """
        if start not in self._adj_list:
            raise ValueError(f"Start vertex {start} not in graph")

        visited: Set[int] = set()
        result: List[int] = []

        def _dfs(u: int) -> None:
            visited.add(u)
            result.append(u)
            for v in self._adj_list.get(u, []):
                if v not in visited:
                    _dfs(v)

        _dfs(start)
        return result

    def dfs_full(self) -> List[int]:
        """Perform DFS on all disconnected components.

        Returns:
            List of all vertices in DFS order across all components.

        Time Complexity: O(V + E)
        """
        visited: Set[int] = set()
        result: List[int] = []

        for vertex in sorted(self._vertices):
            if vertex not in visited:
                stack = [vertex]
                while stack:
                    u = stack.pop()
                    if u not in visited:
                        visited.add(u)
                        result.append(u)
                        for v in reversed(self._adj_list.get(u, [])):
                            if v not in visited:
                                stack.append(v)

        return result

    # ─── Dunder ──────────────────────────────────────────────────────────────

    def __str__(self) -> str:
        """Return adjacency list representation."""
        lines = []
        for u in sorted(self._adj_list.keys()):
            neighbors = self._adj_list[u]
            arrow = "→" if self._directed else "↔"
            lines.append(f"  {u} {arrow} {neighbors}")
        return "Graph:\n" + "\n".join(lines) if lines else "Graph: (empty)"

    def __repr__(self) -> str:
        gt = "directed" if self._directed else "undirected"
        return f"Graph({gt}, V={self.vertex_count()}, E={self.edge_count()})"


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
    g = Graph(directed=False)
    check("undirected", not g.is_directed())
    check("empty V=0", g.vertex_count() == 0)
    check("empty E=0", g.edge_count() == 0)

    # ── Add edges ─────────────────────────────────────────────────────────────
    print("\nAdd edges:")
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(3, 4)
    check("V=5", g.vertex_count() == 5)
    check("E=4 (undirected)", g.edge_count() == 4)
    check("has_edge(0,1)", g.has_edge(0, 1))
    check("has_edge(1,0) symmetric", g.has_edge(1, 0))
    check("not has_edge(0,3)", not g.has_edge(0, 3))

    # ── Neighbors ─────────────────────────────────────────────────────────────
    print("\nNeighbors:")
    check("neighbors(0)", set(g.neighbors(0)) == {1, 2})
    check("neighbors(3)", g.neighbors(3) == [4])
    check("degree(0) == 2", g.degree(0) == 2)

    try:
        g.neighbors(99)
        check("neighbors nonexistent raises", False)
    except ValueError:
        check("neighbors nonexistent raises", True)

    # ── Remove edge ───────────────────────────────────────────────────────────
    print("\nRemove edge:")
    g.remove_edge(0, 1)
    check("after remove has_edge(0,1)=False", not g.has_edge(0, 1))
    check("E after remove", g.edge_count() == 3)

    # ── Adjacency Matrix ─────────────────────────────────────────────────────
    print("\nAdjacency Matrix:")
    # Rebuild a clean graph
    g2 = Graph(directed=False)
    g2.add_edge(0, 1)
    g2.add_edge(0, 2)
    g2.add_edge(1, 2)

    matrix = g2.get_adjacency_matrix()
    # Matrix should be:
    # 0: [0,1,1]
    # 1: [1,0,1]
    # 2: [1,1,0]
    expected_matrix = [
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0],
    ]
    check("adjacency matrix correct", matrix == expected_matrix)

    # ── BFS ───────────────────────────────────────────────────────────────────
    print("\nBFS:")
    g_bfs = Graph(directed=False)
    g_bfs.add_edge(0, 1)
    g_bfs.add_edge(0, 2)
    g_bfs.add_edge(1, 3)
    g_bfs.add_edge(2, 3)
    # BFS from 0: 0, 1, 2, 3
    bfs_order = g_bfs.bfs(0)
    check("BFS starts at 0", bfs_order[0] == 0)
    check("BFS visits all 4", len(bfs_order) == 4)

    distances = g_bfs.bfs_distance(0)
    check("BFS dist[0] == 0", distances[0] == 0)
    check("BFS dist[1] == 1", distances[1] == 1)
    check("BFS dist[3] == 2", distances[3] == 2)

    # ── DFS ───────────────────────────────────────────────────────────────────
    print("\nDFS:")
    g_dfs = Graph(directed=False)
    g_dfs.add_edge(0, 1)
    g_dfs.add_edge(0, 2)
    g_dfs.add_edge(1, 3)
    g_dfs.add_edge(2, 3)

    dfs_iter = g_dfs.dfs(0)
    dfs_recur = g_dfs.dfs_recursive(0)
    check("DFS visits all 4", len(dfs_iter) == 4)
    check("DFS starts at 0", dfs_iter[0] == 0)
    check("DFS recursive visits all 4", len(dfs_recur) == 4)

    dfs_full = g_dfs.dfs_full()
    check("DFS full visits all", len(dfs_full) == 4)

    # ── Directed graph ────────────────────────────────────────────────────────
    print("\nDirected Graph:")
    dg = Graph(directed=True)
    dg.add_edge(0, 1)
    dg.add_edge(1, 2)
    check("has_edge(0,1) True", dg.has_edge(0, 1))
    check("has_edge(1,0) False (directed)", not dg.has_edge(1, 0))
    check("neighbors(1) == [2]", dg.neighbors(1) == [2])

    # ── Summary ───────────────────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
