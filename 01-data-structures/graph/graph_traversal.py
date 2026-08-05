"""
Graph Traversal Applications
==============================

Advanced graph traversal algorithms and applications:

1. Connected Components (undirected) — Find all connected components.
2. Cycle Detection:
   - Undirected: DFS with parent tracking.
   - Directed: DFS with 3-color marking (WHITE/GRAY/BLACK).
3. Topological Sort — Kahn's algorithm (BFS) and DFS-based.
4. Bipartite Check — BFS/DFS coloring.

All algorithms operate on adjacency-list graphs (Dict[int, List[int]]).
"""

from typing import Dict, List, Set, Optional, Tuple
from collections import deque


# ─── 1. Connected Components (Undirected) ───────────────────────────────────


def find_connected_components(graph: Dict[int, List[int]]) -> List[List[int]]:
    """Find all connected components in an undirected graph.

    Uses DFS to explore each component.

    Args:
        graph: Adjacency list {vertex: [neighbors]}.

    Returns:
        List of components, each being a list of vertex IDs.

    Time Complexity: O(V + E)
    Space Complexity: O(V)

    Examples:
        >>> g = {0: [1], 1: [0, 2], 2: [1], 3: [4], 4: [3], 5: []}
        >>> comps = find_connected_components(g)
        >>> sorted([sorted(c) for c in comps])
        [[0, 1, 2], [3, 4], [5]]
    """
    visited: Set[int] = set()
    components: List[List[int]] = []

    def dfs(start: int, component: List[int]) -> None:
        """DFS to collect all vertices in a component."""
        stack = [start]
        while stack:
            u = stack.pop()
            if u not in visited:
                visited.add(u)
                component.append(u)
                for v in graph.get(u, []):
                    if v not in visited:
                        stack.append(v)

    for vertex in graph:
        if vertex not in visited:
            component: List[int] = []
            dfs(vertex, component)
            components.append(component)

    return components


# ─── 2. Cycle Detection ─────────────────────────────────────────────────────


def has_cycle_undirected(graph: Dict[int, List[int]]) -> bool:
    """Check if an undirected graph contains a cycle.

    Uses DFS with parent tracking: if we encounter a visited neighbor
    that's not the parent, a cycle exists.

    Args:
        graph: Adjacency list for an undirected graph.

    Returns:
        True if a cycle exists.

    Time Complexity: O(V + E)
    Space Complexity: O(V)

    Examples:
        >>> has_cycle_undirected({0: [1, 2], 1: [0, 2], 2: [0, 1]})
        True
        >>> has_cycle_undirected({0: [1], 1: [0, 2], 2: [1]})
        False
    """
    visited: Set[int] = set()

    def dfs(u: int, parent: int) -> bool:
        visited.add(u)
        for v in graph.get(u, []):
            if v not in visited:
                if dfs(v, u):
                    return True
            elif v != parent:
                return True  # Back edge to a non-parent → cycle
        return False

    for vertex in graph:
        if vertex not in visited:
            if dfs(vertex, -1):
                return True

    return False


def has_cycle_directed(graph: Dict[int, List[int]]) -> bool:
    """Check if a directed graph contains a cycle using 3-color DFS.

    Colors:
        WHITE (0): Not visited.
        GRAY (1): In current recursion stack.
        BLACK (2): Finished processing.

    A back edge (to a GRAY node) indicates a cycle.

    Args:
        graph: Adjacency list for a directed graph.

    Returns:
        True if a cycle exists.

    Time Complexity: O(V + E)
    Space Complexity: O(V)

    Examples:
        >>> has_cycle_directed({0: [1], 1: [2], 2: [0]})
        True
        >>> has_cycle_directed({0: [1], 1: [2], 2: []})
        False
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color: Dict[int, int] = {v: WHITE for v in graph}

    def dfs(u: int) -> bool:
        color[u] = GRAY
        for v in graph.get(u, []):
            if v not in color:  # Vertex not in graph (unlikely with adjacency list)
                color[v] = WHITE
            if color.get(v, WHITE) == GRAY:
                return True  # Back edge
            if color.get(v, WHITE) == WHITE:
                if dfs(v):
                    return True
        color[u] = BLACK
        return False

    for vertex in graph:
        if color.get(vertex, WHITE) == WHITE:
            if dfs(vertex):
                return True

    return False


# ─── 3. Topological Sort ────────────────────────────────────────────────────


def topological_sort_kahn(graph: Dict[int, List[int]]) -> List[int]:
    """Topological sort using Kahn's algorithm (BFS / indegree).

    Works only on DAGs (Directed Acyclic Graphs).

    Args:
        graph: Adjacency list for a directed graph.

    Returns:
        List of vertices in topological order.

    Raises:
        ValueError: If the graph contains a cycle.

    Time Complexity: O(V + E)
    Space Complexity: O(V)

    Examples:
        >>> g = {0: [], 1: [0], 2: [0], 3: [1, 2]}
        >>> topological_sort_kahn(g)
        [3, 1, 2, 0]
    """
    # Compute indegrees
    indegree: Dict[int, int] = {v: 0 for v in graph}
    for u in graph:
        for v in graph[u]:
            indegree[v] = indegree.get(v, 0) + 1

    # Start with vertices that have indegree 0
    queue = deque([v for v in graph if indegree.get(v, 0) == 0])
    result: List[int] = []

    while queue:
        u = queue.popleft()
        result.append(u)
        for v in graph.get(u, []):
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle — topological sort impossible")

    return result


def topological_sort_dfs(graph: Dict[int, List[int]]) -> List[int]:
    """Topological sort using DFS (post-order reversal).

    Works only on DAGs.

    Args:
        graph: Adjacency list for a directed graph.

    Returns:
        List of vertices in topological order.

    Raises:
        ValueError: If the graph contains a cycle.

    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color: Dict[int, int] = {v: WHITE for v in graph}
    order: List[int] = []

    def dfs(u: int) -> bool:
        """DFS returning False if cycle detected."""
        color[u] = GRAY
        for v in graph.get(u, []):
            if v not in color:
                color[v] = WHITE
            if color.get(v, WHITE) == GRAY:
                return False  # Cycle
            if color.get(v, WHITE) == WHITE:
                if not dfs(v):
                    return False
        color[u] = BLACK
        order.append(u)  # Post-order
        return True

    for vertex in graph:
        if color.get(vertex, WHITE) == WHITE:
            if not dfs(vertex):
                raise ValueError("Graph contains a cycle")

    order.reverse()  # Reverse post-order = topological order
    return order


