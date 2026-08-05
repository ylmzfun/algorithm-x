"""
Advanced graph applications.

Contains:
- Strongly Connected Components (Kosaraju, Tarjan)
- Bridges and articulation points (Tarjan's algorithm)
- Eulerian path (Hierholzer's algorithm)
- Hamiltonian path (backtracking)
"""

from collections import defaultdict
from typing import List, Optional, Set, Tuple


INF = float("inf")


# ======================================================================
# Strongly Connected Components — Kosaraju
# ======================================================================

def kosaraju_scc(n: int, edges: List[Tuple[int, int]]) -> List[List[int]]:
    """
    Find all Strongly Connected Components using Kosaraju's algorithm.

    Two-pass DFS: (1) order vertices by finishing time, (2) DFS on
    reversed graph in reverse-finish order.

    Args:
        n: Number of vertices (0 … n-1).
        edges: List of directed edges (u, v).

    Returns:
        List of SCCs; each SCC is a list of vertices.

    Time:  O(V + E)
    Space: O(V + E)
    """
    adj: List[List[int]] = [[] for _ in range(n)]
    radj: List[List[int]] = [[] for _ in range(n)]  # reversed

    for u, v in edges:
        adj[u].append(v)
        radj[v].append(u)

    # First pass: get finish order (post-order)
    visited = [False] * n
    order: List[int] = []

    def dfs1(u: int) -> None:
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs1(v)
        order.append(u)

    for i in range(n):
        if not visited[i]:
            dfs1(i)

    # Second pass: collect SCCs on reversed graph
    visited = [False] * n
    sccs: List[List[int]] = []

    def dfs2(u: int, comp: List[int]) -> None:
        visited[u] = True
        comp.append(u)
        for v in radj[u]:
            if not visited[v]:
                dfs2(v, comp)

    for u in reversed(order):
        if not visited[u]:
            comp: List[int] = []
            dfs2(u, comp)
            sccs.append(comp)

    return sccs


# ======================================================================
# Strongly Connected Components — Tarjan
# ======================================================================

