#pragma once

#include <cstdint>

namespace algorithm_x {
namespace algo {

// ---- Bit Manipulation Utilities ----
// Template parameter T should be an unsigned integer type.

// Check if x is odd (lowest bit is 1).
template <typename T>
bool is_odd(T x) { return x & 1; }

// Check if x is a power of two.
template <typename T>
bool is_power_of_two(T x) { return x && !(x & (x - 1)); }

// Extract lowest set bit: x & -x.
template <typename T>
T lowbit(T x) { return x & (~x + 1); }

// Clear lowest set bit: x & (x - 1).
template <typename T>
T clear_lowbit(T x) { return x & (x - 1); }

// Population count (Brian Kernighan algorithm).
template <typename T>
int popcount_bk(T x) {
    int cnt = 0;
    while (x) {
        x &= x - 1;
        ++cnt;
    }
    return cnt;
}

// Compiler built-in popcount for uint32_t and uint64_t.
inline int popcount(uint32_t x) { return __builtin_popcount(x); }
inline int popcount(uint64_t x) { return static_cast<int>(__builtin_popcountll(x)); }

// Set the k-th bit (0-based) to 1.
template <typename T>
T set_bit(T x, int k) { return x | (static_cast<T>(1) << k); }

// Clear the k-th bit (0-based) to 0.
template <typename T>
T clear_bit(T x, int k) { return x & ~(static_cast<T>(1) << k); }

// Toggle the k-th bit.
template <typename T>
T toggle_bit(T x, int k) { return x ^ (static_cast<T>(1) << k); }

// Test if the k-th bit is 1.
template <typename T>
bool test_bit(T x, int k) { return (x >> k) & 1; }

// Enumerate all subsets of {0, 1, ..., n-1} via bitmask.
template <typename Func>
void enumerate_subsets(int n, Func f) {
    for (int mask = 0; mask < (1 << n); ++mask) f(mask);
}

}  // namespace algo
}  // namespace algorithm_x