# ─── 4. Bipartite Check ─────────────────────────────────────────────────────


def is_bipartite(graph: Dict[int, List[int]]) -> bool:
    """Check if an undirected graph is bipartite (2-colorable).

    Uses BFS to assign colors 0 and 1. If an edge connects same-color
    vertices, the graph is not bipartite.

    Args:
        graph: Adjacency list for an undirected graph.

    Returns:
        True if bipartite, False otherwise.

    Time Complexity: O(V + E)
    Space Complexity: O(V)

    Examples:
        >>> is_bipartite({0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2]})
        True
        >>> is_bipartite({0: [1, 2, 3], 1: [0, 2], 2: [0, 1, 3], 3: [0, 2]})
        False
    """
    UNCOLORED = -1
    color: Dict[int, int] = {v: UNCOLORED for v in graph}

    for start in graph:
        if color[start] != UNCOLORED:
            continue

        color[start] = 0
        queue = deque([start])

        while queue:
            u = queue.popleft()
            for v in graph.get(u, []):
                if v not in color:
                    color[v] = UNCOLORED
                if color[v] == UNCOLORED:
                    color[v] = 1 - color[u]
                    queue.append(v)
                elif color[v] == color[u]:
                    return False  # Same color adjacent → not bipartite

    return True


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

    # ── Connected Components ─────────────────────────────────────────────────
    print("Connected Components:")
    g1 = {0: [1], 1: [0, 2], 2: [1], 3: [4], 4: [3], 5: []}
    comps = find_connected_components(g1)
    sorted_comps = sorted([sorted(c) for c in comps])
    check("3 components", sorted_comps == [[0, 1, 2], [3, 4], [5]])

    # ── Cycle Detection (Undirected) ─────────────────────────────────────────
    print("\nCycle Detection (Undirected):")
    g_cycle = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
    g_no_cycle = {0: [1], 1: [0, 2], 2: [1]}
    check("has cycle", has_cycle_undirected(g_cycle))
    check("no cycle", not has_cycle_undirected(g_no_cycle))

    # ── Cycle Detection (Directed) ───────────────────────────────────────────
    print("\nCycle Detection (Directed):")
    dg_cycle = {0: [1], 1: [2], 2: [0]}
    dg_no_cycle = {0: [1], 1: [2], 2: []}
    check("directed has cycle", has_cycle_directed(dg_cycle))
    check("directed no cycle", not has_cycle_directed(dg_no_cycle))

    # Self-loop
    dg_self = {0: [0]}
    check("self-loop is cycle", has_cycle_directed(dg_self))

    # ── Topological Sort (Kahn) ──────────────────────────────────────────────
    print("\nTopological Sort (Kahn):")
    dag = {3: [1, 2], 1: [0], 2: [0], 0: []}
    order_kahn = topological_sort_kahn(dag)
    check("Kahn: 3 before 1", order_kahn.index(3) < order_kahn.index(1))
    check("Kahn: 1 before 0", order_kahn.index(1) < order_kahn.index(0))
    check("Kahn: 2 before 0", order_kahn.index(2) < order_kahn.index(0))
    check("Kahn: valid length", len(order_kahn) == 4)

    # Cycle causing exception
    try:
        topological_sort_kahn(dg_cycle)
        check("Kahn cycle raises", False)
    except ValueError:
        check("Kahn cycle raises", True)

    # ── Topological Sort (DFS) ───────────────────────────────────────────────
    print("\nTopological Sort (DFS):")
    order_dfs = topological_sort_dfs(dag)
    check("DFS: 3 before 1", order_dfs.index(3) < order_dfs.index(1))
    check("DFS: valid length", len(order_dfs) == 4)

    try:
        topological_sort_dfs(dg_cycle)
        check("DFS cycle raises", False)
    except ValueError:
        check("DFS cycle raises", True)

    # ── Bipartite Check ──────────────────────────────────────────────────────
    print("\nBipartite:")
    # Even cycle: 0-1-2-3-0 is bipartite
    bip = {0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2]}
    check("bipartite (even cycle)", is_bipartite(bip))

    # Triangle: not bipartite
    not_bip = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
    check("not bipartite (triangle)", not is_bipartite(not_bip))

    # Line graph: bipartite
    line = {0: [1], 1: [0, 2], 2: [1, 3], 3: [2]}
    check("bipartite (line)", is_bipartite(line))

    # ── Summary ───────────────────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
