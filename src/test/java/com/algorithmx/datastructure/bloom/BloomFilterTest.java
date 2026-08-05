package com.algorithmx.datastructure.bloom;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class BloomFilterTest {

    @Test void basicContains() {
        BloomFilter bf = new BloomFilter(1000, 0.01);
        bf.add("hello");
        bf.add("world");
        assertTrue(bf.mightContain("hello"));
        assertTrue(bf.mightContain("world"));
        assertFalse(bf.mightContain("nope"));
    }

    @Test void falsePositiveRate() {
        BloomFilter bf = new BloomFilter(10000, 0.01);
        for (int i = 0; i < 1000; i++) bf.add("key" + i);
        int fp = 0;
        for (int i = 0; i < 1000; i++) if (bf.mightContain("other" + i)) fp++;
        // 1% FPP 下 1000 个新 key 误判应在合理范围
        assertTrue(fp < 200, "fp=" + fp + " exceeds reasonable threshold");
    }
}
