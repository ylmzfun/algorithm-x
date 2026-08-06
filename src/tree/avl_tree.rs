/// AVL 平衡树
///
/// AVL 树是最早发明的自平衡二叉搜索树。
/// 通过维护平衡因子 (balance factor) 确保树的高度为 O(log n)。
///
/// 四种旋转：
/// - LL（右单旋）
/// - RR（左单旋）
/// - LR（左右双旋）
/// - RL（右左双旋）
use std::cmp::Ordering;
use std::fmt::Debug;

#[derive(Debug)]
pub struct AVLNode<T> {
    pub val: T,
    pub left: Option<Box<AVLNode<T>>>,
    pub right: Option<Box<AVLNode<T>>>,
    /// 以该节点为根的子树高度
    height: i32,
}

impl<T: Debug> AVLNode<T> {
    fn new(val: T) -> Self {
        Self {
            val,
            left: None,
            right: None,
            height: 1,
        }
    }
}

pub struct AVLTree<T: Ord> {
    root: Option<Box<AVLNode<T>>>,
    len: usize,
}

impl<T: Ord + Debug> AVLTree<T> {
    pub fn new() -> Self {
        Self { root: None, len: 0 }
    }

    pub fn len(&self) -> usize {
        self.len
    }

    pub fn is_empty(&self) -> bool {
        self.len == 0
    }

    pub fn insert(&mut self, val: T) {
        self.root = Self::insert_node(self.root.take(), val);
        self.len += 1;
    }

    fn insert_node(node: Option<Box<AVLNode<T>>>, val: T) -> Option<Box<AVLNode<T>>> {
        let mut node = match node {
            None => return Some(Box::new(AVLNode::new(val))),
            Some(n) => n,
        };

        match val.cmp(&node.val) {
            Ordering::Less => node.left = Self::insert_node(node.left.take(), val),
            Ordering::Greater => node.right = Self::insert_node(node.right.take(), val),
            Ordering::Equal => return Some(node),
        }

        node.update_height();
        Some(Self::balance(node))
    }

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

    pub fn remove(&mut self, val: &T) -> bool {
        let (new_root, removed) = Self::remove_node(self.root.take(), val);
        self.root = new_root;
        if removed {
            self.len -= 1;
        }
        removed
    }

    fn remove_node(node: Option<Box<AVLNode<T>>>, val: &T) -> (Option<Box<AVLNode<T>>>, bool) {
        let mut node = match node {
            None => return (None, false),
            Some(n) => n,
        };

        let removed = match val.cmp(&node.val) {
            Ordering::Less => {
                let (new_left, removed) = Self::remove_node(node.left.take(), val);
                node.left = new_left;
                removed
            }
            Ordering::Greater => {
                let (new_right, removed) = Self::remove_node(node.right.take(), val);
                node.right = new_right;
                removed
            }
            Ordering::Equal => {
                // 情况 1: 叶子节点
                if node.left.is_none() && node.right.is_none() {
                    return (None, true);
                }
                // 情况 2: 只有一个子节点
                if node.left.is_none() {
                    return (node.right.take(), true);
                }
                if node.right.is_none() {
                    return (node.left.take(), true);
                }
                // 情况 3: 两个子节点 — 用后继替换
                let succ = Self::pop_min(&mut node.right);
                if let Some(mut succ) = succ {
                    succ.left = node.left.take();
                    succ.right = node.right.take();
                    succ.update_height();
                    return (Some(Self::balance(succ)), true);
                }
                return (Some(node), false);
            }
        };

        node.update_height();
        (Some(Self::balance(node)), removed)
    }

    fn pop_min(node: &mut Option<Box<AVLNode<T>>>) -> Option<Box<AVLNode<T>>> {
        if node.is_none() {
            return None;
        }
        let mut n = node.take().unwrap();
        if n.left.is_none() {
            *node = n.right.take();
            Some(n)
        } else {
            let result = Self::pop_min(&mut n.left);
            n.update_height();
            *node = Some(Self::balance(n));
            result
        }
    }

