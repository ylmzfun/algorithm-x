/// 动态规划 (Dynamic Programming)
///
/// 核心思想：
/// 1. 定义状态 (state)
/// 2. 找到状态转移方程 (transition)
/// 3. 确定初始条件和边界
/// 4. 确定计算顺序（自底向上 / 自顶向下 + 记忆化）
///
/// DP 适用条件：
/// - 最优子结构：问题的最优解包含子问题的最优解
/// - 无后效性：状态一旦确定，不受后续决策影响
/// - 重叠子问题：子问题会被反复计算

// ==================== 经典 DP ====================

/// 斐波那契数列（DP 入门）
pub fn fib(n: usize) -> u64 {
    if n <= 1 {
        return n as u64;
    }
    let mut prev2 = 0u64;
    let mut prev1 = 1u64;
    for _ in 2..=n {
        let curr = prev1 + prev2;
        prev2 = prev1;
        prev1 = curr;
    }
    prev1
}

/// 爬楼梯 — 每次爬 1 或 2 阶，到第 n 阶有多少种方法
///
/// dp[i] = dp[i-1] + dp[i-2]
pub fn climb_stairs(n: usize) -> u64 {
    if n <= 2 {
        return n as u64;
    }
    let mut a = 1u64; // dp[i-2]
    let mut b = 2u64; // dp[i-1]
    for _ in 3..=n {
        let c = a + b;
        a = b;
        b = c;
    }
    b
}

// ==================== 背包系列 ====================

/// 0-1 背包问题
///
/// 给定物品重量 wt[] 和价值 val[]，背包容量 W。
/// 每种物品只能选 0 或 1 次，求最大价值。
///
/// dp[i][w] = 前 i 个物品，容量 w 下的最大价值
/// dp[i][w] = max(dp[i-1][w], dp[i-1][w-wt[i]] + val[i])
pub fn knapsack_01(weights: &[usize], values: &[i32], capacity: usize) -> i32 {
    let n = weights.len();
    let mut dp = vec![0i32; capacity + 1];

    for i in 0..n {
        for w in (weights[i]..=capacity).rev() {
            dp[w] = dp[w].max(dp[w - weights[i]] + values[i]);
        }
    }
    dp[capacity]
}

/// 完全背包问题
///
/// 每种物品可以选无限次。
/// 与 0-1 背包的区别：正序遍历容量。
pub fn knapsack_unbounded(weights: &[usize], values: &[i32], capacity: usize) -> i32 {
    let n = weights.len();
    let mut dp = vec![0i32; capacity + 1];

    for i in 0..n {
        for w in weights[i]..=capacity {
            dp[w] = dp[w].max(dp[w - weights[i]] + values[i]);
        }
    }
    dp[capacity]
}

// ==================== 最长子序列 ====================

/// 最长递增子序列 (LIS) — O(n²)
pub fn length_of_lis(nums: &[i32]) -> usize {
    if nums.is_empty() {
        return 0;
    }
    let mut dp = vec![1; nums.len()];
    let mut max_len = 1;
    for i in 1..nums.len() {
        for j in 0..i {
            if nums[j] < nums[i] {
                dp[i] = dp[i].max(dp[j] + 1);
            }
        }
        max_len = max_len.max(dp[i]);
    }
    max_len
}

/// 最长递增子序列 — O(n log n)（耐心排序）
pub fn length_of_lis_fast(nums: &[i32]) -> usize {
    let mut tails = Vec::new();
    for &x in nums {
        let pos = tails.binary_search(&x).unwrap_or_else(|e| e);
        if pos == tails.len() {
            tails.push(x);
        } else {
            tails[pos] = x;
        }
    }
    tails.len()
}

/// 最长公共子序列 (LCS) — O(mn)
///
/// dp[i][j] = text1[..i] 和 text2[..j] 的 LCS 长度
pub fn longest_common_subsequence(text1: &str, text2: &str) -> usize {
    let t1: Vec<char> = text1.chars().collect();
    let t2: Vec<char> = text2.chars().collect();
    let m = t1.len();
    let n = t2.len();
    let mut dp = vec![vec![0usize; n + 1]; m + 1];

    for i in 1..=m {
        for j in 1..=n {
            if t1[i - 1] == t2[j - 1] {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = dp[i - 1][j].max(dp[i][j - 1]);
            }
        }
    }
    dp[m][n]
}

