/// 贪心算法 (Greedy)
///
/// 每步都做当前看来最优的选择，希望最终达到全局最优。
/// 贪心正确性需要证明（通常用数学归纳法或交换论证）。

/// 跳跃游戏
///
/// 判断是否能从第一个位置跳到最后一个位置。
pub fn can_jump(nums: &[i32]) -> bool {
    let mut max_reach = 0i32;
    for i in 0..nums.len() {
        if i as i32 > max_reach {
            return false;
        }
        max_reach = max_reach.max(i as i32 + nums[i]);
    }
    true
}

/// 跳跃游戏 II — 最小跳跃次数
///
/// 保证可达，求最少跳跃次数。
pub fn jump(nums: &[i32]) -> i32 {
    let n = nums.len();
    if n <= 1 {
        return 0;
    }
    let mut jumps = 0;
    let mut curr_end = 0usize;
    let mut farthest = 0usize;

    for i in 0..n - 1 {
        farthest = farthest.max(i + nums[i] as usize);
        if i == curr_end {
            jumps += 1;
            curr_end = farthest;
            if curr_end >= n - 1 {
                break;
            }
        }
    }
    jumps
}

// ==================== 区间调度 ====================

/// 无重叠区间
///
/// 移除最少的区间使剩余区间不重叠。贪心：按结束时间排序。
pub fn erase_overlap_intervals(intervals: &mut Vec<Vec<i32>>) -> i32 {
    if intervals.is_empty() {
        return 0;
    }
    intervals.sort_by_key(|iv| iv[1]);

    let mut count = 0;
    let mut end = intervals[0][1];

    for iv in &intervals[1..] {
        if iv[0] >= end {
            end = iv[1];
        } else {
            count += 1;
        }
    }
    count
}

/// 合并重叠区间
pub fn merge_intervals(intervals: &mut Vec<Vec<i32>>) -> Vec<Vec<i32>> {
    if intervals.is_empty() {
        return vec![];
    }
    intervals.sort_by_key(|iv| iv[0]);

    let mut result: Vec<Vec<i32>> = Vec::new();
    result.push(intervals[0].clone());

    for iv in &intervals[1..] {
        let last = result.last_mut().unwrap();
        if iv[0] <= last[1] {
            last[1] = last[1].max(iv[1]);
        } else {
            result.push(iv.clone());
        }
    }
    result
}

// ==================== 其他贪心题 ====================

/// 分发饼干
///
/// 每个孩子有胃口值 g[i]，每块饼干有大小 s[j]。
/// 最大化被满足的孩子数量。
pub fn find_content_children(g: &mut [i32], s: &mut [i32]) -> usize {
    g.sort_unstable();
    s.sort_unstable();
    let mut i = 0;
    let mut j = 0;
    while i < g.len() && j < s.len() {
        if s[j] >= g[i] {
            i += 1;
        }
        j += 1;
    }
    i
}

/// 最大子数组和 — 贪心视角
///
/// 一旦当前和为负，就重新开始。
pub fn max_subarray_greedy(nums: &[i32]) -> i32 {
    if nums.is_empty() {
        return 0;
    }
    let mut max_sum = nums[0];
    let mut curr_sum = nums[0];
    for &x in &nums[1..] {
        curr_sum = if curr_sum < 0 { x } else { curr_sum + x };
        max_sum = max_sum.max(curr_sum);
    }
    max_sum
}

/// 买卖股票的最佳时机 II
///
/// 可以多次买卖，求最大利润。
/// 贪心：吃掉每一段上涨。
pub fn max_profit(prices: &[i32]) -> i32 {
    prices
        .windows(2)
        .map(|w| (w[1] - w[0]).max(0))
        .sum()
}

/// 按要求重写数字的最小值
///
/// 加油站问题 — 能否绕环路一周。
pub fn can_complete_circuit(gas: &[i32], cost: &[i32]) -> Option<usize> {
    let total: i32 = gas.iter().zip(cost.iter()).map(|(g, c)| g - c).sum();
    if total < 0 {
        return None;
    }
    let mut start = 0;
    let mut tank = 0;
    for i in 0..gas.len() {
        tank += gas[i] - cost[i];
        if tank < 0 {
            start = i + 1;
            tank = 0;
        }
    }
    Some(start)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_can_jump() {
        assert!(can_jump(&[2, 3, 1, 1, 4]));
        assert!(!can_jump(&[3, 2, 1, 0, 4]));
    }

    #[test]
    fn test_jump() {
        assert_eq!(jump(&[2, 3, 1, 1, 4]), 2);
    }

    #[test]
    fn test_merge_intervals() {
        let mut intervals = vec![vec![1, 3], vec![2, 6], vec![8, 10], vec![15, 18]];
        let merged = merge_intervals(&mut intervals);
        assert_eq!(merged, vec![vec![1, 6], vec![8, 10], vec![15, 18]]);
    }

    #[test]
    fn test_find_content_children() {
        let mut g = vec![1, 2, 3];
        let mut s = vec![1, 1];
        assert_eq!(find_content_children(&mut g, &mut s), 1);
    }

    #[test]
    fn test_max_profit() {
        assert_eq!(max_profit(&[7, 1, 5, 3, 6, 4]), 7);
    }

    #[test]
    fn test_can_complete_circuit() {
        assert_eq!(
            can_complete_circuit(&[1, 2, 3, 4, 5], &[3, 4, 5, 1, 2]),
            Some(3)
        );
    }
}
