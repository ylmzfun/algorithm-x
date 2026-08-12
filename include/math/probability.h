#pragma once

#include <cmath>
#include <cstddef>
#include <numeric>
#include <vector>

namespace algorithm_x {
namespace math {

// Expected value of a discrete random variable.
// E[X] = sum(p_i * x_i)
inline double expected_value(const std::vector<double>& probs,
                              const std::vector<double>& values) {
    double ev = 0.0;
    for (std::size_t i = 0; i < probs.size(); ++i) {
        ev += probs[i] * values[i];
    }
    return ev;
}

// Binomial coefficient C(n,k) — helper for binomial probability.
inline double binomial_coeff_double(int n, int k) {
    if (k < 0 || k > n) return 0.0;
    if (k == 0 || k == n) return 1.0;
    double r = 1.0;
    for (int i = 1; i <= k; ++i) {
        r = r * static_cast<double>(n - k + i) / static_cast<double>(i);
    }
    return r;
}

// Binomial probability: P(X = k) = C(n,k) * p^k * (1-p)^(n-k)
inline double binomial_probability(int n, int k, double p) {
    if (k < 0 || k > n) return 0.0;
    double comb = binomial_coeff_double(n, k);
    double pk = std::pow(p, k);
    double qnk = std::pow(1.0 - p, n - k);
    return comb * pk * qnk;
}

}  // namespace math
}  // namespace algorithm_x
