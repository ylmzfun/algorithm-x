/// 回溯算法 (Backtracking)
///
/// 核心思想：在解空间中深度优先搜索，遇到不可行的分支时剪枝回退。
/// 回溯 = DFS + 剪枝
///
/// 适用场景：
/// - 组合问题
/// - 排列问题
/// - 子集问题
/// - 棋盘问题 (N 皇后、数独)

/// 全排列
///
/// 给定不含重复数字的数组，返回所有可能的排列。
pub fn permute(nums: &[i32]) -> Vec<Vec<i32>> {
    let mut result = Vec::new();
    let mut current = Vec::new();
    let mut used = vec![false; nums.len()];

    fn backtrack(
        nums: &[i32],
        current: &mut Vec<i32>,
        used: &mut [bool],
        result: &mut Vec<Vec<i32>>,
    ) {
        if current.len() == nums.len() {
            result.push(current.clone());
            return;
        }
        for i in 0..nums.len() {
            if used[i] {
                continue;
            }
            used[i] = true;
            current.push(nums[i]);
            backtrack(nums, current, used, result);
            current.pop();
            used[i] = false;
        }
    }

    backtrack(nums, &mut current, &mut used, &mut result);
    result
}

/// 含重复数字的全排列
///
/// 先排序，回溯时跳过同层重复元素。
pub fn permute_unique(nums: &[i32]) -> Vec<Vec<i32>> {
    let mut nums = nums.to_vec();
    nums.sort_unstable();
    let mut result = Vec::new();
    let mut current = Vec::new();
    let mut used = vec![false; nums.len()];

    fn backtrack(
        nums: &[i32],
        current: &mut Vec<i32>,
        used: &mut [bool],
        result: &mut Vec<Vec<i32>>,
    ) {
        if current.len() == nums.len() {
            result.push(current.clone());
            return;
        }
        for i in 0..nums.len() {
            if used[i] {
                continue;
            }
            // 跳过同层重复：当前元素与前一个相同，且前一个未使用
            if i > 0 && nums[i] == nums[i - 1] && !used[i - 1] {
                continue;
            }
            used[i] = true;
            current.push(nums[i]);
            backtrack(nums, current, used, result);
            current.pop();
            used[i] = false;
        }
    }

    backtrack(&nums, &mut current, &mut used, &mut result);
    result
}

/// 组合 — 从 [1..n] 中选 k 个数的所有组合
pub fn combine(n: i32, k: i32) -> Vec<Vec<i32>> {
    let mut result = Vec::new();
    let mut current = Vec::new();

    fn backtrack(start: i32, n: i32, k: i32, current: &mut Vec<i32>, result: &mut Vec<Vec<i32>>) {
        if current.len() == k as usize {
            result.push(current.clone());
            return;
        }
        // 剪枝：剩余数字不够
        let need = k as usize - current.len();
        for i in start..=n - need as i32 + 1 {
            current.push(i);
            backtrack(i + 1, n, k, current, result);
            current.pop();
        }
    }

    backtrack(1, n, k, &mut current, &mut result);
    result
}

/// 子集
///
/// 返回数组的所有子集（幂集），解空间大小 2ⁿ。
pub fn subsets(nums: &[i32]) -> Vec<Vec<i32>> {
    let mut result = Vec::new();
    let mut current = Vec::new();

    fn backtrack(nums: &[i32], start: usize, current: &mut Vec<i32>, result: &mut Vec<Vec<i32>>) {
        result.push(current.clone());
        for i in start..nums.len() {
            current.push(nums[i]);
            backtrack(nums, i + 1, current, result);
            current.pop();
        }
    }

    backtrack(nums, 0, &mut current, &mut result);
    result
}

/// 组合总和 — 可重复选取元素，使其和等于 target
///
/// candidates 中无重复元素。
pub fn combination_sum(candidates: &[i32], target: i32) -> Vec<Vec<i32>> {
    let mut result = Vec::new();
    let mut current = Vec::new();

    fn backtrack(
        candidates: &[i32],
        start: usize,
        target: i32,
        sum: i32,
        current: &mut Vec<i32>,
        result: &mut Vec<Vec<i32>>,
    ) {
        if sum == target {
            result.push(current.clone());
            return;
        }
        if sum > target {
            return;
        }
        for i in start..candidates.len() {
            current.push(candidates[i]);
            backtrack(candidates, i, target, sum + candidates[i], current, result);
            current.pop();
        }
    }

    backtrack(candidates, 0, target, 0, &mut current, &mut result);
    result
}

/// N 皇后
///
/// 返回所有合法的 n 皇后摆放方案。
pub fn solve_n_queens(n: usize) -> Vec<Vec<String>> {
    let mut result = Vec::new();
    let mut board = vec![vec!['.'; n]; n];

    fn is_safe(board: &[Vec<char>], row: usize, col: usize, n: usize) -> bool {
        // 检查同列上方
        for r in 0..row {
            if board[r][col] == 'Q' {
                return false;
            }
        }
        // 检查左上方对角线
        let (mut r, mut c) = (row as i32 - 1, col as i32 - 1);
        while r >= 0 && c >= 0 {
            if board[r as usize][c as usize] == 'Q' {
                return false;
            }
            r -= 1;
            c -= 1;
        }
        // 检查右上方对角线
        let (mut r, mut c) = (row as i32 - 1, col + 1);
        while r >= 0 && c < n {
            if board[r as usize][c] == 'Q' {
                return false;
            }
            r -= 1;
            c += 1;
        }
        true
    }

    fn backtrack(
        row: usize,
        n: usize,
        board: &mut Vec<Vec<char>>,
        result: &mut Vec<Vec<String>>,
    ) {
        if row == n {
            let solution: Vec<String> = board
                .iter()
                .map(|r| r.iter().collect())
                .collect();
            result.push(solution);
            return;
        }
        for col in 0..n {
            if is_safe(board, row, col, n) {
                board[row][col] = 'Q';
                backtrack(row + 1, n, board, result);
                board[row][col] = '.';
            }
        }
    }

    backtrack(0, n, &mut board, &mut result);
    result
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_permute() {
        let result = permute(&[1, 2, 3]);
        assert_eq!(result.len(), 6); // 3! = 6
    }

    #[test]
    fn test_permute_unique() {
        let result = permute_unique(&[1, 1, 2]);
        assert_eq!(result.len(), 3); // [1,1,2], [1,2,1], [2,1,1]
    }

    #[test]
    fn test_combine() {
        let result = combine(4, 2);
        assert_eq!(result.len(), 6); // C(4,2) = 6
    }

    #[test]
    fn test_subsets() {
        let result = subsets(&[1, 2, 3]);
        assert_eq!(result.len(), 8); // 2³ = 8
    }

    #[test]
    fn test_combination_sum() {
        let result = combination_sum(&[2, 3, 6, 7], 7);
        assert_eq!(result.len(), 2); // [2,2,3] 和 [7]
    }

    #[test]
    fn test_solve_n_queens() {
        let result = solve_n_queens(4);
        assert_eq!(result.len(), 2); // 4 皇后有 2 个解
    }
}
