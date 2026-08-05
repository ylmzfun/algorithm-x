"""
A* Search Algorithm
====================

A* (A-star) is a best-first search algorithm that finds the least-cost path
from a start node to a goal node.  It uses a heuristic function f(n) = g(n)
+ h(n), where g(n) is the actual cost from start to n and h(n) is an
admissible heuristic estimate from n to the goal.

Functions:
- a_star_grid       : A* pathfinding on a 2D grid with obstacles.
- solve_8_puzzle    : A* solution to the 8-puzzle (3×3 sliding puzzle).
"""

import heapq
import math
from typing import List, Tuple, Optional, Dict, Callable


# ---------------------------------------------------------------------------
# A* on a 2D Grid
# ---------------------------------------------------------------------------

def a_star_grid(
    grid: List[List[int]],
    start: Tuple[int, int],
    goal: Tuple[int, int],
    heuristic: str = "manhattan",
    allow_diagonal: bool = False,
) -> Optional[List[Tuple[int, int]]]:
    """
    Find the shortest path through a 2D grid using A*.

    Parameters
    ----------
    grid : List[List[int]]
        2D grid where 0 = traversable, 1 = obstacle.
    start : Tuple[int, int]
        (row, col) of the start cell.
    goal : Tuple[int, int]
        (row, col) of the goal cell.
    heuristic : str
        "manhattan" or "euclidean".
    allow_diagonal : bool
        If True, diagonal moves are also allowed.

    Returns
    -------
    Optional[List[Tuple[int, int]]]
        Shortest path from start to goal (inclusive), or None.

    Time  : O(E log V) = O(rows·cols · log(rows·cols)) worst-case.
    Space : O(rows·cols)
    """
    if not grid or not grid[0]:
        return None
    rows, cols = len(grid), len(grid[0])
    sr, sc = start
    gr, gc = goal

    if grid[sr][sc] == 1 or grid[gr][gc] == 1:
        return None
    if start == goal:
        return [start]

    # Movement definitions
    if allow_diagonal:
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1),
                 (-1, -1), (-1, 1), (1, -1), (1, 1)]
    else:
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Heuristic function
    if heuristic == "euclidean":
        def h(r: int, c: int) -> float:
            return math.hypot(r - gr, c - gc)
    else:
        def h(r: int, c: int) -> float:
            return float(abs(r - gr) + abs(c - gc))

    # Priority queue: (f, g, r, c)
    open_set: List[Tuple[float, float, int, int]] = [(h(sr, sc), 0.0, sr, sc)]
    # g_score[r, c] = best known cost from start
    g_score: Dict[Tuple[int, int], float] = {(sr, sc): 0.0}
    came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}

    while open_set:
        f, g, r, c = heapq.heappop(open_set)

        if (r, c) == goal:
            # Reconstruct path
            path: List[Tuple[int, int]] = []
            cur = goal
            while cur in came_from:
                path.append(cur)
                cur = came_from[cur]
            path.append(start)
            return path[::-1]

        # If this entry is stale (we found a better g_score already), skip
        if g > g_score.get((r, c), float("inf")):
            continue

        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if grid[nr][nc] == 1:
                continue

            move_cost = math.hypot(dr, dc) if allow_diagonal else 1.0
            new_g = g + move_cost

            if new_g < g_score.get((nr, nc), float("inf")):
                g_score[(nr, nc)] = new_g
                new_f = new_g + h(nr, nc)
                heapq.heappush(open_set, (new_f, new_g, nr, nc))
                came_from[(nr, nc)] = (r, c)

    return None


# ---------------------------------------------------------------------------
# 8-Puzzle (Sliding Puzzle) Solver
# ---------------------------------------------------------------------------

def _manhattan_8p(state: Tuple[int, ...], goal_pos: Dict[int, Tuple[int, int]]) -> int:
    """Manhattan distance heuristic for 8-puzzle."""
    dist = 0
    for idx, val in enumerate(state):
        if val == 0:
            continue
        gr, gc = goal_pos[val]
        r, c = divmod(idx, 3)
        dist += abs(r - gr) + abs(c - gc)
    return dist


