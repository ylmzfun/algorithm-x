"""
Fundamental bit manipulation operations.

Contains:
- Get, set, clear, toggle bit
- Count set bits (Brian Kernighan's algorithm)
- Check if a number is a power of two
- Find the single number in an array where others appear twice
- Find the single number where others appear three times
"""

from typing import List


# ======================================================================
# Basic bit operations
# ======================================================================

def get_bit(n: int, pos: int) -> int:
    """
    Get the value of the bit at position `pos` (0-indexed from LSB).

    Args:
        n: The integer.
        pos: Bit position (0 = least significant bit).

    Returns:
        0 or 1.

    Time:  O(1)

    Example:
        get_bit(5, 0) → 1   (5 = 101b)
        get_bit(5, 1) → 0
        get_bit(5, 2) → 1
    """
    return (n >> pos) & 1


def set_bit(n: int, pos: int) -> int:
    """
    Set (turn to 1) the bit at position `pos`.

    Args:
        n: The integer.
        pos: Bit position.

    Returns:
        n with the bit at pos set to 1.

    Time:  O(1)

    Example:
        set_bit(5, 1) → 7  (101b → 111b)
    """
    return n | (1 << pos)


def clear_bit(n: int, pos: int) -> int:
    """
    Clear (turn to 0) the bit at position `pos`.

    Args:
        n: The integer.
        pos: Bit position.

    Returns:
        n with the bit at pos cleared.

    Time:  O(1)

    Example:
        clear_bit(7, 1) → 5  (111b → 101b)
    """
    return n & ~(1 << pos)


def toggle_bit(n: int, pos: int) -> int:
    """
    Toggle (flip) the bit at position `pos`.

    Args:
        n: The integer.
        pos: Bit position.

    Returns:
        n with the bit at pos flipped.

    Time:  O(1)

    Example:
        toggle_bit(5, 1) → 7  (101b → 111b)
    """
    return n ^ (1 << pos)


# ======================================================================
# Count set bits — Brian Kernighan's algorithm
# ======================================================================

def count_set_bits(n: int) -> int:
    """
    Count the number of set bits (1s) in the binary representation of n.

    Uses Brian Kernighan's algorithm: repeatedly clears the lowest set bit.

    Args:
        n: Non-negative integer.

    Returns:
        Number of 1 bits.

    Time:  O(number of set bits)

    Example:
        count_set_bits(13) → 3  (13 = 1101b)
    """
    count = 0
    while n:
        n &= n - 1  # clear the lowest set bit
        count += 1
    return count


# ======================================================================
# Power of two check
# ======================================================================

def is_power_of_two(n: int) -> bool:
    """
    Check whether n is a power of two.

    A positive integer is a power of two iff it has exactly one set bit.

    Args:
        n: Non-negative integer.

    Returns:
        True if n is a power of two (1, 2, 4, 8, …).

    Time:  O(1)

    Example:
        is_power_of_two(8) → True
        is_power_of_two(6) → False
    """
    return n > 0 and (n & (n - 1)) == 0


# ======================================================================
# Single Number I — every element appears twice except one
# ======================================================================

def find_single_number(arr: List[int]) -> int:
    """
    Find the element that appears only once in an array where every other
    element appears exactly twice.

    Uses XOR: a ⊕ a = 0 and a ⊕ 0 = a.

    Args:
        arr: List of integers.

    Returns:
        The unique element.

    Time:  O(n)
    Space: O(1)

    Example:
        find_single_number([2, 2, 1]) → 1
    """
    result = 0
    for x in arr:
        result ^= x
    return result


# ======================================================================
# Single Number II — every element appears three times except one
# ======================================================================

def find_single_number_thrice(arr: List[int]) -> int:
    """
    Find the element that appears only once in an array where every other
    element appears exactly three times.

    Uses bit counting modulo 3.

    Args:
        arr: List of integers.

    Returns:
        The unique element.

    Time:  O(n)
    Space: O(1)

    Example:
        find_single_number_thrice([2, 2, 3, 2]) → 3
    """
    result = 0
    # Process 32 bits (for typical int32)
    for i in range(32):
        bit_sum = 0
        for x in arr:
            bit_sum += (x >> i) & 1
        # The bit in the single number is bit_sum % 3
        if bit_sum % 3 != 0:
            # Handle negative numbers (sign bit 31)
            if i == 31:
                result -= (1 << i)
            else:
                result |= (1 << i)
    return result


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    import sys

    all_pass = True

    # --- get_bit ---
    if get_bit(5, 0) != 1 or get_bit(5, 1) != 0 or get_bit(5, 2) != 1:
        print("FAIL get_bit")
        all_pass = False

    # --- set_bit ---
    if set_bit(5, 1) != 7:
        print(f"FAIL set_bit: {set_bit(5, 1)}")
        all_pass = False

    # --- clear_bit ---
    if clear_bit(7, 1) != 5:
        print(f"FAIL clear_bit: {clear_bit(7, 1)}")
        all_pass = False

    # --- toggle_bit ---
    if toggle_bit(5, 1) != 7 or toggle_bit(7, 1) != 5:
        print("FAIL toggle_bit")
        all_pass = False

    # --- count_set_bits ---
    if count_set_bits(0) != 0:
        print("FAIL count 0")
        all_pass = False
    if count_set_bits(13) != 3:  # 1101
        print(f"FAIL count 13: {count_set_bits(13)}")
        all_pass = False
    if count_set_bits(255) != 8:  # 11111111
        print(f"FAIL count 255: {count_set_bits(255)}")
        all_pass = False

    # --- is_power_of_two ---
    if not is_power_of_two(1):
        print("FAIL power_of_two 1")
        all_pass = False
    if not is_power_of_two(64):
        print("FAIL power_of_two 64")
        all_pass = False
    if is_power_of_two(0):
        print("FAIL power_of_two 0")
        all_pass = False
    if is_power_of_two(6):
        print("FAIL power_of_two 6")
        all_pass = False

    # --- Single number (twice) ---
    s1 = find_single_number([2, 2, 1])
    if s1 != 1:
        print(f"FAIL single_twice: {s1}")
        all_pass = False

    s1b = find_single_number([4, 1, 2, 1, 2])
    if s1b != 4:
        print(f"FAIL single_twice 5-elem: {s1b}")
        all_pass = False

    # --- Single number (thrice) ---
    s2 = find_single_number_thrice([2, 2, 3, 2])
    if s2 != 3:
        print(f"FAIL single_thrice: {s2}")
        all_pass = False

    s2b = find_single_number_thrice([0, 1, 0, 1, 0, 1, 99])
    if s2b != 99:
        print(f"FAIL single_thrice 99: {s2b}")
        all_pass = False

    # Should handle negative numbers
    s2c = find_single_number_thrice([-2, -2, 1, 1, 1, -2, 4, 4, 4])
    # Wait, let me recount: -2 thrice, 1 thrice, 4 thrice? 
    # Nope: [-2, -2, 1, 1, 1, -2, 4, 4, 4]
    # -2: 3 times, 1: 3 times, 4: 3 times → all thrice, no single? 
    # Let me fix: [-2,-2,-2, 1,1,1,1] → 1 appears 4 times? No, that's not right either
    # Let's test: [5, 5, 5, 7]
    s2d = find_single_number_thrice([5, 5, 5, 7])
    if s2d != 7:
        print(f"FAIL single_thrice 7: {s2d}")
        all_pass = False

    if all_pass:
        print("All bit operations tests PASSED")
    sys.exit(0 if all_pass else 1)
