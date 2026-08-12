//! itertools 迭代器增强
//!
//! 覆盖主题：去重排序、组合/排列、按频率分组取前 K、minmax、
//! 相邻元素成对、笛卡尔积、分块求和、交错合并、不等长 zip 填充。
//!
//! 典型场景：算法题中常见的"去重 + 排序"、"取前 K 高频"、
//! "两两相邻对"等操作，用 itertools 一行即可表达。

use itertools::{Itertools, iproduct};

/// 去重并排序
///
/// `unique()` 保持首次出现顺序去重，`sorted()` 升序排序。
/// 复杂度 O(n log n)。
pub fn unique_sorted(nums: &[i32]) -> Vec<i32> {
    nums.iter().copied().unique().sorted().collect()
}

/// 取 k 个元素的所有无序组合
///
/// `combinations(k)` 按输入顺序枚举 C(n, k) 种组合。
/// 组合数量随输入规模指数增长，只适合小输入。
pub fn combinations_k(nums: &[i32], k: usize) -> Vec<Vec<i32>> {
    nums.iter().copied().combinations(k).collect()
}

/// 字符串全排列个数
///
/// `permutations(k)` 枚举所有排列并计数，k 取字符个数；
/// n 个互异字符结果为 n!，只适合短字符串（测试用长度 ≤5）。
pub fn anagram_count(s: &str) -> usize {
    s.chars().permutations(s.chars().count()).count()
}

/// 按频率降序取前 k 个高频词
///
/// `into_group_map_by(|w| *w)` 把元素按自身分组，得到
/// `HashMap<&str, Vec<&str>>`；再按组大小降序排序取前 k 个转成 String。
/// （itertools 0.14 的分组闭包接收 `&V`，故需 `*w` 解引用回 `&str`。）
pub fn top_k_frequent(words: &[&str], k: usize) -> Vec<String> {
    let groups = words.iter().copied().into_group_map_by(|w| *w);
    let mut items: Vec<(&str, usize)> = groups.into_iter().map(|(w, v)| (w, v.len())).collect();
    items.sort_unstable_by_key(|&(_, count)| std::cmp::Reverse(count));
    items
        .into_iter()
        .take(k)
        .map(|(w, _)| w.to_string())
        .collect()
}

/// 一次遍历同时求最小值与最大值
///
/// `minmax()` 返回 `MinMaxResult`，三个变体分别对应空输入、
/// 单元素、以及同时含最小最大值的正常情形。
pub fn min_max(nums: &[i32]) -> Option<(i32, i32)> {
    match nums.iter().copied().minmax() {
        itertools::MinMaxResult::NoElements => None,
        itertools::MinMaxResult::OneElement(x) => Some((x, x)),
        itertools::MinMaxResult::MinMax(a, b) => Some((a, b)),
    }
}

/// 相邻元素两两成对
///
/// `tuple_windows()` 产生 (a0,a1),(a1,a2),... 的滑动窗口，
/// 长度 n 的输入得到 n-1 对。
pub fn consecutive_pairs(nums: &[i32]) -> Vec<(i32, i32)> {
    nums.iter().copied().tuple_windows().collect()
}

/// 两个集合的笛卡尔积
///
/// `iproduct!` 宏生成 a × b 的全部组合，先固定 a 中元素再遍历 b。
/// 结果规模为 |a| × |b|。
pub fn cartesian_product(a: &[i32], b: &[i32]) -> Vec<(i32, i32)> {
    iproduct!(a.iter().copied(), b.iter().copied()).collect()
}

/// 按固定大小分块并对每块求和
///
/// `chunks(size)` 产生惰性分块，必须 `.into_iter()` 后才能逐块消费；
/// 最后一块可能不足 size 个元素。
pub fn chunk_sums(nums: &[i32], size: usize) -> Vec<i32> {
    nums.iter()
        .copied()
        .chunks(size)
        .into_iter()
        .map(|c| c.sum::<i32>())
        .collect()
}

/// 交错合并两个序列
///
/// `interleave` 轮流取两边元素，先耗尽的一边停止，剩余元素保持原序
/// 追加到末尾。
pub fn interleave(a: &[i32], b: &[i32]) -> Vec<i32> {
    a.iter().copied().interleave(b.iter().copied()).collect()
}

/// 不等长 zip：短边不足时由长边元素补齐
///
/// `zip_longest` 在两边都有元素时产生 `Both`，仅剩一边时产生
/// `Left`/`Right`；这里的映射规则是"优先取 a 的元素，a 耗尽后用
/// b 的元素补齐"，因此结果长度等于两边长度的较大者。
pub fn zip_longest_pad(a: &[i32], b: &[i32]) -> Vec<i32> {
    a.iter()
        .copied()
        .zip_longest(b.iter().copied())
        .map(|e| match e {
            itertools::EitherOrBoth::Left(x)
            | itertools::EitherOrBoth::Both(x, _)
            | itertools::EitherOrBoth::Right(x) => x,
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_unique_sorted() {
        assert_eq!(unique_sorted(&[3, 1, 3, 2, 1]), vec![1, 2, 3]);
    }

    #[test]
    fn test_combinations_k() {
        let mut got = combinations_k(&[1, 2, 3], 2);
        got.sort();
        assert_eq!(got, vec![vec![1, 2], vec![1, 3], vec![2, 3]]);
    }

    #[test]
    fn test_anagram_count() {
        assert_eq!(anagram_count("abc"), 6);
    }

    #[test]
    fn test_top_k_frequent() {
        let got = top_k_frequent(&["a", "b", "a", "c", "a", "b"], 2);
        assert_eq!(got, vec!["a".to_string(), "b".to_string()]);
    }

    #[test]
    fn test_min_max() {
        assert_eq!(min_max(&[3, 1, 4, 1, 5]), Some((1, 5)));
        assert_eq!(min_max(&[7]), Some((7, 7)));
        assert_eq!(min_max(&[]), None);
    }

    #[test]
    fn test_consecutive_pairs() {
        assert_eq!(
            consecutive_pairs(&[1, 2, 3, 4]),
            vec![(1, 2), (2, 3), (3, 4)]
        );
    }

    #[test]
    fn test_cartesian_product() {
        let got = cartesian_product(&[1, 2], &[3, 4]);
        assert_eq!(got.len(), 4);
        assert!(got.contains(&(1, 3)));
        assert!(got.contains(&(1, 4)));
        assert!(got.contains(&(2, 3)));
        assert!(got.contains(&(2, 4)));
    }

    #[test]
    fn test_chunk_sums() {
        assert_eq!(chunk_sums(&[1, 2, 3, 4, 5], 2), vec![3, 7, 5]);
    }

    #[test]
    fn test_interleave() {
        assert_eq!(interleave(&[1, 2, 3], &[10, 20]), vec![1, 10, 2, 20, 3]);
    }

    #[test]
    fn test_zip_longest_pad() {
        // b 更长：Both(1,10)→1、Both(2,20)→2、Right(30)→30
        assert_eq!(zip_longest_pad(&[1, 2], &[10, 20, 30]), vec![1, 2, 30]);
        // a 更长：多余部分 Left 直接透传
        assert_eq!(zip_longest_pad(&[1, 2, 3], &[10]), vec![1, 2, 3]);
    }
}
