"""
Binary Search Module

The classic O(log n) divide-and-conquer searching technique for sorted data.
"""

from .binary_search import (
    binary_search,
    binary_search_first_occurrence,
    binary_search_last_occurrence,
    binary_search_first_ge,
    binary_search_last_le,
)

__all__ = [
    "binary_search",
    "binary_search_first_occurrence",
    "binary_search_last_occurrence",
    "binary_search_first_ge",
    "binary_search_last_le",
]
