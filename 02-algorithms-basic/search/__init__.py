"""
Search Algorithms Module

Graph and tree search algorithms: BFS, DFS, backtracking, and A*.
"""

from .bfs import (
    bfs_shortest_path,
    bfs_shortest_path_grid,
    word_ladder,
    min_moves_grid,
)

from .dfs import (
    dfs_recursive,
    dfs_iterative,
    flood_fill,
    num_islands,
    surrounded_regions,
    word_search,
)

from .backtracking import (
    solve_n_queens,
    solve_sudoku,
    permutations,
    permutations_unique,
    combinations,
    subsets,
    generate_parentheses,
    letter_combinations,
    palindrome_partitioning,
)

from .a_star import (
    a_star_grid,
    solve_8_puzzle,
)

__all__ = [
    # BFS
    "bfs_shortest_path",
    "bfs_shortest_path_grid",
    "word_ladder",
    "min_moves_grid",
    # DFS
    "dfs_recursive",
    "dfs_iterative",
    "flood_fill",
    "num_islands",
    "surrounded_regions",
    "word_search",
    # Backtracking
    "solve_n_queens",
    "solve_sudoku",
    "permutations",
    "permutations_unique",
    "combinations",
    "subsets",
    "generate_parentheses",
    "letter_combinations",
    "palindrome_partitioning",
    # A*
    "a_star_grid",
    "solve_8_puzzle",
]
