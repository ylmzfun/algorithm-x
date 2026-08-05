"""Practical prompt engineering utilities.

Provides:
- Few-shot prompt formatting
- Chain-of-thought prompting
- Structured output parsing
- System prompt creation
- Prompt template class with variable substitution
"""

from typing import Any, Optional
import re
import json


def few_shot_prompt(
    task: str,
    examples: list[tuple[str, str]],
    query: str,
) -> str:
    """Create a few-shot prompt from task description, examples, and query.

    Args:
        task: Description of the task.
        examples: List of (input, output) example pairs.
        query: The input for which we want an output.

    Returns:
        Formatted few-shot prompt string.
    """
    parts = [f"Task: {task}\n"]
    parts.append("Examples:")

    for i, (inp, out) in enumerate(examples, 1):
        parts.append(f"\nExample {i}:")
        parts.append(f"Input: {inp}")
        parts.append(f"Output: {out}")

    parts.append(f"\n\nNow, complete the following:")
    parts.append(f"Input: {query}")
    parts.append(f"Output:")

    return "\n".join(parts)


def chain_of_thought_prompt(question: str) -> str:
    """Generate a chain-of-thought prompt.

    Args:
        question: The question to reason about.

    Returns:
        Formatted chain-of-thought prompt.
    """
    return (
        f"Question: {question}\n\n"
        f"Let's think through this step by step:\n"
        f"Step 1:"
    )


def parse_structured_output(
    text: str,
    format_spec: str = "json",
) -> Optional[Any]:
    """Parse LLM output into structured format.

    Args:
        text: Raw LLM output text.
        format_spec: Output format: 'json', 'key_value', 'csv', or 'list'.

    Returns:
        Parsed data structure, or None if parsing fails.
    """
    if format_spec == "json":
        # Try to extract JSON from text (handles ```json ... ``` blocks)
        json_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1).strip()
        else:
            # Try to find raw JSON
            brace_start = text.find("{")
            bracket_start = text.find("[")
            if brace_start >= 0 and (bracket_start < 0 or brace_start < bracket_start):
                json_str = text[brace_start:]
            elif bracket_start >= 0:
                json_str = text[bracket_start:]
            else:
                return None

        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None

    elif format_spec == "key_value":
        # Parse "key: value" format
        result = {}
        lines = text.strip().split("\n")
        for line in lines:
            if ":" in line:
                key, _, value = line.partition(":")
                result[key.strip()] = value.strip()
        return result if result else None

    elif format_spec == "csv":
        # Parse CSV-like output
        lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
        if not lines:
            return None
        result = []
        for line in lines:
            result.append([cell.strip() for cell in line.split(",")])
        return result

    elif format_spec == "list":
        # Parse bullet-point or numbered list
        items = re.findall(r'(?:^|\n)\s*(?:[-*•]|\d+[.)])\s*(.+)', text)
        if items:
            return [item.strip() for item in items]
        return None

    return None


def create_system_prompt(
    role: str,
    instructions: str,
    constraints: Optional[list[str]] = None,
) -> str:
    """Create a well-formatted system prompt.

    Args:
        role: The role the AI should assume.
        instructions: Main instructions for the AI.
        constraints: Optional list of constraints/rules.

    Returns:
        Formatted system prompt string.
    """
    parts = [f"You are {role}.\n"]
    parts.append(f"{instructions}")

    if constraints:
        parts.append("\nRules:")
        for i, constraint in enumerate(constraints, 1):
            parts.append(f"{i}. {constraint}")

    return "\n".join(parts)


