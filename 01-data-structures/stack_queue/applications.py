"""
Stack Applications
===================

Classic algorithmic problems solved using stacks:

1. Balanced Parentheses — Check if brackets are properly matched.
2. Evaluate RPN — Evaluate reverse Polish notation expressions.
3. Infix to Postfix — Convert infix expression to postfix (Shunting-yard).
4. Min Stack — Stack that supports O(1) minimum retrieval.
"""

from typing import List, Optional, Union


# ─── 1. Balanced Parentheses ──────────────────────────────────────────────────


def is_balanced_parentheses(s: str) -> bool:
    """Check if a string has balanced parentheses, brackets, and braces.

    Supports: () [] {}

    Args:
        s: String containing brackets.

    Returns:
        True if all brackets are properly matched and nested, False otherwise.

    Time Complexity: O(n)
    Space Complexity: O(n) — for stack.

    Examples:
        >>> is_balanced_parentheses("()")
        True
        >>> is_balanced_parentheses("()[]{}")
        True
        >>> is_balanced_parentheses("(]")
        False
        >>> is_balanced_parentheses("([)]")
        False
        >>> is_balanced_parentheses("{[]}")
        True
    """
    matching = {')': '(', ']': '[', '}': '{'}
    stack: List[str] = []

    for ch in s:
        if ch in matching.values():  # Opening bracket
            stack.append(ch)
        elif ch in matching:  # Closing bracket
            if not stack or stack.pop() != matching[ch]:
                return False
        # Ignore other characters

    return len(stack) == 0


def longest_valid_parentheses(s: str) -> int:
    """Find the length of the longest valid (well-formed) parentheses substring.

    Uses a stack that stores indices. When we see a closing paren that matches,
    we pop and compute the length by the distance to the previous unmatched index.

    Args:
        s: String of '(' and ')' characters only.

    Returns:
        Length of the longest valid parentheses substring.

    Time Complexity: O(n)
    Space Complexity: O(n)

    Examples:
        >>> longest_valid_parentheses("(()")
        2
        >>> longest_valid_parentheses(")()())")
        4
        >>> longest_valid_parentheses("")
        0
    """
    # Stack stores index of last unmatched '(' or sentinel index
    stack = [-1]  # Sentinel for the base
    max_len = 0

    for i, ch in enumerate(s):
        if ch == '(':
            stack.append(i)
        else:  # ch == ')'
            stack.pop()
            if not stack:
                # No matching '(', mark this position as new base
                stack.append(i)
            else:
                max_len = max(max_len, i - stack[-1])

    return max_len


# ─── 2. Evaluate RPN (Reverse Polish Notation) ───────────────────────────────


def evaluate_rpn(tokens: List[str]) -> int:
    """Evaluate an arithmetic expression in Reverse Polish Notation.

    Supported operators: +, -, *, /.
    Division truncates toward zero (Python's // on integers).

    Args:
        tokens: List of string tokens (numbers and operators).

    Returns:
        Integer result of the expression.

    Raises:
        ValueError: If expression is malformed.

    Time Complexity: O(n)
    Space Complexity: O(n)

    Examples:
        >>> evaluate_rpn(["2", "1", "+", "3", "*"])
        9
        >>> evaluate_rpn(["4", "13", "5", "/", "+"])
        6
        >>> evaluate_rpn(["10", "6", "9", "3", "/", "-", "*"])
        -30
    """
    operators = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: int(a / b),  # Truncation toward zero
    }
    stack: List[int] = []

    for token in tokens:
        if token in operators:
            if len(stack) < 2:
                raise ValueError(f"Invalid RPN: insufficient operands for '{token}'")
            b = stack.pop()
            a = stack.pop()
            stack.append(operators[token](a, b))
        else:
            try:
                stack.append(int(token))
            except ValueError:
                raise ValueError(f"Invalid token: '{token}'")

    if len(stack) != 1:
        raise ValueError("Invalid RPN: too many operands left")

    return stack[0]


