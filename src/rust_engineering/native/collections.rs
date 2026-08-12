//! 集合与优先队列
//!
//! 覆盖主题：
//! - `HashMap` 计数（`entry` API）
//! - `BinaryHeap` 与 `Reverse`：小顶堆（top-k 套路，LeetCode 347）
//! - `BTreeSet` / `BTreeMap`：有序性与区间查询（`range`）
//! - `VecDeque`：双端队列（FIFO 缓冲淘汰）
//! - `HashSet`：集合运算（并 / 交 / 差）

use std::cmp::Reverse;
use std::collections::{BTreeMap, BinaryHeap, HashMap, HashSet, VecDeque};

/// 字符频率统计
///
/// 用 `HashMap::entry` + `or_insert` 一次遍历计数。
/// 复杂度 O(n)。典型场景：字符串统计分析。
pub fn char_frequency(s: &str) -> HashMap<char, usize> {
    let mut freq = HashMap::new();
    for c in s.chars() {
        *freq.entry(c).or_insert(0) += 1;
    }
    freq
}

/// 出现频率最高的 k 个元素（LeetCode 347 套路）
///
/// 哈希表计数后，用 `BinaryHeap<Reverse<(次数, 元素)>>` 维护大小为 k 的
/// 小顶堆：新元素比堆顶（当前最小者）更大时淘汰堆顶。
/// 复杂度 O(n log k)，空间 O(n)。返回顺序不限。
pub fn top_k_frequent(nums: &[i32], k: usize) -> Vec<i32> {
    let mut freq: HashMap<i32, usize> = HashMap::new();
    for &x in nums {
        *freq.entry(x).or_insert(0) += 1;
    }
    let mut heap: BinaryHeap<Reverse<(usize, i32)>> = BinaryHeap::new();
    for (num, count) in freq {
        let item = Reverse((count, num));
        if heap.len() < k {
            heap.push(item);
        } else if heap.peek().is_some_and(|&top| item < top) {
            heap.pop();
            heap.push(item);
        }
    }
    heap.into_iter().map(|Reverse((_, num))| num).collect()
}

/// 最小的 k 个元素
///
/// 全部压入 `BinaryHeap<Reverse<i32>>`（小顶堆）后连续 `pop` k 次，
/// 依次得到升序的最小 k 个元素。注意 `into_iter` 顺序不定，取最小必须用 `pop`。
/// 复杂度 O(n log n)。
pub fn k_smallest(nums: &[i32], k: usize) -> Vec<i32> {
    let mut heap: BinaryHeap<Reverse<i32>> = nums.iter().copied().map(Reverse).collect();
    let mut out = Vec::with_capacity(k);
    for _ in 0..k.min(heap.len()) {
        out.push(heap.pop().unwrap().0);
    }
    out
}

/// 两个有序数组的合并去重
///
/// `BTreeSet` 插入自动有序且去重，转回 `Vec` 即得到升序结果。
/// 复杂度 O(n log n)。典型场景：有序流合并、唯一性归并。
pub fn merge_dedup_sorted(a: &[i32], b: &[i32]) -> Vec<i32> {
    let mut set = std::collections::BTreeSet::new();
    set.extend(a.iter().copied());
    set.extend(b.iter().copied());
    set.into_iter().collect()
}

/// BTreeMap 区间查询
///
/// `range(lo..=hi)` 只遍历落在区间内的键值对（键有序），
/// 复杂度 O(log n + k)，k 为区间内元素个数。典型场景：按时间范围取数据。
pub fn range_entries(map: &BTreeMap<i32, String>, lo: i32, hi: i32) -> Vec<(i32, String)> {
    map.range(lo..=hi).map(|(&k, v)| (k, v.clone())).collect()
}

/// 队尾插入，超容量时淘汰队头（FIFO 缓冲）
///
/// `VecDeque` 支持 O(1) 的双端 push / pop；返回被淘汰的队头元素，
/// 未淘汰时返回 `None`。典型场景：滑动窗口、LRU 雏形。
pub fn push_back_evict(queue: &mut VecDeque<i32>, value: i32, cap: usize) -> Option<i32> {
    queue.push_back(value);
    if queue.len() > cap {
        queue.pop_front()
    } else {
        None
    }
}

/// 两个集合的并 / 交 / 差
///
/// `HashSet` 的 `union` / `intersection` / `difference` 都返回惰性迭代器，
/// 结果排序后返回以便断言。复杂度 O(n + m)。
pub fn set_operations(a: &[i32], b: &[i32]) -> (Vec<i32>, Vec<i32>, Vec<i32>) {
    let sa: HashSet<i32> = a.iter().copied().collect();
    let sb: HashSet<i32> = b.iter().copied().collect();
    let mut union: Vec<i32> = sa.union(&sb).copied().collect();
    let mut intersection: Vec<i32> = sa.intersection(&sb).copied().collect();
    let mut difference: Vec<i32> = sa.difference(&sb).copied().collect();
    union.sort_unstable();
    intersection.sort_unstable();
    difference.sort_unstable();
    (union, intersection, difference)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_char_frequency() {
        let freq = char_frequency("abbccc");
        assert_eq!(freq.get(&'a'), Some(&1));
        assert_eq!(freq.get(&'b'), Some(&2));
        assert_eq!(freq.get(&'c'), Some(&3));
    }

    #[test]
    fn test_top_k_frequent() {
        let mut top = top_k_frequent(&[1, 1, 1, 2, 2, 3], 2);
        top.sort_unstable();
        assert_eq!(top, vec![1, 2]);
    }

    #[test]
    fn test_k_smallest() {
        assert_eq!(k_smallest(&[5, 2, 8, 1, 9, 3], 3), vec![1, 2, 3]);
        assert_eq!(k_smallest(&[3, 1, 2], 5), vec![1, 2, 3]); // k 超长取全部
    }

    #[test]
    fn test_merge_dedup_sorted() {
        assert_eq!(
            merge_dedup_sorted(&[1, 3, 5], &[2, 3, 6]),
            vec![1, 2, 3, 5, 6]
        );
    }

    #[test]
    fn test_range_entries() {
        let mut map = BTreeMap::new();
        map.insert(1, "一".to_string());
        map.insert(3, "三".to_string());
        map.insert(5, "五".to_string());
        map.insert(7, "七".to_string());
        assert_eq!(
            range_entries(&map, 2, 6),
            vec![(3, "三".to_string()), (5, "五".to_string())]
        );
    }

    #[test]
    fn test_push_back_evict() {
        let mut queue = VecDeque::from([1, 2, 3]);
        assert_eq!(push_back_evict(&mut queue, 4, 3), Some(1));
        assert_eq!(queue, VecDeque::from([2, 3, 4]));
        assert_eq!(push_back_evict(&mut queue, 5, 4), None);
        assert_eq!(queue, VecDeque::from([2, 3, 4, 5]));
    }

    #[test]
    fn test_set_operations() {
        let (union, intersection, difference) = set_operations(&[1, 2, 3], &[2, 3, 4]);
        assert_eq!(union, vec![1, 2, 3, 4]);
        assert_eq!(intersection, vec![2, 3]);
        assert_eq!(difference, vec![1]);
    }
}
