"""
133. Clone Graph
https://leetcode.com/problems/clone-graph/

Given a reference of a node in a connected undirected graph.
Return a deep copy (clone) of the graph.

Each node in the graph contains a value (int) and a list (List[Node]) of its neighbors.
"""

from __future__ import annotations
from collections import deque


class Node:
    def __init__(self, val: int = 0, neighbors: list[Node] | None = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


# ──────────────────────────────────────────────────────────────────────────────
# Approach 1: BFS with HashMap
# Time: O(V + E) — visit each node and copy each edge once.
# Space: O(V) — hash map + queue for BFS.
# ──────────────────────────────────────────────────────────────────────────────
def clone_graph_bfs(node: Node | None) -> Node | None:
    """Clone a graph using BFS and a hash map `old -> new`."""
    if not node:
        return None

    clones: dict[Node, Node] = {node: Node(node.val)}
    q: deque[Node] = deque([node])

    while q:
        cur = q.popleft()
        for nei in cur.neighbors:
            if nei not in clones:
                clones[nei] = Node(nei.val)
                q.append(nei)
            clones[cur].neighbors.append(clones[nei])

    return clones[node]


# ──────────────────────────────────────────────────────────────────────────────
# Approach 2: DFS (recursive) with HashMap
# Time: O(V + E)
# Space: O(V) — recursion stack + hash map.
# ──────────────────────────────────────────────────────────────────────────────
def clone_graph_dfs(node: Node | None) -> Node | None:
    """Clone a graph using recursive DFS and a hash map `old -> new`."""
    clones: dict[Node, Node] = {}

    def dfs(cur: Node) -> Node:
        if cur in clones:
            return clones[cur]
        copy = Node(cur.val)
        clones[cur] = copy
        for nei in cur.neighbors:
            copy.neighbors.append(dfs(nei))
        return copy

    return dfs(node) if node else None


# ──────────────────────────────────────────────────────────────────────────────
# Test helpers
# ──────────────────────────────────────────────────────────────────────────────
def build_graph(adj_list: list[list[int]]) -> Node | None:
    """Build a graph from adjacency list (1-indexed values)."""
    if not adj_list:
        return None
    nodes = {i + 1: Node(i + 1) for i in range(len(adj_list))}
    for i, neighbors in enumerate(adj_list):
        for n in neighbors:
            nodes[i + 1].neighbors.append(nodes[n])
    return nodes[1]


def graph_to_adj(node: Node | None, n: int) -> list[list[int]]:
    """Convert cloned graph back to adjacency list for verification."""
    if not node:
        return []
    visited: set[int] = set()
    result: list[list[int]] = [[] for _ in range(n)]

    def dfs(cur: Node) -> None:
        if cur.val in visited:
            return
        visited.add(cur.val)
        result[cur.val - 1] = sorted(n.val for n in cur.neighbors)
        for nei in cur.neighbors:
            dfs(nei)

    dfs(node)
    return result


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, adj: list[list[int]], *args):
        methods = [
            ("BFS", clone_graph_bfs),
            ("DFS", clone_graph_dfs),
        ]
        original = build_graph(adj)
        n = len(adj)
        expected = [sorted(nbrs) for nbrs in adj]

        for name, fn in methods:
            cloned = fn(original) if original else fn(None)
            # Verify structure
            if original:
                assert cloned is not original, f"{name}: same reference"
                assert cloned.val == 1 or n == 0
            if adj:
                result = graph_to_adj(cloned, n)
                ok = result == expected
            else:
                ok = cloned is None
            print(f"[{label}] {name}: {'✓' if ok else '✗'}")

    test("Example 1", [[2, 4], [1, 3], [2, 4], [1, 3]])
    test("Example 2", [[]])
    test("Example 3", [])
    print("\nAll clone graph tests completed.")