class PromptTemplate:
    """Template-based prompt with variable substitution.

    Supports multiple prompt formats: ChatML, Alpaca, and custom.
    """

    FORMAT_CHATML = "chatml"
    FORMAT_ALPACA = "alpaca"
    FORMAT_CUSTOM = "custom"

    def __init__(
        self,
        template: str,
        input_variables: list[str],
        format_type: str = "custom",
    ):
        """Initialize prompt template.

        Args:
            template: Template string with {variable} placeholders.
            input_variables: List of variable names expected in the template.
            format_type: Format type ('chatml', 'alpaca', 'custom').
        """
        self.template = template
        self.input_variables = input_variables
        self.format_type = format_type

    def format(self, **kwargs) -> str:
        """Substitute variables into the template.

        Args:
            **kwargs: Variable values.

        Returns:
            Formatted prompt string.
        """
        # Validate all required variables are provided
        missing = [v for v in self.input_variables if v not in kwargs]
        if missing:
            raise ValueError(f"Missing template variables: {missing}")

        return self.template.format(**kwargs)

    @classmethod
    def from_chatml(cls, system_content: str, user_template: str) -> "PromptTemplate":
        """Create a ChatML-format template.

        Args:
            system_content: System message content.
            user_template: User message template with {input} placeholder.

        Returns:
            PromptTemplate instance.
        """
        template = (
            f"<|im_start|>system\n"
            f"{system_content}<|im_end|>\n"
            f"<|im_start|>user\n"
            f"{user_template}<|im_end|>\n"
            f"<|im_start|>assistant\n"
        )
        return cls(template, ["input"], cls.FORMAT_CHATML)

    @classmethod
    def from_alpaca(
        cls,
        instruction: str,
        input_template: Optional[str] = None,
    ) -> "PromptTemplate":
        """Create an Alpaca-format template.

        Args:
            instruction: Task instruction.
            input_template: Optional input template.

        Returns:
            PromptTemplate instance.
        """
        variables = ["instruction"]
        template = "Below is an instruction that describes a task. "

        if input_template:
            template += "Write a response that appropriately completes the request.\n\n"
            template += f"### Instruction:\n{instruction}\n\n"
            template += f"### Input:\n{input_template}\n\n"
            template += "### Response:\n"
            variables.append("input")
        else:
            template += "Write a response that appropriately completes the request.\n\n"
            template += f"### Instruction:\n{{instruction}}\n\n"
            template += "### Response:\n"

        return cls(template, variables, cls.FORMAT_ALPACA)


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing Prompt Engineering...")

    # Test 1: Few-shot prompt
    task = "Classify the sentiment as positive or negative."
    examples = [
        ("I love this product!", "positive"),
        ("This is terrible.", "negative"),
        ("It works fine and I'm happy.", "positive"),
    ]
    query = "The service was awful and slow."
    prompt = few_shot_prompt(task, examples, query)

    assert "Task:" in prompt
    assert "Example 1:" in prompt
    assert "I love this product!" in prompt
    assert "positive" in prompt
    assert query in prompt
    assert prompt.endswith("Output:")
    print("  PASS: Few-shot prompt created")
    print(f"  Sample: {prompt[:80]}...")

    # Test 2: Chain-of-thought prompt
    cot = chain_of_thought_prompt("What is 15 * 23 + 7?")
    assert "Let's think through this step by step" in cot
    assert "15 * 23 + 7" in cot
    print("  PASS: Chain-of-thought prompt created")

    # Test 3: Parse JSON output
    json_text = '```json\n{"sentiment": "positive", "confidence": 0.95}\n```'
    parsed = parse_structured_output(json_text, "json")
    assert parsed == {"sentiment": "positive", "confidence": 0.95}, f"Wrong parse: {parsed}"
    print("  PASS: JSON parsing from code block")

    # Test 4: Parse bare JSON
    bare_json = '{"name": "Alice", "age": 30}'
    parsed2 = parse_structured_output(bare_json, "json")
    assert parsed2 == {"name": "Alice", "age": 30}
    print("  PASS: Bare JSON parsing")

    # Test 5: Parse key-value output
    kv_text = "name: Alice\nage: 30\ncity: New York"
    parsed_kv = parse_structured_output(kv_text, "key_value")
    assert parsed_kv == {"name": "Alice", "age": "30", "city": "New York"}
    print("  PASS: Key-value parsing")

    # Test 6: Parse list output
    list_text = "- apple\n- banana\n- cherry"
    parsed_list = parse_structured_output(list_text, "list")
    assert parsed_list == ["apple", "banana", "cherry"]
    print("  PASS: List parsing")

    # Test 7: Parse CSV output
    csv_text = "name,age,city\nAlice,30,NYC\nBob,25,LA"
    parsed_csv = parse_structured_output(csv_text, "csv")
    assert len(parsed_csv) == 3
    assert parsed_csv[0] == ["name", "age", "city"]
    print("  PASS: CSV parsing")

    # Test 8: Create system prompt
    sys_prompt = create_system_prompt(
        role="a helpful coding assistant",
        instructions="Help the user write clean, efficient Python code.",
        constraints=["Use type hints", "Include docstrings", "Follow PEP 8"],
    )
    assert "coding assistant" in sys_prompt
    assert "type hints" in sys_prompt
    assert "PEP 8" in sys_prompt
    print("  PASS: System prompt created")

    # Test 9: PromptTemplate variable substitution
    tmpl = PromptTemplate(
        template="Translate '{text}' to {language}:",
        input_variables=["text", "language"],
    )
    formatted = tmpl.format(text="hello", language="French")
    assert formatted == "Translate 'hello' to French:"
    print("  PASS: Template variable substitution")

    # Test 10: PromptTemplate missing variable error
    try:
        tmpl.format(text="hello")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "language" in str(e)
    print("  PASS: Missing variable raises ValueError")

    # Test 11: ChatML template
    chatml = PromptTemplate.from_chatml(
        system_content="You are a helpful assistant.",
        user_template="Please help with: {input}",
    )
    chatml_prompt = chatml.format(input="debugging my code")
    assert "<|im_start|>system" in chatml_prompt
    assert "debugging my code" in chatml_prompt
    print("  PASS: ChatML template")

    # Test 12: Alpaca template
    alpaca = PromptTemplate.from_alpaca(
        instruction="Summarize the following text.",
        input_template="{input}",
    )
    alpaca_prompt = alpaca.format(instruction="Summarize text", input="Long article...")
    assert "### Instruction:" in alpaca_prompt
    assert "### Input:" in alpaca_prompt
    assert "### Response:" in alpaca_prompt
    print("  PASS: Alpaca template")

    # Test 13: Empty list parsing
    empty_parse = parse_structured_output("some random text", "list")
    assert empty_parse is None, "Should be None for no list items"
    print("  PASS: Empty list returns None")

    print("\nAll Prompt Engineering tests passed!")
