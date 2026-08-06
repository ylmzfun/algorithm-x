/// 高级排序算法
///
/// - 归并排序 O(n log n) — 稳定，需要 O(n) 额外空间
/// - 快速排序 O(n log n) — 不稳定，原地排序
/// - 堆排序 O(n log n) — 不稳定，原地排序（实现在 `heap.rs`）

// ==================== 归并排序 ====================

/// 归并排序（自顶向下，递归）
///
/// 分治思想：将数组分成两半，分别排序后合并。
pub fn merge_sort<T: Ord + Clone>(arr: &mut [T]) {
    let n = arr.len();
    if n <= 1 {
        return;
    }
    let mid = n / 2;
    merge_sort(&mut arr[..mid]);
    merge_sort(&mut arr[mid..]);
    merge(arr, mid);
}

fn merge<T: Ord + Clone>(arr: &mut [T], mid: usize) {
    let left = arr[..mid].to_vec();
    let right = arr[mid..].to_vec();
    let mut i = 0;
    let mut j = 0;
    let mut k = 0;

    while i < left.len() && j < right.len() {
        if left[i] <= right[j] {
            arr[k] = left[i].clone();
            i += 1;
        } else {
            arr[k] = right[j].clone();
            j += 1;
        }
        k += 1;
    }
    while i < left.len() {
        arr[k] = left[i].clone();
        i += 1;
        k += 1;
    }
    while j < right.len() {
        arr[k] = right[j].clone();
        j += 1;
        k += 1;
    }
}

/// 归并排序（自底向上，迭代）
///
/// 避免了递归开销，适合链表等非随机访问结构。
pub fn merge_sort_bottom_up<T: Ord + Clone>(arr: &mut [T]) {
    let n = arr.len();

    let mut width = 1;
    while width < n {
        let mut i = 0;
        while i < n {
            let mid = (i + width).min(n);
            let end = (i + 2 * width).min(n);
            if mid < end {
                merge_range(arr, i, mid, end);
            }
            i += 2 * width;
        }
        width *= 2;
    }
}

fn merge_range<T: Ord + Clone>(arr: &mut [T], start: usize, mid: usize, end: usize) {
    let left = arr[start..mid].to_vec();
    let right = arr[mid..end].to_vec();
    let mut i = 0;
    let mut j = 0;
    let mut k = start;

    while i < left.len() && j < right.len() {
        if left[i] <= right[j] {
            arr[k] = left[i].clone();
            i += 1;
        } else {
            arr[k] = right[j].clone();
            j += 1;
        }
        k += 1;
    }
    while i < left.len() {
        arr[k] = left[i].clone();
        i += 1;
        k += 1;
    }
    while j < right.len() {
        arr[k] = right[j].clone();
        j += 1;
        k += 1;
    }
}

// ==================== 快速排序 ====================

/// 快速排序
///
/// 选取基准值 (pivot)，将数组分为"小于 pivot"和"大于 pivot"两部分，递归排序。
/// 采用三数取中法选择 pivot 以优化最坏情况。
pub fn quick_sort<T: Ord>(arr: &mut [T]) {
    quick_sort_range(arr, 0, arr.len());
}

fn quick_sort_range<T: Ord>(arr: &mut [T], lo: usize, hi: usize) {
    if lo + 1 >= hi {
        return;
    }
    let p = partition(arr, lo, hi);
    quick_sort_range(arr, lo, p);
    quick_sort_range(arr, p + 1, hi);
}

/// Lomuto 分区方案
///
/// 选择最后一个元素为 pivot，返回 pivot 最终位置。
fn partition<T: Ord>(arr: &mut [T], lo: usize, hi: usize) -> usize {
    // 三数取中：将 lo, mid, hi-1 的中位数放到 hi-1
    let mid = lo + (hi - lo) / 2;
    if arr[mid] < arr[lo] {
        arr.swap(lo, mid);
    }
    if arr[hi - 1] < arr[lo] {
        arr.swap(lo, hi - 1);
    }
    if arr[hi - 1] < arr[mid] {
        arr.swap(mid, hi - 1);
    }
    // 现在 pivot 在 hi-1

    let mut i = lo;
    for j in lo..hi - 1 {
        if arr[j] <= arr[hi - 1] {
            arr.swap(i, j);
            i += 1;
        }
    }
    arr.swap(i, hi - 1);
    i
}

// ==================== 快速选择 ====================

/// 快速选择算法 — 查找数组中第 k 小的元素（k 从 0 开始）
///
/// 基于快速排序的分区思想，平均 O(n)。
pub fn quick_select<T: Ord>(arr: &mut [T], k: usize) -> Option<&T> {
    if k >= arr.len() {
        return None;
    }
    quick_select_range(arr, k, 0, arr.len());
    Some(&arr[k])
}

fn quick_select_range<T: Ord>(arr: &mut [T], k: usize, lo: usize, hi: usize) {
    if lo + 1 >= hi {
        return;
    }
    let p = partition(arr, lo, hi);
    match k.cmp(&p) {
        std::cmp::Ordering::Less => quick_select_range(arr, k, lo, p),
        std::cmp::Ordering::Greater => quick_select_range(arr, k, p + 1, hi),
        std::cmp::Ordering::Equal => {}
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn assert_sorted<F>(sort_fn: F)
    where
        F: Fn(&mut [i32]),
    {
        let cases: Vec<Vec<i32>> = vec![
            vec![],
            vec![1],
            vec![5, 2, 8, 1, 9, 3],
            vec![1, 2, 3, 4, 5],
            vec![5, 4, 3, 2, 1],
            vec![3, 1, 2, 3, 1, 2],
        ];
        for mut arr in cases {
            let mut expected = arr.clone();
            expected.sort();
            sort_fn(&mut arr);
            assert_eq!(arr, expected);
        }
    }

    #[test]
    fn test_merge_sort() {
        assert_sorted(merge_sort);
    }

    #[test]
    fn test_merge_sort_bottom_up() {
        assert_sorted(merge_sort_bottom_up);
    }

    #[test]
    fn test_quick_sort() {
        assert_sorted(quick_sort);
    }

    #[test]
    fn test_quick_select() {
        let mut arr = vec![3, 2, 1, 5, 6, 4];
        assert_eq!(quick_select(&mut arr, 0), Some(&1));
        assert_eq!(quick_select(&mut arr, 2), Some(&3));
        assert_eq!(quick_select(&mut arr, 5), Some(&6));
        assert_eq!(quick_select(&mut arr, 6), None);
    }
}
