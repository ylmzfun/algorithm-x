package com.algorithmx.datastructure.tree;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.List;

class MorrisTraversalTest {

    @Test void inorder() {
        //     4
        //    / \
        //   2   6
        //  / \ / \
        // 1  3 5  7
        BinaryTree.TreeNode root =
            new BinaryTree.TreeNode(4,
                new BinaryTree.TreeNode(2, new BinaryTree.TreeNode(1), new BinaryTree.TreeNode(3)),
                new BinaryTree.TreeNode(6, new BinaryTree.TreeNode(5), new BinaryTree.TreeNode(7)));
        assertEquals(List.of(1, 2, 3, 4, 5, 6, 7), MorrisTraversal.inorder(root));
    }

    @Test void preorder() {
        BinaryTree.TreeNode root =
            new BinaryTree.TreeNode(1,
                new BinaryTree.TreeNode(2, new BinaryTree.TreeNode(4), null),
                new BinaryTree.TreeNode(3));
        assertEquals(List.of(1, 2, 4, 3), MorrisTraversal.preorder(root));
    }

    @Test void singleNode() {
        BinaryTree.TreeNode root = new BinaryTree.TreeNode(42);
        assertEquals(List.of(42), MorrisTraversal.inorder(root));
        assertEquals(List.of(42), MorrisTraversal.preorder(root));
    }
}
