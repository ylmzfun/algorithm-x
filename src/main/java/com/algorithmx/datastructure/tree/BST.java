package com.algorithmx.datastructure.tree;

/**
 * 二叉搜索树 BST + 自平衡 AVL 树
 */
public class BST {

    static class Node {
        int val;
        Node left, right;
        int height; // AVL 用
        Node(int val) { this.val = val; this.height = 1; }
    }

    private Node root;

    // ==================== BST 操作 ====================

    public void insert(int val) { root = insert(root, val); }

    private Node insert(Node node, int val) {
        if (node == null) return new Node(val);
        if (val < node.val) node.left = insert(node.left, val);
        else if (val > node.val) node.right = insert(node.right, val);
        return node;
    }

    public boolean search(int val) { return search(root, val) != null; }

    private Node search(Node node, int val) {
        if (node == null || node.val == val) return node;
        return val < node.val ? search(node.left, val) : search(node.right, val);
    }

    public void delete(int val) { root = delete(root, val); }

    private Node delete(Node node, int val) {
        if (node == null) return null;
        if (val < node.val) { node.left = delete(node.left, val); return node; }
        if (val > node.val) { node.right = delete(node.right, val); return node; }
        // 找到要删除的节点
        if (node.left == null) return node.right;
        if (node.right == null) return node.left;
        // 有两个子节点：用后继（右子树最小节点）替换
        Node successor = minNode(node.right);
        node.right = delete(node.right, successor.val);
        successor.left = node.left;
        successor.right = node.right;
        return successor;
    }

    private Node minNode(Node node) {
        while (node.left != null) node = node.left;
        return node;
    }

    // ==================== AVL 树操作 ====================

    public void avlInsert(int val) { root = avlInsert(root, val); }

    private Node avlInsert(Node node, int val) {
        if (node == null) return new Node(val);
        if (val < node.val) node.left = avlInsert(node.left, val);
        else if (val > node.val) node.right = avlInsert(node.right, val);
        else return node;

        node.height = 1 + Math.max(height(node.left), height(node.right));
        return balance(node);
    }

    public void avlDelete(int val) { root = avlDelete(root, val); }

    private Node avlDelete(Node node, int val) {
        if (node == null) return null;
        if (val < node.val) node.left = avlDelete(node.left, val);
        else if (val > node.val) node.right = avlDelete(node.right, val);
        else {
            if (node.left == null) return node.right;
            if (node.right == null) return node.left;
            Node successor = minNode(node.right);
            node.val = successor.val;
            node.right = avlDelete(node.right, successor.val);
        }
        node.height = 1 + Math.max(height(node.left), height(node.right));
        return balance(node);
    }

    private Node balance(Node node) {
        int bf = balanceFactor(node);
        // LL — 右旋
        if (bf > 1 && balanceFactor(node.left) >= 0) return rotateRight(node);
        // LR — 左旋左子节点，再右旋
        if (bf > 1 && balanceFactor(node.left) < 0) {
            node.left = rotateLeft(node.left);
            return rotateRight(node);
        }
        // RR — 左旋
        if (bf < -1 && balanceFactor(node.right) <= 0) return rotateLeft(node);
        // RL — 右旋右子节点，再左旋
        if (bf < -1 && balanceFactor(node.right) > 0) {
            node.right = rotateRight(node.right);
            return rotateLeft(node);
        }
        return node;
    }

    private int height(Node n) { return n == null ? 0 : n.height; }
    private int balanceFactor(Node n) { return n == null ? 0 : height(n.left) - height(n.right); }

    private Node rotateRight(Node y) {
        Node x = y.left;
        Node t2 = x.right;
        x.right = y; y.left = t2;
        y.height = 1 + Math.max(height(y.left), height(y.right));
        x.height = 1 + Math.max(height(x.left), height(x.right));
        return x;
    }

    private Node rotateLeft(Node x) {
        Node y = x.right;
        Node t2 = y.left;
        y.left = x; x.right = t2;
        x.height = 1 + Math.max(height(x.left), height(x.right));
        y.height = 1 + Math.max(height(y.left), height(y.right));
        return y;
    }

    // ==================== 工具 ====================

    public void inorder() { inorder(root); System.out.println(); }
    private void inorder(Node n) { if (n != null) { inorder(n.left); System.out.print(n.val + " "); inorder(n.right); } }
}
