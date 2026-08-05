package com.algorithmx.datastructure.tree;

import java.util.*;

/**
 * Morris 遍历 — O(1) 额外空间完成二叉树中序遍历
 *
 * 核心思想：利用叶子节点的空闲右指针指向后继节点（线索二叉树），
 * 遍历结束后恢复原结构。
 */
public class MorrisTraversal {

    /** 中序 Morris — 返回遍历结果 */
    public static List<Integer> inorder(BinaryTree.TreeNode root) {
        List<Integer> res = new ArrayList<>();
        BinaryTree.TreeNode cur = root;
        while (cur != null) {
            if (cur.left == null) {
                res.add(cur.val);
                cur = cur.right;
            } else {
                BinaryTree.TreeNode pre = cur.left;
                while (pre.right != null && pre.right != cur) pre = pre.right;
                if (pre.right == null) {       // 第一次到达，建线索
                    pre.right = cur;
                    // 前序：res.add(cur.val); （在此处输出即变前序遍历）
                    cur = cur.left;
                } else {                        // 第二次到达，拆线索
                    pre.right = null;
                    res.add(cur.val);
                    cur = cur.right;
                }
            }
        }
        return res;
    }

    /** 前序 Morris */
    public static List<Integer> preorder(BinaryTree.TreeNode root) {
        List<Integer> res = new ArrayList<>();
        BinaryTree.TreeNode cur = root;
        while (cur != null) {
            if (cur.left == null) {
                res.add(cur.val);
                cur = cur.right;
            } else {
                BinaryTree.TreeNode pre = cur.left;
                while (pre.right != null && pre.right != cur) pre = pre.right;
                if (pre.right == null) {
                    res.add(cur.val); // 第一次到达时输出 = 前序
                    pre.right = cur;
                    cur = cur.left;
                } else {
                    pre.right = null;
                    cur = cur.right;
                }
            }
        }
        return res;
    }
}
