/// 二叉搜索树 (BST)
///
/// 性质：左子树所有值 < 根节点值 < 右子树所有值
/// 操作：插入、删除、查找、验证 BST 性质
use std::cmp::Ordering;
use std::fmt::Debug;

#[derive(Debug, PartialEq)]
pub struct BSTNode<T> {
    pub val: T,
    pub left: Option<Box<BSTNode<T>>>,
    pub right: Option<Box<BSTNode<T>>>,
}

impl<T: Debug> BSTNode<T> {
    pub fn new(val: T) -> Self {
        Self {
            val,
            left: None,
            right: None,
        }
    }
}

pub struct BinarySearchTree<T: Ord> {
    root: Option<Box<BSTNode<T>>>,
    len: usize,
}

impl<T: Ord + Debug> BinarySearchTree<T> {
    pub fn new() -> Self {
        Self { root: None, len: 0 }
    }

    pub fn len(&self) -> usize {
        self.len
    }

    pub fn is_empty(&self) -> bool {
        self.len == 0
    }

    /// 插入 — O(h)，h 为树高，平均 O(log n)
    pub fn insert(&mut self, val: T) {
        self.root = Self::insert_node(self.root.take(), val);
        self.len += 1;
    }

    fn insert_node(node: Option<Box<BSTNode<T>>>, val: T) -> Option<Box<BSTNode<T>>> {
        match node {
            None => Some(Box::new(BSTNode::new(val))),
            Some(mut n) => {
                match val.cmp(&n.val) {
                    Ordering::Less => {
                        n.left = Self::insert_node(n.left.take(), val);
                    }
                    Ordering::Greater => {
                        n.right = Self::insert_node(n.right.take(), val);
                    }
                    Ordering::Equal => return Some(n), // 不允许重复
                }
                Some(n)
            }
        }
    }

    /// 查找 — O(h)
    pub fn contains(&self, val: &T) -> bool {
        let mut curr = &self.root;
        while let Some(node) = curr {
            match val.cmp(&node.val) {
                Ordering::Less => curr = &node.left,
                Ordering::Greater => curr = &node.right,
                Ordering::Equal => return true,
            }
        }
        false
    }

    /// 删除 — O(h)
    ///
    /// 三种情况：
    /// 1. 叶子节点：直接删除
    /// 2. 只有一个子节点：用子节点替换
    /// 3. 有两个子节点：用后继（右子树最小节点）替换
    pub fn remove(&mut self, val: &T) -> bool {
        let (new_root, removed) = Self::remove_node(self.root.take(), val);
        self.root = new_root;
        if removed {
            self.len -= 1;
        }
        removed
    }

    fn remove_node(node: Option<Box<BSTNode<T>>>, val: &T) -> (Option<Box<BSTNode<T>>>, bool) {
        match node {
            None => (None, false),
            Some(mut n) => match val.cmp(&n.val) {
                Ordering::Less => {
                    let (new_left, removed) = Self::remove_node(n.left.take(), val);
                    n.left = new_left;
                    (Some(n), removed)
                }
                Ordering::Greater => {
                    let (new_right, removed) = Self::remove_node(n.right.take(), val);
                    n.right = new_right;
                    (Some(n), removed)
                }
                Ordering::Equal => {
                    // 情况1 & 2：0 或 1 个子节点
                    if n.left.is_none() {
                        return (n.right.take(), true);
                    }
                    if n.right.is_none() {
                        return (n.left.take(), true);
                    }
                    // 情况3：有两个子节点，找后继
                    let successor = Self::extract_min(&mut n.right);
                    if let Some(mut succ) = successor {
                        succ.left = n.left.take();
                        succ.right = n.right.take();
                        (Some(succ), true)
                    } else {
                        (Some(n), false)
                    }
                }
            },
        }
    }

