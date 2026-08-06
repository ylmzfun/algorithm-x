/// 动态数组深入
///
/// 演示 Rust `Vec` 的内部原理：扩容策略、常见遍历模式、
/// 以及手动实现一个简易动态数组来理解内存管理。

/// 简易动态数组实现 — 理解 Vec 的底层原理
///
/// 核心概念：
/// - 在堆上分配连续内存
/// - 当容量不足时，分配更大的内存并将元素移动过去（扩容策略）
/// - 通过 `ptr` 管理原始指针，手动处理内存分配与释放
pub struct MyVec<T> {
    ptr: *mut T,
    len: usize,
    cap: usize,
}

impl<T> MyVec<T> {
    pub fn new() -> Self {
        Self {
            ptr: std::ptr::null_mut(),
            len: 0,
            cap: 0,
        }
    }

    pub fn with_capacity(cap: usize) -> Self {
        let layout = std::alloc::Layout::array::<T>(cap).unwrap();
        let ptr = if cap > 0 {
            unsafe { std::alloc::alloc(layout) as *mut T }
        } else {
            std::ptr::null_mut()
        };
        Self { ptr, len: 0, cap }
    }

    pub fn len(&self) -> usize {
        self.len
    }

    pub fn is_empty(&self) -> bool {
        self.len == 0
    }

    pub fn capacity(&self) -> usize {
        self.cap
    }

    /// 摊销 O(1)：多数情况直接写入，仅在容量不足时触发 O(n) 扩容
    ///
    /// Rust 的 Vec 扩容系数通常为 2，保持摊销常数时间
    pub fn push(&mut self, value: T) {
        if self.len == self.cap {
            self.grow();
        }
        unsafe {
            self.ptr.add(self.len).write(value);
        }
        self.len += 1;
    }

    pub fn pop(&mut self) -> Option<T> {
        if self.len == 0 {
            None
        } else {
            self.len -= 1;
            unsafe { Some(self.ptr.add(self.len).read()) }
        }
    }

    pub fn get(&self, index: usize) -> Option<&T> {
        if index >= self.len {
            None
        } else {
            unsafe { Some(&*self.ptr.add(index)) }
        }
    }

    fn grow(&mut self) {
        let new_cap = if self.cap == 0 { 4 } else { self.cap * 2 };
        let new_layout = std::alloc::Layout::array::<T>(new_cap).unwrap();
        let new_ptr = unsafe { std::alloc::alloc(new_layout) as *mut T };

        // 将旧数据移动到新内存
        for i in 0..self.len {
            unsafe {
                new_ptr.add(i).write(self.ptr.add(i).read());
            }
        }

        // 释放旧内存
        if self.cap > 0 {
            let old_layout = std::alloc::Layout::array::<T>(self.cap).unwrap();
            unsafe { std::alloc::dealloc(self.ptr as *mut u8, old_layout) };
        }

        self.ptr = new_ptr;
        self.cap = new_cap;
    }
}

impl<T> Drop for MyVec<T> {
    fn drop(&mut self) {
        // 逐个删除有效元素（调用其 Drop）
        for i in 0..self.len {
            unsafe {
                std::ptr::drop_in_place(self.ptr.add(i));
            }
        }
        // 释放底层内存
        if self.cap > 0 {
            let layout = std::alloc::Layout::array::<T>(self.cap).unwrap();
            unsafe { std::alloc::dealloc(self.ptr as *mut u8, layout) };
        }
    }
}

// ========== 常用数组操作 ==========

/// 双指针反转数组
pub fn reverse<T>(arr: &mut [T]) {
    let mut left = 0;
    let mut right = arr.len().wrapping_sub(1);
    while left < right {
        arr.swap(left, right);
        left += 1;
        right = right.wrapping_sub(1);
    }
}

/// 移除有序数组中的重复项，返回去重后长度（双指针，原地修改）
pub fn remove_duplicates<T: PartialEq>(arr: &mut Vec<T>) -> usize {
    if arr.is_empty() {
        return 0;
    }
    let mut slow = 0;
    for fast in 1..arr.len() {
        if arr[fast] != arr[slow] {
            slow += 1;
            arr.swap(slow, fast);
        }
    }
    slow + 1
}

/// 合并两个有序数组（结果存入 nums1，假设 nums1 有足够容量）
pub fn merge_sorted(nums1: &mut Vec<i32>, m: usize, nums2: &[i32], n: usize) {
    let mut i = m as i32 - 1;
    let mut j = n as i32 - 1;
    let mut k = (m + n) as i32 - 1;
    nums1.resize(m + n, 0);
    while j >= 0 {
        if i >= 0 && nums1[i as usize] > nums2[j as usize] {
            nums1[k as usize] = nums1[i as usize];
            i -= 1;
        } else {
            nums1[k as usize] = nums2[j as usize];
            j -= 1;
        }
        k -= 1;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_my_vec_push_pop() {
        let mut v = MyVec::new();
        assert!(v.is_empty());
        v.push(1);
        v.push(2);
        v.push(3);
        assert_eq!(v.len(), 3);
        assert_eq!(v.pop(), Some(3));
        assert_eq!(v.pop(), Some(2));
        assert_eq!(v.pop(), Some(1));
        assert_eq!(v.pop(), None);
    }

    #[test]
    fn test_my_vec_grow() {
        let mut v = MyVec::new();
        for i in 0..100 {
            v.push(i);
        }
        assert_eq!(v.len(), 100);
        assert_eq!(v.get(0), Some(&0));
        assert_eq!(v.get(99), Some(&99));
    }

    #[test]
    fn test_reverse() {
        let mut arr = [1, 2, 3, 4, 5];
        reverse(&mut arr);
        assert_eq!(arr, [5, 4, 3, 2, 1]);
    }

    #[test]
    fn test_remove_duplicates() {
        let mut v = vec![1, 1, 2, 2, 3, 4, 4, 5];
        let new_len = remove_duplicates(&mut v);
        assert_eq!(&v[..new_len], &[1, 2, 3, 4, 5]);
    }

    #[test]
    fn test_merge_sorted() {
        let mut nums1 = vec![1, 3, 5];
        let nums2 = vec![2, 4, 6];
        merge_sorted(&mut nums1, 3, &nums2, 3);
        assert_eq!(nums1, vec![1, 2, 3, 4, 5, 6]);
    }
}
