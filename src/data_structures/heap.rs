/// 二叉堆 / 优先队列
///
/// 使用 `Vec` 实现的完全二叉树。
/// - 最小堆：父节点 ≤ 子节点
/// - 最大堆：父节点 ≥ 子节点

/// 最小堆 — 基于 Vec 实现
///
/// 索引关系：
/// - 父节点: (i - 1) / 2
/// - 左子节点: 2 * i + 1
/// - 右子节点: 2 * i + 2
#[derive(Debug)]
pub struct MinHeap<T: Ord> {
    data: Vec<T>,
}

impl<T: Ord> MinHeap<T> {
    pub fn new() -> Self {
        Self { data: Vec::new() }
    }

    pub fn with_capacity(cap: usize) -> Self {
        Self {
            data: Vec::with_capacity(cap),
        }
    }

    pub fn len(&self) -> usize {
        self.data.len()
    }

    pub fn is_empty(&self) -> bool {
        self.data.is_empty()
    }

    pub fn peek(&self) -> Option<&T> {
        self.data.first()
    }

    /// 插入元素 O(log n) — 上浮 (bubble-up)
    pub fn push(&mut self, item: T) {
        self.data.push(item);
        self.sift_up(self.data.len() - 1);
    }

    /// 删除堆顶 O(log n) — 下沉 (sink-down)
    pub fn pop(&mut self) -> Option<T> {
        if self.data.is_empty() {
            return None;
        }
        let last = self.data.pop().unwrap();
        if self.data.is_empty() {
            return Some(last);
        }
        let min = std::mem::replace(&mut self.data[0], last);
        self.sift_down(0);
        Some(min)
    }

    fn sift_up(&mut self, mut idx: usize) {
        while idx > 0 {
            let parent = (idx - 1) / 2;
            if self.data[idx] >= self.data[parent] {
                break;
            }
            self.data.swap(idx, parent);
            idx = parent;
        }
    }

    fn sift_down(&mut self, mut idx: usize) {
        let n = self.data.len();
        loop {
            let left = 2 * idx + 1;
            let right = 2 * idx + 2;
            let mut smallest = idx;
            if left < n && self.data[left] < self.data[smallest] {
                smallest = left;
            }
            if right < n && self.data[right] < self.data[smallest] {
                smallest = right;
            }
            if smallest == idx {
                break;
            }
            self.data.swap(idx, smallest);
            idx = smallest;
        }
    }
}

/// 最大堆
#[derive(Debug)]
pub struct MaxHeap<T: Ord> {
    data: Vec<T>,
}

impl<T: Ord> MaxHeap<T> {
    pub fn new() -> Self {
        Self { data: Vec::new() }
    }

    pub fn len(&self) -> usize {
        self.data.len()
    }

    pub fn is_empty(&self) -> bool {
        self.data.is_empty()
    }

    pub fn peek(&self) -> Option<&T> {
        self.data.first()
    }

    pub fn push(&mut self, item: T) {
        self.data.push(item);
        self.sift_up(self.data.len() - 1);
    }

    pub fn pop(&mut self) -> Option<T> {
        if self.data.is_empty() {
            return None;
        }
        let last = self.data.pop().unwrap();
        if self.data.is_empty() {
            return Some(last);
        }
        let max = std::mem::replace(&mut self.data[0], last);
        self.sift_down(0);
        Some(max)
    }

    fn sift_up(&mut self, mut idx: usize) {
        while idx > 0 {
            let parent = (idx - 1) / 2;
            if self.data[idx] <= self.data[parent] {
                break;
            }
            self.data.swap(idx, parent);
            idx = parent;
        }
    }

    fn sift_down(&mut self, mut idx: usize) {
        let n = self.data.len();
        loop {
            let left = 2 * idx + 1;
            let right = 2 * idx + 2;
            let mut largest = idx;
            if left < n && self.data[left] > self.data[largest] {
                largest = left;
            }
            if right < n && self.data[right] > self.data[largest] {
                largest = right;
            }
            if largest == idx {
                break;
            }
            self.data.swap(idx, largest);
            idx = largest;
        }
    }
}