    /// 从子树中弹出最小节点
    fn extract_min(node: &mut Option<Box<BSTNode<T>>>) -> Option<Box<BSTNode<T>>> {
        if node.is_none() {
            return None;
        }
        if node.as_ref().unwrap().left.is_none() {
            let mut min = node.take().unwrap();
            *node = min.right.take();
            Some(min)
        } else {
            Self::extract_min(&mut node.as_mut().unwrap().left)
        }
    }

    /// 中序遍历 — 输出有序序列
    pub fn inorder(&self) -> Vec<&T> {
        fn traverse<'a, T>(node: &'a Option<Box<BSTNode<T>>>, result: &mut Vec<&'a T>) {
            if let Some(n) = node {
                traverse(&n.left, result);
                result.push(&n.val);
                traverse(&n.right, result);
            }
        }
        let mut result = Vec::new();
        traverse(&self.root, &mut result);
        result
    }
}

/// 验证二叉搜索树（迭代，使用中序遍历）
///
/// 检查中序遍历结果是否为严格递增序列。
pub fn validate_bst<T: Ord>(root: &Option<Box<BSTNode<T>>>) -> bool {
    let mut prev: Option<&T> = None;
    let mut stack: Vec<&Box<BSTNode<T>>> = Vec::new();
    let mut curr = root.as_ref();

    while curr.is_some() || !stack.is_empty() {
        while let Some(node) = curr {
            stack.push(node);
            curr = node.left.as_ref();
        }
        if let Some(node) = stack.pop() {
            if let Some(p) = prev {
                if node.val <= *p {
                    return false;
                }
            }
            prev = Some(&node.val);
            curr = node.right.as_ref();
        }
    }
    true
}

/// 有序数组转平衡二叉搜索树（分治法）
///
/// 取中间元素为根，递归构造左右子树。
pub fn sorted_array_to_bst<T: Copy + Debug>(arr: &[T]) -> Option<Box<BSTNode<T>>> {
    if arr.is_empty() {
        return None;
    }
    let mid = arr.len() / 2;
    let mut root = Box::new(BSTNode::new(arr[mid]));
    root.left = sorted_array_to_bst(&arr[..mid]);
    root.right = sorted_array_to_bst(&arr[mid + 1..]);
    Some(root)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bst_insert_contains() {
        let mut bst = BinarySearchTree::new();
        bst.insert(5);
        bst.insert(3);
        bst.insert(7);
        bst.insert(1);
        bst.insert(9);
        assert_eq!(bst.len(), 5);
        assert!(bst.contains(&5));
        assert!(bst.contains(&1));
        assert!(bst.contains(&9));
        assert!(!bst.contains(&4));
    }

    #[test]
    fn test_bst_inorder() {
        let mut bst = BinarySearchTree::new();
        bst.insert(5);
        bst.insert(3);
        bst.insert(7);
        bst.insert(1);
        bst.insert(9);
        let inorder: Vec<i32> = bst.inorder().into_iter().copied().collect();
        assert_eq!(inorder, vec![1, 3, 5, 7, 9]);
    }

    #[test]
    fn test_bst_remove() {
        let mut bst = BinarySearchTree::new();
        bst.insert(5);
        bst.insert(3);
        bst.insert(7);
        bst.insert(1);
        bst.insert(9);

        assert!(bst.remove(&1));
        assert!(!bst.contains(&1));
        assert_eq!(bst.len(), 4);

        assert!(bst.remove(&5));
        assert!(!bst.contains(&5));
        assert_eq!(bst.len(), 3);

        let inorder: Vec<i32> = bst.inorder().into_iter().copied().collect();
        assert_eq!(inorder, vec![3, 7, 9]);
    }

    #[test]
    fn test_validate_bst() {
        let mut bst = BinarySearchTree::new();
        bst.insert(2);
        bst.insert(1);
        bst.insert(3);
        assert!(validate_bst(&bst.root));
    }

    #[test]
    fn test_sorted_array_to_bst() {
        let arr = [1, 2, 3, 4, 5, 6, 7];
        let root = sorted_array_to_bst(&arr);
        assert!(validate_bst(&root));
    }
}
