"""
Tree data structures.

This package provides:
- binary_tree: Basic binary tree operations and traversals
- binary_search_tree: BST with search, insert, delete, range queries
- avl_tree: Self-balancing AVL tree with rotations
- red_black_tree: Simplified Red-Black tree with recoloring/rotations
- segment_tree: Segment tree with range queries and lazy propagation
"""

from . import binary_tree
from . import binary_search_tree
from . import avl_tree
from . import red_black_tree
from . import segment_tree

__all__ = [
    "binary_tree", "binary_search_tree",
    "avl_tree", "red_black_tree", "segment_tree",
]
