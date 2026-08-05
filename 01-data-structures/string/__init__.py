"""
String data structures.

This package provides:
- trie: Trie (prefix tree) for efficient string prefix operations
- suffix_array: Suffix array and LCP array construction
- aho_corasick: Aho-Corasick automaton for multi-pattern matching
"""

from .trie import TrieNode, Trie
from .suffix_array import SuffixArray
from .aho_corasick import AhoCorasick

__all__ = [
    "TrieNode", "Trie",
    "SuffixArray",
    "AhoCorasick",
]
