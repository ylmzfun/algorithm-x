#pragma once

#include <cstddef>
#include <cstdint>
#include <vector>

namespace algorithm_x {
namespace math {

// Catalan number C(n) = (2n)! / (n! * (n+1)!)
inline int64_t catalan_number(int n) {
    if (n <= 1) return 1;
    // C(n) = C(n-1) * 2*(2n-1) / (n+1)
    int64_t res = 1;
    for (int i = 1; i <= n; ++i) {
        res = res * 2 * (2 * i - 1) / (i + 1);
    }
    return res;
}

// Binomial coefficient C(n, k) — multiplicative formula.
inline int64_t binomial(int n, int k) {
    if (k < 0 || k > n) return 0;
    if (k > n - k) k = n - k;
    int64_t res = 1;
    for (int i = 0; i < k; ++i) {
        res = res * (n - i) / (i + 1);
    }
    return res;
}

}  // namespace math
}  // namespace algorithm_x
