"""
Backtracking Algorithms
========================

Backtracking is a systematic way to iterate through all possible
configurations of a search space.  It incrementally builds candidates and
abandons a candidate ("backtracks") as soon as it determines the candidate
cannot lead to a valid solution.

Functions:
- solve_n_queens          : All valid N-Queens board placements.
- solve_sudoku            : Solve a standard 9×9 Sudoku puzzle.
- permutations            : All permutations of distinct numbers.
- permutations_unique     : All permutations with duplicates.
- combinations            : All k-combinations from [1, n].
- subsets                 : All subsets (power set).
- generate_parentheses    : All well-formed parentheses strings.
- letter_combinations     : Letter combinations of a phone number.
- palindrome_partitioning : All palindrome partitions of a string.
"""

from typing import List


# ---------------------------------------------------------------------------
# N-Queens
# ---------------------------------------------------------------------------

def solve_n_queens(n: int) -> List[List[str]]:
    """
    Return all distinct solutions to the N-Queens puzzle.

    Each solution is a board configuration where '.' represents an empty cell
    and 'Q' a queen, with no two queens attacking each other.

    Parameters
    ----------
    n : int
        Board size (n × n).

    Returns
    -------
    List[List[str]]
        List of solutions; each solution is a list of n strings.

    Time  : O(n!) — pruning makes it faster in practice.
    Space : O(n) recursion + O(n²) per stored board.
    """
    solutions: List[List[str]] = []
    # cols[i] = True if column i is occupied
    cols = [False] * n
    # diag1[r+c] = True if main-diagonal r+c is occupied
    diag1 = [False] * (2 * n - 1)
    # diag2[r-c+n-1] = True if anti-diagonal r-c is occupied
    diag2 = [False] * (2 * n - 1)

    board: List[List[str]] = [["."] * n for _ in range(n)]

    def _backtrack(row: int) -> None:
        if row == n:
            solutions.append(["".join(r) for r in board])
            return
        for col in range(n):
            d1 = row + col
            d2 = row - col + n - 1
            if cols[col] or diag1[d1] or diag2[d2]:
                continue
            # Place queen
            board[row][col] = "Q"
            cols[col] = diag1[d1] = diag2[d2] = True
            _backtrack(row + 1)
            # Remove queen (backtrack)
            board[row][col] = "."
            cols[col] = diag1[d1] = diag2[d2] = False

    _backtrack(0)
    return solutions


# ---------------------------------------------------------------------------
# Sudoku Solver
# ---------------------------------------------------------------------------

