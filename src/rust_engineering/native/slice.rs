//! 切片 / Vec 核心算法
//!
//! 覆盖主题：
//! - 排序变体与快速选择：`sort_unstable`、`select_nth_unstable`（top-k、第 k 大）
//! - 二分查找与边界：`binary_search`、`partition_point`（lower_bound / upper_bound）
//! - 原地分区与去重：双指针手写实现（`partition` / `partition_dedup` 见下方说明）
//! - 旋转与窗口：`rotate_right`、`windows`、`chunks`
//! - 安全索引：`get` / `get_mut` / `split_at_mut`
//!
//! # 说明
//!
//! `[T]::partition` 与 `[T]::partition_dedup` 在本工具链上尚不可用
//! （前者未稳定、后者仍为 unstable feature），故本文件用手写双指针版本
//! 实现等价语义，复杂度不变。
//!
//! # 安全索引
//!
//! 直接用下标 `a[i]` 越界会 panic，而 `get` / `get_mut` 返回 `Option`，
//! 越界得到 `None`，需要"可失败访问"或链式处理时更安全。
//!
//! ```
//! let mut a = [1, 2, 3, 4];
//! assert_eq!(a.get(0), Some(&1));
//! assert_eq!(a.get(99), None); // 越界返回 None，不 panic
//! assert_eq!(a.get_mut(2), Some(&mut 3));
//! ```
//!
//! `split_at_mut` 把一个切片拆成两段互不重叠的可变借用，从而可以同时修改
//! 两个位置而不触发借用冲突（这正是 `&mut a[i]` + `&mut a[j]` 做不到的）。
//!
//! ```
//! let mut a = [1, 2, 3, 4];
//! let (left, right) = a.split_at_mut(2);
//! left[0] = 10;
//! right[1] = 40;
//! assert_eq!(a, [10, 2, 3, 40]);
//! ```

/// 统计有序数组中 target 的出现次数（lower_bound / upper_bound 之差）
///
/// 用 `partition_point` 分别求出第一个 `>= target` 与第一个 `> target` 的
/// 下标，二者之差即为出现次数。要求输入已升序排列。
/// 复杂度 O(log n)。典型场景：有序容器中的频次统计。
pub fn binary_search_count(sorted: &[i32], target: i32) -> usize {
    let lower = sorted.partition_point(|&x| x < target);
    let upper = sorted.partition_point(|&x| x <= target);
    upper - lower
}

/// 中位数
///
/// 排序后取中间元素；偶数长度时取中间两数平均。
/// 用 `total_cmp` 对 f64 排序，NaN 也有确定顺序。空输入返回 `f64::NAN`。
/// 复杂度 O(n log n)。典型场景：统计、离群值分析。
pub fn median(nums: &mut [f64]) -> f64 {
    if nums.is_empty() {
        return f64::NAN;
    }
    nums.sort_by(|a, b| a.total_cmp(b));
    let n = nums.len();
    if n % 2 == 1 {
        nums[n / 2]
    } else {
        (nums[n / 2 - 1] + nums[n / 2]) / 2.0
    }
}

/// 最小的 k 个元素（top-k）
///
/// `select_nth_unstable(k - 1)` 快速选择后，前 k 个位置即包含最小的 k 个
/// 元素，再排序保证输出升序。平均复杂度 O(n)。典型场景：排行榜截取。
pub fn top_k_smallest(nums: &mut [i32], k: usize) -> Vec<i32> {
    let k = k.min(nums.len());
    if k == 0 {
        return Vec::new();
    }
    nums.select_nth_unstable(k - 1);
    nums[..k].sort_unstable();
    nums[..k].to_vec()
}

/// 第 k 大元素（k 从 1 计）
///
/// 等价于第 `n - k` 小：`select_nth_unstable(n - k)` 后该下标元素即处于
/// 最终有序位置。前提 `1 <= k <= nums.len()`。平均复杂度 O(n)。
pub fn kth_largest(nums: &mut [i32], k: usize) -> i32 {
    let idx = nums.len() - k;
    nums.select_nth_unstable(idx);
    nums[idx]
}

/// 原地分区：偶数在前、奇数在后
///
/// 双指针扫描：`boundary` 指向下一个偶数应放置的位置，每遇到一个偶数就
/// 与 `boundary` 处交换并前移。返回值即偶数个数，也即偶数区间的边界
/// （`[0, n)` 全部为偶数）。复杂度 O(n)。典型场景：荷兰国旗问题的两色简化版。
pub fn partition_evens_odds(nums: &mut [i32]) -> usize {
    let mut boundary = 0;
    for i in 0..nums.len() {
        if nums[i] % 2 == 0 {
            nums.swap(boundary, i);
            boundary += 1;
        }
    }
    boundary
}

/// 有序数组原地去重
///
/// 双指针：`write` 指向下一个唯一元素应写入的位置，`read` 向后扫描，
/// 遇到与已写入末尾不同的元素就写过去。返回去重后的新长度，
/// 前 n 个元素唯一。复杂度 O(n)。
pub fn dedup_sorted(nums: &mut [i32]) -> usize {
    if nums.is_empty() {
        return 0;
    }
    let mut write = 1;
    for read in 1..nums.len() {
        if nums[read] != nums[write - 1] {
            nums[write] = nums[read];
            write += 1;
        }
    }
    write
}

