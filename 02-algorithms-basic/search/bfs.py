"""
Breadth-First Search (BFS) Algorithms
======================================

BFS explores a graph level by level using a queue.  It is optimal for
unweighted graphs and finds the shortest path in terms of the number of
edges.

Functions:
- bfs_shortest_path       : Generic BFS for adjacency-list graphs.
- bfs_shortest_path_grid  : BFS on a 2D grid (4-directional / 8-dir).
- word_ladder             : Shortest transformation sequence between words.
- min_moves_grid          : Minimum moves in a grid with obstacles.
"""

from collections import deque
from typing import List, Dict, Set, Optional, Tuple, Callable


# ---------------------------------------------------------------------------
# Generic BFS Shortest Path (adjacency list)
# ---------------------------------------------------------------------------

def bfs_shortest_path(graph: Dict[int, List[int]], start: int,
                      target: int) -> Optional[List[int]]:
    """
    Find the shortest path (fewest edges) from `start` to `target` in an
    unweighted graph represented as an adjacency list.

    Parameters
    ----------
    graph : Dict[int, List[int]]
        Adjacency list: node -> list of neighbours.
    start : int
        Starting node.
    target : int
        Target node.

    Returns
    -------
    Optional[List[int]]
        List of nodes representing the shortest path (inclusive of start and
        target), or None if no path exists.

    Time  : O(V + E)
    Space : O(V)
    """
    if start == target:
        return [start]

    queue: deque[int] = deque([start])
    visited: Dict[int, int] = {start: -1}  # node -> parent

    while queue:
        u = queue.popleft()
        for v in graph.get(u, []):
            if v not in visited:
                visited[v] = u
                if v == target:
                    # Reconstruct path
                    path: List[int] = []
                    cur = v
                    while cur != -1:
                        path.append(cur)
                        cur = visited[cur]
                    return path[::-1]
                queue.append(v)
    return None


# ---------------------------------------------------------------------------
# BFS on Grid (Shortest Path in Maze)
# ---------------------------------------------------------------------------

def bfs_shortest_path_grid(
    grid: List[List[int]],
    start: Tuple[int, int],
    target: Tuple[int, int],
    directions: int = 4,
) -> Optional[int]:
    """
    Find the shortest-path distance in a 2D grid from `start` to `target`.

    ``grid[i][j] == 0`` means traversable, ``1`` means obstacle.

    Parameters
    ----------
    grid : List[List[int]]
        2D grid (0 = free, 1 = obstacle).
    start : Tuple[int, int]
        (row, col) of the start.
    target : Tuple[int, int]
        (row, col) of the target.
    directions : int
        4 for cardinal directions (up, down, left, right) or 8 for also
        diagonals.

    Returns
    -------
    Optional[int]
        Minimum number of steps, or None if unreachable.

    Time  : O(rows × cols)
    Space : O(rows × cols)
    """
    if not grid or not grid[0]:
        return None
    rows, cols = len(grid), len(grid[0])

    dirs: List[Tuple[int, int]]
    if directions == 8:
        dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                (0, 1), (1, -1), (1, 0), (1, 1)]
    else:
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    sr, sc = start
    tr, tc = target
    if grid[sr][sc] == 1 or grid[tr][tc] == 1:
        return None
    if start == target:
        return 0

    queue: deque[Tuple[int, int, int]] = deque([(sr, sc, 0)])
    visited: Set[Tuple[int, int]] = {(sr, sc)}

    while queue:
        r, c, dist = queue.popleft()
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if (nr, nc) not in visited and grid[nr][nc] == 0:
                    if (nr, nc) == target:
                        return dist + 1
                    visited.add((nr, nc))
                    queue.append((nr, nc, dist + 1))
    return None


# ---------------------------------------------------------------------------
# Word Ladder
# ---------------------------------------------------------------------------

