/// 队列 (Queue)
///
/// FIFO (First In, First Out) 数据结构。
/// 包含普通队列、双端队列 (Deque)、循环队列。

use std::collections::VecDeque;

// ==================== 循环队列 ====================

/// 循环队列（环形缓冲）
///
/// 使用定长数组 + 两个指针实现，避免频繁分配内存。
/// - `head` 指向队首元素
/// - `tail` 指向下一个入队位置
/// - 牺牲一个位置来区分队空和队满
pub struct CircularQueue<T> {
    data: Vec<Option<T>>,
    head: usize,
    tail: usize,
    cap: usize,
}

impl<T: std::fmt::Debug> CircularQueue<T> {
    /// 创建容量为 k 的循环队列（实际分配 k+1，预留一个空位）
    pub fn new(k: usize) -> Self {
        let cap = k + 1;
        let mut data = Vec::with_capacity(cap);
        for _ in 0..cap {
            data.push(None);
        }
        Self {
            data,
            head: 0,
            tail: 0,
            cap,
        }
    }

    pub fn enqueue(&mut self, item: T) -> bool {
        if self.is_full() {
            return false;
        }
        self.data[self.tail] = Some(item);
        self.tail = (self.tail + 1) % self.cap;
        true
    }

    pub fn dequeue(&mut self) -> Option<T> {
        if self.is_empty() {
            return None;
        }
        let val = self.data[self.head].take();
        self.head = (self.head + 1) % self.cap;
        val
    }

    pub fn front(&self) -> Option<&T> {
        if self.is_empty() {
            None
        } else {
            self.data[self.head].as_ref()
        }
    }

    pub fn rear(&self) -> Option<&T> {
        if self.is_empty() {
            None
        } else {
            let idx = (self.tail + self.cap - 1) % self.cap;
            self.data[idx].as_ref()
        }
    }

    pub fn is_empty(&self) -> bool {
        self.head == self.tail
    }

    pub fn is_full(&self) -> bool {
        (self.tail + 1) % self.cap == self.head
    }

    pub fn len(&self) -> usize {
        if self.tail >= self.head {
            self.tail - self.head
        } else {
            self.cap - self.head + self.tail
        }
    }
}

// ==================== 单调队列 ====================

/// 滑动窗口最大值 — 单调队列经典应用
///
/// 给定数组 nums 和窗口大小 k，返回每个窗口内的最大值。
/// 时间复杂度 O(n)
pub fn max_sliding_window(nums: &[i32], k: usize) -> Vec<i32> {
    if nums.is_empty() || k == 0 {
        return vec![];
    }
    let mut result = Vec::with_capacity(nums.len() - k + 1);
    let mut deque = VecDeque::new(); // 存索引，维护单调递减

    for i in 0..nums.len() {
        // 移除窗口外的元素
        while let Some(&front) = deque.front() {
            if front + k <= i {
                deque.pop_front();
            } else {
                break;
            }
        }
        // 维护单调递减
        while let Some(&back) = deque.back() {
            if nums[back] <= nums[i] {
                deque.pop_back();
            } else {
                break;
            }
        }
        deque.push_back(i);
        // 窗口形成后记录结果
        if i >= k - 1 {
            result.push(nums[*deque.front().unwrap()]);
        }
    }
    result
}

// ==================== BFS 辅助函数 ====================

/// 使用队列实现的 BFS 层序遍历（以二维网格为例）
///
/// 返回从 (start_r, start_c) 出发到达每个点的最短距离（-1 表示不可达）
pub fn bfs_grid(grid: &[Vec<i32>], start: (usize, usize)) -> Vec<Vec<i32>> {
    let rows = grid.len();
    let cols = if rows > 0 { grid[0].len() } else { 0 };
    let mut dist = vec![vec![-1; cols]; rows];

    if grid[start.0][start.1] == 1 {
        return dist; // 障碍物
    }

    let mut queue = VecDeque::new();
    queue.push_back(start);
    dist[start.0][start.1] = 0;

    let dirs = [(0, 1), (1, 0), (0, -1i32), (-1i32, 0)];

    while let Some((r, c)) = queue.pop_front() {
        for (dr, dc) in &dirs {
            let nr = r as i32 + dr;
            let nc = c as i32 + dc;
            if nr >= 0 && nr < rows as i32 && nc >= 0 && nc < cols as i32 {
                let (nr, nc) = (nr as usize, nc as usize);
                if dist[nr][nc] == -1 && grid[nr][nc] == 0 {
                    dist[nr][nc] = dist[r][c] + 1;
                    queue.push_back((nr, nc));
                }
            }
        }
    }
    dist
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_circular_queue() {
        let mut q = CircularQueue::new(3);
        assert!(q.is_empty());
        assert!(q.enqueue(1));
        assert!(q.enqueue(2));
        assert!(q.enqueue(3));
        assert!(!q.enqueue(4)); // 满
        assert_eq!(q.front(), Some(&1));
        assert_eq!(q.rear(), Some(&3));
        assert_eq!(q.dequeue(), Some(1));
        assert!(q.enqueue(4));
        assert_eq!(q.rear(), Some(&4));
        assert_eq!(q.len(), 3);
    }

    #[test]
    fn test_max_sliding_window() {
        assert_eq!(
            max_sliding_window(&[1, 3, -1, -3, 5, 3, 6, 7], 3),
            vec![3, 3, 5, 5, 6, 7]
        );
        assert_eq!(max_sliding_window(&[1], 1), vec![1]);
    }

    #[test]
    fn test_bfs_grid() {
        let grid = vec![
            vec![0, 0, 0],
            vec![0, 1, 0],
            vec![0, 0, 0],
        ];
        let dist = bfs_grid(&grid, (0, 0));
        assert_eq!(dist[2][2], 4);
        assert_eq!(dist[1][1], -1); // 障碍物
    }
}
