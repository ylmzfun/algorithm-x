//! Rust 工程专题：应用场景与使用技巧
//!
//! 本文件以"速查"形式汇总工程实战中的高频知识点，包括场景选型、
//! LeetCode 刷题套路、性能与内存技巧、常见陷阱，并给出可套用的模板函数。

//! ## 场景选型速查
//!
//! | 需求 | 推荐方案 | 参考模块 |
//! |------|----------|----------|
//! | Top-K / 优先队列 | `BinaryHeap`（配合 `Reverse` 做小顶堆） | `native::collections` |
//! | 频率统计 | `HashMap` entry API / `itertools::counts` | `native::collections` / `third_party::itertools` |
//! | 有序区间查询 | `BTreeMap::range` | `native::collections` |
//! | 图遍历 / 最短路 / 最小生成树 | `petgraph` | `third_party::petgraph` |
//! | 大数据量并行处理 | `rayon` | `third_party::rayon` |
//! | 大整数（阶乘、加密） | `num-bigint` | `third_party::num_bigint` |
//! | 保持插入顺序的 Map | `indexmap::IndexMap` | `third_party::collections` |
//! | 小集合避免堆分配 | `smallvec::SmallVec` | `third_party::collections` |
//! | 配置 / JSON | `serde` + `serde_json` | `third_party::serde` |
//! | 错误处理 | `anyhow`（应用层）/ `thiserror`（库） | `third_party::errors` |
//! | 文本匹配 | `regex` | `third_party::regex` |
//! | 日期计算 | `chrono` | `third_party::chrono` |
//! | 高并发 IO | `tokio` / `futures` | `third_party::async_runtime` |
//!
//! ## 性能技巧
//!
//! 1. **预分配容量**：`Vec::with_capacity`、`HashMap::with_capacity`，避免反复扩容拷贝。
//! 2. **迭代器是零成本抽象**：`iter().map().filter().collect()` 会被优化为与手写
//!    循环等价甚至更好的代码，优先可读性。
//! 3. **不稳定排序更快**：数据无序时用 `sort_unstable` / `par_sort_unstable`。
//! 4. **避免不必要的 clone**：优先借用 `&T` / `&str`，需要所有权时再 `to_owned()`。
//! 5. **ASCII 处理用字节**：已知是 ASCII 时用 `bytes()` 而非 `chars()`，配合
//!    `u8::is_ascii_*` 系列方法。
//! 6. **批量 IO**：读文件用 `BufReader` / `read_to_string`，逐行处理用 `.lines()`。
//! 7. **发布构建**：`cargo build --release`，并可在 `Cargo.toml` 的
//!    `[profile.release]` 开启 `lto = true` 等优化。
//!
//! ## 内存与所有权技巧
//!
//! - **`Cow<str>`**：读多写少时避免拷贝，仅在需要修改时才 clone。
//! - **`Box<[T]>`**：把 `Vec` 收缩为定长切片，减少元数据开销。
//! - **借用拆分**：`slice::split_at_mut` / 多个字段同时可变借用，解决借用冲突。
//! - **共享所有权**：单线程 `Rc<RefCell<T>>`，多线程 `Arc<Mutex<T>>` / `Arc<RwLock<T>>`。
//!
//! ## 常见陷阱
//!
//! - **字符串切片越界**：`&s[i..j]` 必须落在字符边界，否则 panic；
//!   用 `s.get(i..j)` 安全获取，或用 `char_indices()` 定位边界。
//! - **整数溢出**：debug 构建下溢出会 panic，release 下回绕；
//!   用 `checked_add` / `saturating_add` / `wrapping_add` 明确意图。
//! - **浮点比较**：不要用 `==` 比较浮点，用差值小于阈值判断。
//! - **迭代器借用冲突**：`let x = v.iter().max(); v.push(1);` 会借用冲突，
//!   先 `collect` 结束借用再修改容器。
//! - **`HashMap` 无序**：依赖顺序时用 `BTreeMap` 或 `IndexMap`。
//! - **多锁死锁**：多线程加多个锁时保持全局一致的加锁顺序。
//!
//! ## LeetCode 高频套路（Rust 版）
//!
//! 下面给出几个可直接套用的模板。

/// 模式一：频率统计 + Top-K（LeetCode 347）
///
/// 统计频率用 `HashMap` entry API；取 Top-K 用 `BinaryHeap` 小顶堆，
/// 堆大小超过 k 时弹出最小者，保证堆中始终是当前最大的 k 个。
pub fn top_k_frequent(nums: &[i32], k: usize) -> Vec<i32> {
    use std::cmp::Reverse;
    use std::collections::{BinaryHeap, HashMap};

    let mut freq: HashMap<i32, usize> = HashMap::new();
    for &n in nums {
        *freq.entry(n).or_insert(0) += 1;
    }

    let mut heap: BinaryHeap<Reverse<(usize, i32)>> = BinaryHeap::new();
    for (num, count) in freq {
        heap.push(Reverse((count, num)));
        if heap.len() > k {
            heap.pop();
        }
    }

    heap.into_sorted_vec()
        .into_iter()
        .map(|Reverse((_, n))| n)
        .collect()
}

/// 模式二：滑动窗口最大值（LeetCode 239）
///
/// 用 `VecDeque` 维护窗口内候选下标，保证队首是当前窗口最大值。
pub fn sliding_window_max(nums: &[i32], k: usize) -> Vec<i32> {
    use std::collections::VecDeque;

    let mut result = Vec::with_capacity(nums.len().saturating_sub(k) + 1);
    let mut dq: VecDeque<usize> = VecDeque::new();
    for (i, &n) in nums.iter().enumerate() {
        while let Some(&front) = dq.front() {
            if i >= front + k {
                dq.pop_front();
            } else {
                break;
            }
        }
        while let Some(&back) = dq.back() {
            if nums[back] <= n {
                dq.pop_back();
            } else {
                break;
            }
        }
        dq.push_back(i);
        if i + 1 >= k {
            result.push(nums[dq[0]]);
        }
    }
    result
}

/// 模式三：有序数组边界搜索
///
/// `partition_point` 返回"谓词为真的最长前缀长度"，
/// 等价于二分查找中的 lower_bound / upper_bound，O(log n)。
pub fn lower_bound(nums: &[i32], target: i32) -> usize {
    nums.partition_point(|&x| x < target)
}

/// 有序数组中的 upper_bound：第一个大于 target 的位置
pub fn upper_bound(nums: &[i32], target: i32) -> usize {
    nums.partition_point(|&x| x <= target)
}

/// 统计有序数组中 target 的出现次数
pub fn count_occurrences(nums: &[i32], target: i32) -> usize {
    upper_bound(nums, target) - lower_bound(nums, target)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_top_k_frequent() {
        assert_eq!(top_k_frequent(&[1, 1, 1, 2, 2, 3], 2), vec![1, 2]);
        assert_eq!(top_k_frequent(&[1], 1), vec![1]);
    }

    #[test]
    fn test_sliding_window_max() {
        assert_eq!(
            sliding_window_max(&[1, 3, -1, -3, 5, 3, 6, 7], 3),
            vec![3, 3, 5, 5, 6, 7]
        );
        assert_eq!(sliding_window_max(&[1], 1), vec![1]);
    }

    #[test]
    fn test_bound_search() {
        let nums = [1, 2, 2, 2, 3, 5];
        assert_eq!(lower_bound(&nums, 2), 1);
        assert_eq!(upper_bound(&nums, 2), 4);
        assert_eq!(count_occurrences(&nums, 2), 3);
        assert_eq!(count_occurrences(&nums, 4), 0);
    }
}
