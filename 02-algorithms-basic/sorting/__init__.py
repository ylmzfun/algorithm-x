"""
Sorting Algorithms Module

This module contains implementations of various sorting algorithms,
categorized into:

- comparison_sorts: O(n²) and O(n log n) comparison-based sorts
- linear_sorts: Non-comparison sorts achieving O(n) time
- sort_problems: Classic problems that use sorting techniques
"""

from .comparison_sorts import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    shell_sort,
    merge_sort,
    merge_sort_iterative,
    merge_sort_bottom_up,
    quick_sort,
    quick_sort_three_way,
    heap_sort,
)

from .linear_sorts import (
    counting_sort,
    bucket_sort,
    radix_sort_lsd,
)

from .sort_problems import (
    sort_colors,
    find_kth_largest,
    merge_intervals,
    sort_nearly_sorted,
)

__all__ = [
    # Comparison sorts
    "bubble_sort",
    "selection_sort",
    "insertion_sort",
    "shell_sort",
    "merge_sort",
    "merge_sort_iterative",
    "merge_sort_bottom_up",
    "quick_sort",
    "quick_sort_three_way",
    "heap_sort",
    # Linear sorts
    "counting_sort",
    "bucket_sort",
    "radix_sort_lsd",
    # Sort problems
    "sort_colors",
    "find_kth_largest",
    "merge_intervals",
    "sort_nearly_sorted",
]
