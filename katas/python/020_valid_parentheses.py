"""
LeetCode #20 - Valid Parentheses (Easy)

Given a string s containing just the characters '(', ')', '{', '}', '[' and ']',
determine if the input string is valid.

An input string is valid if:
    1. Open brackets must be closed by the same type of brackets.
    2. Open brackets must be closed in the correct order.
    3. Every close bracket has a corresponding open bracket of the same type.

Example 1:
    Input: s = "()"
    Output: true

Example 2:
    Input: s = "()[]{}"
    Output: true

Example 3:
    Input: s = "(]"
    Output: false

Example 4:
    Input: s = "([])"
    Output: true

Example 5:
    Input: s = "([)]"
    Output: false

Constraints:
    1 <= s.length <= 10^4
    s consists of parentheses only '()[]{}'.
"""

import unittest
from typing import List


class Solution:
    """Stack-based approach — O(n) time, O(n) space.

    Use a stack to track opening brackets. For each character:
      - If it's an opening bracket, push the matching closing bracket
        onto the stack (this avoids a second lookup map).
      - If it's a closing bracket, check if it matches the top of the stack.
        If not (or stack is empty), the string is invalid.
    At the end, the stack must be empty for a valid string.

    Pushing the *expected* closing bracket (instead of the opening one)
    lets us compare directly with the current character — no map needed
    for the closing side.
    """

    def isValid(self, s: str) -> bool:
        # Map of opening bracket -> expected closing bracket
        matching = {"(": ")", "[": "]", "{": "}"}
        stack: List[str] = []

        for ch in s:
            if ch in matching:
                # Opening bracket: push the expected closing bracket
                stack.append(matching[ch])
            elif not stack or stack.pop() != ch:
                # Closing bracket that doesn't match top of stack (or stack empty)
                return False

        # Valid only if all opening brackets were matched
        return not stack


class SolutionAlternative:
    """Alternative stack approach — push opening brackets and map closings.

    Instead of pushing the expected closing bracket, this version pushes
    the actual opening bracket and uses a reverse map to validate closings.
    Same O(n) time and space complexity.
    """

    def isValid(self, s: str) -> bool:
        matching = {")": "(", "]": "[", "}": "{"}
        stack: List[str] = []

        for ch in s:
            if ch in matching:
                # Closing bracket: check top of stack
                if not stack or stack.pop() != matching[ch]:
                    return False
            else:
                # Opening bracket: push onto stack
                stack.append(ch)

        return not stack


# --- Tests ---


class TestValidParentheses(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()
        self.sol2 = SolutionAlternative()

    def _check_both(self, s: str, expected: bool):
        self.assertEqual(self.sol.isValid(s), expected)
        self.assertEqual(self.sol2.isValid(s), expected)

    def test_example_1(self):
        self._check_both("()", True)

    def test_example_2(self):
        self._check_both("()[]{}", True)

    def test_example_3(self):
        self._check_both("(]", False)

    def test_example_4(self):
        self._check_both("([])", True)

    def test_example_5(self):
        self._check_both("([)]", False)

    def test_empty_string(self):
        # Not a valid input per constraints, but good edge case
        self._check_both("", True)

    def test_single_open(self):
        self._check_both("(", False)

    def test_single_close(self):
        self._check_both(")", False)

    def test_nested_same_type(self):
        self._check_both("((((", False)

    def test_nested_mixed(self):
        self._check_both("{[()]}", True)

    def test_only_closing(self):
        self._check_both("))]", False)

    def test_long_valid(self):
        self._check_both("()" * 5000, True)

    def test_long_mismatch(self):
        # Many opens of one type, close with a different type
        self._check_both("(" * 5000 + "]", False)

    def test_interleaved_mismatch(self):
        self._check_both("[{]}", False)

    def test_deep_nesting(self):
        self._check_both("(((())))", True)


if __name__ == "__main__":
    unittest.main()
