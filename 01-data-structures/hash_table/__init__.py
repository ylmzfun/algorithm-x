"""
Hash table data structures.

This package provides:
- HashMap: Key-value store with separate chaining
- HashSet: Unique element set with open addressing (linear probing)
- LRUCache: Least Recently Used cache (manual + OrderedDict variants)
- ConsistentHash: Simple consistent hashing ring
"""

from .hash_map import HashMap
from .hash_set import HashSet
from .lru_cache import LRUCache, LRUCacheOrderedDict
from .consistent_hash import ConsistentHash

__all__ = [
    "HashMap", "HashSet",
    "LRUCache", "LRUCacheOrderedDict",
    "ConsistentHash",
]