// ==================== 打家劫舍 ====================

/// 打家劫舍 — 不能偷相邻的房屋
///
/// dp[i] = max(dp[i-1], dp[i-2] + nums[i])
pub fn rob(nums: &[i32]) -> i32 {
    if nums.is_empty() {
        return 0;
    }
    if nums.len() == 1 {
        return nums[0];
    }
    let mut prev2 = nums[0];
    let mut prev1 = nums[0].max(nums[1]);
    for &x in &nums[2..] {
        let curr = prev1.max(prev2 + x);
        prev2 = prev1;
        prev1 = curr;
    }
    prev1
}

// ==================== 编辑距离 ====================

/// 编辑距离 (Levenshtein Distance) — O(mn)
///
/// 将 word1 转为 word2 的最少操作数（插入、删除、替换）。
pub fn edit_distance(word1: &str, word2: &str) -> usize {
    let w1: Vec<char> = word1.chars().collect();
    let w2: Vec<char> = word2.chars().collect();
    let m = w1.len();
    let n = w2.len();
    let mut dp = vec![vec![0usize; n + 1]; m + 1];

    for i in 0..=m {
        dp[i][0] = i;
    }
    for j in 0..=n {
        dp[0][j] = j;
    }

    for i in 1..=m {
        for j in 1..=n {
            if w1[i - 1] == w2[j - 1] {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = 1 + dp[i - 1][j] // 删除
                    .min(dp[i][j - 1]) // 插入
                    .min(dp[i - 1][j - 1]); // 替换
            }
        }
    }
    dp[m][n]
}

/// 硬币找零（最少硬币数）
///
/// dp[i] = 凑成金额 i 所需的最少硬币数
/// dp[i] = min(dp[i - coin] + 1) for each coin
pub fn coin_change(coins: &[i32], amount: i32) -> i32 {
    let amount = amount as usize;
    let mut dp = vec![amount + 1; amount + 1];
    dp[0] = 0;

    for i in 1..=amount {
        for &coin in coins {
            let c = coin as usize;
            if c <= i {
                dp[i] = dp[i].min(dp[i - c] + 1);
            }
        }
    }
    if dp[amount] > amount {
        -1
    } else {
        dp[amount] as i32
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_fib() {
        assert_eq!(fib(0), 0);
        assert_eq!(fib(1), 1);
        assert_eq!(fib(10), 55);
    }

    #[test]
    fn test_climb_stairs() {
        assert_eq!(climb_stairs(3), 3);
        assert_eq!(climb_stairs(5), 8);
    }

    #[test]
    fn test_knapsack_01() {
        let weights = [2, 3, 4, 5];
        let values = [3, 4, 5, 6];
        assert_eq!(knapsack_01(&weights, &values, 8), 10);
    }

    #[test]
    fn test_length_of_lis() {
        let nums = [10, 9, 2, 5, 3, 7, 101, 18];
        assert_eq!(length_of_lis(&nums), 4);
        assert_eq!(length_of_lis_fast(&nums), 4);
    }

    #[test]
    fn test_lcs() {
        assert_eq!(longest_common_subsequence("abcde", "ace"), 3);
        assert_eq!(longest_common_subsequence("abc", "def"), 0);
    }

    #[test]
    fn test_rob() {
        assert_eq!(rob(&[1, 2, 3, 1]), 4);
        assert_eq!(rob(&[2, 7, 9, 3, 1]), 12);
    }

    #[test]
    fn test_edit_distance() {
        assert_eq!(edit_distance("horse", "ros"), 3);
        assert_eq!(edit_distance("intention", "execution"), 5);
    }

    #[test]
    fn test_coin_change() {
        assert_eq!(coin_change(&[1, 2, 5], 11), 3);
        assert_eq!(coin_change(&[2], 3), -1);
    }
}
