//! num-bigint 大整数运算
//!
//! 覆盖主题：大数阶乘、斐波那契、模幂、数位和、十进制字符串解析。
//!
//! 典型场景：需要超过 u64 范围的整数运算（如阶乘、密码学模幂）。
//! `BigUint` 是无符号任意精度整数，底层按 limb 存储，运算自动扩容。

use num_bigint::BigUint;

/// 计算 n 的阶乘
///
/// 从 2 累乘到 n，结果用 `BigUint` 表示可支持任意大；n=0 时返回 1。
/// 复杂度 O(n log n)（乘法开销随位数增长）。
pub fn factorial(n: u32) -> BigUint {
    (2..=n).fold(BigUint::from(1u32), |acc, i| acc * i)
}

/// 计算第 n 个斐波那契数（F0=0, F1=1）
///
/// 用两个 `BigUint` 迭代递推，避免递归爆炸；n=100 时结果已达 21 位，
/// 普通 u64 早已溢出，正是大整数的用武之地。
pub fn fibonacci(n: u32) -> BigUint {
    if n == 0 {
        return BigUint::from(0u32);
    }
    let mut a = BigUint::from(0u32);
    let mut b = BigUint::from(1u32);
    for _ in 1..n {
        let next = &a + &b;
        a = b;
        b = next;
    }
    b
}

/// 快速模幂 base^exp mod modulus
///
/// `BigUint::modpow` 内置平方-乘算法（O(log exp) 次乘法），
/// 是密码学与数论中的常用原语，可避免中间结果爆炸。
pub fn mod_pow(base: u64, exp: u64, modulus: u64) -> BigUint {
    BigUint::from(base).modpow(&BigUint::from(exp), &BigUint::from(modulus))
}

/// 大整数的十进制数位和
///
/// 先 `to_string()` 得到十进制表示，再逐字符累加数字。
/// 复杂度 O(位数)。
pub fn digits_sum(n: &BigUint) -> u32 {
    n.to_string().chars().filter_map(|c| c.to_digit(10)).sum()
}

/// 解析十进制字符串为 BigUint
///
/// `BigUint::parse_bytes(s, 10)` 支持任意长度的十进制串；
/// 非法输入（空串、含非数字字符、负数前缀）返回 None。
pub fn from_dec_str(s: &str) -> Option<BigUint> {
    BigUint::parse_bytes(s.as_bytes(), 10)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_factorial() {
        assert_eq!(factorial(5), BigUint::from(120u32));
        assert_eq!(factorial(0), BigUint::from(1u32));
    }

    #[test]
    fn test_fibonacci() {
        assert_eq!(fibonacci(10), BigUint::from(55u32));
        let s = fibonacci(100).to_string();
        assert_eq!(s.len(), 21);
        assert_eq!(s, "354224848179261915075");
    }

    #[test]
    fn test_mod_pow() {
        // 7³ = 343，343 mod 13 = 5
        assert_eq!(mod_pow(7, 3, 13), BigUint::from(5u32));
    }

    #[test]
    fn test_digits_sum() {
        assert_eq!(digits_sum(&BigUint::from(12345u32)), 15);
    }

    #[test]
    fn test_from_dec_str() {
        let n = from_dec_str("12345678901234567890").unwrap();
        assert_eq!(n.to_string(), "12345678901234567890");
        assert!(from_dec_str("12a34").is_none());
        assert!(from_dec_str("").is_none());
    }
}
