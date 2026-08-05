package com.algorithmx.technique.math;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.List;

class NumberTheoryTest {

    @Test void gcd() {
        assertEquals(6, NumberTheory.gcd(12, 18));
        assertEquals(1, NumberTheory.gcd(17, 13));
    }

    @Test void lcm() {
        assertEquals(36, NumberTheory.lcm(12, 18));
    }

    @Test void extendedGcd() {
        int[] res = NumberTheory.extendedGcd(30, 20);
        assertEquals(10, res[0]); // gcd
        assertEquals(30 * res[1] + 20 * res[2], res[0]);
    }

    @Test void fastPow() {
        assertEquals(8, NumberTheory.fastPow(2, 3, 1000));
        assertEquals(1, NumberTheory.fastPow(2, 0, 1000));
        assertEquals(1024 % 100, NumberTheory.fastPow(2, 10, 100));
    }

    @Test void fibMatrix() {
        assertEquals(0, NumberTheory.fibMatrix(0, Long.MAX_VALUE));
        assertEquals(1, NumberTheory.fibMatrix(1, Long.MAX_VALUE));
        assertEquals(55, NumberTheory.fibMatrix(10, Long.MAX_VALUE));
    }

    @Test void sieveEratosthenes() {
        List<Integer> primes = NumberTheory.sieveEratosthenes(20);
        assertEquals(List.of(2, 3, 5, 7, 11, 13, 17, 19), primes);
    }

    @Test void sieveEuler() {
        List<Integer> primes = NumberTheory.sieveEuler(20);
        assertEquals(List.of(2, 3, 5, 7, 11, 13, 17, 19), primes);
    }

    @Test void isPrime() {
        assertTrue(NumberTheory.isPrime(2));
        assertTrue(NumberTheory.isPrime(17));
        assertFalse(NumberTheory.isPrime(1));
        assertFalse(NumberTheory.isPrime(100));
    }

    @Test void toBase() {
        assertEquals("1010", NumberTheory.toBase(10, 2));
        assertEquals("a", NumberTheory.toBase(10, 16));
    }

    @Test void addStrings() {
        assertEquals("100", NumberTheory.addStrings("99", "1"));
        assertEquals("0", NumberTheory.addStrings("0", "0"));
    }

    @Test void multiplyStrings() {
        assertEquals("56088", NumberTheory.multiplyStrings("123", "456"));
        assertEquals("0", NumberTheory.multiplyStrings("0", "999"));
    }
}
