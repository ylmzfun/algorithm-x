package com.algorithmx.foundation.recursion;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.List;

class RecursionTest {

    @Test void factorial() {
        assertEquals(1, Recursion.factorial(0));
        assertEquals(120, Recursion.factorial(5));
    }

    @Test void fibMemo() {
        assertEquals(0, Recursion.fibMemo(0));
        assertEquals(1, Recursion.fibMemo(1));
        assertEquals(55, Recursion.fibMemo(10));
    }

    @Test void fastPow() {
        assertEquals(8.0, Recursion.fastPow(2, 3), 1e-9);
        assertEquals(0.125, Recursion.fastPow(2, -3), 1e-9);
        assertEquals(1.0, Recursion.fastPow(5, 0), 1e-9);
    }

    @Test void hanoi() {
        List<String> moves = Recursion.hanoi(3);
        assertEquals(7, moves.size());
        assertEquals("A -> C", moves.get(0));
        assertEquals("A -> C", moves.get(moves.size() - 1));
    }

    @Test void generateParenthesis() {
        List<String> res = Recursion.generateParenthesis(3);
        assertEquals(5, res.size());
        assertTrue(res.contains("((()))"));
        assertTrue(res.contains("()()()"));
    }

    @Test void letterCombinations() {
        List<String> res = Recursion.letterCombinations("23");
        assertEquals(9, res.size());
        assertTrue(res.contains("ad"));
        assertTrue(res.contains("cf"));
    }
}
