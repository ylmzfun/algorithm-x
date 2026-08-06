/// 二分搜索及其变体
///
/// 核心思想：每次将搜索空间减半，时间复杂度 O(log n)。
/// 前提：数据必须有序（或具有单调性）。

/// 标准二分搜索 — 返回目标值的索引
///
/// 在有序数组中查找 target，找到返回 Some(index)，否则返回 None。
pub fn binary_search<T: Ord>(arr: &[T], target: &T) -> Option<usize> {
    let mut lo = 0i32;
    let mut hi = arr.len() as i32 - 1;

    while lo <= hi {
        let mid = lo + (hi - lo) / 2;
        match arr[mid as usize].cmp(target) {
            std::cmp::Ordering::Less => lo = mid + 1,
            std::cmp::Ordering::Greater => hi = mid - 1,
            std::cmp::Ordering::Equal => return Some(mid as usize),
        }
    }
    None
}

/// 二分查找左边界 — 第一个 ≥ target 的位置
///
/// 适用于查找第一个大于等于目标值的元素。
pub fn lower_bound<T: Ord>(arr: &[T], target: &T) -> usize {
    let mut lo = 0i32;
    let mut hi = arr.len() as i32;

    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if arr[mid as usize] < *target {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    lo as usize
}

/// 二分查找右边界 — 第一个 > target 的位置
///
/// 适用于查找第一个大于目标值的元素。
pub fn upper_bound<T: Ord>(arr: &[T], target: &T) -> usize {
    let mut lo = 0i32;
    let mut hi = arr.len() as i32;

    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if arr[mid as usize] <= *target {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    lo as usize
}

/// 二分查找目标值的范围 [left, right) — target 出现次数 = right - left
pub fn search_range<T: Ord>(arr: &[T], target: &T) -> (usize, usize) {
    let left = lower_bound(arr, target);
    if left == arr.len() || arr[left] != *target {
        return (left, left); // 未找到
    }
    let right = upper_bound(arr, target);
    (left, right)
}

// ==================== 变体问题 ====================

/// 搜索旋转有序数组
///
/// 如 [4,5,6,7,0,1,2] 中查找 target。
/// 通过判断 mid 在左半还是右半来确定搜索方向。
pub fn search_in_rotated<T: Ord>(arr: &[T], target: &T) -> Option<usize> {
    if arr.is_empty() {
        return None;
    }
    let mut lo = 0i32;
    let mut hi = arr.len() as i32 - 1;

    while lo <= hi {
        let mid = lo + (hi - lo) / 2;
        let m = mid as usize;
        if arr[m] == *target {
            return Some(m);
        }
        // 判断 mid 在哪个有序段
        if arr[lo as usize] <= arr[m] {
            // mid 在左半段（有序）
            if *target >= arr[lo as usize] && *target < arr[m] {
                hi = mid - 1;
            } else {
                lo = mid + 1;
            }
        } else {
            // mid 在右半段（有序）
            if *target > arr[m] && *target <= arr[hi as usize] {
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
    }
    None
}

/// 查找峰值元素
///
/// 峰值：元素大于其左右相邻元素。
/// 假设 nums[-1] = nums[n] = -∞。
pub fn find_peak_element(nums: &[i32]) -> Option<usize> {
    if nums.is_empty() {
        return None;
    }
    let mut lo = 0i32;
    let mut hi = nums.len() as i32 - 1;

    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        let m = mid as usize;
        if nums[m] < nums[m + 1] {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    Some(lo as usize)
}

/// 寻找两个正序数组的中位数（二分法）
///
/// 时间复杂度 O(log(min(m, n)))。
pub fn find_median_sorted_arrays(nums1: &[i32], nums2: &[i32]) -> f64 {
    // 保证 nums1 为较短数组
    let (a, b) = if nums1.len() <= nums2.len() {
        (nums1, nums2)
    } else {
        (nums2, nums1)
    };
    let m = a.len();
    let n = b.len();
    let total_left = (m + n + 1) / 2;

    let mut lo = 0i32;
    let mut hi = m as i32;

    while lo <= hi {
        let i = (lo + (hi - lo) / 2) as usize;
        let j = total_left - i;

        let a_left = if i == 0 { i32::MIN } else { a[i - 1] };
        let a_right = if i == m { i32::MAX } else { a[i] };
        let b_left = if j == 0 { i32::MIN } else { b[j - 1] };
        let b_right = if j == n { i32::MAX } else { b[j] };

        if a_left <= b_right && b_left <= a_right {
            if (m + n) % 2 == 0 {
                return (a_left.max(b_left) as f64 + a_right.min(b_right) as f64) / 2.0;
            } else {
                return a_left.max(b_left) as f64;
            }
        } else if a_left > b_right {
            hi = i as i32 - 1;
        } else {
            lo = i as i32 + 1;
        }
    }
    0.0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_binary_search() {
        let arr = [1, 3, 5, 7, 9];
        assert_eq!(binary_search(&arr, &5), Some(2));
        assert_eq!(binary_search(&arr, &4), None);
    }

    #[test]
    fn test_lower_upper_bound() {
        let arr = [1, 2, 2, 2, 3, 4];
        assert_eq!(lower_bound(&arr, &2), 1); // 第一个 ≥2 的位置
        assert_eq!(upper_bound(&arr, &2), 4); // 第一个 >2 的位置
        assert_eq!(search_range(&arr, &2), (1, 4));
        assert_eq!(search_range(&arr, &5), (6, 6));
    }

    #[test]
    fn test_search_in_rotated() {
        let arr = [4, 5, 6, 7, 0, 1, 2];
        assert_eq!(search_in_rotated(&arr, &0), Some(4));
        assert_eq!(search_in_rotated(&arr, &3), None);
    }

    #[test]
    fn test_find_peak_element() {
        let arr = [1, 2, 3, 1];
        assert_eq!(find_peak_element(&arr), Some(2));

        let arr2 = [1, 2, 1, 3, 5, 6, 4];
        // 6 是峰值
        let peak = find_peak_element(&arr2).unwrap();
        assert_eq!(arr2[peak], 6);
    }

    #[test]
    fn test_find_median_sorted_arrays() {
        assert_eq!(find_median_sorted_arrays(&[1, 3], &[2]), 2.0);
        assert_eq!(find_median_sorted_arrays(&[1, 2], &[3, 4]), 2.5);
    }
}
