#pragma once

#include <cstdint>
#include <numeric>
#include <vector>

namespace algorithm_x {
namespace math {

// Inclusion-Exclusion Principle: compute union size of n sets.
// `intersections` is a vector where intersections[i] = size of intersection of
// sets indexed by the bits set in i. intersections[0] = 0.
// Example: for sets A, B, C:
//   intersections = {0, |A|, |B|, |A∩B|, |C|, |A∩C|, |B∩C|, |A∩B∩C|}
// Returns |A ∪ B ∪ C|.
inline int64_t inclusion_exclusion(const std::vector<int64_t>& intersections) {
    int n_bits = 0;
    while ((1 << n_bits) < static_cast<int>(intersections.size())) ++n_bits;

    int64_t total = 0;
    for (int mask = 1; mask < static_cast<int>(intersections.size()); ++mask) {
        int bits = __builtin_popcount(mask);
        if (bits % 2 == 1) {
            total += intersections[static_cast<std::size_t>(mask)];
        } else {
            total -= intersections[static_cast<std::size_t>(mask)];
        }
    }
    return total;
}

// Pigeonhole Principle: returns true if placing n items into m boxes
// guarantees at least one box has >1 item.
inline bool pigeonhole(int64_t n, int64_t m) {
    return n > m;
}

// Pigeonhole — generalized: minimum number of items in the fullest box.
inline int64_t pigeonhole_max_min(int64_t n, int64_t m) {
    if (m <= 0) return n;
    return (n + m - 1) / m;  // ceil(n / m)
}

}  // namespace math
}  // namespace algorithm_x
