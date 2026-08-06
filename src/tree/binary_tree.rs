/// 二叉树基础与遍历
///
/// - 前序、中序、后序、层序遍历
/// - 递归与迭代实现
use std::cell::RefCell;
use std::collections::VecDeque;
use std::fmt::Debug;
use std::rc::Rc;

pub type TreeNodeRef<T> = Option<Rc<RefCell<TreeNode<T>>>>;

#[derive(Debug, PartialEq)]
pub struct TreeNode<T> {
    pub val: T,
    pub left: TreeNodeRef<T>,
    pub right: TreeNodeRef<T>,
}

impl<T: Debug> TreeNode<T> {
    pub fn new(val: T) -> Rc<RefCell<Self>> {
        Rc::new(RefCell::new(Self {
            val,
            left: None,
            right: None,
        }))
    }
}

/// 二叉树
pub struct BinaryTree<T> {
    pub root: TreeNodeRef<T>,
}

impl<T: Debug + Copy + PartialEq> BinaryTree<T> {
    pub fn new(root: TreeNodeRef<T>) -> Self {
        Self { root }
    }

    // ===== 递归遍历 =====

    /// 前序遍历（递归）：根 → 左 → 右
    pub fn preorder(&self) -> Vec<T> {
        fn traverse<T: Copy>(node: &TreeNodeRef<T>, result: &mut Vec<T>) {
            if let Some(n) = node {
                let n = n.borrow();
                result.push(n.val);
                traverse(&n.left, result);
                traverse(&n.right, result);
            }
        }
        let mut result = Vec::new();
        traverse(&self.root, &mut result);
        result
    }

    /// 中序遍历（递归）：左 → 根 → 右
    pub fn inorder(&self) -> Vec<T> {
        fn traverse<T: Copy>(node: &TreeNodeRef<T>, result: &mut Vec<T>) {
            if let Some(n) = node {
                let n = n.borrow();
                traverse(&n.left, result);
                result.push(n.val);
                traverse(&n.right, result);
            }
        }
        let mut result = Vec::new();
        traverse(&self.root, &mut result);
        result
    }

    /// 后序遍历（递归）：左 → 右 → 根
    pub fn postorder(&self) -> Vec<T> {
        fn traverse<T: Copy>(node: &TreeNodeRef<T>, result: &mut Vec<T>) {
            if let Some(n) = node {
                let n = n.borrow();
                traverse(&n.left, result);
                traverse(&n.right, result);
                result.push(n.val);
            }
        }
        let mut result = Vec::new();
        traverse(&self.root, &mut result);
        result
    }

    // ===== 迭代遍历（用栈模拟递归） =====

    /// 前序遍历（迭代）
    pub fn preorder_iter(&self) -> Vec<T> {
        let mut result = Vec::new();
        let mut stack: Vec<TreeNodeRef<T>> = Vec::new();
        stack.push(self.root.clone());

        while let Some(node) = stack.pop() {
            if let Some(n) = node {
                let n = n.borrow();
                result.push(n.val);
                stack.push(n.right.clone()); // 先压右，后出栈先处理左
                stack.push(n.left.clone());
            }
        }
        result
    }

    /// 中序遍历（迭代）
    pub fn inorder_iter(&self) -> Vec<T> {
        let mut result = Vec::new();
        let mut stack: Vec<TreeNodeRef<T>> = Vec::new();
        let mut curr = self.root.clone();

        while curr.is_some() || !stack.is_empty() {
            while let Some(node) = curr {
                let next = node.borrow().left.clone();
                stack.push(Some(node));
                curr = next;
            }
            if let Some(Some(node)) = stack.pop() {
                result.push(node.borrow().val);
                curr = node.borrow().right.clone();
            }
        }
        result
    }

    /// 后序遍历（迭代 — 双栈法）
    pub fn postorder_iter(&self) -> Vec<T> {
        let mut result = Vec::new();
        let mut stack1: Vec<TreeNodeRef<T>> = Vec::new();
        let mut stack2: Vec<TreeNodeRef<T>> = Vec::new();
        stack1.push(self.root.clone());

        while let Some(node) = stack1.pop() {
            if let Some(n) = node {
                stack2.push(Some(n.clone()));
                let n = n.borrow();
                stack1.push(n.left.clone());
                stack1.push(n.right.clone());
            }
        }
        while let Some(Some(node)) = stack2.pop() {
            result.push(node.borrow().val);
        }
        result
    }

