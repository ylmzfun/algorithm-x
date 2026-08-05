"""
Topological sorting algorithms.

Contains:
- Kahn's algorithm (BFS-based, indegree tracking)
- DFS-based topological sort
- All topological orderings (backtracking)
- Course schedule / cycle detection problems
"""

from collections import deque
from typing import List, Optional, Set, Tuple


# ======================================================================
# Kahn's algorithm (BFS)
# ======================================================================

def kahn_topological_sort(
    n: int, edges: List[Tuple[int, int]]
) -> Optional[List[int]]:
    """
    Topological sort using Kahn's algorithm (BFS with indegree tracking).

    Args:
        n: Number of vertices (0 … n-1).
        edges: List of directed edges (u, v) where u → v.

    Returns:
        A topological ordering as a list of vertices, or None if the graph
        contains a cycle.

    Time:  O(V + E)
    Space: O(V + E)
    """
    # Build adjacency list and indegree array
    adj: List[List[int]] = [[] for _ in range(n)]
    indegree = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indegree[v] += 1

    # Start with all vertices that have indegree 0
    q: deque[int] = deque([i for i in range(n) if indegree[i] == 0])
    order: List[int] = []

    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                q.append(v)

    # If not all vertices visited → cycle exists
    if len(order) != n:
        return None
    return order


# ======================================================================
# DFS-based topological sort
# ======================================================================

