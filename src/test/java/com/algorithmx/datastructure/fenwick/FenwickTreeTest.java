package com.algorithmx.datastructure.fenwick;

import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

class FenwickTreeTest {

    @Test void basic() {
        FenwickTree ft = FenwickTree.fromArray(new int[]{1, 3, 5, 7, 9});
        assertEquals(1, ft.query(1));
        assertEquals(4, ft.query(2));
        assertEquals(9, ft.query(3));
        assertEquals(16, ft.query(4));
        assertEquals(25, ft.query(5));
    }

    @Test void rangeQuery() {
        FenwickTree ft = FenwickTree.fromArray(new int[]{1, 3, 5, 7, 9});
        assertEquals(8, ft.rangeQuery(2, 3));  // 3 + 5
        assertEquals(21, ft.rangeQuery(3, 5)); // 5 + 7 + 9 = 21
    }

    @Test void update() {
        FenwickTree ft = FenwickTree.fromArray(new int[]{1, 3, 5});
        ft.update(2, 10); // index 2 += 10 → arr[1] 变为 13
        assertEquals(1 + 13 + 5, ft.query(3));
    }
}
