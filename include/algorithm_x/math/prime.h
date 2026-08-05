#pragma once

#include <cmath>
#include <cstddef>
#include <cstdint>
#include <vector>

namespace algorithm_x {
namespace math {

// 试除法判定素数 — O(√n)。
inline bool is_prime_trial(int64_t n) {
    if (n < 2) return false;
    if (n == 2 || n == 3) return true;
    if (n % 2 == 0) return false;
    for (int64_t i = 3; i * i <= n; i += 2)
        if (n % i == 0) return false;
    return true;
}

// Miller-Rabin 素数判定（确定性，适用于 int64_t 范围）。
// 使用已知的确定性底数集合。
inline int64_t mul_mod(int64_t a, int64_t b, int64_t mod) {
    int64_t r = 0;
    a %= mod; b %= mod;
    while (b) {
        if (b & 1) r = (r + a) % mod;
        a = (a + a) % mod;
        b >>= 1;
    }
    return r;
}

inline int64_t pow_mod(int64_t a, int64_t n, int64_t mod) {
    int64_t r = 1;
    a %= mod;
    while (n) {
        if (n & 1) r = mul_mod(r, a, mod);
        a = mul_mod(a, a, mod);
        n >>= 1;
    }
    return r;
}

inline bool is_prime_miller_rabin(int64_t n) {
    if (n < 2) return false;
    if (n == 2 || n == 3) return true;
    if (n % 2 == 0) return false;

    int64_t d = n - 1;
    int s = 0;
    while (d % 2 == 0) { d /= 2; ++s; }

    // 确定性底数，覆盖 n < 2^64
    for (int64_t a : {2, 3, 5, 7, 11, 13, 17}) {
        if (a >= n) continue;
        int64_t x = pow_mod(a, d, n);
        if (x == 1 || x == n - 1) continue;
        bool composite = true;
        for (int r = 0; r < s - 1; ++r) {
            x = mul_mod(x, x, n);
            if (x == n - 1) { composite = false; break; }
        }
        if (composite) return false;
    }
    return true;
}

// ---- Sieve ----

// 埃氏筛 — 返回 [0, n] 的素数表 O(n log log n)。
inline std::vector<bool> sieve_bool(std::size_t n) {
    std::vector<bool> is_prime(n + 1, true);
    is_prime[0] = is_prime[1] = false;
    for (std::size_t i = 2; i * i <= n; ++i)
        if (is_prime[i])
            for (std::size_t j = i * i; j <= n; j += i)
                is_prime[j] = false;
    return is_prime;
}

// 线性筛（欧拉筛）— 同时计算每个数的最小质因子 O(n)。
// 返回 {is_prime, min_prime_factor}。
inline std::pair<std::vector<bool>, std::vector<std::size_t>>
linear_sieve(std::size_t n) {
    std::vector<bool> is_prime(n + 1, true);
    std::vector<std::size_t> min_p(n + 1, 0);
    std::vector<std::size_t> primes;
    is_prime[0] = is_prime[1] = false;

    for (std::size_t i = 2; i <= n; ++i) {
        if (is_prime[i]) {
            primes.push_back(i);
            min_p[i] = i;
        }
        for (std::size_t p : primes) {
            if (i * p > n) break;
            is_prime[i * p] = false;
            min_p[i * p] = p;
            if (i % p == 0) break;
        }
    }
    return {is_prime, min_p};
}

// ---- Factorization ----

// Pollard-Rho 质因数分解 — O(n^(1/4)) 期望。
inline int64_t gcd(int64_t a, int64_t b) {
    while (b) { int64_t t = b; b = a % b; a = t; }
    return a < 0 ? -a : a;
}

inline int64_t pollard_rho(int64_t n) {
    if (n % 2 == 0) return 2;
    if (n % 3 == 0) return 3;

    int64_t x = 2, y = 2, d = 1;
    auto f = [&](int64_t v) { return (mul_mod(v, v, n) + 1) % n; };

    while (d == 1) {
        x = f(x);
        y = f(f(y));
        d = gcd(std::abs(x - y), n);
    }
    return d == n ? pollard_rho(n) : d;
}

inline void factorize(int64_t n, std::vector<int64_t>& factors) {
    if (n == 1) return;
    if (is_prime_miller_rabin(n)) {
        factors.push_back(n);
        return;
    }
    int64_t d = pollard_rho(n);
    factorize(d, factors);
    factorize(n / d, factors);
}

// 质因数分解（入口函数）。先去掉小因子，再用 Pollard-Rho。
inline std::vector<int64_t> prime_factors(int64_t n) {
    std::vector<int64_t> factors;
    if (n < 2) return factors;
    for (int64_t p : {2, 3, 5, 7, 11, 13}) {
        while (n % p == 0) {
            factors.push_back(p);
            n /= p;
        }
    }
    if (n > 1) factorize(n, factors);
    return factors;
}

}  // namespace math
}  // namespace algorithm_x
