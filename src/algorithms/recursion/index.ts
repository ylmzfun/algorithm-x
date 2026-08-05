// 全排列
export function permute<T>(arr: T[]): T[][] {
  const result: T[][] = [];
  const used = new Array(arr.length).fill(false);

  function backtrack(path: T[]) {
    if (path.length === arr.length) {
      result.push([...path]);
      return;
    }
    for (let i = 0; i < arr.length; i++) {
      if (used[i]) continue;
      used[i] = true;
      path.push(arr[i]);
      backtrack(path);
      path.pop();
      used[i] = false;
    }
  }

  backtrack([]);
  return result;
}

// 所有子集
export function subsets<T>(arr: T[]): T[][] {
  const result: T[][] = [];

  function backtrack(start: number, path: T[]) {
    result.push([...path]);
    for (let i = start; i < arr.length; i++) {
      path.push(arr[i]);
      backtrack(i + 1, path);
      path.pop();
    }
  }

  backtrack(0, []);
  return result;
}

// N 皇后 —— 返回所有解法（棋盘布局），-1 表示空，1 表示皇后
export function solveNQueens(n: number): number[][][] {
  const result: number[][][] = [];
  const cols = new Array(n).fill(false);
  const diag1 = new Array(2 * n - 1).fill(false); // 主对角线 r-c
  const diag2 = new Array(2 * n - 1).fill(false); // 副对角线 r+c
  const board: number[][] = Array.from({ length: n }, () => new Array(n).fill(0));

  function backtrack(row: number) {
    if (row === n) {
      result.push(board.map((r) => [...r]));
      return;
    }
    for (let col = 0; col < n; col++) {
      if (cols[col] || diag1[row - col + n - 1] || diag2[row + col]) continue;
      cols[col] = diag1[row - col + n - 1] = diag2[row + col] = true;
      board[row][col] = 1;
      backtrack(row + 1);
      board[row][col] = 0;
      cols[col] = diag1[row - col + n - 1] = diag2[row + col] = false;
    }
  }

  backtrack(0);
  return result;
}

// 组合求和 —— 从 arr 中找出所有和等于 target 的组合（可重复使用元素）
export function combinationSum(arr: number[], target: number): number[][] {
  const result: number[][] = [];

  function backtrack(start: number, path: number[], sum: number) {
    if (sum === target) {
      result.push([...path]);
      return;
    }
    if (sum > target) return;
    for (let i = start; i < arr.length; i++) {
      path.push(arr[i]);
      backtrack(i, path, sum + arr[i]);
      path.pop();
    }
  }

  backtrack(0, [], 0);
  return result;
}
