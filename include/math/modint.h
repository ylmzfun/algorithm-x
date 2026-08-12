#pragma once

#include <cstddef>
#include <cstdint>
#include <tuple>
#include <vector>

namespace algorithm_x {
namespace math {

// ---- GCD & Extended ----

// 扩展欧几里得算法 — 解 ax + by = gcd(a, b)。
// 返回 {gcd, x, y}。
inline std::tuple<int64_t, int64_t, int64_t>
extended_gcd(int64_t a, int64_t b) {
    if (b == 0) return {a, 1, 0};
    auto [g, x1, y1] = extended_gcd(b, a % b);
    return {g, y1, x1 - (a / b) * y1};
}

// 最大公约数。
inline int64_t gcd_ext(int64_t a, int64_t b) {
    return std::get<0>(extended_gcd(a, b));
}

// ---- Modular Arithmetic ----

// 模逆元 — a^(-1) mod m，要求 gcd(a, m) = 1。
inline int64_t mod_inverse(int64_t a, int64_t m) {
    auto [g, x, y] = extended_gcd(a, m);
    return (x % m + m) % m;
}

// 快速幂 — a^n % mod。
inline int64_t fast_pow(int64_t a, int64_t n, int64_t mod) {
    int64_t r = 1 % mod;
    a %= mod;
    while (n) {
        if (n & 1) r = (r * a) % mod;
        a = (a * a) % mod;
        n >>= 1;
    }
    return r;
}

// ---- CRT & Totient ----

// 中国剩余定理 (CRT)。
// 求解 x ≡ r[i] (mod m[i])，其中所有 m[i] 两两互质。
// 返回最小非负解，M = product of m[i]。
inline int64_t crt(const std::vector<int64_t>& r,
                    const std::vector<int64_t>& m) {
    int64_t M = 1;
    for (int64_t mi : m) M *= mi;

    int64_t x = 0;
    for (std::size_t i = 0; i < r.size(); ++i) {
        int64_t Mi = M / m[i];
        int64_t inv = mod_inverse(Mi, m[i]);
        x = (x + r[i] * Mi % M * inv) % M;
    }
    return (x + M) % M;
}

// 欧拉函数 φ(n) — O(√n)。
inline int64_t euler_phi(int64_t n) {
    int64_t result = n;
    for (int64_t p = 2; p * p <= n; ++p) {
        if (n % p == 0) {
            while (n % p == 0) n /= p;
            result -= result / p;
        }
    }
    if (n > 1) result -= result / n;
    return result;
}

}  // namespace math
}  // namespace algorithm_x
