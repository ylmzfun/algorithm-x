/// 数学算法
///
/// - 素数筛
/// - 最大公约数 / 最小公倍数
/// - 快速幂
/// - 组合数

/// 埃拉托色尼筛 (Sieve of Eratosthenes)
///
/// 找出 [2, n] 范围内的所有素数。
/// 时间复杂度 O(n log log n)
pub fn sieve_of_eratosthenes(n: usize) -> Vec<usize> {
    if n < 2 {
        return vec![];
    }
    let mut is_prime = vec![true; n + 1];
    is_prime[0] = false;
    is_prime[1] = false;

    let mut i = 2;
    while i * i <= n {
        if is_prime[i] {
            let mut j = i * i;
            while j <= n {
                is_prime[j] = false;
                j += i;
            }
        }
        i += 1;
    }

    (2..=n).filter(|&i| is_prime[i]).collect()
}

/// 判断 n 是否为素数 — O(√n)
pub fn is_prime(n: u64) -> bool {
    if n < 2 {
        return false;
    }
    if n == 2 || n == 3 {
        return true;
    }
    if n % 2 == 0 || n % 3 == 0 {
        return false;
    }
    let mut i = 5;
    while i * i <= n {
        if n % i == 0 || n % (i + 2) == 0 {
            return false;
        }
        i += 6;
    }
    true
}

/// 最大公约数 (GCD) — 欧几里得算法
pub fn gcd(mut a: u64, mut b: u64) -> u64 {
    while b != 0 {
        let temp = b;
        b = a % b;
        a = temp;
    }
    a
}

/// 最小公倍数 (LCM)
pub fn lcm(a: u64, b: u64) -> u64 {
    if a == 0 || b == 0 {
        return 0;
    }
    a / gcd(a, b) * b
}

/// 扩展欧几里得算法
///
/// 求 ax + by = gcd(a, b) 的一组整数解 (x, y)。
pub fn extended_gcd(a: i64, b: i64) -> (i64, i64, i64) {
    if b == 0 {
        (a, 1, 0)
    } else {
        let (g, x1, y1) = extended_gcd(b, a % b);
        (g, y1, x1 - (a / b) * y1)
    }
}

/// 快速幂 — 计算 x^n mod m
pub fn mod_pow(x: i64, mut n: u64, m: i64) -> i64 {
    if m == 1 {
        return 0;
    }
    let mut result = 1i64 % m;
    let mut base = x % m;
    while n > 0 {
        if n & 1 == 1 {
            result = (result as i128 * base as i128 % m as i128) as i64;
        }
        base = (base as i128 * base as i128 % m as i128) as i64;
        n >>= 1;
    }
    result
}

/// 组合数 C(n, k) — 乘法逆元法
///
/// C(n, k) = n! / (k! * (n-k)!) mod MOD
pub fn combination_mod(n: usize, k: usize, modulo: i64) -> i64 {
    if k > n {
        return 0;
    }
    let k = k.min(n - k);

    let mut numerator = 1i64;
    let mut denominator = 1i64;

    for i in 0..k {
        numerator = (numerator * (n - i) as i64) % modulo;
        denominator = (denominator * (i + 1) as i64) % modulo;
    }

    // 求 denominator 的逆元
    let inv = mod_inverse(denominator, modulo);
    (numerator * inv) % modulo
}

/// 乘法逆元（费马小定理，模数为素数时）
fn mod_inverse(a: i64, m: i64) -> i64 {
    mod_pow(a, (m - 2) as u64, m)
}

/// 生成帕斯卡三角的前 n 行
pub fn pascals_triangle(n: usize) -> Vec<Vec<u64>> {
    let mut triangle: Vec<Vec<u64>> = Vec::with_capacity(n);
    for i in 0..n {
        let mut row = vec![1u64; i + 1];
        for j in 1..i {
            row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j];
        }
        triangle.push(row);
    }
    triangle
}

/// 分数到小数
///
/// 返回分数的字符串表示，如果有循环节，用括号括起来。
/// 如 1/3 = "0.(3)", 1/6 = "0.1(6)"
pub fn fraction_to_decimal(numerator: i64, denominator: i64) -> String {
    if numerator == 0 {
        return "0".to_string();
    }
    let sign = if (numerator < 0) ^ (denominator < 0) {
        "-"
    } else {
        ""
    };
    let num = (numerator as i64).abs() as u64;
    let den = (denominator as i64).abs() as u64;

    let integer = num / den;
    let mut remainder = num % den;

    if remainder == 0 {
        return format!("{}{}", sign, integer);
    }

    let mut fractional = String::new();
    let mut map = std::collections::HashMap::new();
    let mut pos = 0;

    while remainder != 0 {
        if let Some(&start) = map.get(&remainder) {
            fractional.insert(start, '(');
            fractional.push(')');
            break;
        }
        map.insert(remainder, pos);
        remainder *= 10;
        fractional.push_str(&(remainder / den).to_string());
        remainder %= den;
        pos += 1;
    }

    format!("{}{}.{}", sign, integer, fractional)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sieve() {
        assert_eq!(sieve_of_eratosthenes(20), vec![2, 3, 5, 7, 11, 13, 17, 19]);
    }

    #[test]
    fn test_is_prime() {
        assert!(is_prime(2));
        assert!(is_prime(17));
        assert!(!is_prime(1));
        assert!(!is_prime(15));
    }

    #[test]
    fn test_gcd_lcm() {
        assert_eq!(gcd(12, 18), 6);
        assert_eq!(gcd(17, 13), 1);
        assert_eq!(lcm(4, 6), 12);
    }

    #[test]
    fn test_extended_gcd() {
        let (g, x, y) = extended_gcd(30, 12);
        assert_eq!(g, 6);
        assert_eq!(30 * x + 12 * y, 6);
    }

    #[test]
    fn test_mod_pow() {
        assert_eq!(mod_pow(2, 10, 1000), 24);
        assert_eq!(mod_pow(3, 5, 13), 9);
    }

    #[test]
    fn test_combination_mod() {
        let modulo = 1_000_000_007;
        assert_eq!(combination_mod(5, 2, modulo), 10);
        assert_eq!(combination_mod(10, 3, modulo), 120);
    }

    #[test]
    fn test_pascals_triangle() {
        let rows = pascals_triangle(5);
        assert_eq!(rows[0], vec![1]);
        assert_eq!(rows[1], vec![1, 1]);
        assert_eq!(rows[2], vec![1, 2, 1]);
        assert_eq!(rows[3], vec![1, 3, 3, 1]);
        assert_eq!(rows[4], vec![1, 4, 6, 4, 1]);
    }

    #[test]
    fn test_fraction_to_decimal() {
        assert_eq!(fraction_to_decimal(1, 2), "0.5");
        assert_eq!(fraction_to_decimal(1, 3), "0.(3)");
        assert_eq!(fraction_to_decimal(1, 6), "0.1(6)");
        assert_eq!(fraction_to_decimal(-50, 8), "-6.25");
    }
}
