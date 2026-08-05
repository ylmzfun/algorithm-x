"""Advanced string algorithms package."""

from .kmp import kmp_search, build_lps, kmp_count_occurrences
from .rabin_karp import rabin_karp_search, rabin_karp_multi_pattern
from .manacher import longest_palindromic_substring, count_palindromic_substrings
from .z_algorithm import z_algorithm, z_algorithm_search
from .suffix_automaton import SuffixAutomaton

__all__ = [
    # KMP
    "kmp_search",
    "build_lps",
    "kmp_count_occurrences",
    # Rabin-Karp
    "rabin_karp_search",
    "rabin_karp_multi_pattern",
    # Manacher
    "longest_palindromic_substring",
    "count_palindromic_substrings",
    # Z Algorithm
    "z_algorithm",
    "z_algorithm_search",
    # Suffix Automaton
    "SuffixAutomaton",
]
