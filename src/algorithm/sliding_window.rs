/// 滑动窗口 / 双指针
///
/// 滑动窗口：维护一个满足约束的连续区间，窗口边界单调移动。
/// 双指针：两个指针协同移动，常见于数组和链表问题。

use std::collections::HashMap;

/// 无重复字符的最长子串
///
/// 滑动窗口 + HashMap 记录字符最后出现位置。
pub fn length_of_longest_substring(s: &str) -> usize {
    let mut last_pos = HashMap::new();
    let mut max_len = 0;
    let mut start = 0i32;

    for (i, c) in s.chars().enumerate() {
        if let Some(&pos) = last_pos.get(&c) {
            start = start.max(pos + 1);
        }
        max_len = max_len.max(i as i32 - start + 1);
        last_pos.insert(c, i as i32);
    }
    max_len as usize
}

/// 最小覆盖子串
///
/// 找到包含 t 中所有字符的最小子串。
pub fn min_window(s: &str, t: &str) -> String {
    if s.is_empty() || t.is_empty() {
        return String::new();
    }

    let s_bytes: Vec<char> = s.chars().collect();
    let mut need = HashMap::new();
    for c in t.chars() {
        *need.entry(c).or_insert(0) += 1;
    }
    let required = need.len();

    let mut window = HashMap::new();
    let mut formed = 0;
    let mut left = 0;
    let mut min_len = usize::MAX;
    let mut min_start = 0;

    for (right, &c) in s_bytes.iter().enumerate() {
        *window.entry(c).or_insert(0) += 1;

        if need.get(&c).map_or(false, |&n| window[&c] == n) {
            formed += 1;
        }

        while left <= right && formed == required {
            let curr_len = right - left + 1;
            if curr_len < min_len {
                min_len = curr_len;
                min_start = left;
            }

            let left_char = s_bytes[left];
            *window.get_mut(&left_char).unwrap() -= 1;

            if need.get(&left_char).map_or(false, |&n| window[&left_char] < n) {
                formed -= 1;
            }
            left += 1;
        }
    }

    if min_len == usize::MAX {
        String::new()
    } else {
        s_bytes[min_start..min_start + min_len]
            .iter()
            .collect()
    }
}

// ==================== 双指针 ====================

/// 盛最多水的容器
///
/// 从两端向中间收缩，每次移动较短的边。
pub fn max_area(height: &[i32]) -> i32 {
    let mut left = 0i32;
    let mut right = height.len() as i32 - 1;
    let mut max_water = 0;

    while left < right {
        let h = height[left as usize].min(height[right as usize]);
        let w = right - left;
        max_water = max_water.max(h * w);

        if height[left as usize] < height[right as usize] {
            left += 1;
        } else {
            right -= 1;
        }
    }
    max_water
}

/// 三数之和
///
/// 找到所有不重复的三元组，其和为 0。
pub fn three_sum(nums: &mut [i32]) -> Vec<Vec<i32>> {
    nums.sort_unstable();
    let mut result = Vec::new();
    let n = nums.len();

    for i in 0..n {
        if i > 0 && nums[i] == nums[i - 1] {
            continue;
        }
        let mut left = i + 1;
        let mut right = n - 1;
        while left < right {
            let sum = nums[i] + nums[left] + nums[right];
            match sum.cmp(&0) {
                std::cmp::Ordering::Less => left += 1,
                std::cmp::Ordering::Greater => right -= 1,
                std::cmp::Ordering::Equal => {
                    result.push(vec![nums[i], nums[left], nums[right]]);
                    left += 1;
                    right -= 1;
                    while left < right && nums[left] == nums[left - 1] {
                        left += 1;
                    }
                    while left < right && nums[right] == nums[right + 1] {
                        right -= 1;
                    }
                }
            }
        }
    }
    result
}

/// 接雨水 — 双指针法
///
/// 每个位置能接的雨水量 = min(左侧最大高度, 右侧最大高度) - 当前位置高度
pub fn trap(height: &[i32]) -> i32 {
    if height.is_empty() {
        return 0;
    }
    let mut left = 0;
    let mut right = height.len() - 1;
    let mut left_max = 0;
    let mut right_max = 0;
    let mut water = 0;

    while left < right {
        if height[left] < height[right] {
            if height[left] >= left_max {
                left_max = height[left];
            } else {
                water += left_max - height[left];
            }
            left += 1;
        } else {
            if height[right] >= right_max {
                right_max = height[right];
            } else {
                water += right_max - height[right];
            }
            right -= 1;
        }
    }
    water
}

/// 环形链表检测（返回环的入口）
///
/// Floyd 判圈算法变体：快慢指针相遇后，从 head 和相遇点同速前进，相遇点即环的入口。
/// 此处以数组形式模拟链表: nums[i] = 下一个节点的索引。
/// 假设 nums 中的值在 [0, n-1] 范围且形成含环的链表（如找重复数问题）。
pub fn find_duplicate(nums: &[i32]) -> i32 {
    // Floyd 判圈法找重复数
    let mut slow = nums[0] as usize;
    let mut fast = nums[0] as usize;

    loop {
        slow = nums[slow] as usize;
        fast = nums[nums[fast] as usize] as usize;
        if slow == fast {
            break;
        }
    }

    // 找环的入口
    slow = nums[0] as usize;
    while slow != fast {
        slow = nums[slow] as usize;
        fast = nums[fast] as usize;
    }
    slow as i32
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_length_of_longest_substring() {
        assert_eq!(length_of_longest_substring("abcabcbb"), 3);
        assert_eq!(length_of_longest_substring("bbbbb"), 1);
        assert_eq!(length_of_longest_substring("pwwkew"), 3);
    }

    #[test]
    fn test_min_window() {
        assert_eq!(min_window("ADOBECODEBANC", "ABC"), "BANC");
    }

    #[test]
    fn test_max_area() {
        assert_eq!(max_area(&[1, 8, 6, 2, 5, 4, 8, 3, 7]), 49);
    }

    #[test]
    fn test_three_sum() {
        let mut nums = vec![-1, 0, 1, 2, -1, -4];
        let result = three_sum(&mut nums);
        assert_eq!(result.len(), 2);
    }

    #[test]
    fn test_trap() {
        assert_eq!(trap(&[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]), 6);
    }

    #[test]
    fn test_find_duplicate() {
        assert_eq!(find_duplicate(&[1, 3, 4, 2, 2]), 2);
    }
}
