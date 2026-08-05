"""
Divide & Conquer Module

Classic divide-and-conquer algorithms and problems.
"""

from .divide_conquer import (
    binary_search_dc,
    merge_sort_dc,
    quick_sort_dc,
    find_max_min_dc,
    closest_pair,
    count_inversions,
)

from .pow_functions import (
    fast_pow,
    fast_pow_recursive,
    fast_pow_mod,
    matrix_fast_pow,
    fibonacci_matrix,
)

__all__ = [
    "binary_search_dc",
    "merge_sort_dc",
    "quick_sort_dc",
    "find_max_min_dc",
    "closest_pair",
    "count_inversions",
    "fast_pow",
    "fast_pow_recursive",
    "fast_pow_mod",
    "matrix_fast_pow",
    "fibonacci_matrix",
]