def tarjan_scc(n: int, edges: List[Tuple[int, int]]) -> List[List[int]]:
    """
    Find all SCCs using Tarjan's single-pass algorithm.

    Uses low-link values and an explicit stack.

    Args:
        n: Number of vertices.
        edges: List of (u, v).

    Returns:
        List of SCCs.

    Time:  O(V + E)
    Space: O(V + E)
    """
    adj: List[List[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)

    index = 0
    indices = [-1] * n
    lowlink = [0] * n
    on_stack = [False] * n
    stack: List[int] = []
    sccs: List[List[int]] = []

    def strongconnect(v: int) -> None:
        nonlocal index
        indices[v] = index
        lowlink[v] = index
        index += 1
        stack.append(v)
        on_stack[v] = True

        for w in adj[v]:
            if indices[w] == -1:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif on_stack[w]:
                lowlink[v] = min(lowlink[v], indices[w])

        if lowlink[v] == indices[v]:
            comp: List[int] = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                comp.append(w)
                if w == v:
                    break
            sccs.append(comp)

    for i in range(n):
        if indices[i] == -1:
            strongconnect(i)

    return sccs


# ======================================================================
# Bridges and Articulation Points (Tarjan)
# ======================================================================

def find_bridges(
    n: int, edges: List[Tuple[int, int]]
) -> List[Tuple[int, int]]:
    """
    Find all bridges in an undirected graph using Tarjan's algorithm.

    A bridge is an edge whose removal increases the number of connected
    components.

    Args:
        n: Number of vertices.
        edges: List of (u, v) for an undirected graph.

    Returns:
        List of bridge edges (each as (u, v) with u < v for consistency).

    Time:  O(V + E)
    Space: O(V + E)
    """
    adj: List[List[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    tin = [-1] * n
    low = [0] * n
    visited = [False] * n
    timer = 0
    bridges: List[Tuple[int, int]] = []

    def dfs(v: int, p: int) -> None:
        nonlocal timer
        visited[v] = True
        tin[v] = low[v] = timer
        timer += 1

        for to in adj[v]:
            if to == p:
                continue
            if visited[to]:
                low[v] = min(low[v], tin[to])
            else:
                dfs(to, v)
                low[v] = min(low[v], low[to])
                if low[to] > tin[v]:
                    bridges.append((min(v, to), max(v, to)))

    for i in range(n):
        if not visited[i]:
            dfs(i, -1)

    return bridges


def find_articulation_points(
    n: int, edges: List[Tuple[int, int]]
) -> Set[int]:
    """
    Find all articulation points (cut vertices) in an undirected graph.

    An articulation point is a vertex whose removal increases the number
    of connected components.

    Args:
        n: Number of vertices.
        edges: List of (u, v).

    Returns:
        Set of articulation point vertices.

    Time:  O(V + E)
    Space: O(V + E)
    """
    adj: List[List[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    tin = [-1] * n
    low = [0] * n
    visited = [False] * n
    timer = 0
    points: Set[int] = set()

    def dfs(v: int, p: int) -> None:
        nonlocal timer
        visited[v] = True
        tin[v] = low[v] = timer
        timer += 1
        children = 0

        for to in adj[v]:
            if to == p:
                continue
            if visited[to]:
                low[v] = min(low[v], tin[to])
            else:
                dfs(to, v)
                low[v] = min(low[v], low[to])
                if low[to] >= tin[v] and p != -1:
                    points.add(v)
                children += 1

        if p == -1 and children > 1:
            points.add(v)

    for i in range(n):
        if not visited[i]:
            dfs(i, -1)

    return points


# ======================================================================
# Eulerian Path (Hierholzer's algorithm)
# ======================================================================

def hierholzer_eulerian_path(
    n: int, edges: List[Tuple[int, int]], directed: bool = True
) -> Optional[List[int]]:
    """
    Find an Eulerian path / circuit using Hierholzer's algorithm.

    For a directed graph, an Eulerian path exists iff:
      - At most one vertex has out_degree - in_degree == 1 (start)
      - At most one vertex has in_degree - out_degree == 1 (end)
      - All other vertices have equal in and out degree

    For an undirected graph, set `directed=False`.

    Args:
        n: Number of vertices.
        edges: List of (u, v).
        directed: Whether the graph is directed (default True).

    Returns:
        List of vertices representing the Eulerian path, or None if
        no such path exists.

    Time:  O(V + E)
    Space: O(V + E)
    """
    if directed:
        out_deg = [0] * n
        in_deg = [0] * n
        adj: List[List[int]] = [[] for _ in range(n)]

        for u, v in edges:
            adj[u].append(v)
            out_deg[u] += 1
            in_deg[v] += 1

        start_nodes = []
        end_nodes = []
        for i in range(n):
            diff = out_deg[i] - in_deg[i]
            if diff == 1:
                start_nodes.append(i)
            elif diff == -1:
                end_nodes.append(i)
            elif diff != 0:
                return None

        # at most one start and one end
        if len(start_nodes) > 1 or len(end_nodes) > 1:
            return None

        # Determine start vertex
        if start_nodes:
            start = start_nodes[0]
        else:
            # Any vertex with an outgoing edge (Eulerian circuit)
            start = next((i for i in range(n) if out_deg[i] > 0), 0)

        # Hierholzer: iterative DFS using stack
        stack = [start]
        path: List[int] = []

        # Use index tracking to avoid re-scanning adjacency lists
        edge_index = [0] * n
        adj_list = [list(a) for a in adj]  # copy to modify

        while stack:
            u = stack[-1]
            if edge_index[u] < len(adj_list[u]):
                v = adj_list[u][edge_index[u]]
                edge_index[u] += 1
                stack.append(v)
            else:
                path.append(stack.pop())

        path.reverse()

        # Check if all edges used
        if len(path) != len(edges) + 1:
            return None

        return path
    else:
        # Undirected version
        deg = [0] * n
        adj: List[List[int]] = [[] for _ in range(n)]
        edge_idx_map = {}  # (u,v) -> edge index

        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
            deg[u] += 1
            deg[v] += 1

        odd_nodes = [i for i in range(n) if deg[i] % 2 == 1]
        if len(odd_nodes) not in (0, 2):
            return None

        start = odd_nodes[0] if odd_nodes else (next((i for i in range(n) if deg[i] > 0), 0))

        # We need to track used edges (an edge can be traversed from either direction)
        adj_list = [list(a) for a in adj]
        edge_index = [0] * n
        used_edges = set()

        stack = [start]
        path = []

        while stack:
            u = stack[-1]
            found = False
            while edge_index[u] < len(adj_list[u]):
                v = adj_list[u][edge_index[u]]
                edge_index[u] += 1
                edge_key = (min(u, v), max(u, v))
                if edge_key not in used_edges:
                    used_edges.add(edge_key)
                    stack.append(v)
                    found = True
                    break
            if not found:
                path.append(stack.pop())

        path.reverse()

        if len(path) != len(edges) + 1:
            return None
        return path


# ======================================================================
# Hamiltonian Path (backtracking)
# ======================================================================

def hamiltonian_path(
    n: int, edges: List[Tuple[int, int]]
) -> Optional[List[int]]:
    """
    Find a Hamiltonian path using backtracking.

    A Hamiltonian path visits every vertex exactly once.

    Args:
        n: Number of vertices.
        edges: List of (u, v) for an undirected graph.

    Returns:
        A Hamiltonian path as a list of vertices, or None if none exists.

    Time:  O(n!) worst-case
    Space: O(n)
    """
    # Build adjacency set for O(1) neighbour lookup
    adj_set = [set() for _ in range(n)]
    for u, v in edges:
        adj_set[u].add(v)
        adj_set[v].add(u)

    def backtrack(path: List[int], visited: int) -> Optional[List[int]]:
        if len(path) == n:
            return list(path)
        u = path[-1]
        for v in adj_set[u]:
            if not (visited >> v) & 1:
                path.append(v)
                result = backtrack(path, visited | (1 << v))
                if result is not None:
                    return result
                path.pop()
        return None

    for start in range(n):
        result = backtrack([start], 1 << start)
        if result is not None:
            return result

    return None


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    import sys

    all_pass = True

    # ---------- SCC (Kosaraju) ----------
    # Graph: 0→1, 1→2, 2→0, 2→3, 3→4
    scc_edges = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4)]
    scc_k = kosaraju_scc(5, scc_edges)
    # Sort each SCC and the list to compare
    scc_k_sorted = sorted([sorted(c) for c in scc_k])
    expected_scc = sorted([[0, 1, 2], [3], [4]])
    if scc_k_sorted != expected_scc:
        print(f"FAIL kosaraju_scc: {scc_k_sorted} != {expected_scc}")
        all_pass = False

    # ---------- SCC (Tarjan) ----------
    scc_t = tarjan_scc(5, scc_edges)
    scc_t_sorted = sorted([sorted(c) for c in scc_t])
    if scc_t_sorted != expected_scc:
        print(f"FAIL tarjan_scc: {scc_t_sorted} != {expected_scc}")
        all_pass = False

    # ---------- Bridges ----------
    # Graph: triangle 0-1-2 plus bridge 2-3
    bridge_edges = [(0, 1), (1, 2), (2, 0), (2, 3)]
    bridges = find_bridges(4, bridge_edges)
    if set(bridges) != {(2, 3)}:
        print(f"FAIL bridges: {bridges}")
        all_pass = False

    # ---------- Articulation Points ----------
    # Same graph: articulation point is 2
    ap = find_articulation_points(4, bridge_edges)
    if ap != {2}:
        print(f"FAIL articulation_points: {ap}")
        all_pass = False

    # ---------- Eulerian Path ----------
    # Directed graph: 0→1, 1→2, 2→0, 0→3, 3→4
    euler_edges = [(0, 1), (1, 2), (2, 0), (0, 3), (3, 4)]
    euler_path = hierholzer_eulerian_path(5, euler_edges, directed=True)
    if euler_path is None:
        print("FAIL eulerian: no path found")
        all_pass = False
    else:
        if euler_path[0] != 0 or euler_path[-1] != 4 or len(euler_path) != 6:
            print(f"FAIL eulerian path: {euler_path}")
            all_pass = False

    # Undirected: 0-1-2-3
    euler_undirected = [(0, 1), (1, 2), (2, 3)]
    euler_path_u = hierholzer_eulerian_path(4, euler_undirected, directed=False)
    if euler_path_u is None or len(euler_path_u) != 4:
        print(f"FAIL undirected eulerian: {euler_path_u}")
        all_pass = False

    # ---------- Hamiltonian Path ----------
    # Simple line: 0-1-2
    ham_edges = [(0, 1), (1, 2)]
    ham_path = hamiltonian_path(3, ham_edges)
    if ham_path is None or set(ham_path) != {0, 1, 2}:
        print(f"FAIL hamiltonian: {ham_path}")
        all_pass = False

    # Star K_{1,2}: 0-1, 0-2 — Hamiltonian path exists (1-0-2)
    ham_edges2 = [(0, 1), (0, 2)]
    ham_path2 = hamiltonian_path(3, ham_edges2)
    if ham_path2 is None or len(ham_path2) != 3:
        print(f"FAIL hamiltonian star: {ham_path2}")
        all_pass = False

    if all_pass:
        print("All graph applications tests PASSED")
    sys.exit(0 if all_pass else 1)
