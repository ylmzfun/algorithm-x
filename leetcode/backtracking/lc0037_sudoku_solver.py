"""
37. Sudoku Solver
https://leetcode.com/problems/sudoku-solver/

Write a program to solve a Sudoku puzzle by filling the empty cells.

A Sudoku solution must satisfy all of the following rules:
1. Each of the digits 1-9 must occur exactly once in each row.
2. Each of the digits 1-9 must occur exactly once in each column.
3. Each of the digits 1-9 must occur exactly once in each of the 9 3x3
   sub-boxes of the grid.

The '.' character indicates empty cells.
"""

from __future__ import annotations


# ──────────────────────────────────────────────────────────────────────────────
# Approach: Backtracking with constraint propagation
# Use three boolean arrays (rows, cols, boxes) to track used digits.
# Find the cell with fewest candidates (MRV heuristic) for pruning.
# Time: O(9^(empty cells)) worst, but heavily pruned.
# Space: O(1) — fixed 9x9 board.
# ──────────────────────────────────────────────────────────────────────────────
def solve_sudoku(board: list[list[str]]) -> None:
    """Solve Sudoku in-place using backtracking with MRV heuristic."""
    rows = [[False] * 9 for _ in range(9)]
    cols = [[False] * 9 for _ in range(9)]
    boxes = [[False] * 9 for _ in range(9)]

    # Initialize constraints from given cells
    for r in range(9):
        for c in range(9):
            if board[r][c] != ".":
                d = int(board[r][c]) - 1
                box_idx = (r // 3) * 3 + (c // 3)
                rows[r][d] = cols[c][d] = boxes[box_idx][d] = True

    def is_valid(r: int, c: int, d: int) -> bool:
        box_idx = (r // 3) * 3 + (c // 3)
        return not (rows[r][d] or cols[c][d] or boxes[box_idx][d])

    def solve() -> bool:
        # Find empty cell with fewest candidates
        min_candidates = 10
        best: tuple[int, int] | None = None
        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    box_idx = (r // 3) * 3 + (c // 3)
                    count = sum(
                        1 for d in range(9)
                        if not (rows[r][d] or cols[c][d] or boxes[box_idx][d])
                    )
                    if count < min_candidates:
                        min_candidates = count
                        best = (r, c)
                        if count == 0:
                            return False

        if best is None:
            return True  # solved

        r, c = best
        box_idx = (r // 3) * 3 + (c // 3)
        for d in range(9):
            if not (rows[r][d] or cols[c][d] or boxes[box_idx][d]):
                rows[r][d] = cols[c][d] = boxes[box_idx][d] = True
                board[r][c] = str(d + 1)
                if solve():
                    return True
                board[r][c] = "."
                rows[r][d] = cols[c][d] = boxes[box_idx][d] = False
        return False

    solve()


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def is_solved(board: list[list[str]]) -> bool:
        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    return False
        # Check rows
        for r in range(9):
            if set(board[r]) != set("123456789"):
                return False
        # Check columns
        for c in range(9):
            if {board[r][c] for r in range(9)} != set("123456789"):
                return False
        # Check boxes
        for br in range(3):
            for bc in range(3):
                vals = set()
                for r in range(3):
                    for c in range(3):
                        vals.add(board[br * 3 + r][bc * 3 + c])
                if vals != set("123456789"):
                    return False
        return True

    def test(label: str, board_in: list[list[str]]):
        import copy
        board = copy.deepcopy(board_in)
        solve_sudoku(board)
        ok = is_solved(board)
        print(f"[{label}] {'✓' if ok else '✗'}")

    test("Example 1", [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ])

    test("Easy puzzle", [
        ["1", ".", ".", ".", ".", "7", ".", "9", "."],
        [".", "3", ".", ".", "2", ".", ".", ".", "8"],
        [".", ".", "9", "6", ".", ".", "5", ".", "."],
        [".", ".", "5", "3", ".", ".", "9", ".", "."],
        [".", "1", ".", ".", "8", ".", ".", ".", "2"],
        ["6", ".", ".", ".", ".", "4", ".", ".", "."],
        ["3", ".", ".", ".", ".", ".", ".", "1", "."],
        [".", "4", ".", ".", ".", ".", ".", ".", "7"],
        [".", ".", "7", ".", ".", ".", "3", ".", "."],
    ])

    print("\nAll sudoku solver tests completed.")
