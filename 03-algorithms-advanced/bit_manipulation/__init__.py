"""Bit manipulation package."""

from .bit_operations import (
    get_bit,
    set_bit,
    clear_bit,
    toggle_bit,
    count_set_bits,
    is_power_of_two,
    find_single_number,
    find_single_number_thrice,
)
from .bit_applications import (
    generate_subsets,
    gray_code,
    tsp_bit_dp,
    assign_tasks_bit_dp,
    subset_sum_bitset,
)

__all__ = [
    # Bit operations
    "get_bit",
    "set_bit",
    "clear_bit",
    "toggle_bit",
    "count_set_bits",
    "is_power_of_two",
    "find_single_number",
    "find_single_number_thrice",
    # Bit applications
    "generate_subsets",
    "gray_code",
    "tsp_bit_dp",
    "assign_tasks_bit_dp",
    "subset_sum_bitset",
]
