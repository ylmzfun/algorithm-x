package com.algorithmx.datastructure.tree;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class BSTTest {

    @Test void insertAndSearch() {
        BST bst = new BST();
        bst.insert(5);
        bst.insert(3);
        bst.insert(7);
        assertTrue(bst.search(5));
        assertTrue(bst.search(3));
        assertTrue(bst.search(7));
        assertFalse(bst.search(4));
    }

    @Test void deleteLeaf() {
        BST bst = new BST();
        bst.insert(5); bst.insert(3); bst.insert(7);
        bst.delete(3);
        assertFalse(bst.search(3));
        assertTrue(bst.search(5));
        assertTrue(bst.search(7));
    }

    @Test void avlInsert() {
        BST bst = new BST();
        int[] vals = {10, 20, 30, 40, 50, 25};
        for (int v : vals) bst.avlInsert(v);
        for (int v : vals) assertTrue(bst.search(v));
    }
}
