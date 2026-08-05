package com.algorithmx.datastructure.sparsetable;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class SparseTableTest {

    @Test void basic() {
        int[] arr = {5, 2, 8, 1, 9, 3};
        SparseTable st = new SparseTable(arr);
        assertEquals(5, st.queryMin(0, 0));
        assertEquals(2, st.queryMin(0, 1));
        assertEquals(1, st.queryMin(0, 5));
        assertEquals(1, st.queryMin(3, 5)); // 1,9,3 → 1
        assertEquals(3, st.queryMin(4, 5)); // 9,3 → 3
    }
}
