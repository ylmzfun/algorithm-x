/// 递归与分治
///
/// 递归三要素：
/// 1. 基准条件 (base case)
/// 2. 递归条件 (recursive case)
/// 3. 向基准条件逼近
///
/// 分治策略：
/// - 分解 (Divide)
/// - 解决 (Conquer)
/// - 合并 (Combine)

/// 汉诺塔
///
/// 将 n 个盘子从 src 借助 aux 移动到 dst。
/// 递推关系：T(n) = 2T(n-1) + 1 → O(2ⁿ)
pub fn hanoi(n: usize) -> Vec<(usize, usize, usize)> {
    fn move_disks(n: usize, src: usize, aux: usize, dst: usize, steps: &mut Vec<(usize, usize, usize)>) {
        if n == 1 {
            steps.push((src, dst, 1));
            return;
        }
        // Step 1: 将上面 n-1 个移到辅助柱
        move_disks(n - 1, src, dst, aux, steps);
        // Step 2: 将最大的移到目标柱
        steps.push((src, dst, n));
        // Step 3: 将 n-1 个从辅助柱移到目标柱
        move_disks(n - 1, aux, src, dst, steps);
    }
    let mut steps = Vec::new();
    move_disks(n, 0, 1, 2, &mut steps);
    steps
}

/// 快速幂（递归分治）
///
/// 计算 x^n mod m，时间复杂度 O(log n)
pub fn fast_pow(x: i64, n: u32, m: i64) -> i64 {
    if n == 0 {
        return 1i64 % m;
    }
    let half = fast_pow(x, n / 2, m);
    let result = (half as i128 * half as i128 % m as i128) as i64;
    if n % 2 == 0 {
        result
    } else {
        (result as i128 * x as i128 % m as i128) as i64
    }
}

/// 最大子数组和 — 分治解法 O(n log n)
///
/// 核心递归：
/// - 左半部分的最大子数组
/// - 右半部分的最大子数组
/// - 跨越中点的最大子数组
pub fn max_subarray_divide(arr: &[i32]) -> i32 {
    if arr.is_empty() {
        return 0;
    }
    max_subarray_rec(arr, 0, arr.len() - 1)
}

fn max_subarray_rec(arr: &[i32], lo: usize, hi: usize) -> i32 {
    if lo == hi {
        return arr[lo];
    }
    let mid = lo + (hi - lo) / 2;

    let left_max = max_subarray_rec(arr, lo, mid);
    let right_max = max_subarray_rec(arr, mid + 1, hi);
    let cross_max = max_crossing(arr, lo, mid, hi);

    left_max.max(right_max).max(cross_max)
}

fn max_crossing(arr: &[i32], lo: usize, mid: usize, hi: usize) -> i32 {
    let mut left_sum = i32::MIN;
    let mut sum = 0;
    for i in (lo..=mid).rev() {
        sum += arr[i];
        left_sum = left_sum.max(sum);
    }

    let mut right_sum = i32::MIN;
    sum = 0;
    for i in mid + 1..=hi {
        sum += arr[i];
        right_sum = right_sum.max(sum);
    }

    left_sum + right_sum
}

/// 最大子数组和 — Kadane 算法 O(n)
///
/// 动态规划：dp[i] = max(dp[i-1] + arr[i], arr[i])
pub fn max_subarray_kadane(arr: &[i32]) -> i32 {
    if arr.is_empty() {
        return 0;
    }
    let mut max_ending_here = arr[0];
    let mut max_so_far = arr[0];
    for &x in &arr[1..] {
        max_ending_here = max_ending_here.max(0) + x;
        max_so_far = max_so_far.max(max_ending_here);
    }
    max_so_far
}

/// 生成 n 对有效括号组合（递归回溯）
///
/// 卡特兰数应用。
pub fn generate_parenthesis(n: usize) -> Vec<String> {
    let mut result = Vec::new();
    fn backtrack(current: &mut String, open: usize, close: usize, max: usize, result: &mut Vec<String>) {
        if current.len() == max * 2 {
            result.push(current.clone());
            return;
        }
        if open < max {
            current.push('(');
            backtrack(current, open + 1, close, max, result);
            current.pop();
        }
        if close < open {
            current.push(')');
            backtrack(current, open, close + 1, max, result);
            current.pop();
        }
    }
    backtrack(&mut String::new(), 0, 0, n, &mut result);
    result
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hanoi() {
        let steps = hanoi(3);
        // 最少步数: 2³ - 1 = 7
        assert_eq!(steps.len(), 7);
    }

    #[test]
    fn test_fast_pow() {
        assert_eq!(fast_pow(2, 10, i64::MAX), 1024);
        assert_eq!(fast_pow(2, 10, 1000), 24);
    }

    #[test]
    fn test_max_subarray() {
        let arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4];
        assert_eq!(max_subarray_divide(&arr), 6);
        assert_eq!(max_subarray_kadane(&arr), 6);
    }

    #[test]
    fn test_generate_parenthesis() {
        let result = generate_parenthesis(3);
        let expected = vec!["((()))", "(()())", "(())()", "()(())", "()()()"];
        assert_eq!(result.len(), expected.len());
    }
}
