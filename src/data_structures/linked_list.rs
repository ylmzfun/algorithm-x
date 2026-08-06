/// 链表
///
/// - 单链表：使用 `Box<T>` 实现的递归链表，展示 Rust 所有权模型
/// - 双链表：使用 `Rc<RefCell<T>>` 处理多重所有权
use std::fmt::Debug;

// ==================== 单链表 ====================

/// 单链表节点 — `Box` 确保编译期确定大小的递归类型
#[derive(Debug, PartialEq, Clone)]
pub struct ListNode<T> {
    pub val: T,
    pub next: Option<Box<ListNode<T>>>,
}

impl<T> ListNode<T> {
    pub fn new(val: T) -> Self {
        Self { val, next: None }
    }
}

/// 单链表
#[derive(Debug)]
pub struct SinglyLinkedList<T> {
    head: Option<Box<ListNode<T>>>,
    len: usize,
}

impl<T: Debug + PartialEq> SinglyLinkedList<T> {
    pub fn new() -> Self {
        Self { head: None, len: 0 }
    }

    pub fn len(&self) -> usize {
        self.len
    }

    pub fn is_empty(&self) -> bool {
        self.len == 0
    }

    /// 头插法 O(1) — 充分利用 Rust 所有权移动
    pub fn push_front(&mut self, val: T) {
        let new_node = Box::new(ListNode {
            val,
            next: self.head.take(),
        });
        self.head = Some(new_node);
        self.len += 1;
    }

    /// 头删 O(1)
    pub fn pop_front(&mut self) -> Option<T> {
        self.head.take().map(|mut old_head| {
            self.head = old_head.next.take();
            self.len -= 1;
            old_head.val
        })
    }

    /// 尾插 O(n)
    pub fn push_back(&mut self, val: T) {
        let new_node = Box::new(ListNode::new(val));
        if self.head.is_none() {
            self.head = Some(new_node);
            self.len = 1;
            return;
        }
        let mut curr = self.head.as_mut().unwrap();
        while curr.next.is_some() {
            curr = curr.next.as_mut().unwrap();
        }
        curr.next = Some(new_node);
        self.len += 1;
    }

    /// 查找是否存在某值 O(n)
    pub fn contains(&self, val: &T) -> bool {
        let mut curr = &self.head;
        while let Some(node) = curr {
            if &node.val == val {
                return true;
            }
            curr = &node.next;
        }
        false
    }

    /// 反转链表 — 迭代实现 O(n)
    pub fn reverse(&mut self) {
        let mut prev = None;
        let mut curr = self.head.take();
        while let Some(mut node) = curr {
            let next = node.next.take();
            node.next = prev;
            prev = Some(node);
            curr = next;
        }
        self.head = prev;
    }

    /// 获取中间节点（快慢指针）
    pub fn middle(&self) -> Option<&T> {
        let mut slow = &self.head;
        let mut fast = &self.head;
        loop {
            let fast_node = match fast.as_ref() {
                Some(n) => n,
                None => break,
            };
            if fast_node.next.is_none() {
                break;
            }
            fast = &fast_node.next.as_ref().unwrap().next;
            slow = &slow.as_ref().unwrap().next;
        }
        slow.as_ref().map(|n| &n.val)
    }

    /// 检测环 — Floyd 判圈算法
    /// 注意：普通单链表不会产生环；这里只为演示算法
    pub fn has_cycle(head: &Option<Box<ListNode<T>>>) -> bool {
        let mut slow = head;
        let mut fast = head;
        while fast.is_some() && fast.as_ref().unwrap().next.is_some() {
            slow = &slow.as_ref().unwrap().next;
            fast = &fast.as_ref().unwrap().next.as_ref().unwrap().next;
            if std::ptr::eq(
                slow.as_ref().map(|n| &**n).unwrap(),
                fast.as_ref().map(|n| &**n).unwrap(),
            ) {
                return true;
            }
        }
        false
    }
}

// ==================== 双链表 ====================

use std::cell::{Ref, RefCell};
use std::rc::Rc;

type Link<T> = Option<Rc<RefCell<DoublyNode<T>>>>;

#[derive(Debug)]
pub struct DoublyNode<T> {
    pub val: T,
    pub prev: Link<T>,
    pub next: Link<T>,
}

impl<T> DoublyNode<T> {
    pub fn new(val: T) -> Rc<RefCell<Self>> {
        Rc::new(RefCell::new(Self {
            val,
            prev: None,
            next: None,
        }))
    }
}

/// 双链表 — `Rc<RefCell<T>>` 实现多重所有权
#[derive(Debug)]
pub struct DoublyLinkedList<T> {
    head: Link<T>,
    tail: Link<T>,
    len: usize,
}

impl<T: Debug + PartialEq> DoublyLinkedList<T> {
    pub fn new() -> Self {
        Self {
            head: None,
            tail: None,
            len: 0,
        }
    }

    pub fn len(&self) -> usize {
        self.len
    }

    pub fn is_empty(&self) -> bool {
        self.len == 0
    }

    pub fn push_front(&mut self, val: T) {
        let new_node = DoublyNode::new(val);
        match self.head.take() {
            Some(old_head) => {
                old_head.borrow_mut().prev = Some(new_node.clone());
                new_node.borrow_mut().next = Some(old_head);
                self.head = Some(new_node);
            }
            None => {
                self.tail = Some(new_node.clone());
                self.head = Some(new_node);
            }
        }
        self.len += 1;
    }