/// 从 Vec 构建堆 — Floyd 建堆法 O(n)
///
/// 从最后一个非叶子节点开始向前下沉
impl<T: Ord> From<Vec<T>> for MinHeap<T> {
    fn from(items: Vec<T>) -> Self {
        let mut heap = Self { data: items };
        let n = heap.data.len();
        for i in (0..n / 2).rev() {
            heap.sift_down(i);
        }
        heap
    }
}

// ========== 堆的应用 ==========

/// 查找数组中第 k 大的元素 — 使用最小堆
///
/// 维护一个大小为 k 的最小堆，堆顶即为第 k 大。
/// 时间复杂度 O(n log k)
pub fn find_kth_largest(nums: &[i32], k: usize) -> Option<i32> {
    if k == 0 || nums.len() < k {
        return None;
    }
    let mut heap = MinHeap::new();
    for &num in nums {
        heap.push(num);
        if heap.len() > k {
            heap.pop();
        }
    }
    heap.peek().copied()
}

/// 堆排序 — 使用最大堆
///
/// 1. 将数组构建为最大堆
/// 2. 逐个将堆顶（最大值）移到数组末尾
/// 时间复杂度 O(n log n)，空间复杂度 O(1)（原地排序）
pub fn heap_sort<T: Ord>(arr: &mut [T]) {
    let n = arr.len();
    if n <= 1 {
        return;
    }
    // 建堆
    for i in (0..n / 2).rev() {
        max_heapify(arr, n, i);
    }
    // 排序
    for i in (1..n).rev() {
        arr.swap(0, i);
        max_heapify(arr, i, 0);
    }
}

fn max_heapify<T: Ord>(arr: &mut [T], heap_size: usize, mut i: usize) {
    loop {
        let left = 2 * i + 1;
        let right = 2 * i + 2;
        let mut largest = i;
        if left < heap_size && arr[left] > arr[largest] {
            largest = left;
        }
        if right < heap_size && arr[right] > arr[largest] {
            largest = right;
        }
        if largest == i {
            break;
        }
        arr.swap(i, largest);
        i = largest;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_min_heap_push_pop() {
        let mut heap = MinHeap::new();
        heap.push(5);
        heap.push(3);
        heap.push(8);
        heap.push(1);
        heap.push(6);
        assert_eq!(heap.peek(), Some(&1));
        assert_eq!(heap.pop(), Some(1));
        assert_eq!(heap.pop(), Some(3));
        assert_eq!(heap.pop(), Some(5));
        assert_eq!(heap.pop(), Some(6));
        assert_eq!(heap.pop(), Some(8));
        assert_eq!(heap.pop(), None);
    }

    #[test]
    fn test_max_heap() {
        let mut heap = MaxHeap::new();
        heap.push(5);
        heap.push(3);
        heap.push(8);
        heap.push(1);
        assert_eq!(heap.peek(), Some(&8));
        assert_eq!(heap.pop(), Some(8));
        assert_eq!(heap.pop(), Some(5));
        assert_eq!(heap.pop(), Some(3));
        assert_eq!(heap.pop(), Some(1));
    }

    #[test]
    fn test_heapify() {
        let heap = MinHeap::from(vec![5, 3, 8, 1, 6]);
        assert_eq!(heap.peek(), Some(&1));
    }

    #[test]
    fn test_find_kth_largest() {
        assert_eq!(find_kth_largest(&[3, 2, 1, 5, 6, 4], 2), Some(5));
        assert_eq!(find_kth_largest(&[3, 2, 3, 1, 2, 4, 5, 5, 6], 4), Some(4));
    }

    #[test]
    fn test_heap_sort() {
        let mut arr = [5, 3, 8, 1, 6, 2, 7, 4];
        heap_sort(&mut arr);
        assert_eq!(arr, [1, 2, 3, 4, 5, 6, 7, 8]);

        let mut arr2: [i32; 0] = [];
        heap_sort(&mut arr2);
    }
}