def solve_sudoku(board: List[List[str]]) -> bool:
    """
    Solve a standard 9×9 Sudoku puzzle in-place.

    Empty cells are represented by '.' and filled cells by digits '1'-'9'.

    Parameters
    ----------
    board : List[List[str]]
        9×9 Sudoku board.  Modified in place if solvable.

    Returns
    -------
    bool
        True if the puzzle is solvable, False otherwise.

    Time  : O(9^(n)) in theory; heavily pruned.
    Space : O(1) auxiliary.
    """
    rows = [[False] * 10 for _ in range(9)]
    cols = [[False] * 10 for _ in range(9)]
    boxes = [[False] * 10 for _ in range(9)]

    # Initialise constraints from pre-filled cells
    for r in range(9):
        for c in range(9):
            if board[r][c] != ".":
                d = int(board[r][c])
                rows[r][d] = cols[c][d] = boxes[(r // 3) * 3 + c // 3][d] = True

    def _backtrack(r: int, c: int) -> bool:
        if r == 9:
            return True
        nr, nc = (r, c + 1) if c < 8 else (r + 1, 0)
        if board[r][c] != ".":
            return _backtrack(nr, nc)

        box_idx = (r // 3) * 3 + c // 3
        for d in range(1, 10):
            if rows[r][d] or cols[c][d] or boxes[box_idx][d]:
                continue
            board[r][c] = str(d)
            rows[r][d] = cols[c][d] = boxes[box_idx][d] = True
            if _backtrack(nr, nc):
                return True
            board[r][c] = "."
            rows[r][d] = cols[c][d] = boxes[box_idx][d] = False
        return False

    return _backtrack(0, 0)


# ---------------------------------------------------------------------------
# Permutations
# ---------------------------------------------------------------------------

def permutations(nums: List[int]) -> List[List[int]]:
    """
    Generate all permutations of a list of distinct integers.

    Parameters
    ----------
    nums : List[int]
        Distinct integers.

    Returns
    -------
    List[List[int]]
        All possible orderings.

    Time  : O(n·n!)
    Space : O(n) recursion.
    """
    result: List[List[int]] = []
    used = [False] * len(nums)
    path: List[int] = []

    def _backtrack() -> None:
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if not used[i]:
                used[i] = True
                path.append(nums[i])
                _backtrack()
                path.pop()
                used[i] = False

    _backtrack()
    return result


# ---------------------------------------------------------------------------
# Permutations with Duplicates
# ---------------------------------------------------------------------------

def permutations_unique(nums: List[int]) -> List[List[int]]:
    """
    Generate all unique permutations when the input may contain duplicates.

    Parameters
    ----------
    nums : List[int]
        List possibly containing duplicates.

    Returns
    -------
    List[List[int]]
        Unique permutations.

    Time  : O(n·n!)
    Space : O(n)
    """
    result: List[List[int]] = []
    nums.sort()
    used = [False] * len(nums)
    path: List[int] = []

    def _backtrack() -> None:
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            # Skip duplicate: only use the first among identical siblings
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            path.append(nums[i])
            _backtrack()
            path.pop()
            used[i] = False

    _backtrack()
    return result


# ---------------------------------------------------------------------------
# Combinations
# ---------------------------------------------------------------------------

def combinations(n: int, k: int) -> List[List[int]]:
    """
    Generate all combinations of k numbers chosen from 1..n.

    Parameters
    ----------
    n : int
        Upper bound (inclusive) of the pool [1, n].
    k : int
        Size of each combination.

    Returns
    -------
    List[List[int]]
        All C(n, k) combinations.

    Time  : O(C(n, k) × k)
    Space : O(k) recursion.
    """
    result: List[List[int]] = []
    path: List[int] = []

    def _backtrack(start: int) -> None:
        if len(path) == k:
            result.append(path[:])
            return
        # Prune: not enough numbers remaining
        need = k - len(path)
        for i in range(start, n - need + 2):
            path.append(i)
            _backtrack(i + 1)
            path.pop()

    _backtrack(1)
    return result


# ---------------------------------------------------------------------------
# Subsets
# ---------------------------------------------------------------------------

def subsets(nums: List[int]) -> List[List[int]]:
    """
    Generate all possible subsets (the power set) of `nums`.

    Parameters
    ----------
    nums : List[int]
        Distinct integers.

    Returns
    -------
    List[List[int]]
        All 2^n subsets.

    Time  : O(n·2^n)
    Space : O(n) recursion.
    """
    result: List[List[int]] = []
    path: List[int] = []

    def _backtrack(idx: int) -> None:
        result.append(path[:])
        for i in range(idx, len(nums)):
            path.append(nums[i])
            _backtrack(i + 1)
            path.pop()

    _backtrack(0)
    return result


# ---------------------------------------------------------------------------
# Generate Parentheses
# ---------------------------------------------------------------------------

def generate_parentheses(n: int) -> List[str]:
    """
    Generate all combinations of n pairs of well-formed parentheses.

    Parameters
    ----------
    n : int
        Number of pairs.

    Returns
    -------
    List[str]
        Valid parentheses strings.

    Time  : O(Catalan(n) × n)  — Catalan(n) = C(2n, n)/(n+1).
    Space : O(n) recursion.
    """
    result: List[str] = []

    def _backtrack(open_cnt: int, close_cnt: int, s: str) -> None:
        if len(s) == 2 * n:
            result.append(s)
            return
        if open_cnt < n:
            _backtrack(open_cnt + 1, close_cnt, s + "(")
        if close_cnt < open_cnt:
            _backtrack(open_cnt, close_cnt + 1, s + ")")

    _backtrack(0, 0, "")
    return result


# ---------------------------------------------------------------------------
# Letter Combinations of a Phone Number
# ---------------------------------------------------------------------------

def letter_combinations(digits: str) -> List[str]:
    """
    Return all possible letter combinations that a phone number could
    represent (traditional T9 mapping).

    Parameters
    ----------
    digits : str
        Digits "2"-"9".

    Returns
    -------
    List[str]
        All letter combinations.

    Time  : O(4^n × n) where n = len(digits).
    Space : O(n) recursion.
    """
    if not digits:
        return []

    mapping = {
        "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
        "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz",
    }
    result: List[str] = []

    def _backtrack(idx: int, s: str) -> None:
        if idx == len(digits):
            result.append(s)
            return
        for ch in mapping[digits[idx]]:
            _backtrack(idx + 1, s + ch)

    _backtrack(0, "")
    return result


# ---------------------------------------------------------------------------
# Palindrome Partitioning
# ---------------------------------------------------------------------------

def _is_palindrome(s: str, lo: int, hi: int) -> bool:
    while lo < hi:
        if s[lo] != s[hi]:
            return False
        lo += 1
        hi -= 1
    return True


def palindrome_partitioning(s: str) -> List[List[str]]:
    """
    Partition `s` such that every substring of the partition is a palindrome.
    Return all possible palindrome partitions.

    Parameters
    ----------
    s : str
        Input string.

    Returns
    -------
    List[List[str]]
        All palindrome partitions.

    Time  : O(n·2^n)
    Space : O(n)
    """
    result: List[List[str]] = []
    path: List[str] = []

    def _backtrack(start: int) -> None:
        if start == len(s):
            result.append(path[:])
            return
        for end in range(start, len(s)):
            if _is_palindrome(s, start, end):
                path.append(s[start:end + 1])
                _backtrack(end + 1)
                path.pop()

    _backtrack(0)
    return result


# ===========================================================================
# Tests
# ===========================================================================

if __name__ == "__main__":
    print("=== Backtracking Tests ===\n")

    # N-Queens
    sols4 = solve_n_queens(4)
    assert len(sols4) == 2, f"4-Queens: expected 2 solutions, got {len(sols4)}"
    sols8 = solve_n_queens(8)
    assert len(sols8) == 92, f"8-Queens: expected 92, got {len(sols8)}"
    print("  PASS solve_n_queens")

    # Sudoku
    board = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]
    assert solve_sudoku(board) == True
    # Quick check: no dots left
    assert all(board[r][c] != "." for r in range(9) for c in range(9))
    print("  PASS solve_sudoku")

    # permutations
    p = permutations([1, 2, 3])
    assert len(p) == 6 and [1, 2, 3] in p
    print("  PASS permutations")

    # permutations_unique
    pu = permutations_unique([1, 1, 2])
    assert len(pu) == 3  # [1,1,2], [1,2,1], [2,1,1]
    print("  PASS permutations_unique")

    # combinations
    c = combinations(4, 2)
    assert len(c) == 6
    assert [1, 2] in c and [3, 4] in c
    print("  PASS combinations")

    # subsets
    ss = subsets([1, 2, 3])
    assert len(ss) == 8
    print("  PASS subsets")

    # generate_parentheses
    gp = generate_parentheses(3)
    assert len(gp) == 5  # Catalan(3) = 5
    assert "((()))" in gp and "()()()" in gp
    print("  PASS generate_parentheses")

    # letter_combinations
    lc = letter_combinations("23")
    assert len(lc) == 9  # "abc" × "def" = 9
    assert "ad" in lc and "cf" in lc
    print("  PASS letter_combinations")

    # palindrome_partitioning
    pp = palindrome_partitioning("aab")
    expected = [["a", "a", "b"], ["aa", "b"]]
    assert sorted(pp) == sorted(expected), f"{pp}"
    print("  PASS palindrome_partitioning")

    print("\nAll backtracking tests completed!")
