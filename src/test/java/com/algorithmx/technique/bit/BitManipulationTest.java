package com.algorithmx.technique.bit;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class BitManipulationTest {

    @Test void isOdd() {
        assertTrue(BitManipulation.isOdd(3));
        assertFalse(BitManipulation.isOdd(4));
    }

    @Test void swap() {
        assertArrayEquals(new int[]{2, 1}, BitManipulation.swap(1, 2));
    }

    @Test void countOnes() {
        assertEquals(3, BitManipulation.countOnes(13)); // 1101
    }

    @Test void isPowerOfTwo() {
        assertTrue(BitManipulation.isPowerOfTwo(16));
        assertFalse(BitManipulation.isPowerOfTwo(15));
        assertFalse(BitManipulation.isPowerOfTwo(0));
    }

    @Test void bitOps() {
        int n = 0b0100;
        assertEquals(0b0101, BitManipulation.setBit(n, 0));
        assertEquals(0b0000, BitManipulation.clearBit(n, 2));
        assertEquals(0b0000, BitManipulation.toggleBit(n, 2));
        assertTrue(BitManipulation.testBit(n, 2));
        assertFalse(BitManipulation.testBit(n, 0));
    }
}