    /// 层序遍历（BFS）
    pub fn level_order(&self) -> Vec<Vec<T>> {
        let mut result = Vec::new();
        if self.root.is_none() {
            return result;
        }
        let mut queue = VecDeque::new();
        queue.push_back(self.root.clone());

        while !queue.is_empty() {
            let level_size = queue.len();
            let mut level = Vec::with_capacity(level_size);
            for _ in 0..level_size {
                if let Some(Some(node)) = queue.pop_front() {
                    let n = node.borrow();
                    level.push(n.val);
                    if n.left.is_some() {
                        queue.push_back(n.left.clone());
                    }
                    if n.right.is_some() {
                        queue.push_back(n.right.clone());
                    }
                }
            }
            result.push(level);
        }
        result
    }

    /// 树的最大深度
    pub fn max_depth(&self) -> usize {
        fn depth<T>(node: &TreeNodeRef<T>) -> usize {
            match node {
                None => 0,
                Some(n) => {
                    let n = n.borrow();
                    1 + depth(&n.left).max(depth(&n.right))
                }
            }
        }
        depth(&self.root)
    }

    /// 是否对称二叉树（镜像对称）
    pub fn is_symmetric(&self) -> bool {
        fn is_mirror<T: PartialEq>(left: &TreeNodeRef<T>, right: &TreeNodeRef<T>) -> bool {
            match (left, right) {
                (None, None) => true,
                (Some(l), Some(r)) => {
                    let l = l.borrow();
                    let r = r.borrow();
                    l.val == r.val && is_mirror(&l.left, &r.right) && is_mirror(&l.right, &r.left)
                }
                _ => false,
            }
        }
        match &self.root {
            None => true,
            Some(root) => {
                let root = root.borrow();
                is_mirror(&root.left, &root.right)
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    /// 构造测试树:
    ///       1
    ///      / \
    ///     2   3
    ///    / \   \
    ///   4   5   6
    fn build_test_tree() -> BinaryTree<i32> {
        let root = TreeNode::new(1);
        {
            let mut r = root.borrow_mut();
            let left = TreeNode::new(2);
            let right = TreeNode::new(3);
            {
                let mut l = left.borrow_mut();
                l.left = Some(TreeNode::new(4));
                l.right = Some(TreeNode::new(5));
            }
            {
                let mut r = right.borrow_mut();
                r.right = Some(TreeNode::new(6));
            }
            r.left = Some(left);
            r.right = Some(right);
        }
        BinaryTree::new(Some(root))
    }

    #[test]
    fn test_preorder() {
        let tree = build_test_tree();
        assert_eq!(tree.preorder(), vec![1, 2, 4, 5, 3, 6]);
        assert_eq!(tree.preorder_iter(), vec![1, 2, 4, 5, 3, 6]);
    }

    #[test]
    fn test_inorder() {
        let tree = build_test_tree();
        assert_eq!(tree.inorder(), vec![4, 2, 5, 1, 3, 6]);
        assert_eq!(tree.inorder_iter(), vec![4, 2, 5, 1, 3, 6]);
    }

    #[test]
    fn test_postorder() {
        let tree = build_test_tree();
        assert_eq!(tree.postorder(), vec![4, 5, 2, 6, 3, 1]);
        assert_eq!(tree.postorder_iter(), vec![4, 5, 2, 6, 3, 1]);
    }

    #[test]
    fn test_level_order() {
        let tree = build_test_tree();
        assert_eq!(tree.level_order(), vec![vec![1], vec![2, 3], vec![4, 5, 6]]);
    }

    #[test]
    fn test_max_depth() {
        let tree = build_test_tree();
        assert_eq!(tree.max_depth(), 3);
    }

    #[test]
    fn test_is_symmetric() {
        // 对称树:
        //     1
        //    / \
        //   2   2
        //  / \ / \
        // 3  4 4  3
        let root = TreeNode::new(1);
        {
            let mut r = root.borrow_mut();
            let left = TreeNode::new(2);
            let right = TreeNode::new(2);
            {
                let mut l = left.borrow_mut();
                l.left = Some(TreeNode::new(3));
                l.right = Some(TreeNode::new(4));
            }
            {
                let mut r = right.borrow_mut();
                r.left = Some(TreeNode::new(4));
                r.right = Some(TreeNode::new(3));
            }
            r.left = Some(left);
            r.right = Some(right);
        }
        let tree = BinaryTree::new(Some(root));
        assert!(tree.is_symmetric());

        let tree2 = build_test_tree();
        assert!(!tree2.is_symmetric());
    }
}