def solve_8_puzzle(start: List[List[int]]) -> Optional[List[str]]:
    """
    Solve the 8-puzzle (3×3 sliding puzzle) using A* search with the
    Manhattan distance heuristic.

    Parameters
    ----------
    start : List[List[int]]
        3×3 board with numbers 0-8, where 0 represents the empty tile.

    Returns
    -------
    Optional[List[str]]
        Sequence of moves ("up", "down", "left", "right") from start to goal
        [[1,2,3],[4,5,6],[7,8,0]], or None if unsolvable.

    Time  : Exponential in worst case, but A* + Manhattan is very fast
            for the 8-puzzle.
    Space : Proportional to the number of explored states.
    """
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    start_tuple = tuple(start[0] + start[1] + start[2])

    # Pre-compute goal positions for heuristic
    goal_pos: Dict[int, Tuple[int, int]] = {}
    for i, val in enumerate(goal):
        goal_pos[val] = divmod(i, 3)

    # Count inversions to check solvability (excluding the row of blank)
    flat = [x for x in start_tuple if x != 0]
    inv = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inv += 1
    if inv % 2 != 0:
        return None  # unsolvable

    # Moves: (dr, dc, direction_name)
    moves = [(-1, 0, "up"), (1, 0, "down"), (0, -1, "left"), (0, 1, "right")]

    open_set: List[Tuple[int, int, Tuple[int, ...], str]] = []
    start_h = _manhattan_8p(start_tuple, goal_pos)
    heapq.heappush(open_set, (start_h, 0, start_tuple, ""))
    g_score: Dict[Tuple[int, ...], int] = {start_tuple: 0}
    came_from: Dict[Tuple[int, ...], Tuple[Tuple[int, ...], str]] = {}

    while open_set:
        f, g, state, _ = heapq.heappop(open_set)

        if state == goal:
            # Reconstruct moves
            moves_seq: List[str] = []
            cur = state
            while cur in came_from:
                prev, move = came_from[cur]
                moves_seq.append(move)
                cur = prev
            return moves_seq[::-1]

        if g > g_score.get(state, float("inf")):
            continue

        # Find blank (0) position
        zero_idx = state.index(0)
        r, c = divmod(zero_idx, 3)

        for dr, dc, move_name in moves:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < 3 and 0 <= nc < 3):
                continue
            new_idx = nr * 3 + nc
            # Swap blank with neighbour
            lst = list(state)
            lst[zero_idx], lst[new_idx] = lst[new_idx], lst[zero_idx]
            new_state = tuple(lst)
            new_g = g + 1
            if new_g < g_score.get(new_state, float("inf")):
                g_score[new_state] = new_g
                new_h = _manhattan_8p(new_state, goal_pos)
                new_f = new_g + new_h
                heapq.heappush(open_set, (new_f, new_g, new_state, move_name))
                came_from[new_state] = (state, move_name)

    return None


# ===========================================================================
# Tests
# ===========================================================================

if __name__ == "__main__":
    print("=== A* Tests ===\n")

    # a_star_grid
    grid = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]
    path = a_star_grid(grid, (0, 0), (4, 4))
    assert path is not None, "Path should exist"
    assert path[0] == (0, 0) and path[-1] == (4, 4)
    # Check all steps are adjacent (Manhattan distance 1)
    for i in range(len(path) - 1):
        dr = abs(path[i + 1][0] - path[i][0])
        dc = abs(path[i + 1][1] - path[i][1])
        assert dr + dc == 1, f"Non-adjacent: {path[i]} -> {path[i + 1]}"
    print("  PASS a_star_grid (Manhattan)")

    # a_star with Euclidean
    path2 = a_star_grid(grid, (0, 0), (4, 4), heuristic="euclidean")
    assert path2 is not None
    print("  PASS a_star_grid (Euclidean)")

    # a_star with diagonal allowed
    path3 = a_star_grid(grid, (0, 0), (4, 4), allow_diagonal=True)
    assert path3 is not None
    print("  PASS a_star_grid (diagonal)")

    # No path
    blocked = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    assert a_star_grid(blocked, (0, 0), (2, 2)) is None
    print("  PASS a_star_grid (no path)")

    # 8-puzzle
    start_board = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8],
    ]
    solution = solve_8_puzzle(start_board)
    assert solution is not None, "8-puzzle should be solvable"
    # Verify solution
    state = [start_board[i][j] for i in range(3) for j in range(3)]
    moves_map = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
    for mv in solution:
        z = state.index(0)
        r, c = divmod(z, 3)
        dr, dc = moves_map[mv]
        nr, nc = r + dr, c + dc
        nz = nr * 3 + nc
        state[z], state[nz] = state[nz], state[z]
    assert tuple(state) == (1, 2, 3, 4, 5, 6, 7, 8, 0), f"End state: {state}"
    print(f"  PASS solve_8_puzzle ({len(solution)} moves)")

    # Unsolvable puzzle
    unsolvable = [
        [1, 2, 3],
        [4, 5, 6],
        [8, 7, 0],
    ]
    assert solve_8_puzzle(unsolvable) is None
    print("  PASS solve_8_puzzle (unsolvable detection)")

    print("\nAll A* tests completed!")