    pub fn push_back(&mut self, val: T) {
        let new_node = DoublyNode::new(val);
        match self.tail.take() {
            Some(old_tail) => {
                old_tail.borrow_mut().next = Some(new_node.clone());
                new_node.borrow_mut().prev = Some(old_tail);
                self.tail = Some(new_node);
            }
            None => {
                self.head = Some(new_node.clone());
                self.tail = Some(new_node);
            }
        }
        self.len += 1;
    }

    pub fn pop_front(&mut self) -> Option<T> {
        self.head.take().map(|old_head| {
            match old_head.borrow_mut().next.take() {
                Some(new_head) => {
                    new_head.borrow_mut().prev = None;
                    self.head = Some(new_head);
                }
                None => {
                    self.tail = None;
                }
            }
            self.len -= 1;
            Rc::try_unwrap(old_head).ok().unwrap().into_inner().val
        })
    }

    pub fn pop_back(&mut self) -> Option<T> {
        self.tail.take().map(|old_tail| {
            match old_tail.borrow_mut().prev.take() {
                Some(new_tail) => {
                    new_tail.borrow_mut().next = None;
                    self.tail = Some(new_tail);
                }
                None => {
                    self.head = None;
                }
            }
            self.len -= 1;
            Rc::try_unwrap(old_tail).ok().unwrap().into_inner().val
        })
    }

    pub fn front(&self) -> Option<Ref<'_, T>> {
        self.head
            .as_ref()
            .map(|node| Ref::map(node.borrow(), |n| &n.val))
    }

    pub fn back(&self) -> Option<Ref<'_, T>> {
        self.tail
            .as_ref()
            .map(|node| Ref::map(node.borrow(), |n| &n.val))
    }
}

// ==================== 从 Vec 构造链表 ====================

impl<T: Debug + PartialEq> From<Vec<T>> for SinglyLinkedList<T> {
    fn from(values: Vec<T>) -> Self {
        let mut list = Self::new();
        for v in values.into_iter().rev() {
            list.push_front(v);
        }
        list
    }
}

/// 合并两个有序单链表（递归实现）
pub fn merge_two_sorted_lists<T: Ord>(
    l1: Option<Box<ListNode<T>>>,
    l2: Option<Box<ListNode<T>>>,
) -> Option<Box<ListNode<T>>> {
    match (l1, l2) {
        (None, None) => None,
        (Some(n), None) | (None, Some(n)) => Some(n),
        (Some(mut n1), Some(mut n2)) => {
            if n1.val <= n2.val {
                n1.next = merge_two_sorted_lists(n1.next.take(), Some(n2));
                Some(n1)
            } else {
                n2.next = merge_two_sorted_lists(Some(n1), n2.next.take());
                Some(n2)
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    // ===== 单链表测试 =====

    #[test]
    fn test_singly_push_front_pop_front() {
        let mut list = SinglyLinkedList::new();
        list.push_front(3);
        list.push_front(2);
        list.push_front(1);
        assert_eq!(list.len(), 3);
        assert_eq!(list.pop_front(), Some(1));
        assert_eq!(list.pop_front(), Some(2));
        assert_eq!(list.pop_front(), Some(3));
        assert_eq!(list.pop_front(), None);
        assert!(list.is_empty());
    }

    #[test]
    fn test_singly_push_back() {
        let mut list = SinglyLinkedList::new();
        list.push_back(1);
        list.push_back(2);
        list.push_back(3);
        assert_eq!(list.len(), 3);
        assert_eq!(list.pop_front(), Some(1));
        assert_eq!(list.pop_front(), Some(2));
        assert_eq!(list.pop_front(), Some(3));
    }

    #[test]
    fn test_singly_reverse() {
        let mut list: SinglyLinkedList<i32> = vec![1, 2, 3, 4, 5].into();
        list.reverse();
        assert_eq!(list.pop_front(), Some(5));
        assert_eq!(list.pop_front(), Some(4));
        assert_eq!(list.pop_front(), Some(3));
    }

    #[test]
    fn test_singly_contains() {
        let list: SinglyLinkedList<i32> = vec![1, 2, 3].into();
        assert!(list.contains(&2));
        assert!(!list.contains(&5));
    }

    #[test]
    fn test_singly_middle() {
        let list: SinglyLinkedList<i32> = vec![1, 2, 3, 4, 5].into();
        assert_eq!(list.middle(), Some(&3));

        let list: SinglyLinkedList<i32> = vec![1, 2, 3, 4].into();
        assert_eq!(list.middle(), Some(&3));
    }

    #[test]
    fn test_merge_two_sorted_lists() {
        let l1 = Some(Box::new(ListNode {
            val: 1,
            next: Some(Box::new(ListNode { val: 3, next: None })),
        }));
        let l2 = Some(Box::new(ListNode {
            val: 2,
            next: Some(Box::new(ListNode { val: 4, next: None })),
        }));
        let merged = merge_two_sorted_lists(l1, l2);
        let result: SinglyLinkedList<i32> = SinglyLinkedList {
            head: merged,
            len: 0,
        };
        assert!(result.contains(&1));
        assert!(result.contains(&2));
        assert!(result.contains(&3));
        assert!(result.contains(&4));
    }

    // ===== 双链表测试 =====

    #[test]
    fn test_doubly_push_pop() {
        let mut list = DoublyLinkedList::new();
        list.push_front(2);
        list.push_front(1);
        list.push_back(3);
        assert_eq!(list.len(), 3);
        assert_eq!(list.pop_front(), Some(1));
        assert_eq!(list.pop_back(), Some(3));
        assert_eq!(list.pop_front(), Some(2));
        assert!(list.is_empty());
    }
}
