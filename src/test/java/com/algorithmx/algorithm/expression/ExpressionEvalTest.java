package com.algorithmx.algorithm.expression;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.List;

class ExpressionEvalTest {

    @Test void calculate() {
        assertEquals(7, ExpressionEval.calculate("3+4"));
        assertEquals(23, ExpressionEval.calculate("3+4*5"));
        assertEquals(11, ExpressionEval.calculate("(3+4)*2-3"));
        assertEquals(-1, ExpressionEval.calculate("0-1"));
    }

    @Test void evalRPN() {
        assertEquals(9, ExpressionEval.evalRPN(new String[]{"2","1","+","3","*"}));
        assertEquals(6, ExpressionEval.evalRPN(new String[]{"4","13","5","/","+"}));
    }

    @Test void infixToPostfix() {
        List<String> pf = ExpressionEval.infixToPostfix("3+4*5");
        assertEquals(List.of("3","4","5","*","+"), pf);
    }
}