# ─── 3. Infix to Postfix (Shunting-yard Algorithm) ────────────────────────────


def infix_to_postfix(expression: str) -> str:
    """Convert infix mathematical expression to postfix (RPN).

    Uses the Shunting-yard algorithm with operator precedence.
    Supports: +, -, *, /, ^ (right-associative), and parentheses.

    Args:
        expression: Space-separated infix expression (e.g., "A + B * C").

    Returns:
        Space-separated postfix expression.

    Raises:
        ValueError: If parentheses are mismatched.

    Time Complexity: O(n)
    Space Complexity: O(n)

    Examples:
        >>> infix_to_postfix("A + B * C")
        'A B C * +'
        >>> infix_to_postfix("( A + B ) * C")
        'A B + C *'
        >>> infix_to_postfix("A * B + C * D")
        'A B * C D * +'
    """
    # Precedence: higher = more tightly binding
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    right_associative = {'^'}

    output: List[str] = []
    stack: List[str] = []

    tokens = expression.split()

    for token in tokens:
        if token.isalnum():  # Operand (variable or number)
            output.append(token)

        elif token == '(':
            stack.append(token)

        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if not stack:
                raise ValueError("Mismatched parentheses")
            stack.pop()  # Discard '('

        elif token in precedence:  # Operator
            while (stack and stack[-1] != '(' and (
                precedence[stack[-1]] > precedence[token] or
                (precedence[stack[-1]] == precedence[token] and
                 token not in right_associative)
            )):
                output.append(stack.pop())
            stack.append(token)

    # Pop remaining operators
    while stack:
        if stack[-1] == '(':
            raise ValueError("Mismatched parentheses")
        output.append(stack.pop())

    return ' '.join(output)


# ─── 4. Min Stack ─────────────────────────────────────────────────────────────


class MinStack:
    """A stack that supports push, pop, top, and retrieving the minimum
    element — all in O(1) time.

    Uses an auxiliary stack to track the minimum at each level.

    Examples:
        >>> ms = MinStack()
        >>> ms.push(-2)
        >>> ms.push(0)
        >>> ms.push(-3)
        >>> ms.get_min()
        -3
        >>> ms.pop()
        >>> ms.top()
        0
        >>> ms.get_min()
        -2
    """

    def __init__(self) -> None:
        """Initialize an empty MinStack."""
        self._stack: List[int] = []
        self._min_stack: List[int] = []  # Tracks minimum up to each position

    def push(self, val: int) -> None:
        """Push `val` onto the stack.

        Time Complexity: O(1)

        Args:
            val: Integer value to push.
        """
        self._stack.append(val)
        if not self._min_stack:
            self._min_stack.append(val)
        else:
            self._min_stack.append(min(val, self._min_stack[-1]))

    def pop(self) -> None:
        """Remove the top element.

        Raises:
            IndexError: If stack is empty.

        Time Complexity: O(1)
        """
        if not self._stack:
            raise IndexError("pop from empty MinStack")
        self._stack.pop()
        self._min_stack.pop()

    def top(self) -> int:
        """Return the top element.

        Returns:
            Top value.

        Raises:
            IndexError: If empty.

        Time Complexity: O(1)
        """
        if not self._stack:
            raise IndexError("top from empty MinStack")
        return self._stack[-1]

    def get_min(self) -> int:
        """Return the minimum element in the stack.

        Returns:
            Minimum value.

        Raises:
            IndexError: If empty.

        Time Complexity: O(1)
        """
        if not self._min_stack:
            raise IndexError("get_min from empty MinStack")
        return self._min_stack[-1]

    def size(self) -> int:
        """Return number of elements."""
        return len(self._stack)

    def is_empty(self) -> bool:
        """Check if stack is empty."""
        return len(self._stack) == 0


# ─── Tests ────────────────────────────────────────────────────────────────────