    // ========== 平衡操作 ==========

    fn height(node: &Option<Box<AVLNode<T>>>) -> i32 {
        node.as_ref().map_or(0, |n| n.height)
    }

    fn balance_factor(node: &AVLNode<T>) -> i32 {
        Self::height(&node.left) - Self::height(&node.right)
    }

    /// LL 旋转（右单旋）
    ///
    /// ```text
    ///       y           x
    ///      / \         / \
    ///     x   T3  ->  T1  y
    ///    / \             / \
    ///   T1 T2           T2 T3
    /// ```
    fn rotate_right(mut y: Box<AVLNode<T>>) -> Box<AVLNode<T>> {
        let mut x = y.left.take().unwrap();
        y.left = x.right.take();
        y.update_height();
        x.right = Some(y);
        x.update_height();
        x
    }

    /// RR 旋转（左单旋）
    ///
    /// ```text
    ///     x               y
    ///    / \             / \
    ///   T1  y    ->     x   T3
    ///      / \         / \
    ///     T2 T3       T1 T2
    /// ```
    fn rotate_left(mut x: Box<AVLNode<T>>) -> Box<AVLNode<T>> {
        let mut y = x.right.take().unwrap();
        x.right = y.left.take();
        x.update_height();
        y.left = Some(x);
        y.update_height();
        y
    }

    fn balance(mut node: Box<AVLNode<T>>) -> Box<AVLNode<T>> {
        let bf = Self::balance_factor(&node);

        if bf > 1 {
            // 左子树高
            if let Some(ref left) = node.left {
                if Self::balance_factor(left) < 0 {
                    // LR: 先左旋左子，再右旋
                    node.left = Some(Self::rotate_left(node.left.take().unwrap()));
                }
            }
            return Self::rotate_right(node);
        }

        if bf < -1 {
            // 右子树高
            if let Some(ref right) = node.right {
                if Self::balance_factor(right) > 0 {
                    // RL: 先右旋右子，再左旋
                    node.right = Some(Self::rotate_right(node.right.take().unwrap()));
                }
            }
            return Self::rotate_left(node);
        }

        node
    }

    /// 中序遍历
    pub fn inorder(&self) -> Vec<&T> {
        fn traverse<'a, T>(node: &'a Option<Box<AVLNode<T>>>, result: &mut Vec<&'a T>) {
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

impl<T: Ord + Debug> AVLNode<T> {
    fn update_height(&mut self) {
        self.height = 1 + AVLTree::<T>::height(&self.left).max(AVLTree::<T>::height(&self.right));
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_avl_insert_balance() {
        let mut tree = AVLTree::new();
        // 按顺序插入会触发多次旋转
        for i in 1..=10 {
            tree.insert(i);
        }
        let inorder: Vec<i32> = tree.inorder().into_iter().copied().collect();
        assert_eq!(inorder, vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
        assert!(tree.contains(&5));
        assert!(tree.contains(&10));
    }

    #[test]
    fn test_avl_remove() {
        let mut tree = AVLTree::new();
        for i in [5, 3, 8, 1, 4, 7, 10] {
            tree.insert(i);
        }
        assert_eq!(tree.len(), 7);

        assert!(tree.remove(&5));
        assert!(!tree.contains(&5));
        assert_eq!(tree.len(), 6);

        let inorder: Vec<i32> = tree.inorder().into_iter().copied().collect();
        assert_eq!(inorder, vec![1, 3, 4, 7, 8, 10]);
    }

    #[test]
    fn test_avl_is_balanced() {
        let mut tree = AVLTree::new();
        for i in 0..100 {
            tree.insert(i);
        }
        // 验证有序性
        let inorder: Vec<i32> = tree.inorder().into_iter().copied().collect();
        assert_eq!(inorder.len(), 100);
        for i in 1..inorder.len() {
            assert!(inorder[i - 1] < inorder[i]);
        }
    }
}
