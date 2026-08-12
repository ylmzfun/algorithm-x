//! rayon 并行计算
//!
//! 覆盖主题：
//! - 并行归约：求和、求最值（`par_iter` + `sum` / `max`）
//! - 并行变换：`map`、`filter`、并行排序（`par_sort_unstable_by`）
//! - `join` 分治并行，以及 `fold` + `reduce` 的 map-reduce 词频统计
//!
//! 典型场景：CPU 密集且数据量大的运算，把 `iter()` 换成 `par_iter()`
//! 即可自动利用多核；rayon 采用工作窃取调度，无需手动管理线程。

use rayon::prelude::*;
use std::collections::HashMap;

/// 并行求和
///
/// 通过 `par_iter().sum()` 将求和拆分为多个子任务并行执行。
/// 复杂度 O(n)，数据量足够大时接近线性加速比。
pub fn parallel_sum(nums: &[i64]) -> i64 {
    nums.par_iter().sum()
}

/// 并行计算平方
///
/// `par_iter().map(...).collect()` 并行逐元素映射，结果顺序与输入一致。
pub fn parallel_squares(nums: &[i32]) -> Vec<i32> {
    nums.par_iter().map(|&x| x * x).collect()
}

/// 并行降序排序
///
/// `par_sort_unstable_by` 是不稳定并行排序，用 `b.cmp(a)` 得到降序。
/// 复杂度 O(n log n)。
pub fn parallel_sort_desc(nums: &mut [i32]) {
    nums.par_sort_unstable_by(|a, b| b.cmp(a));
}

/// 并行统计偶数个数
///
/// `par_iter().filter(...).count()` 并行过滤并计数。
pub fn parallel_count_evens(nums: &[i32]) -> usize {
    nums.par_iter().filter(|&&x| x % 2 == 0).count()
}

/// 并行求最大值
///
/// `par_iter().copied().max()` 并行归约出最大元素，空输入返回 None。
pub fn parallel_max(nums: &[i64]) -> Option<i64> {
    nums.par_iter().copied().max()
}

/// `join` 分治并行演示
///
/// `rayon::join` 把两个闭包分派到线程池并行执行，两者都完成后返回
/// 结果二元组。这里演示把区间 [0, 200) 拆成两半分别求和（分治思想）。
pub fn join_demo() -> (i64, i64) {
    rayon::join(|| (0..100).sum::<i64>(), || (100..200).sum::<i64>())
}

/// 并行词频统计（map-reduce 模式）
///
/// map 阶段：`fold` 把每个子分区中的单词各自聚合成局部 `HashMap`；
/// reduce 阶段：`reduce` 把所有局部表两两合并。适合海量文本的统计，
/// 可扩展到跨机器框架（如 MapReduce）的同一思路。
pub fn parallel_word_count(words: &[String]) -> HashMap<String, usize> {
    words
        .par_iter()
        .cloned()
        .fold(HashMap::new, |mut m, w| {
            *m.entry(w).or_insert(0) += 1;
            m
        })
        .reduce(HashMap::new, |mut a, b| {
            for (k, v) in b {
                *a.entry(k).or_insert(0) += v;
            }
            a
        })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parallel_sum() {
        let nums = (1..=100).collect::<Vec<i64>>();
        assert_eq!(parallel_sum(&nums), 5050);
    }

    #[test]
    fn test_parallel_squares() {
        assert_eq!(parallel_squares(&[1, 2, 3]), vec![1, 4, 9]);
    }

    #[test]
    fn test_parallel_sort_desc() {
        let mut nums = vec![3, 1, 4, 1, 5];
        parallel_sort_desc(&mut nums);
        assert_eq!(nums, vec![5, 4, 3, 1, 1]);
    }

    #[test]
    fn test_parallel_count_evens() {
        assert_eq!(parallel_count_evens(&[1, 2, 3, 4, 5, 6]), 3);
    }

    #[test]
    fn test_parallel_max() {
        assert_eq!(parallel_max(&[3, 9, 4]), Some(9));
        assert_eq!(parallel_max(&[]), None);
    }

    #[test]
    fn test_join_demo() {
        assert_eq!(join_demo(), (4950, 14950));
    }

    #[test]
    fn test_parallel_word_count() {
        let words: Vec<String> = ["a", "b", "a", "c", "a", "b"]
            .iter()
            .map(|s| s.to_string())
            .collect();
        let counts = parallel_word_count(&words);
        assert_eq!(counts.get("a"), Some(&3));
        assert_eq!(counts.get("b"), Some(&2));
        assert_eq!(counts.get("c"), Some(&1));
        assert_eq!(counts.len(), 3);
    }
}