def _run_tests() -> None:
    """Run all tests and report results."""
    import sys

    passed = 0
    failed = 0

    def check(description: str, condition: bool) -> None:
        nonlocal passed, failed
        if condition:
            passed += 1
            print(f"  ✓ {description}")
        else:
            failed += 1
            print(f"  ✗ {description}", file=sys.stderr)

    # ── Balanced Parentheses ─────────────────────────────────────────────────
    print("Balanced Parentheses:")
    check("empty", is_balanced_parentheses("") is True)
    check("simple ()", is_balanced_parentheses("()") is True)
    check("mixed ()[]{}", is_balanced_parentheses("()[]{}") is True)
    check("nested ({[]})", is_balanced_parentheses("({[]})") is True)
    check("mismatch (]", is_balanced_parentheses("(]") is False)
    check("wrong order ([)]", is_balanced_parentheses("([)]") is False)
    check("unclosed ((", is_balanced_parentheses("((") is False)
    check("extra close ))", is_balanced_parentheses("))") is False)
    check("with other chars", is_balanced_parentheses("a(b)c") is True)

    # Longest valid
    check("longest valid '(()' == 2", longest_valid_parentheses("(()") == 2)
    check("longest valid ')()())' == 4", longest_valid_parentheses(")()())") == 4)
    check("longest valid '' == 0", longest_valid_parentheses("") == 0)
    check("longest valid '()(()' == 2", longest_valid_parentheses("()(()") == 2)

    # ── Evaluate RPN ──────────────────────────────────────────────────────────
    print("\nEvaluate RPN:")
    check("2 1 + 3 * = 9", evaluate_rpn(["2", "1", "+", "3", "*"]) == 9)
    check("4 13 5 / + = 6", evaluate_rpn(["4", "13", "5", "/", "+"]) == 6)
    check("neg result", evaluate_rpn(["10", "6", "9", "3", "/", "-", "*"]) == 30)
    check("single", evaluate_rpn(["42"]) == 42)

    try:
        evaluate_rpn(["1", "+"])
        check("malformed RPN raises", False)
    except ValueError:
        check("malformed RPN raises", True)

    try:
        evaluate_rpn(["a", "b", "+"])
        check("invalid token raises", False)
    except ValueError:
        check("invalid token raises", True)

    # ── Infix to Postfix ──────────────────────────────────────────────────────
    print("\nInfix to Postfix:")
    check("A + B * C", infix_to_postfix("A + B * C") == "A B C * +")
    check("(A+B)*C", infix_to_postfix("( A + B ) * C") == "A B + C *")
    check("A*B+C*D", infix_to_postfix("A * B + C * D") == "A B * C D * +")
    check("right assoc ^", infix_to_postfix("A ^ B ^ C") == "A B C ^ ^")
    check("with parens", infix_to_postfix("A + ( B - C ) * D") == "A B C - D * +")

    try:
        infix_to_postfix("( A + B")
        check("mismatched parens raises", False)
    except ValueError:
        check("mismatched parens raises", True)

    # ── MinStack ──────────────────────────────────────────────────────────────
    print("\nMinStack:")
    ms = MinStack()
    ms.push(-2)
    ms.push(0)
    ms.push(-3)
    check("get_min == -3", ms.get_min() == -3)
    ms.pop()
    check("top == 0 after pop", ms.top() == 0)
    check("get_min == -2 after pop", ms.get_min() == -2)

    ms.push(-5)
    check("get_min == -5", ms.get_min() == -5)
    ms.pop()
    check("get_min restored to -2", ms.get_min() == -2)

    try:
        empty_ms = MinStack()
        empty_ms.get_min()
        check("get_min empty raises", False)
    except IndexError:
        check("get_min empty raises", True)

    try:
        empty_ms = MinStack()
        empty_ms.top()
        check("top empty raises", False)
    except IndexError:
        check("top empty raises", True)

    check("size", ms.size() == 2)

    # ── Summary ───────────────────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
