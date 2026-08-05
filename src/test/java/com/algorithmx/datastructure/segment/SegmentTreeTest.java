package com.algorithmx.datastructure.segment;

import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

class SegmentTreeTest {

    @Test void rangeQuery() {
        int[] arr = {1, 3, 5, 7, 9, 11};
        SegmentTree st = new SegmentTree(arr);
        assertEquals(8, st.rangeQuery(1, 2));  // 3+5
        assertEquals(36, st.rangeQuery(0, 5)); // total
        assertEquals(1, st.rangeQuery(0, 0));
    }

    @Test void rangeAdd() {
        int[] arr = {1, 2, 3, 4, 5};
        SegmentTree st = new SegmentTree(arr);
        st.rangeAdd(1, 3, 10); // arr[1..3] += 10 → {1,12,13,14,5}
        assertEquals(12, st.rangeQuery(1, 1));
        assertEquals(45, st.rangeQuery(0, 4));
    }
}
