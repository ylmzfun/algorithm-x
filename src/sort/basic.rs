/// 基础排序算法
///
/// - 冒泡排序 O(n²) — 稳定
/// - 选择排序 O(n²) — 不稳定
/// - 插入排序 O(n²) — 稳定，对近乎有序数据接近 O(n)

/// 冒泡排序
///
/// 每轮将最大的元素"浮"到数组末尾。
/// 优化：提前终止（若一轮无交换则已有序）。
pub fn bubble_sort<T: Ord>(arr: &mut [T]) {
    let n = arr.len();
    for i in 0..n {
        let mut swapped = false;
        for j in 0..n - 1 - i {
            if arr[j] > arr[j + 1] {
                arr.swap(j, j + 1);
                swapped = true;
            }
        }
        if !swapped {
            break;
        }
    }
}

/// 选择排序
///
/// 每轮选择未排序部分的最小元素，放到已排序部分的末尾。
pub fn selection_sort<T: Ord>(arr: &mut [T]) {
    let n = arr.len();
    for i in 0..n {
        let mut min_idx = i;
        for j in i + 1..n {
            if arr[j] < arr[min_idx] {
                min_idx = j;
            }
        }
        arr.swap(i, min_idx);
    }
}

/// 插入排序
///
/// 将每个元素插入到前面已排序部分的合适位置。
/// 类比打牌时整理手牌。
pub fn insertion_sort<T: Ord>(arr: &mut [T]) {
    let n = arr.len();
    for i in 1..n {
        let mut j = i;
        while j > 0 && arr[j] < arr[j - 1] {
            arr.swap(j, j - 1);
            j -= 1;
        }
    }
}

/// 插入排序（二分优化版本）
///
/// 使用二分查找确定插入位置，减少比较次数（移动次数不变）。
pub fn insertion_sort_binary<T: Ord>(arr: &mut [T]) {
    let n = arr.len();
    for i in 1..n {
        let pos = arr[..i].binary_search(&arr[i]).unwrap_or_else(|e| e);
        if pos < i {
            arr[pos..=i].rotate_right(1);
        }
    }
}

/// Shell 排序（缩小增量排序）
///
/// 对插入排序的改进，通过分组使元素快速接近最终位置。
pub fn shell_sort<T: Ord>(arr: &mut [T]) {
    let n = arr.len();
    let mut gap = n / 2;
    while gap > 0 {
        for i in gap..n {
            let mut j = i;
            while j >= gap && arr[j] < arr[j - gap] {
                arr.swap(j, j - gap);
                j -= gap;
            }
        }
        gap /= 2;
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
    fn test_bubble_sort() {
        assert_sorted(bubble_sort);
    }

    #[test]
    fn test_selection_sort() {
        assert_sorted(selection_sort);
    }

    #[test]
    fn test_insertion_sort() {
        assert_sorted(insertion_sort);
    }

    #[test]
    fn test_insertion_sort_binary() {
        assert_sorted(insertion_sort_binary);
    }

    #[test]
    fn test_shell_sort() {
        assert_sorted(shell_sort);
    }
}
