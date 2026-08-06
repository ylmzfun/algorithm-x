/// 位运算技巧
///
/// 常用位运算：
/// - `&` (AND), `|` (OR), `^` (XOR), `~` (NOT)
/// - `<<` (左移), `>>` (右移)
///
/// 常见技巧：
/// - `x & (x - 1)`: 清除最低位的 1
/// - `x & -x`: 获取最低位的 1
/// - `x ^ x = 0`, `x ^ 0 = x`

/// 统计二进制表示中 1 的个数（汉明重量）
///
/// Brian Kernighan 算法：每次 `n & (n - 1)` 清除最低位的 1。
pub fn hamming_weight(mut n: u32) -> u32 {
    let mut count = 0;
    while n != 0 {
        n &= n - 1;
        count += 1;
    }
    count
}

/// 是否是 2 的幂
///
/// 2 的幂的二进制表示只有一个 1。
pub fn is_power_of_two(n: u32) -> bool {
    n > 0 && n & (n - 1) == 0
}

/// 只出现一次的数字
///
/// 数组中除一个元素外其他都出现两次，找到它。
/// 利用 XOR 性质：a ^ a = 0, a ^ 0 = a
pub fn single_number(nums: &[i32]) -> i32 {
    nums.iter().fold(0, |acc, &x| acc ^ x)
}

/// 颠倒二进制位
pub fn reverse_bits(mut n: u32) -> u32 {
    let mut result = 0u32;
    for _ in 0..32 {
        result = (result << 1) | (n & 1);
        n >>= 1;
    }
    result
}

/// 位运算实现加法
///
/// a ^ b 得到无进位加法的结果，(a & b) << 1 得到进位。
pub fn add_bitwise(mut a: i32, mut b: i32) -> i32 {
    while b != 0 {
        let carry = (a & b) << 1;
        a ^= b;
        b = carry;
    }
    a
}

/// 缺失的数字
///
/// [0, n] 的 n 个数，缺少一个，找到它。
/// XOR 所有索引和值。
pub fn missing_number(nums: &[i32]) -> i32 {
    let n = nums.len() as i32;
    let mut result = n;
    for (i, &x) in nums.iter().enumerate() {
        result ^= i as i32 ^ x;
    }
    result
}

/// 生成 [0, n) 所有大小为 k 的子集的位掩码表示
///
/// 使用 Gosper's Hack 迭代所有大小为 k 的子集。
pub fn k_subsets(n: usize, k: usize) -> Vec<usize> {
    if k == 0 {
        return vec![0];
    }
    if k > n {
        return vec![];
    }
    let mut result = Vec::new();
    let mut mask = (1usize << k) - 1;
    let limit = 1usize << n;

    while mask < limit {
        result.push(mask);
        // Gosper's Hack: next combination
        let c = mask & mask.wrapping_neg();
        let r = mask + c;
        mask = (((r ^ mask) >> 2) / c) | r;
    }
    result
}

/// 不使用额外变量交换两个整数
pub fn swap_xor(a: &mut i32, b: &mut i32) {
    *a ^= *b;
    *b ^= *a;
    *a ^= *b;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hamming_weight() {
        assert_eq!(hamming_weight(0b1011), 3);
        assert_eq!(hamming_weight(0), 0);
    }

    #[test]
    fn test_is_power_of_two() {
        assert!(is_power_of_two(1));
        assert!(is_power_of_two(2));
        assert!(is_power_of_two(64));
        assert!(!is_power_of_two(3));
        assert!(!is_power_of_two(0));
    }

    #[test]
    fn test_single_number() {
        assert_eq!(single_number(&[2, 2, 1]), 1);
        assert_eq!(single_number(&[4, 1, 2, 1, 2]), 4);
    }

    #[test]
    fn test_reverse_bits() {
        // 43261596 (0b00000010100101000001111010011100) → 964176192
        assert_eq!(reverse_bits(43261596), 964176192);
    }

    #[test]
    fn test_add_bitwise() {
        assert_eq!(add_bitwise(5, 3), 8);
        assert_eq!(add_bitwise(-2, 3), 1);
    }

    #[test]
    fn test_missing_number() {
        assert_eq!(missing_number(&[3, 0, 1]), 2);
        assert_eq!(missing_number(&[0, 1]), 2);
    }

    #[test]
    fn test_swap_xor() {
        let mut a = 5;
        let mut b = 10;
        swap_xor(&mut a, &mut b);
        assert_eq!(a, 10);
        assert_eq!(b, 5);
    }
}
