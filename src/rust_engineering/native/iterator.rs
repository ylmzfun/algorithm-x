//! 迭代器核心算法
//!
//! 覆盖主题：
//! - 适配器：`map` / `filter` / `filter_map` / `enumerate` / `zip`
//! - 归约：`scan` / `partition` / `flatten` / `collect`
//! - collect 到 `Result`（`?` 传播与短路）
//! - 自定义 `Iterator` 实现（Fibonacci）
//!
//! 迭代器是惰性的：适配器链本身不执行，直到 `collect` / `sum` / `for` 等
//! 消费性操作触发求值。

use std::collections::HashMap;

/// 斐波那契迭代器
///
/// 语义：内部状态为 `(a, b)`，初始 `(0, 1)`；每次 `next()` 产出当前 `b`，
/// 并把状态滚动为 `(b, a + b)`，因此依次产生 1, 1, 2, 3, 5, 8, ...
#[derive(Debug, Clone)]
pub struct Fibonacci {
    a: u64,
    b: u64,
}

impl Fibonacci {
    /// 创建从 1, 1 开始的斐波那契迭代器
    pub fn new() -> Self {
        Fibonacci { a: 0, b: 1 }
    }
}

impl Default for Fibonacci {
    fn default() -> Self {
        Self::new()
    }
}

impl Iterator for Fibonacci {
    type Item = u64;

    fn next(&mut self) -> Option<u64> {
        let next = self.b;
        self.b += self.a;
        self.a = next;
        Some(next)
    }
}

/// 取斐波那契数列前 n 项
///
/// 组合自定义迭代器与 `take` / `collect`。复杂度 O(n)。
pub fn fibonacci_take(n: usize) -> Vec<u64> {
    Fibonacci::new().take(n).collect()
}

/// 前缀和（running sum）
///
/// `scan` 维护一个跨元素的状态（这里是累加器），每个元素产生一个输出。
/// 复杂度 O(n)。典型场景：前缀和预处理、状态压缩遍历。
pub fn running_sum(nums: &[i32]) -> Vec<i32> {
    nums.iter()
        .scan(0, |acc, &x| {
            *acc += x;
            Some(*acc)
        })
        .collect()
}

/// 偶数的平方
///
/// `filter` 保留偶数，`map` 变换为平方，链式组合两个适配器。
/// 复杂度 O(n)。
pub fn squares_of_evens(nums: &[i32]) -> Vec<i32> {
    nums.iter()
        .filter(|&&x| x % 2 == 0)
        .map(|&x| x * x)
        .collect()
}

/// 词频统计
///
/// 用 `HashMap::entry` 的 `or_insert` 对每个单词计数（一次遍历）。
/// 复杂度 O(n) 期望。典型场景：文本分析、关键词统计。
pub fn word_frequency<'a>(words: &'a [&'a str]) -> HashMap<&'a str, usize> {
    let mut freq = HashMap::new();
    for &w in words {
        *freq.entry(w).or_insert(0) += 1;
    }
    freq
}

/// 按奇偶分组
///
/// `Iterator::partition` 一次遍历把元素分为满足 / 不满足谓词两组，
/// 返回 `(偶数, 奇数)`，组内保持原有相对顺序。复杂度 O(n)。
pub fn group_by_parity(nums: &[i32]) -> (Vec<i32>, Vec<i32>) {
    nums.iter().copied().partition(|&x| x % 2 == 0)
}

/// 两个数组逐元素求和
///
/// `zip` 将两个迭代器按位配对，长度取较短者（多出的部分丢弃）。
/// 复杂度 O(min(n, m))。典型场景：向量加法、按列合并。
pub fn zip_sum(a: &[i32], b: &[i32]) -> Vec<i32> {
    a.iter().zip(b.iter()).map(|(&x, &y)| x + y).collect()
}

/// 展平二维数组
///
/// `flatten` 把 `Iterator<Item = Vec<i32>>` 展平为 `Iterator<Item = i32>`。
/// 复杂度 O(元素总数)。典型场景：二维矩阵拉直、嵌套列表合并。
pub fn flatten_2d(matrix: &[Vec<i32>]) -> Vec<i32> {
    matrix.iter().flatten().copied().collect()
}

/// 把字符串数组全部解析为整数
///
/// `collect::<Result<Vec<_>, _>>()`：任一个解析失败立即返回第一个错误，
/// 展示 `?` 的错误短路（而不是收集部分成功的结果）。
pub fn try_parse_all(nums: &[&str]) -> Result<Vec<i64>, std::num::ParseIntError> {
    nums.iter().map(|s| s.parse::<i64>()).collect()
}

/// 取出奇数元素及其原始下标
///
/// `enumerate` 给元素带上下标，`filter` 保留奇数，`map` 重组为 `(下标, 值)`。
/// 复杂度 O(n)。
pub fn enumerate_odds(nums: &[i32]) -> Vec<(usize, i32)> {
    nums.iter()
        .enumerate()
        .filter(|&(_, &x)| x % 2 == 1)
        .map(|(i, &x)| (i, x))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_fibonacci() {
        assert_eq!(fibonacci_take(8), vec![1, 1, 2, 3, 5, 8, 13, 21]);
        assert_eq!(fibonacci_take(0), Vec::<u64>::new());
        assert_eq!(Fibonacci::new().nth(9), Some(55));
    }

    #[test]
    fn test_running_sum() {
        assert_eq!(running_sum(&[1, 2, 3, 4]), vec![1, 3, 6, 10]);
        assert_eq!(running_sum(&[]), Vec::<i32>::new());
    }

    #[test]
    fn test_squares_of_evens() {
        assert_eq!(squares_of_evens(&[1, 2, 3, 4, 5, 6]), vec![4, 16, 36]);
    }

    #[test]
    fn test_word_frequency() {
        let freq = word_frequency(&["a", "b", "a", "c", "a"]);
        assert_eq!(freq.get("a"), Some(&3));
        assert_eq!(freq.get("b"), Some(&1));
        assert_eq!(freq.get("z"), None);
    }

    #[test]
    fn test_group_by_parity() {
        let (evens, odds) = group_by_parity(&[1, 2, 3, 4, 5, 6]);
        assert_eq!(evens, vec![2, 4, 6]);
        assert_eq!(odds, vec![1, 3, 5]);
    }

    #[test]
    fn test_zip_sum() {
        assert_eq!(zip_sum(&[1, 2, 3], &[10, 20, 30]), vec![11, 22, 33]);
        assert_eq!(zip_sum(&[1, 2], &[1, 2, 3]), vec![2, 4]); // 取较短者
    }

    #[test]
    fn test_flatten_2d() {
        assert_eq!(flatten_2d(&[vec![1, 2], vec![3], vec![]]), vec![1, 2, 3]);
    }

    #[test]
    fn test_try_parse_all() {
        assert_eq!(try_parse_all(&["1", "2"]), Ok(vec![1, 2]));
        assert!(try_parse_all(&["1", "x"]).is_err());
    }

    #[test]
    fn test_enumerate_odds() {
        assert_eq!(enumerate_odds(&[2, 5, 8, 9]), vec![(1, 5), (3, 9)]);
    }
}
