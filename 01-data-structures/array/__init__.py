"""
Array data structures and common array problem solutions.

This package provides:
- DynamicArray: A resizable array implementation with automatic resizing
- array_problems: Solutions to common array-based algorithmic problems
"""

from .dynamic_array import DynamicArray
from . import array_problems

__all__ = ["DynamicArray", "array_problems"]