def word_ladder(begin_word: str, end_word: str,
                word_list: List[str]) -> int:
    """
    Find the length of the shortest transformation sequence from begin_word
    to end_word, where each intermediate word must exist in word_list and
    adjacent words differ by exactly one letter.

    Parameters
    ----------
    begin_word : str
        Starting word.
    end_word : str
        Target word.
    word_list : List[str]
        Dictionary of valid words.  Must contain end_word for a valid path.

    Returns
    -------
    int
        Number of words in the shortest transformation sequence (including
        begin_word), or 0 if no sequence exists.

    Time  : O(M²·N) where M = word length, N = number of words.
            Can be optimised to O(M²·N) with pattern-based neighbour finding.
    Space : O(N)

    Example
    -------
    >>> word_ladder("hit", "cog", ["hot","dot","dog","lot","log","cog"])
    5   # hit -> hot -> dot -> dog -> cog
    """
    word_set = set(word_list)
    if end_word not in word_set:
        return 0

    queue: deque[Tuple[str, int]] = deque([(begin_word, 1)])
    visited: Set[str] = {begin_word}

    while queue:
        word, steps = queue.popleft()
        if word == end_word:
            return steps

        # Generate all possible one-letter transformations
        for i in range(len(word)):
            for ch in "abcdefghijklmnopqrstuvwxyz":
                new_word = word[:i] + ch + word[i + 1:]
                if new_word in word_set and new_word not in visited:
                    visited.add(new_word)
                    queue.append((new_word, steps + 1))
    return 0


# ---------------------------------------------------------------------------
# Minimum Moves in Grid
# ---------------------------------------------------------------------------

def min_moves_grid(grid: List[List[int]]) -> int:
    """
    Find the minimum number of moves to go from top-left (0, 0) to
    bottom-right (rows-1, cols-1) in a grid.  You may only move to cells
    with value 0 (free).  Moves are allowed up, down, left, right.

    This is a specialisation of ``bfs_shortest_path_grid``.

    Parameters
    ----------
    grid : List[List[int]]
        2D grid (0 = free, 1 = obstacle).

    Returns
    -------
    int
        Minimum number of steps, or -1 if unreachable.

    Time  : O(rows × cols)
    Space : O(rows × cols)
    """
    if not grid or not grid[0]:
        return -1
    rows, cols = len(grid), len(grid[0])
    if grid[0][0] == 1 or grid[rows - 1][cols - 1] == 1:
        return -1

    res = bfs_shortest_path_grid(grid, (0, 0), (rows - 1, cols - 1))
    return res if res is not None else -1


# ===========================================================================
# Tests
# ===========================================================================

if __name__ == "__main__":
    print("=== BFS Tests ===\n")

    # bfs_shortest_path
    g: Dict[int, List[int]] = {
        0: [1, 2], 1: [0, 3], 2: [0, 3, 4],
        3: [1, 2, 5], 4: [2, 5], 5: [3, 4]
    }
    path = bfs_shortest_path(g, 0, 5)
    assert path is not None and len(path) == 4, f"Failed: {path}"
    assert bfs_shortest_path(g, 0, 6) is None
    assert bfs_shortest_path(g, 0, 0) == [0]
    print("  PASS bfs_shortest_path")

    # bfs_shortest_path_grid
    grid = [
        [0, 0, 0],
        [1, 1, 0],
        [0, 0, 0],
    ]
    d = bfs_shortest_path_grid(grid, (0, 0), (2, 2))
    assert d == 4, f"Expected 4, got {d}"
    # Test unreachable: fully blocked
    blocked = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    d2 = bfs_shortest_path_grid(blocked, (0, 0), (2, 2))
    assert d2 is None
    print("  PASS bfs_shortest_path_grid")

    # word_ladder
    wl = word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"])
    assert wl == 5, f"word_ladder: expected 5, got {wl}"
    wl2 = word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log"])
    assert wl2 == 0, f"word_ladder (no path): expected 0, got {wl2}"
    print("  PASS word_ladder")

    # min_moves_grid
    assert min_moves_grid(grid) == 4
    blocked = [[0, 1], [1, 0]]
    assert min_moves_grid(blocked) == -1
    single = [[0]]
    assert min_moves_grid(single) == 0
    print("  PASS min_moves_grid")

    print("\nAll BFS tests completed!")