/// 数组循环右移 k 位
///
/// 用 `rotate_right` 实现；k 先对长度取模，避免超出长度 panic
/// （`rotate_*` 要求 `k <= len`）。复杂度 O(n)。
pub fn rotate_k(nums: &mut [i32], k: usize) {
    let n = nums.len();
    if n > 0 {
        nums.rotate_right(k % n);
    }
}

/// 按 chunk 大小分组，每组求和
///
/// `chunks(chunk)` 自动处理末尾不足一组的情况。复杂度 O(n)。
/// 典型场景：分页 / 分批处理的规约。
pub fn chunk_sums(nums: &[i32], chunk: usize) -> Vec<i32> {
    nums.chunks(chunk).map(|c| c.iter().sum()).collect()
}

/// 相邻元素之差
///
/// `windows(2)` 产生长度为 2 的滑动窗口，对每对取后减前。
/// 复杂度 O(n)。典型场景：差分数组、股价日涨跌。
pub fn adjacent_diffs(nums: &[i32]) -> Vec<i32> {
    nums.windows(2).map(|w| w[1] - w[0]).collect()
}

/// 交换首尾元素（演示 `split_at_mut` 同时可变借用两个位置）
///
/// 直接写 `&mut nums[0]` 与 `&mut nums[n - 1]` 会因可变借用重叠而无法编译；
/// 通过 `split_at_mut` / `split_last_mut` 拆出互不重叠的可变引用即可。
pub fn swap_first_last(nums: &mut [i32]) {
    let n = nums.len();
    if n < 2 {
        return;
    }
    let (first, rest) = nums.split_at_mut(1);
    let (last, _) = rest.split_last_mut().unwrap();
    std::mem::swap(&mut first[0], last);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_binary_search_count() {
        assert_eq!(binary_search_count(&[1, 2, 2, 2, 3, 5], 2), 3);
        assert_eq!(binary_search_count(&[1, 2, 2, 2, 3, 5], 4), 0);
        assert_eq!(binary_search_count(&[], 1), 0);
    }

    #[test]
    fn test_median() {
        assert_eq!(median(&mut [3.0, 1.0, 2.0]), 2.0); // 奇数个
        assert_eq!(median(&mut [1.0, 2.0, 3.0, 4.0]), 2.5); // 偶数个
        assert!(median(&mut []).is_nan());
    }

    #[test]
    fn test_top_k_smallest() {
        assert_eq!(top_k_smallest(&mut [5, 2, 8, 1, 9, 3], 3), vec![1, 2, 3]);
        assert_eq!(top_k_smallest(&mut [4, 4, 4], 2), vec![4, 4]);
        assert!(top_k_smallest(&mut [1, 2], 0).is_empty());
    }

    #[test]
    fn test_kth_largest() {
        assert_eq!(kth_largest(&mut [3, 2, 1, 5, 6, 4], 2), 5);
        assert_eq!(kth_largest(&mut [3, 2, 3, 1, 2, 4, 5, 5, 6], 4), 4);
    }

    #[test]
    fn test_partition_evens_odds() {
        let mut nums = [1, 2, 3, 4, 5, 6];
        let boundary = partition_evens_odds(&mut nums);
        assert_eq!(boundary, 3);
        assert!(nums[..boundary].iter().all(|&x| x % 2 == 0));
        assert!(nums[boundary..].iter().all(|&x| x % 2 == 1));
    }

    #[test]
    fn test_dedup_sorted() {
        let mut nums = [1, 1, 2, 2, 2, 3];
        let len = dedup_sorted(&mut nums);
        assert_eq!(len, 3);
        assert_eq!(&nums[..len], &[1, 2, 3]);
    }

    #[test]
    fn test_rotate_k() {
        let mut nums = [1, 2, 3, 4, 5];
        rotate_k(&mut nums, 2);
        assert_eq!(nums, [4, 5, 1, 2, 3]);
        rotate_k(&mut nums, 7); // 取模后等价右移 2
        assert_eq!(nums, [2, 3, 4, 5, 1]);
    }

    #[test]
    fn test_chunk_sums() {
        assert_eq!(chunk_sums(&[1, 2, 3, 4, 5], 2), vec![3, 7, 5]);
        assert_eq!(chunk_sums(&[1, 2, 3], 3), vec![6]);
    }

    #[test]
    fn test_adjacent_diffs() {
        assert_eq!(adjacent_diffs(&[1, 3, 6, 10]), vec![2, 3, 4]);
        assert!(adjacent_diffs(&[7]).is_empty());
    }

    #[test]
    fn test_swap_first_last() {
        let mut nums = [1, 2, 3, 4];
        swap_first_last(&mut nums);
        assert_eq!(nums, [4, 2, 3, 1]);
        let mut one = [9];
        swap_first_last(&mut one);
        assert_eq!(one, [9]);
    }
}