def dfs_topological_sort(
    n: int, edges: List[Tuple[int, int]]
) -> Optional[List[int]]:
    """
    Topological sort using DFS with three-colour marking.

    Args:
        n: Number of vertices.
        edges: List of (u, v) directed edges.

    Returns:
        A topological ordering, or None if a cycle is detected.

    Time:  O(V + E)
    Space: O(V + E)
    """
    adj: List[List[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)

    WHITE, GREY, BLACK = 0, 1, 2
    colour = [WHITE] * n
    order: List[int] = []

    def dfs(u: int) -> bool:
        """
        Post-order DFS. Returns False if a cycle is detected.
        """
        colour[u] = GREY
        for v in adj[u]:
            if colour[v] == GREY:
                return False  # back edge → cycle
            if colour[v] == WHITE:
                if not dfs(v):
                    return False
        colour[u] = BLACK
        order.append(u)
        return True

    for i in range(n):
        if colour[i] == WHITE:
            if not dfs(i):
                return None

    order.reverse()
    return order


# ======================================================================
# All topological orderings
# ======================================================================

def all_topological_orderings(
    n: int, edges: List[Tuple[int, int]]
) -> List[List[int]]:
    """
    Enumerate all possible topological orderings of a DAG.

    Uses backtracking with indegree tracking.  May produce many results
    for large graphs — use with caution.

    Args:
        n: Number of vertices.
        edges: List of (u, v).

    Returns:
        All topological orderings (list of lists).  Empty list if cycle exists.

    Time:  O(V! * (V+E)) in worst case (exponential)
    Space: O(V + E)
    """
    adj: List[List[int]] = [[] for _ in range(n)]
    indegree = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indegree[v] += 1

    result: List[List[int]] = []

    def backtrack(path: List[int], indeg: List[int], visited: int) -> None:
        if visited == n:
            result.append(list(path))
            return
        for v in range(n):
            if indeg[v] == 0:  # not yet visited and indegree zero
                path.append(v)
                # temporarily reduce indegree of neighbors
                for nb in adj[v]:
                    indeg[nb] -= 1
                indeg[v] = -1  # mark as visited
                backtrack(path, indeg, visited + 1)
                indeg[v] = 0  # restore
                for nb in adj[v]:
                    indeg[nb] += 1
                path.pop()

    backtrack([], indegree.copy(), 0)

    return result if result else []


# ======================================================================
# Course schedule / cycle detection
# ======================================================================

def can_finish_courses(
    num_courses: int, prerequisites: List[Tuple[int, int]]
) -> Tuple[bool, Optional[List[int]]]:
    """
    Determine whether all courses can be finished (i.e. DAG check).

    This solves LeetCode 207 / 210 (Course Schedule I & II).

    Args:
        num_courses: Number of courses (0 … num_courses-1).
        prerequisites: List of (course, prerequisite) pairs; each
                       means to take `course` you must first take
                       `prerequisite`.

    Returns:
        (possible, order) where possible is True if all courses can be
        completed, and order is a valid course ordering (or None if not
        possible).

    Time:  O(V + E)
    Space: O(V + E)
    """
    # prerequisite → course (directed edge)
    edges = [(pre, course) for course, pre in prerequisites]
    order = kahn_topological_sort(num_courses, edges)
    if order is None:
        return False, None
    return True, order


def has_cycle(n: int, edges: List[Tuple[int, int]]) -> bool:
    """
    Check whether a directed graph contains a cycle.

    Args:
        n: Number of vertices.
        edges: List of (u, v).

    Returns:
        True if the graph contains a cycle.

    Time:  O(V + E)
    """
    return dfs_topological_sort(n, edges) is None


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    import sys

    all_pass = True

    # DAG: 0 → 1 → 3, 0 → 2 → 3, 4 is isolated
    n_dag = 5
    edges_dag = [(0, 1), (0, 2), (1, 3), (2, 3)]

    # --- Kahn ---
    order_k = kahn_topological_sort(n_dag, edges_dag)
    if order_k is None:
        print("FAIL kahn: returned None for DAG")
        all_pass = False
    else:
        # Verify topological ordering property
        pos = {v: i for i, v in enumerate(order_k)}
        for u, v in edges_dag:
            if pos[u] > pos[v]:
                print(f"FAIL kahn: edge {u}→{v} violated order {order_k}")
                all_pass = False

    # --- DFS ---
    order_d = dfs_topological_sort(n_dag, edges_dag)
    if order_d is None:
        print("FAIL dfs_topological: returned None for DAG")
        all_pass = False
    else:
        pos = {v: i for i, v in enumerate(order_d)}
        for u, v in edges_dag:
            if pos[u] > pos[v]:
                print(f"FAIL dfs_topological: edge {u}→{v} violated order {order_d}")
                all_pass = False

    # --- Cycle detection ---
    edges_cycle = [(0, 1), (1, 2), (2, 0)]
    if kahn_topological_sort(3, edges_cycle) is not None:
        print("FAIL kahn: should detect cycle")
        all_pass = False
    if dfs_topological_sort(3, edges_cycle) is not None:
        print("FAIL dfs_topological: should detect cycle")
        all_pass = False
    if not has_cycle(3, edges_cycle):
        print("FAIL has_cycle: should return True")
        all_pass = False

    # --- Course schedule ---
    # Courses: 4, prereqs: [1→0, 2→0, 3→1, 3→2] → [0,1,2,3] or [0,2,1,3]
    possible, order_c = can_finish_courses(4, [(1, 0), (2, 0), (3, 1), (3, 2)])
    if not possible or order_c is None:
        print("FAIL course schedule: should be possible")
        all_pass = False

    # Cycle: 0→1, 1→0
    possible_c, order_cc = can_finish_courses(2, [(0, 1), (1, 0)])
    if possible_c:
        print("FAIL course schedule: should detect cycle")
        all_pass = False

    # --- All topological orderings ---
    # Simple DAG: 0 → 1 → 2
    all_ord = all_topological_orderings(3, [(0, 1), (1, 2)])
    if all_ord != [[0, 1, 2]]:
        print(f"FAIL all_topological: expected [[0,1,2]], got {all_ord}")
        all_pass = False

    # DAG with multiple orderings: 0→1, 0→2
    all_ord2 = all_topological_orderings(3, [(0, 1), (0, 2)])
    expected2 = [[0, 1, 2], [0, 2, 1]]
    if sorted(all_ord2) != sorted(expected2):
        print(f"FAIL all_topological: expected {expected2}, got {sorted(all_ord2)}")
        all_pass = False

    if all_pass:
        print("All topological sort tests PASSED")
    sys.exit(0 if all_pass else 1)
